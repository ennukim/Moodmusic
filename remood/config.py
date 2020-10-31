#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 12 21:43:18 2020

@author: sallykim
"""
import json

d = {0: [0,4, 0,50, 85,float('inf'), 0,float('inf')], 
     1: [0,4, 50,float('inf'), 85,float('inf'), 70,float('inf')], 
     2: [4,float('inf'), 50,0, 85,float('inf'), 70,float('inf')],
     3: [4,float('inf'), 0,50, 85,float('inf'), 0,float('inf')]}

#json.dump(d, open("config.txt",'w'))


mood_dict = json.load(open("config.txt"))

#print(mood_dict)

for mood in mood_dict:
    config = mood_dict.get(mood)
    print(config)
    if(config[0] <= 1 <= config[1] and config[2] <= 49 <= config[3]):
        print(int(mood))