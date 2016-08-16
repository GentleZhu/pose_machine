--[[
Author: Qi Zhu, Robotics Institute at Carnegie Mellon University
Simulator controls whole pipeline for image rendering in UE4:
	SetIteration
		load config data
		add animator hook, execute by block_animation script
		add screen capture hook
		add data recorder
	SaveJsondata:
		calculate keypoints in camera 2D projection plane
--]]


--Watch line 219
require 'torch'
local uetorch = require 'uetorch'
local image = require 'image'
local config = require 'config'
local block

--uetorch.SetFPS(8)
JSON = assert(loadfile("/home/qi/Desktop/cvpr/lua_scripts/JSON.lua"))()
--SetCurrentIteration(3)

local currentIteration = 0

local actors = {}
local target = {}
local keypoints = {}
local camera = {}
local simulator_params = {}
local animator = {}
--default setting: adjust by config.json
local world_center={0,0,0}
local calibration
--local flen = 0
--local px2cm = 0

local step = 0


--Simulate each frame in block_animation.json
GetSceneTime = config.GetSceneTime
local tSimulate = 0
local tLastSimulate = 0
local function Simulate(dt)
	-- body
	if tSimulate - tLastSimulate >= config.GetScreenCaptureInterval() then
		step = step + 1
		--print('Simulate is called'..tSimulate..step)
		block.SetBlock(animator[step])
		tLastSimulate = tSimulate
	end
	tSimulate = tSimulate + dt
end


--SaveScreen screenshots/depth image/object mask
--Please adjust tSaveScreen, which helps get stable screenshot after rendering,
--e.g. 1s time lapse below
local tLastSaveScreen = 0
local tSaveScreen = -1
local tmp={}
local function SaveScreen(dt)
	if tSaveScreen - tLastSaveScreen >= config.GetScreenCaptureInterval() then
		--step = step + 1
		--print('SaveScreen is called'..tSimulate)
		local file = config.GetDataPath() .. 'screenshots/' .. 'batch' .. currentIteration .. '_' .. step .. '.jpg'
		local i1 = uetorch.Screen()
		if i1 then
			--print(tSaveScreen)
			image.save(file, i1)
		end

		--if (step==1) then
		--	print('params')
		--	simulator_params['img_width']=i1:size(3)
		--	simulator_params['img_height']=i1:size(2)
		--end

		file = config.GetDataPath() .. 'segmentation/' .. 'batch' .. currentIteration .. '_' .. step .. '.jpg'
		--print(target)
		--local i2 = uetorch.ObjectSegmentation(target, 1)
		if i2 then
			torch.save('/home/qi/Desktop/'..'batch' .. currentIteration .. '_' .. step .. '.t7', i2)
			--image.save(file,i2)
		end

		--local i3 = uetorch.ObjectMasks(actors, config.GetStride())
		if i3 then
			actor = 1

			for k, v in pairs(block.actors) do
				file = config.GetDataPath() .. currentIteration .. '/' .. step .. '_' .. k .. '.jpg'
				image.save(file,i3[actor])
				actor = actor + 1
			end
		end

		tLastSaveScreen = tSaveScreen
	end
	tSaveScreen = tSaveScreen + dt
end

local data = {}
local tSaveText = -0.4
local tLastSaveText = 0

local function SaveTextHook(dt)
	--[[
	print('SaveText is called')
	--'Now location and rotation and read from animator'
	local aux = {t = tSaveText}
	if tSaveText - tLastSaveText >= config.GetScreenCaptureInterval() then
		for k,v in pairs(actors) do
			aux[k] = {
				location = uetorch.GetActorLocation(v),
				rotation = uetorch.GetActorRotation(v)
			}
		end
		table.insert(data, aux)

		tLastSaveText = tSaveText
	end
	tSaveText = tSaveText + dt
	--]]
	
	--'Now location and rotation and read from animator'
	local aux = {t = tSaveText}
	if tSaveText - tLastSaveText >= config.GetScreenCaptureInterval() then
		--print('SaveText is called'..tSimulate)
		--print(animator[step]['object'])
		aux[animator[step]['object']] = {
			location = {x=animator[step]['object_location'][1],y=animator[step]['object_location'][2],z=animator[step]['object_location'][3]},
			rotation = {yaw=animator[step]['object_rotation'][1],pitch=animator[step]['object_rotation'][2],roll=animator[step]['object_rotation'][3]}
		}

		if aux then
			table.insert(data, aux)
		end

		tLastSaveText = tSaveText
	end
	tSaveText = tSaveText + dt

