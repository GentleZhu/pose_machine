#Author: Qi Zhu, Robotics Institute at Carnegie Mellon University
#From Json data to create ground truth keypoints/object position&rotation/viewport .mat file

import cv2
import numpy as np
import torchfile

mask_path='/home/qi/Desktop/cvpr/data/segmentation/scissors1_exp5/batch1_5.jpg'
#mask_path='/home/qi/Desktop/batch1_1.t7'
img_dir='/home/qi/Desktop/cvpr/data/screenshots/scissors1_exp4/batch1_5.jpg'
#img_dir='/home/qi/Desktop/cvpr/data/screenshots/batch1_1.jpg'
indoor_img='/home/qi/Desktop/hdd/MITindoor/children_room/06playroom_2_.jpg'
obj_pos=[548.073,295.783]
#img_height=720
#img_width=1280
def readMask(mask_path,img_dir,obj_pos,stride=3):
	msk=cv2.imread(mask_path,cv2.IMREAD_GRAYSCALE)
	#print(img.shape)
	#msk=torchfile.load(mask_path)
	#print msk.shape
	#return 
	x=np.where(msk>128)
	img=cv2.imread(img_dir)
	output=cv2.imread(indoor_img)
	img_height=output.shape[0]
	img_width=output.shape[1]
	offset_x=img_height/2-obj_pos[1]
	offset_y=img_width/2-obj_pos[0]
	#print(img.shape)
	t=[]
	t.append(x[0]+int(offset_x/stride))
	t.append(x[1]+int(offset_y/stride))
	for i in range(len(x[0])):
		#print stride
		output[stride*t[0][i]:stride*t[0][i]+3,stride*t[1][i]:stride*t[1][i]+3,:]=\
		img[stride*x[0][i]:stride*x[0][i]+3,stride*x[1][i]:stride*x[1][i]+3,:]#=np.zeros((3,3),dtype=np.int)
		#img[x[0][i],x[1][i],:]=np.zeros((3),dtype=np.int)
		#=np.array([0,0,0])

	cv2.imwrite('/home/qi/Desktop/cvpr/test_img/test_mit/2.jpg',output)
	#cv2.imshow('mask',output)
	#cv2.waitKey(0)

if __name__=="__main__":
	readMask(mask_path,img_dir,obj_pos)

