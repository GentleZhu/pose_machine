#Author: Qi Zhu, Robotics Institute at Carnegie Mellon University
#Generate JSON file used for LMDB generation
import json
import random
batchNum=41
path='/home/qi/Desktop/cvpr/data/jsondata/scissors1_exp4/'
jsondata=dict()
jsondata['root']=[]
cnt=0
for i in range(1,batchNum+1):
	file=open(path+'batch'+str(i)+'.json','r')
	for line in file:
		#print(line)
		#if random.uniform(0, 1)>0.5:
		cnt+=1
		tmp=json.loads(line)
		tmp['annolist_index']=cnt
		tmp['img_paths']=tmp['img_paths'].replace('screenshots','screenshots/scissors1_exp4')
		jsondata['root'].append(tmp)

jsonfile=open('/home/qi/Desktop/cvpr/data/jsondata/'+'scissors1_exp4.json','w')
jsonfile.write(json.dumps(jsondata, sort_keys=True, indent=4, separators=(',', ': ')))
#jsonfile.write(json.dumps(jsondata))