end

local function ListToVector(array)
	local vector=torch.zeros(3)
	vector[1] = array[1]-world_center[1]
	vector[3] = array[2]-world_center[2]
	vector[2] = array[3]-world_center[3]
	return vector
end

local function ListToTensor(keypoints)
	local N=#keypoints+1;
	local keytensor = torch.Tensor(3,N)
	keytensor[{{},{1}}] = torch.zeros(3)
	--print(keypoints)
	for i=2,N do
		keytensor[1][i] = keypoints[i-1][1]
		keytensor[3][i] = keypoints[i-1][2]
		keytensor[2][i] = keypoints[i-1][3]
	end
	--print(keytensor)
	return keytensor
end


--Convert world coordinate to camera coordinate
local Rc = torch.Tensor(3,3)
local Tw = torch.zeros(3,1)
local function WorldToCamera(camera_location,camera_radius)
	
	local world_z=torch.Tensor({{0},{1},{0}})
	local world_frame=torch.eye(3)
	local camera_frame=torch.Tensor(3,3)
	camera_frame[{{},{1}}]=-camera_location/torch.norm(camera_location)
	local camera_x=camera_frame[{{},{1}}]
	local camera_y=torch.cross(camera_x,world_z)
	local camera_z=torch.cross(camera_y,camera_x)
	if torch.all(torch.eq(camera_y,torch.zeros(3,1))) then 
		--print('Should be here')
		camera_frame[{{},{3}}]=torch.Tensor({{0},{0},{1}})
		camera_frame[{{},{2}}]=torch.Tensor({{1},{0},{0}})
	else
		--print('OMG here')
		camera_frame[{{},{3}}]=camera_y/torch.norm(camera_y)
		camera_frame[{{},{2}}]=camera_z/torch.norm(camera_z)
	end
	--print("Look here")
	--print(camera_frame)

	for camera_dim=1,3 do
		for world_dim=1,3 do
			Rc[camera_dim][world_dim]=torch.dot(camera_frame[{{},{camera_dim}}],world_frame[{{},{world_dim}}])
		end
	end
	Tw[1][1] = camera_radius
end 

function SetCurrentIteration(iteration)
	currentIteration = iteration
	print('current iteration =', currentIteration)
	local batch = config.GetBlock(currentIteration)

	if batch['batchID']=='camera_calibration' then
		calibration = false
		block = require('camera_calibration')
		actors ,camera = block.Calibrate(batch)

	else
		calibration = true
		local file = assert(io.open(config.GetDataPath() .. 'jsondata/' .. 'simulator_params.json', "r"))
		simulator_params=JSON:decode(file:read('*all'))
		file.close()
		--actually block_animation can have multiple batch-ID.json

		--file = assert(io.open('/home/qi/Desktop/cvpr/Config_file/Realistic_rendering/' .. batch['batchID'] .. '.json', "r"))
		file = assert(io.open('/home/qi/Desktop/cvpr/Config_file/Office/' .. batch['batchID'] .. '.json', "r"))
		block = require(batch['batchID'])
		animator = JSON:decode(file:read('*all'))
		file.close()

		world_center=config.GetWorldCenter(iteration)
		--actors = dict_to_array(block.actors)
		
		actors ,target ,camera = block.LoadBatch(batch)
		--keypoints now generate by animator
		
		local cl = ListToVector(camera['location'])
		WorldToCamera(cl,camera['radius'])
		block.SetCamera()
	end

	if config.GetScreen(currentIteration) then
		uetorch.AddTickHook(Simulate)
		uetorch.AddTickHook(SaveScreen)
	end

	if config.GetText(currentIteration) then
		uetorch.AddTickHook(SaveTextHook)
	end
	--print('Set Iteration done')
