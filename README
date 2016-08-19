#UE4 Renderer & Pose Estimation 
Author: Qi Zhu, Robotics Institute at Carnegie Mellon University

##Set up:
	1. Install Unreal Engine 4.8 and UETorch Plugin https://github.com/facebook/UETorch
	2. Try with two existing projects: Realistic Rendering and Office
	3. Modify and Run ./engine_script/SetConfig.py to set up configuration files in ./Config_files/
	4. Modify and Run ./articulate_config.py to set up keypoints and animation control 
For new objects and scenes, make sure,

	1. Create new model file by ./engine_script/writeModel.py --model --parts --constraints(joint angle only currently) --axis --minmax
	2. Change the path in ./engine_script/SetConfig.py, generate new configuration file
	3. Registrate a new scene in ./engine_script/scene_registration.py, look into the example there
	4. Change the way generate objects arrangement in ./engine_script/scene_generating.py
	5. Modify and Run ./articulate_config.py to set up keypoints and animation control 

##Generate training data
	1. Look into ./engine_script/simulator.lua, set appropriate frame rate and screenshot rate and time delay
	2. Set up blueprints in the UE4 projects, look at setloop and mainmap blueprints in the project
	3. Run the engine in standalone game and wait for image generation