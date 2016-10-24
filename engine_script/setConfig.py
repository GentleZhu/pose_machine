#Author: Qi Zhu, Robotics Institute at Carnegie Mellon University
#Set config.json for Scene: realistic rendering
import json
import math
import numpy as np
#Write a dict, which record different objects
model_path='/home/qi/Desktop/cvpr/models/scissors_1.txt'
cluster_path='/home/qi/Desktop/cvpr/scripts/scissors_1_cluster'
def cameraConfig(outfile):
	config=dict()
	config['dataPath']='/home/qi/Desktop/cvpr/data/'
	config['scene']='BluePrint'
	config['sceneTime']=3
	config['batchID']='camera_calibration'
	config['screenshots']=False
	config['objectmasks']=False
	config['objects']=list()
	obj=dict()
	obj['id']='MainMap_CameraActor_Blueprint_C_0'
	config['objects'].append(obj)
	obj=dict()
	obj['id']='Cube_01'
	config['objects'].append(obj)
	obj=dict()
	obj['id']='Cube_02'
	config['objects'].append(obj)

	json.dump(config, outfile)
	outfile.write('\n')
#config['objects'][0]['keypoints']=[2,2,2]
#json.dump(config, outfile)
#outfile.write('\n')
#config['objects'][0]['keypoints']=[3,3,3]
#json.dump(config, outfile)




#keypoints config for 
def keypointsConfig(model_path,scale,cluster_path=None):
	f = open ( model_path , 'r')
	keypoint=[]
	for line in f:
		for w in line.split(' '):
			try:
			#print float(w)
				if len(keypoint) % 3 ==1:
					keypoint.append(round(-scale*float(w),3))
				else:
					keypoint.append(round(scale*float(w),3))
			except:
				pass
	#print len(l)
	f.close()
	if cluster_path:
		f = open ( cluster_path, 'r')
		key=[]
		for line in f:
			cnt=0
			tmpx=0
			tmpy=0
			tmpz=0
			for w in line.split(' '):
				if w!='' and w!='\n':
					cnt+=1
					tmpx+=keypoint[3*int(w)-3]
					tmpy+=keypoint[3*int(w)-2]
					tmpz+=keypoint[3*int(w)-1]
			key.append(tmpx/cnt)
			key.append(tmpy/cnt)
			key.append(tmpz/cnt)
		f.close()
		print('length of keypoints'+str(len(key)))
		return key
	else:
		return keypoint



#Now config file doesn't contain any keypoints
def cubeConfig(outfile,camera_settings,keypoints=None):
	#default for single object, need to be fixed for multiple object
	config=dict()
	config['dataPath']='/home/qi/Desktop/cvpr/data/'
	config['scene']='BluePrint'
	config['sceneTime']=203
	config['objects']=list()
	#keypoint=[-50,-50,-50, -50,50,-50, -50,50,50, -50,-50,50,
	#50,-50,-50, 50,50,-50, 50,50,50, 50,-50,50]
	obj=dict()
	#obj['id']='Medical_Scissors'
	obj['id']='scissors1'
	obj['articulate']=True
	obj['parts']=[]
	obj['parts'].append('scissors_l')
	obj['parts'].append('scissors_r')
	config['objects'].append(obj)

	obj=dict()
	obj['id']='Desk'
	obj['articulate']=False
	config['objects'].append(obj)

	obj=dict()
	obj['id']='DeskBook1'
	obj['articulate']=False
	config['objects'].append(obj)

	obj=dict()
	obj['id']='DeskBook2'
	obj['articulate']=False
	config['objects'].append(obj)

	#obj=dict()
	#obj['id']='DeskBowl1'
	#obj['articulate']=False
	#config['objects'].append(obj)

	obj=dict()
	obj['id']='DeskBowl2'
	obj['articulate']=False
	config['objects'].append(obj)

	obj=dict()
	obj['id']='DeskMug1'
	obj['articulate']=False
	config['objects'].append(obj)

	obj=dict()
	obj['id']='DeskMug2'
	obj['articulate']=False
	config['objects'].append(obj)

	obj=dict()
	obj['id']='DeskVase1'
	obj['articulate']=False
	config['objects'].append(obj)

	obj=dict()
	obj['id']='DeskVase2'
	obj['articulate']=False
	config['objects'].append(obj)

	obj=dict()
	obj['id']='DeskVase3'
	obj['articulate']=False
	config['objects'].append(obj)


	obj=dict()
	obj['id']='MainMap_CameraActor_Blueprint_C_0'
	#obj['keypoints']=[]
	config['objects'].append(obj)
	#config['keypoints'].append(keypoint)
	config['world_center']=[0,0,46]
	config['camera_settings']=camera_settings
	#config['camera_settings']=dict()
	#config['camera_settings']['id']='MainMap_CameraActor_Blueprint_C_0'
	#config['camera_settings']['radius']=500
	#config['camera_settings']['location']=[-250,0,250*1.73]
	#config['camera_settings']['rotation']=[60,0]
	config['batchID']='block_animation_fps'
	config['screenshots']=True
	config['objectmasks']=True
	config['landmark']=True
	json.dump(config, outfile)
	outfile.write('\n')




if __name__ == "__main__":
        outfile_var = '../Realistic_rendering/config.json' 
        print "Writing config file to: " + outfile_var
	outfile=open(outfile_var, 'w')
	#pt=keypointsConfig(model_path,1500,cluster_path)
	camera_settings=dict()
	camera_settings['id']='MainMap_CameraActor_Blueprint_C_0'
	camera_settings['radius']=90
	world_center=[0,0,46]
	#camera_settings['location']=[-250,0,250*1.73]
	#camera_settings['rotation']=[60,0]
	split=5
	d_theta=math.pi/2/split
	d_thetad=90/split
	d_phi=math.pi/split
	d_phid=180/split


	for lat in range(1,split):
		r=camera_settings['radius']*math.cos(d_theta*lat)
		z=round(camera_settings['radius']*math.sin(lat*d_theta),3)
		for i in range(2*split):
			x=round(-r*math.cos(d_phi*i),3)
			y=round(-r*math.sin(d_phi*i),3)
			camera_settings['location']=[x,y,z+world_center[2]]
			camera_settings['rotation']=[-lat*d_thetad,d_phid*i]
			cubeConfig(outfile,camera_settings)


	#Add top view
	camera_settings['location']=[0,0,camera_settings['radius']+world_center[2]]
	camera_settings['rotation']=[-90,0]
	cubeConfig(outfile,camera_settings)
	
	#cameraConfig(outfile)

	#Animator Config
	#animationfile=open('/home/qi/Desktop/cvpr/data/jsondata/block_animation_fps.json','w')
	#bounding_box={}
	#bounding_box['min']=np.array([-100,-100,100])
	#bounding_box['gap']=np.array([200,200,200])
	#animatorConfig(animationfile,10,bounding_box)

	#animationfile.close()
	outfile.close()
