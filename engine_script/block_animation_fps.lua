--[[
Author: Qi Zhu, Robotics Institute at Carnegie Mellon University
Block animation for articulate object
This script animate object and camera movement and return objects and keypoints to simulator
Keypoints change with different articulate pose
--]]
local uetorch = require 'uetorch'
local block = {}
block.name = 'block_animation_fps'
local objects={}
local keypoints={}
local camera={}
local angle=-1
JSON = assert(loadfile("/home/qi/Desktop/cvpr/lua_scripts/JSON.lua"))()

--Get each object needed in generating dataset
function block.LoadBatch(data)
	--target for segmentation capture
	local target={}
	camera=data['camera_settings']

	for k, v in ipairs(data['objects']) do
		
		if v['articulate']==true then
			for p,q in ipairs(v['parts']) do
				objects[q]=uetorch.GetActor(q)
				--uncommeted next line for capture object mask
				--target[#target+1]=uetorch.GetActor(q)
			end
		else
			objects[v['id']]=uetorch.GetActor(v['id'])
		end
	end
	return objects,target,camera
end

--Print objects and keypoints in the simulator
function block.Print()
	for i,v in pairs(objects) do print(v) end
	for i,v in pairs(keypoints) do 
		print(i,#v) 
		for k,j in ipairs(v) do
			print(j)
		end
	end
end

function block.SetCamera()
	--print(objects[camera['id']])
	uetorch.SetActorLocation(objects[camera['id']],camera['location'][1],camera['location'][2],camera['location'][3])
	uetorch.SetActorRotation(objects[camera['id']],camera['rotation'][1],camera['rotation'][2],0)
	
end

local function SetMaterial(obj,mat)
	--material path should be specified
	local materialId = "Material'/Game/GTFreeMaterials/Materials/" .. mat .. "." .. mat .. "'"
	--print(materialId)
	local material = UE.FindObject(Material.Class(), nil, materialId)
	uetorch.SetMaterial(obj, material)
end


--This script seems to be general and easy to use for different scenes
function block.SetBlock(data)
	--print('Set Block')
	--print(objects[data['object']])
	--uetorch.SetActorLocation(objects[data['object']],0,0,100)
	--uetorch.SetActorRotation(objects[data['object']],data['object_rotation'][2],data['object_rotation'][1],data['object_rotation'][3])
	if not data then
		return nil
	end

	--Set observed objects
	for p,q in pairs(data['parts']) do
	--print(p)
		--print(p)
		uetorch.SetActorLocation(objects[p],data['object_location'][1],data['object_location'][2],data['object_location'][3])
		uetorch.SetActorRotation(objects[p],q.pitch,q.yaw,q.roll)
	end

	if not data['scene_settings']['bkg'] then
		return nil
	end

	--Set background
	for k,v in pairs(data['scene_settings']['bkg']) do 
		if data['angle']>angle and v['id']~=data['object'] then
			--print(v['id'])
			if v['location'] then
				uetorch.SetActorLocation(objects[v['id']],v['location'][1],v['location'][2],v['location'][3])
			end
			if v['material'] then
				--uetorch.SetMaterial(objects[v['id']],v['material'])
				--print(v['material'])
				SetMaterial(objects[v['id']],v['material'])
			end
		end
	end
	angle=data['angle']
end

return block