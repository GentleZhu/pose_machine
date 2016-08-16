--[[
Author: Qi Zhu, Robotics Institute at Carnegie Mellon University
Block_animation for rigid object
This script animate object and camera movement and return objects and keypoints to simulator
--]]
local uetorch = require 'uetorch'
local block = {}
block.name='block_animation'

local objects={}
local keypoints={}
local camera={}

--Load config_file
function block.LoadBatch(data)
	camera=data['camera_settings']
	for k, v in ipairs(data['objects']) do
		objects[v['id']]=uetorch.GetActor(v['id'])
		if #v['keypoints']>0 then
			keypoints[v['id']]=v['keypoints']
		end
	end
	return objects, camera, keypoints
end

function block.Print()
	for i,v in pairs(objects) do print(v) end
	for i,v in pairs(keypoints) do 
		print(i,#v) 
		for k,j in ipairs(v) do
			print(j)
		end
	end
end

--Only set camera when viewport changes
function block.SetBlock()
	for i,v in pairs(objects) do
		if i=='scissors_1' then
			uetorch.SetActorLocation(v,-100,0,100)
			--pitch yaw roll
			uetorch.SetActorRotation(v,30,30,30)
			uetorch.AddForce(v, 10000, 0, 10000)
		elseif i==camera['id'] then
			uetorch.SetActorLocation(v,camera['location'][1],camera['location'][2],camera['location'][3])
			uetorch.SetActorRotation(v,camera['rotation'][1],camera['rotation'][2],0)
		end
	end
	
end

return block