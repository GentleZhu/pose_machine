--[[
Author: Qi Zhu, Robotics Institute at Carnegie Mellon University
This script fetch configurations from config.json
--]]

local config = {}
JSON = assert(loadfile("/home/qi/Desktop/cvpr/lua_scripts/JSON.lua"))()
conf={}
conf['dataPath'] = '/home/qi/Desktop/cvpr/data/'
conf['screenCaptureInterval'] = 2
conf['batch']={}

--Configure this per project
--local file = assert(io.open('/home/qi/Desktop/cvpr/Config_file/Realistic_rendering/config.json'))
local file = assert(io.open('/home/qi/Desktop/cvpr/Config_file/Office/config.json'))
--local file = assert(io.open('/home/qi/Desktop/cvpr/lua_scripts/config.json'))
while true do
	line=file:read('*line')
	if line~=nil then
		conf['batch'][#conf['batch']+1]=JSON:decode(line)
	else
		break
	end
end
--for k,v in pairs(conf['batch'][1]) do
--	print(k,v)
--end

function config.GetDataPath()
	return conf['dataPath']
end

function config.GetScreenCaptureInterval()
	return conf['screenCaptureInterval']
end

function config.GetSceneTime(iteration)
	iteration = tonumber(iteration)
	--print(conf['batch'][iteration]['sceneTime'])
	return conf['batch'][iteration]['sceneTime']
end

function config.GetWorldCenter(iteration)
	iteration = tonumber(iteration)
	--print(conf['batch'][iteration]['sceneTime'])
	return conf['batch'][iteration]['world_center']
end

function GetIterations()
	return #conf['batch']
end

function config.GetScreen(iteration)
	iteration = tonumber(iteration)
	return conf['batch'][iteration]['screenshots']
end

function config.GetText(iteration)
	iteration = tonumber(iteration)
	return conf['batch'][iteration]['screenshots']
end

function config.GetBlock(iteration)
	iteration = tonumber(iteration)
	return conf['batch'][iteration]
end


return config