#Author: Qi Zhu, Robotics Institute at Carnegie Mellon University
#Write articulate object model file in 'models' folder
import argparse
import json
import sys
import math
import numpy as np
model_dir='../models/'

def parseMinmax(string):
	minmax=[]
	for sub in string.split(','):
		minmax.append(map(int, sub.split(':')))
	return minmax

def readKeypoints(model_file,scale=1):
	keypoint=[]
	for line in f:
		#print line.rstrip().replace('\n','').split(' ')
		keypoint.append(map(float,line.rstrip().replace('\n','').split(' ')))
		
	keypoint=np.round(scale*np.array(keypoint),3)
	return keypoint



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--model', type=str, help='model_*', required=True)
    parser.add_argument('--parts', type=str, help='partA,partB,etc', required=True)
    parser.add_argument('--constraints', type=str, help='constraintA,constraintB,etc', required=True)
    parser.add_argument('--axis', type=str, help='X,Y,Z,etc', required=True)
    parser.add_argument('--minmax', type=parseMinmax, help='minA:maxA,minB:maxB,etc')
    args = parser.parse_args()
    parts=args.parts.split(',')
    constraints=args.constraints.split(',')
    axis=args.axis.split(',')
    if args.minmax:
    	if not len(parts)==len(constraints)==len(axis)==len(args.minmax):
    		raise ValueError('Length of parameters: parts, contrainst, axis and minmax should be same')
    else:
    	if not len(parts)==len(constraints)==len(axis):
    		 raise ValueError('Length of parameters: parts, contrainst, axis should be same')
    try:
    	key={}
    	for i in range(len(parts)):
    		with open(model_dir+args.model+'_'+parts[i],'r') as f:
    			key[parts[i]]=readKeypoints(f,120)
                key[parts[i]][:,1]=-key[parts[i]][:,1]
    		f.close()
    except IOError,e:
    	print (str(e))
    	sys.exit()
    #print('Pass parameter check')
    
    #args.inputsize_x, args.inputsize_y = map(int, args.inputsize.split(','))
    output={}
    output['id']=args.model
    output['parts']=[]
    for i in range(len(parts)):
    	part={}
    	part['id']=args.model+'_'+parts[i]
    	part['constraints']=constraints[i]
    	part['axis']=axis[i]
    	part['keypoints']=key[parts[i]].tolist()
    	if args.minmax:
    		part['min']=args.minmax[i][0]
    		part['max']=args.minmax[i][1]
    	output['parts'].append(part)
    #print(output)
    with open(model_dir+args.model+'.model','w') as f:
    	json.dump(output,f,sort_keys=True, indent=4, separators=(',', ': '))
    f.close()
