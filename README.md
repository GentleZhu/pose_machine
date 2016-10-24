#UE4 Renderer & Pose Estimation 
Author: Qi Zhu, Robotics Institute at Carnegie Mellon University

##Set up:
	1. Install Unreal Engine 4.8 and (UETorch Plugin)[https://github.com/facebook/UETorch]
	2. Try with two existing projects: Realistic Rendering and Office
	3. Modify and Run ./engine_script/setConfig.py to set up configuration files in ./Realistic_rendering/ (e.g.); this writes config.json
	4. Modify and Run ./engine_script/articulate_config.py to set up keypoints and animation control to ./Office/ (e.g.); this writes block_animation_fps.json

@todo Need scissors4.model 

### For new objects and scenes, make sure, 
	1. Create new model file by ./engine_script/writeModel.py --model --parts --constraints(joint angle only currently) --axis --minmax
	2. Change the path in ./engine_script/setConfig.py, generate new configuration file
	3. Registrate a new scene in ./engine_script/scene_registration.py, look into the example there
	4. Change the way generate objects arrangement in ./engine_script/scene_generating.py
	5. Modify and Run ./engine_script/articulate_config.py to set up keypoints and animation control

##Generate training data
	1. Look into ./engine_script/simulator.lua, set appropriate frame rate and screenshot rate and time delay 

	2. Set up blueprints in the UE4 projects, look at setloop and mainmap blueprints in the project 

@todo Please give step by step directions.  E.g., do File->Open, hit play, etc. 

	3. Run the engine in standalone game and wait for image generation 

@todo Please give step by step directions.  E.g., do File->Open, hit play, etc. 

## Training
        1. Run ./engine_script/genLMDB.py
        2. Edit the training prototxt
        3. @todo

## Testing
        1. Edit the testing / deploy protoxt
        2. @todo

## Appendix: How to Start Unreal
````
cd <where Unreal was installed> 
source Engine/Plugins/UETorch/uetorch_activate.sh 
cd Engine/Binaries/Linux 
./UE4Editor 
````

