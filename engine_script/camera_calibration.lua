--[[
Author: Qi Zhu, Robotics Institute at Carnegie Mellon University
This script is used for camera caliberation -- see camera part in simulator
--]]
local uetorch = require 'uetorch'
local block = {}
local objects = {}
local camera
--local initial_location={}

function block.Calibrate(data)
	--objects=data['objects']
	--print('here')
	--print(data['objects'][1]['id'])
	objects[1]=uetorch.GetActor('Cube_01')
	objects[2]=uetorch.GetActor('Cube_02')
	camera=uetorch.GetActor('MainMap_CameraActor_Blueprint_C_0')
	uetorch.SetActorLocation(camera,-500,0,300)
	uetorch.SetActorRotation(camera,0,0,0)

	uetorch.SetActorLocation(objects[1],0,-100,300)
	uetorch.SetActorRotation(objects[1],0,0,0)
	uetorch.SetActorLocation(objects[2],0,100,300)
	uetorch.SetActorRotation(objects[2],0,0,0)
	--print('here')
	return objects,camera
end

function block.Destroy()
	uetorch.SetActorLocation(objects[1],0,-100,-300)
	uetorch.SetActorLocation(objects[2],0,100,-300)
end

return block