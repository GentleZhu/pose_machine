#Author: Qi Zhu, Robotics Institute at Carnegie Mellon University
#Generate different scenes based on configuration scripts: Look into scene_registration.py

import cv2
import numpy as np
import random
import scene_registration as sr

#Scissors1=np.array((20,20))
#DeskBook1=np.array((19,27))*0.819641
#DeskBook2=np.array((19,27))*0.819641
#DeskMug1=np.array((20,13))*0.75
#DeskMug2=np.array((20,13))*0.75
#DeskBowl1=np.array((43,43))*0.862164
#DeskBowl2=np.array((43,43))*0.613688
#DeskVase1=np.array((16,16))*0.716157
#DeskVase2=np.array((16,16))*0.515515
#DeskVase3=np.array((16,16))*0.560982

#Desk=np.array((69,160))
#Desk=np.array((220,120))

#obj_list=[Scissors1,DeskBowl2,DeskBook1,DeskBook2,DeskMug1,\
#DeskMug2,DeskVase1,DeskVase3,DeskVase2]
#obj_name=['scissors1','DeskBowl2','DeskBook1','DeskBook2','DeskMug1',\
#'DeskMug2','DeskVase1','DeskVase3','DeskVase2']
#material_pool={
#	'Desk':['M_Tiles_Mat','M_CoathookBack','M_CoffeTable_MAT','M_Curtain_MAT','M_Ceramic_Mat'],
#	'DeskVase1':['M_Ceramic_Mat','M_PlantBark_Mat','M_PlantLeaf_Mat'],
#	'DeskVase2':['M_Ceramic_Mat','M_Glas_MAt'],
#	'DeskVase3':['M_Statue','M_Socket']
#}
Desk,material_pool,obj_list,obj_name,obj_changes=sr.scene_office()
def detect_occulusion(pos,ptr,obj_pos,obj_list):
	for i in range(ptr):
		#print i
		#print(pos,obj_pos[i])
		if (abs(pos[0]-obj_pos[i][0])<(obj_list[i][0]+obj_list[ptr][0])/2 and \
		abs(pos[1]-obj_pos[i][1])<(obj_list[i][1]+obj_list[ptr][1])/2):
			return True
		#else:
			#print(i,pos,obj_pos[i])
	return False


def scene_generate(iteration,target,world_center):
	l=len(obj_list)
	#candidate_pool=Desk*np.random.random([l*100,2])
	scene_settings=[]
	cnt=0
	
	
	#print(obj_list)
	result=scene_arrangement(10000,iteration,target)
	

	for iteration in range(iteration):
		ptr=0
		scene={}

		#scene background objects
		scene['bkg']=[]
		scene['bkg'].append({'id':'Desk', 'material':random.choice(material_pool)})
		obj_pos=result[iteration]
		for ptr in range(len(obj_list)):
		#while ptr<len(obj_list):
			candidate=obj_pos[ptr]
				
			temp=np.round(candidate-Desk/2,3).tolist()
			temp[0]+=world_center[0]
			temp[1]+=world_center[1]
			if obj_name[ptr]==target:
				temp.append(world_center[2]+12)
				scene[target]=temp
				#print temp
			else:
				temp.append(world_center[2])
				if obj_name[ptr] in obj_changes:
					scene['bkg'].append({'id':obj_name[ptr],'material':random.choice(material_pool), 'location':temp})
				else:
					scene['bkg'].append({'id':obj_name[ptr],'location':temp})
				obj_pos.append(candidate)
				ptr+=1

		scene_settings.append(scene)
	return scene_settings


def scene_generating(iteration,target,world_center):
	l=len(obj_list)
	#candidate_pool=Desk*np.random.random([l*100,2])
	scene_settings=[]
	cnt=0
	
	
	#print(obj_list)
	for iteration in range(iteration):
		ptr=0
		scene={}
		obj_pos=[]
		while ptr<len(obj_list):
			cnt+=1
			if obj_name[ptr]==target:
				#print('here')
				#print(Desk-obj_list[ptr]*2)
				candidate=(Desk-np.array([110,40]))*np.random.random(2)+np.array([55,20])
				#print(candidate)
				temp=np.round(candidate-Desk/2,3).tolist()
				temp[0]+=world_center[0]
				temp[1]+=world_center[1]
				if obj_name[ptr]==target:
					temp.append(world_center[2]+10)
					scene[target]=temp
					#print temp
				else:
					temp.append(world_center[2])
				obj_pos.append(candidate)
				ptr+=1
		scene_settings.append(scene)
	return scene_settings

def dis(pos):
	Sum=0
	for i in range(1,len(pos)):
		Sum+=np.linalg.norm(pos[i]-pos[0])
	return Sum
def scene_arrangement(iteration,iter,target='scissors1'):
	l=len(obj_list)
	#candidate_pool=Desk*np.random.random([l*100,2])
	pool=[]
	result=[]
	dis_pool={}
	cnt=0
	
	
	#print(obj_list)
	for iteration in range(iteration):
		ptr=0
		#scene background objects
		obj_pos=[]
		cnt=0
		while ptr<len(obj_list):
			if cnt>10000:
				break
			cnt+=1
			if obj_name[ptr]==target:
				candidate=(Desk-np.array([60,20]))*np.random.random(2)+np.array([20,10])
				#candidate=(Desk-np.array([15,70]))*np.random.random(2)+np.array([7.5,35])
			else:
				candidate=(Desk-obj_list[ptr])*np.random.random(2)+obj_list[ptr]/2
			if not detect_occulusion(candidate,ptr,obj_pos,obj_list):
				obj_pos.append(candidate)
				ptr+=1
		if ptr==len(obj_list):
			dis_pool[iteration]=dis(obj_pos)
			pool.append(obj_pos)
		else:
			print('else')
			dis_pool[iteration]=1000000
			pool.append(obj_pos)
	top=0
	for key, value in sorted(dis_pool.iteritems(), key=lambda (k,v): (v,k)):
		if top>iter:
			break
		else:
			result.append(pool[key])
		top+=1
	return result

if __name__=='__main__':
	result=scene_arrangement(10000,200)
		