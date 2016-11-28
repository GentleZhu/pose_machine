#UE4 Renderer & Pose Estimation 
Author: Qi Zhu, Robotics Institute at Carnegie Mellon University

##Set up
1. Install Unreal Engine 4.8 and [UETorch Plugin]([https://github.com/facebook/UETorch)
2. Try with two existing projects: Realistic rendering and Office
3. Modify and run ./engine_script/setConfig.py to set up configuration files in ./Realistic_rendering/ (e.g.)

_CONFIG_FILENAME is which config.json to write; it sets where the viewpoint of the camera is  
@Update:

	In setConfig.py
	Params: 
		camera_settings['radius']: camera is around object in a sphere
		world_center: camera orient at world center, set it regarding location in unreal engine 4
		split: by defaut, we have (5-1)*10+1=41 different camera pose

4. Modify and run ./engine_script/articulate_config.py to set up keypoints and animation control to ./Realistic_rendering/ (e.g.)  

_MODEL_FILENAME is the model to load; it has keypoints in it  
_BLOCK_ANIMATION_FILENAME is which block_animation_fps.json to write; it will animate the object  
@Update:

	frame_count: #different object pose
	diff_count: #different articulate pose, each articulate correspond to a different location.
	So we have #frame_count*#diff_count*#camera_view
	In Realistic rendering: 10*20*41=8200 training images
	In Office: 10*30*41=12300 images

### For new objects and scenes, make sure, 
	1. Create new model file by ./engine_script/writeModel.py --model --parts --constraints(joint angle only currently) --axis --minmax
	2. Change the path in ./engine_script/setConfig.py, generate new configuration file
	3. Registrate a new scene in ./engine_script/scene_registration.py, look into the example there
	4. Change the way generate objects arrangement in ./engine_script/scene_generating.py
	5. Modify and Run ./engine_script/articulate_config.py to set up keypoints and animation control

##Generate training data
	1. Look into ./engine_script/simulator.lua, set appropriate frame rate and screenshot rate and time delay 

This will write to ./Realistic_rendering/batchXX.json and ...

	2. Set up blueprints in the UE4 projects, look at setloop and mainmap blueprints in the project 
	Step by Step(take realistic rendering as example)
		1. Open Project Realistic_rendering(it should work in your settings)
		2. You may need set up lua scripts path properly

	3. Run the engine in standalone game and wait for image generation 
		1. Hit the pull down bar of 'play' in top toolbar
		2. Choose play in a standalone game, it should capture 1280*1024 images in data/screenshots/
		3. Set up json path and generate json file via engine_scripts/genJSON.py

## Training
        
        1. Run ./scripts/genLMDB.py (I update the json file in genLMDB.py, specifically it uses output of step 4.)
        2. Modify and run setLayers to setup caffe configuration files
        3. Find and run train_pose.sh under above configuration path(you can try to train this on CMU skynet server, where I setup caffe stuffs already)
        4. You can find generated lmdb files on skynet server. You can download it to your local machine.

## Testing
        1. Edit the testing / deploy protoxt
        2. Later I will warp up matlab/python scripts, which take raw image as input and output 6DOF pose

## Appendix: How to Start Unreal
````
cd <where Unreal was installed> 
source Engine/Plugins/UETorch/uetorch_activate.sh 
cd Engine/Binaries/Linux 
./UE4Editor 
````