end

local function ObjectToWorld(ypr)
	--print(ypr)
	ypr.roll=-ypr.roll/180*math.pi
	ypr.pitch=-ypr.pitch/180*math.pi
	ypr.yaw=ypr.yaw/180*math.pi
	local R_roll=torch.Tensor({{1,0,0},{0,math.cos(ypr.roll),math.sin(ypr.roll)},{0,-math.sin(ypr.roll),math.cos(ypr.roll)}})
	local R_yaw=torch.Tensor({{math.cos(ypr.yaw),0,-math.sin(ypr.yaw)},{0,1,0},{math.sin(ypr.yaw),0,math.cos(ypr.yaw)}})
	local R_pitch=torch.Tensor({{math.cos(ypr.pitch),math.sin(ypr.pitch),0},{-math.sin(ypr.pitch),math.cos(ypr.pitch),0},{0,0,1}})
	return R_yaw*R_pitch*R_roll
end


--Convert from object coordinate to world coordinate
local function ObjectInCamera(keypoints,object_location,object_rotation)
	--notice offset 46 here
	local To = torch.Tensor({{object_location.x-world_center[1]},{object_location.z-world_center[3]},{object_location.y-world_center[2]}})
	local Rw = ObjectToWorld(object_rotation)
	local Xo = ListToTensor(keypoints)
	return Rc*Rw*Xo+torch.expandAs((Rc*To+Tw),Xo)
	--Rc is a global parameter, since camera doesn't move in one settings
end

--Note not all functions are could in one import "action", every plugin in blueprint = one code import
--Consider move segments like these into sub-scripts, can reduce the code imported once
--By saying this, I mean I could consider dynamically import code segment rather than static


--Call Camera Calibrator
local function GetCameraFocus()
	local mask=uetorch.ObjectSegmentation(actors)
	h=math.floor(mask:size(1)/2)
	w=mask:size(2)
	local centerL,centerR
	simulator_params['img_width']=w
	simulator_params['img_height']=mask:size(1)
	for i = 1,w do
		if mask[h][i]==0 and mask[h][i+1]==1 then
			centerL=i
			break
		end
	end
	
	for i = 1,w do
		if mask[h][i]==2 and mask[h][i+1]==0 then
			centerR=i
			break
		end
	end
	print(centerL,centerR)
	simulator_params['cm2px'] = (centerR-centerL)/300
	simulator_params['focus'] = w/2/simulator_params['cm2px']
	--print('Focus Length is '..focus..'cm')
	--print('pixel to cm is '..px2cm)

end

--Deprecated prototype, see SaveJsonData below
function SaveData()
	local datacube={}
	--return nil
	--print(calibration)
	if not calibration then
		GetCameraFocus()
		block.Destroy()
		calibration = true
		--return nil
	else
		
		local datafile = config.GetDataPath() .. 'textdata/' .. 'keypoints_batch' .. currentIteration
		--print(logfile)
		local file = assert(io.open(logfile, "w"))

		--file:write("block = " .. config.GetBlock(currentIteration) .. "\n")

		--local possible = block.IsPossible()
		
		--if possible then
		--	file:write("possible = true\n")
		--else
		--	file:write("possible = false\n")
		--end
		
		--local bounds = uetorch.GetActorBounds(floor)
		--local minx = bounds["x"] - bounds["boxX"]
		--local maxx = bounds["x"] + bounds["boxX"]
		--local miny = bounds["y"] - bounds["boxY"]
		--local maxy = bounds["y"] + bounds["boxY"]
		--file:write("minX = " .. minx .. " maxX = " .. maxx .. " minY = " .. miny .. " maxY = " .. maxy .. "\n")

		
		for k, v in ipairs(data) do
			file:write("step = " .. k .. "\n")
			file:write("t = " .. v["t"] .. "\n")

			for k2,v2 in pairs(actors) do
				file:write("actor " .. k2 .. "\n")
				for k3,v3 in pairs(v[k2]["location"]) do
					file:write(k3 .. " = " .. v3 .. " ")
				end
				file:write("\n")
				for k3,v3 in pairs(v[k2]["rotation"]) do
					file:write(k3 .. " = " .. v3 .. " ")
				end
				file:write("\n")
				if k2~=camera['id'] then
					--need to be fix when have more than one object
					datacube[k] = ObjectInCamera(k2,v[k2]["location"],v[k2]["rotation"])
				end
			end
		end
		--print(datacube)
		torch.save(datafile, datacube)
		file:close()
	end
