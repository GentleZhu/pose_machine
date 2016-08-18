#Author: Qi Zhu, Robotics Institute at Carnegie Mellon University
#From Json data to create ground truth keypoints/object position&rotation/viewport .mat file

import scipy.io as sio
import numpy as np
import json
import math

batchNum=41
path='/home/qi/Desktop/cvpr/data/jsondata/scissors2_exp1_RR/'
world_center=np.array([0,0,46])
#world_center=np.array([277.5,140.5,40])
def readKeypoints(path,batchNum,line_per_batch,num_points):
	batch=np.zeros((batchNum,),dtype=np.object)
	
	for i in range(batchNum):
		keypoints=np.zeros((line_per_batch,num_points*2))
		file=open(path+'batch'+str(i+1)+'.json','r')
		cnt=0
		for line in file:
			data=json.loads(line)
			n_kp=0
			for keypoint in data['joint_self']:
				keypoints[cnt,2*n_kp]=keypoint[0]
				keypoints[cnt,2*n_kp+1]=keypoint[1]
				n_kp+=1
				if n_kp>=num_points:
					break
			cnt+=1
		if cnt!=200:
			print('Error in batch line number'+str(i)+'!')
		batch[i]=keypoints

	sio.savemat('/home/qi/Desktop/cvpr/testing/data/scissors2_exp1_RR/keypoints.mat',{'data':batch})



def WorldToCamera(camera_location,camera_radius,world_center):
	tmp=camera_location-world_center
	camera_location[0]=tmp[0]
	camera_location[1]=tmp[2]
	camera_location[2]=tmp[1]

	Rc=np.zeros((3,3))
	#local world_z=torch.Tensor({{0},{1},{0}})
	world_z=np.array([0,1,0])
	#local world_frame=torch.eye(3)
	world_frame=np.eye(3)
	#local camera_frame=torch.Tensor(3,3)
	camera_frame=np.zeros((3,3))
	#camera_frame[{{},{1}}]=-camera_location/torch.norm(camera_location)
	#print camera_location
	#print camera_frame
	camera_frame[:,0]=-camera_location/np.linalg.norm(camera_location)
	#local camera_x=camera_frame[{{},{1}}]
	camera_x=camera_frame[:,0]
	#local camera_y=torch.cross(camera_x,world_z)
	camera_y=np.cross(camera_x,world_z)
	#local camera_z=torch.cross(camera_y,camera_x)
	camera_z=np.cross(camera_y,camera_x)
	
	#print camera_y
	#if torch.all(torch.eq(camera_y,torch.zeros(3,1))) then 
	if np.all(np.equal(camera_y,np.zeros((3,1)))):
		print('Should be here')
		#camera_frame[{{},{3}}]=torch.Tensor({{0},{0},{1}})
		camera_frame[:,2]=np.array([0,0,1])
		#camera_frame[{{},{2}}]=torch.Tensor({{1},{0},{0}})
		camera_frame[:,1]=np.array([1,0,0])
	else:
		#print('OMG here')
		
		#camera_frame[{{},{3}}]=camera_y/torch.norm(camera_y)
		camera_frame[:,2]=camera_y/np.linalg.norm(camera_y)
		#camera_frame[{{},{2}}]=camera_z/torch.norm(camera_z)
		camera_frame[:,1]=camera_z/np.linalg.norm(camera_z)
	#end
	#print("Look here")
	#print(camera_frame)

	#for camera_dim=1,3 do
	for camera_dim in range(3):
		for world_dim in range(3):
	#	for world_dim=1,3 do
			#Rc[camera_dim][world_dim]=torch.dot(camera_frame[{{},{camera_dim}}],world_frame[{{},{world_dim}}])
			Rc[camera_dim][world_dim]=np.dot(camera_frame[:,camera_dim],world_frame[:,world_dim])
		#end
	#end
	#Tw[1][1] = camera_radius
	#print(camera_frame)
	print(Rc)
	#return Rotation_wc
	return Rc,np.array([camera_radius,0.0,0.0])

def ObjectToWorld(y,p,r,location,world_center,verbose=False):
	R_roll=np.array([[1,0,0],[0,math.cos(r),math.sin(r)],[0,-math.sin(r),math.cos(r)]])
	R_yaw=np.array([[math.cos(y),0,-math.sin(y)],[0,1,0],[math.sin(y),0,math.cos(y)]])
	R_pitch=np.array([[math.cos(p),math.sin(p),0],[-math.sin(p),math.cos(p),0],[0,0,1]])
	if verbose==True:
		print(math.degrees(y),math.degrees(p),math.degrees(r))
		print(rotation2ypl(reduce(np.dot, [R_yaw,R_pitch,R_roll])))
	return reduce(np.dot, [R_yaw,R_pitch,R_roll]),np.array([location[0]-world_center[0],\
		location[2]-world_center[2],location[1]-world_center[1]])

