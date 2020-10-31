"""
Created on Tue May 12 22:35:49 2020

@author: sallykim
"""

import json

'''
dictionary will look like:
{mood,accel_var_low,accel_var_high,photo_ewma_low,
photo_ewma_high,int_temp_low,int_temp_high,ext_temp_low,ext_temp_high}

d = {"Mellow": [0,4, 0,50, 85,float('inf'), 0,float('inf')], 
     "Happy": [0,4, 50,float('inf'), 85,float('inf'), 70,float('inf')], 
     "Melancholy": [4,float('inf'), 0,50, 85,float('inf'), 0,float('inf')], 
     "Upbeat": [4,float('inf'), 50,0, 85,float('inf'), 70,float('inf')]}
'''

def config(filename):
    #json.dump(d, open("config.txt",'w'))
    mood_dict = json.load(open(filename))
    
    return mood_dict

    
while True:
    mood_dict = config(filename)
    key_lst = []
    for key in mood_dict.keys():
        key_lst.append(key)
        
    current_mood = key_lst[0] # default mood
    for mood in mood_dict:
        config = mood_dict.get(mood)
        if config[0] <= accel_var_max <= config[1] and config[2] <= photo_ewma <= config[3] and config[4] <= temp_int_ewma <= config[5] and config[6] <= temp_ext_ewma <= config[7]:
            print("current mood is %s" % mood)
            current_mood = mood
            # update current mood globally


