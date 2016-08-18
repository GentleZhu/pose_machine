#Author: Qi Zhu, Robotics Institute at Carnegie Mellon University
#This script checks the keypoints projection in generated images 

import json
import cv2
import numpy as np
import math

#batchNum=38
#jsondata=[]
path='/home/qi/Desktop/cvpr/data/jsondata/scissors2_exp1_RR/'
img_path='/home/qi/Desktop/cvpr/data/'
vertex_connection=dict()
vertex_connection[1]=[2,4,5]
vertex_connection[2]=[3,6]
vertex_connection[3]=[4,7]
vertex_connection[4]=8
vertex_connection[5]=[6,8]
vertex_connection[6]=7
vertex_connection[7]=8

if __name__ == "__main__":	
	
	#print(vertex_connection)
	
	for batchNum in range(1):
		file=open(path+'batch'+str(batchNum+1)+'.json','r')
		tt=0
		for line in file:
			tt+=1
			#print(line)
			#jsondata.append(json.loads(line))
			data=json.loads(line)
			blank_image = cv2.imread(img_path+data['img_paths'].replace('screenshots','screenshots/scissors2_exp1_RR'))
			#blank_image = cv2.imread(img_path+data['img_paths'])
			#blank_image = np.zeros((data['img_height'],data['img_width'],3), np.uint8)
			#print(data['img_paths'])
			center=data['objpos']
			cv2.circle(blank_image, (int(round(center[0])),int(round(center[1]))), 5, (255,0,0), -1)
			cnt=1
			for keypoint in data['joint_self']:
				#print(keypoint)
				if (keypoint[2]==1):
					#cv2.putText(img, text, org, fontFace, fontScale, color[, thickness[, lineType[, 
					#cv2.putText(blank_image,str(cnt),(int(keypoint[0]),int(keypoint[1])),cv2.FONT_HERSHEY_SIMPLEX, 0.3, np.random.randint(0,255,(3)).tolist())
					cv2.circle(blank_image, (int(round(keypoint[0])),int(round(keypoint[1]))), 1, (0,255,0), -1)
				cnt+=1
			#cv2.imshow('Pose_test',blank_image)
			cv2.imwrite('/home/qi/Desktop/cvpr/data/groundtruth/'+str(batchNum)+'_'+str(tt)+'.jpg',blank_image)
		#cv2.waitKey(0)	
		#break