end

local function Tensor2List(t)
	--default the tensor is 3*M
	--print(t)
	local cube={}
	local visible
	for i=1,t:size(2) do
		cube[i]={}
		visible=true
		for j=1,t:size(1) do
			cube[i][j]=t[j][i]
		end
		if cube[i][1]<0 or cube[i][1]>=simulator_params['img_width'] or cube[i][2]<0 or cube[i][2]>= simulator_params['img_height']  then
			visible=false
		end 
		--if not obj_pos, predict visibility
		if i>1 then
			if visible then
			cube[i][3] = 1
			else
				cube[i][1] = 0
				cube[i][2] = 0
				cube[i][3] = 0
			end
		end
	end
	--print(cube)
	return cube
end

local function Projection2D(keypoints)
	--print(keypoints)
	local focus = torch.ones(1,keypoints:size(2))*simulator_params['focus']
	local ratio = torch.cdiv(focus,keypoints[{{1},{}}])
	local x=simulator_params['cm2px']*torch.cmul(keypoints,torch.expandAs(ratio,keypoints))
	local pd=torch.cat(x[{{3},{}}]+simulator_params['img_width']/2,simulator_params['img_height']/2-x[{{2},{}}],1)
	return torch.round(1000*pd)/1000
end

function SaveJson()
	if not calibration then
		--print('here')
		GetCameraFocus()
		--print('here')
		local paramsfile = config.GetDataPath() .. 'jsondata/' .. 'simulator_params.json' 
		local file = assert(io.open(paramsfile, "w"))
		--print(simulator_params)
		
		file:write(JSON:encode(simulator_params))
		file:close()
		block.Destroy()
		calibration = true
		--return nil
	else
		--print('Finish one batch')
		local datafile = config.GetDataPath() .. 'jsondata/' .. 'batch' .. currentIteration .. '.json'
		local data_cube = {}
		local jsontext
		local data3d
		--print(logfile)
		local file = assert(io.open(datafile, "w"))
		--Every data cube record one object
		--k is step of image
		for k, v in ipairs(data) do
			--print(k)
			--Now only consider one object
			--for k2,v2 in pairs(actors) do
				--Below can record to 3D pose and rotation
			k2=animator[k]['object']
				--print(animator[k]['keypoints'])
			--print(v[animator['object']])
			data3d=ObjectInCamera(animator[k]['keypoints'],v[k2]["location"],v[k2]["rotation"])
			
			array=Tensor2List(Projection2D(data3d))
			--print(array)
			data_cube['objpos'] = array[1]
			data_cube['joint_self'] = {}
			data_cube['dataset'] = 'UE4'
			data_cube['isValidation'] = 0
			data_cube['img_paths'] = 'screenshots/' .. 'batch' .. currentIteration .. '_' .. k .. '.jpg'
			data_cube['img_width'] = simulator_params['img_width']
			data_cube['img_height'] = simulator_params['img_height']
			data_cube['scale_provided'] = math.floor(data3d[1][1]*10)/1000
			data_cube['people_index'] = 1
			data_cube['numOtherPeople'] = 0

			for i = 2,#array do
				data_cube['joint_self'][i-1] = array[i]
			end
				--need to be fix when have more than one object
				--datacube[k] = ObjectInCamera(k2,v[k2]["location"],v[k2]["rotation"])
			--end
			jsontext=JSON:encode(data_cube)
			file:write(jsontext)
			file:write('\n')
		end
		--print(datacube)
		--torch.save(datafile, datacube)
		file:close()
	end
end