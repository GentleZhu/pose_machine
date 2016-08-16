#Author: Qi Zhu, Robotics Institute at Carnegie Mellon University
#This script write articulate object per frame animation
import json
import math
import numpy as np
import scene_generating as sg

model_path='/home/qi/Desktop/cvpr/models/scissors4.model'

#Same as UE4 settings,Coordinate XZY
def rotation2ypl(rot):
	angle={}
	angle['yaw']=math.degrees(math.atan2(rot[1][0], rot[0][0]))
	angle['pitch']=math.degrees(math.atan2(-rot[2][0],(rot[2][1]**2+rot[2][2]**2)**0.5))
	angle['roll']=math.degrees(math.atan2(rot[2][1],rot[2][2]))
	return angle

#Coordinate XYZ
def getRotationmatrix(yaw,pitch,roll,verbose=False):
	r=roll/180*math.pi
	p=pitch/180*math.pi
	y=yaw/180*math.pi
	
	R_roll=np.array([[1,0,0],[0,math.cos(r),-math.sin(r)],[0,math.sin(r),math.cos(r)]])
	R_yaw=np.array([[math.cos(y),-math.sin(y),0],[math.sin(y),math.cos(y),0],[0,0,1]])
	R_pitch=np.array([[math.cos(p),0,math.sin(p)],[0,1,0],[-math.sin(p),0,math.cos(p)]])
	if verbose==True:
		print(math.degrees(y),math.degrees(p),math.degrees(r))
		print(rotation2ypl(reduce(np.dot, [R_yaw,R_pitch,R_roll])))
	return reduce(np.dot, [R_yaw,R_pitch,R_roll])

#Coordinate XZY
def getUE4Rotation(yaw,pitch,roll):
	r=-roll/180*math.pi
	p=-pitch/180*math.pi
	y=yaw/180*math.pi
	
	R_roll=np.array([[1,0,0],[0,math.cos(r),-math.sin(r)],[0,math.sin(r),math.cos(r)]])
	R_yaw=np.array([[math.cos(y),-math.sin(y),0],[math.sin(y),math.cos(y),0],[0,0,1]])
	R_pitch=np.array([[math.cos(p),0,math.sin(p)],[0,1,0],[-math.sin(p),0,math.cos(p)]])
	return reduce(np.dot, [R_yaw,R_pitch,R_roll])

#Params: --model_path xxx.model --diff_count #articulation pose
#Outputs: --pose rotated keypoints --rotation articulation_pose --oid object_id
def articulateConfig(model_path,diff_count):
	with open(model_path,'r') as f:
		content = f.read()
	f.close()
	model=json.loads(content)
	pose=[]
	rotation=[]
	oid=model['id']
	for i in range(diff_count):
		sub_rot={}
		sub_pose=[]
		for part in model['parts']:
			if diff_count==1:
				unit=0
			else:
				unit=float(part['max']-part['min'])/(diff_count-1)
			if part['axis']=='X':
				sub_pose.append(np.dot(getRotationmatrix(0,0,i*unit+part['min']),np.array(part['keypoints']).T))
				sub_rot[part['id']]=[0,0,i*unit+part['min']]
			elif part['axis']=='Y':
				sub_pose.append(np.dot(getRotationmatrix(0,i*unit+part['min'],0),np.array(part['keypoints']).T))
				sub_rot[part['id']]=[0,i*unit+part['min'],0]
			else:
				sub_pose.append(np.dot(getRotationmatrix(i*unit+part['min'],0,0),np.array(part['keypoints']).T))
				sub_rot[part['id']]=[i*unit+part['min'],0,0]
		rotation.append(sub_rot)
		pose.append(np.concatenate(sub_pose,1))
	return pose,rotation,oid

#Configure rigid object keypoints, support keypoints cluster
def keypointsConfig(model_path,scale,cluster_path=None):
	f = open ( model_path , 'r')
	keypoint=[]
	for line in f:
		for w in line.split(' '):
			try:
				if len(keypoint) % 3 ==1:
					keypoint.append(round(-scale*float(w),3))
				else:
					keypoint.append(round(scale*float(w),3))
			except:
				pass

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
		return key
	else:
		return keypoint

def Dot(A,B):
	return np.dot(A,B)

#Params: --outfile animation_fps --frame_count #frame each(pose,viewport) --diff_count #articulation pose
def animatorConfig(outfile,frame_count,diff_count,obj_location):
	config=[]
	#Now one object is considered
	pose,rot,oid=articulateConfig(model_path,diff_count)

	rotation=np.random.random([frame_count,3])*360
	for p in range(diff_count):
		for i in range(frame_count):
			sub_animator={}
			sub_animator['object']=oid
			sub_animator['object_location']=obj_location[p][oid]
			sub_animator['object_rotation']=[rotation[i,0],rotation[i,1],rotation[i,2]]
			sub_animator['frame']=i
			sub_animator['angle']=p
			sub_animator['keypoints']=[]
			sub_animator['parts']={}
			sub_animator['parts']['scissors_l']=rotation2ypl(Dot(getRotationmatrix(rotation[i][0],rotation[i][1],rotation[i][2]),\
				getRotationmatrix(rot[p]['scissors_l'][0],rot[p]['scissors_l'][1],rot[p]['scissors_l'][2])))
			#Yaw, Pitch, Raw in UE4
			sub_animator['parts']['scissors_r']=rotation2ypl(Dot(getRotationmatrix(rotation[i][0],rotation[i][1],rotation[i][2]),\
				getRotationmatrix(rot[p]['scissors_r'][0],rot[p]['scissors_r'][1],rot[p]['scissors_r'][2])))
			sub_animator['keypoints']=pose[p].T.tolist()
			sub_animator['scene_settings']=obj_location[p]
			#sub_animator['keypoints'].append(np.dot(temp_rot,pose['r'][p]).T.tolist())
			config.append(sub_animator)

	json.dump(config,outfile,sort_keys=True, indent=4, separators=(',', ': '))
	#return config

if __name__=="__main__":
	frame_count=10 
	diff_count=40
	#world_center in scene(will write a json file to store all scenes)
	world_center=[277.5,140.5,40]
	#world_center=[0,0,46]
	target='scissors1'
	with open('/home/qi/Desktop/cvpr/Config_file/Office/block_animation_fps.json','w') as f:
		#Look into module scene_generating for more details
		animatorConfig(f,frame_count,diff_count,sg.scene_generate(diff_count,target,world_center))