def ObjectInCamera(keypoints,object_location,object_rotation):
	#notice offset 46 here
	To = np.array([[object_location[0]-world_center[0]],[object_location[1]-world_center[1]],[object_location[2]-world_center[2]]])
	#local Rw = ObjectToWorld(object_rotation)
	#local Xo = ListToTensor(keypoints)
	#return Rc*Rw*Xo+torch.expandAs((Rc*To+Tw),Xo)


#config_path='/home/qi/Desktop/cvpr/lua_scripts/config_RR.json'
config_path='/home/qi/Desktop/cvpr/Config_file/Realistic_rendering/config.json'
def readCamera(config_path):
	batch=np.zeros((batchNum,2),dtype=np.object)
	with open(config_path,'r') as f:
		cnt=0
		for line in f:
			
			data=json.loads(line)
			#camera_location=np.zeros((3))
			#camera_location[0]=tmp[0]
			#camera_location[1]=tmp[2]
			#camera_location[2]=tmp[1]
			batch[cnt,:]=WorldToCamera(np.array(data['camera_settings']['location']),data['camera_settings']['radius'],world_center)
			cnt+=1
			#tmp=np.array(data['camera_settings']['location'])-world_center
			
			#if cnt==40:
			#WorldToCamera(camera_location)
			#print(cnt)
			#camera=np.array(data['camera_settings']['radius'])
			#print WorldToCamera(camera_location)
			
			#break
	sio.savemat('/home/qi/Desktop/cvpr/testing/data/scissors2_exp1_RR/Camera.mat',{'Rw':batch})
	f.close()


def swap_cols(arr, frm, to):
    arr[:,[frm, to]] = arr[:,[to, frm]]
    return arr
animation_path='/home/qi/Desktop/cvpr/Config_file/Realistic_rendering/block_animation_fps.json'
def readObject(animation_path,verbose=False):
	Frame=np.zeros((300,2),dtype=np.object)
	Keypoints=np.zeros((300,),dtype=np.object)
	with open(animation_path,'r') as f:
		content=f.read()
		data=json.loads(content)
		print(len(data))
		cnt=0
		for frame in data:
			#print np.array(frame['keypoints'])
			#Xo=swap_cols(np.array(frame['keypoints'])[:9,:],1,2)

			#This is in xzy axis
			Keypoints[cnt]=swap_cols(np.array(frame['keypoints']),1,2)
			#np.array(frame['keypoints'])
			#print Xo
			#r=-frame['parts']['scissors_l']['roll']/180*math.pi
			#p=-frame['parts']['scissors_l']['pitch']/180*math.pi
			#y=frame['parts']['scissors_l']['yaw']/180*math.pi
			r=-frame['object_rotation'][2]/180*math.pi
			p=-frame['object_rotation'][1]/180*math.pi
			y=frame['object_rotation'][0]/180*math.pi

			Frame[cnt,:]=ObjectToWorld(y,p,r,frame['object_location'],world_center)
			#r=0
			#p=0
			#y=0
			#print(r,p,y)
			#print(frame['parts']['scissors_l']['yaw'],frame['parts']['scissors_l']['pitch'],frame['parts']['scissors_l']['roll'])

			
			cnt+=1
			#if cnt==2:
			#	break
			
			#print(rotation2ypl(R_yaw))
			#print(rotation2ypl(R_pitch))
			#print(rotation2ypl(R_roll))
			#print(R_yaw,R_pitch,R_roll)
	#return reduce(np.dot, [R_yaw,R_pitch,R_roll]),Xo
	print('Count of frame number is '+str(cnt))
	sio.savemat('/home/qi/Desktop/cvpr/testing/data/scissors2_exp1_RR/Object.mat',{'Ro':Frame,'keypoints':Keypoints})
if __name__ == '__main__':
	readKeypoints(path,batchNum,200,18)
	#readCamera(config_path)
	#print c
	#readObject(animation_path)
	#print o
	#print np.dot(c,o)
	#print o.transpose()
	#t=swap_cols(o.transpose(),1,2)
	
	#sio.savemat('/home/qi/Desktop/cvpr/EPnP/Matlab/data/test.mat',{'camera':c, 'object':o, 'keypoint':x})
	#print np.dot(c,o)
