import moodmusicV2 as moodmusic
import time
import os
from threading import Thread, Event
from queue import Queue
import json

#0 = "Mellow/Relax"
#1 = "Fun/Happy"
#2 = "Upbeat/Exercising"
#3 = "Sad/Melancholy"

current_mood = 0
e = Event()
q = Queue()

def mood_file(file):
    global current_mood
    mood_read = file.read()
    current_mood = int(mood_read)

def save_mood(file):
    while True:
        new_mood = str(current_mood)
        file.seek(0)
        print(new_mood) #to see what is being stored/being used by moodreader)
        file.write(new_mood)
        time.sleep(0.1)
    
        
#False for low-normal / True for normal-high
def photo_label(sensor_data):
    if sensor_data >= 0 and sensor_data <= 50:
        return False
    elif sensor_data > 50:
        return True

def int_temp_label(sensor_data):
    if sensor_data >= 0 and sensor_data <= 95:
        return False
    elif sensor_data > 95:
        return True

def ext_temp_label(sensor_data):
    if sensor_data >= 0 and sensor_data <= 80:
        return False
    elif sensor_data > 80:
        return True

# is the reading fluctuating high or low?
def accel_label(sensor_data):
    if sensor_data < 4:
        return False
    else:
        return True
    return


def read_mood_from_file(filename):
    #json.dump(d, open("config.txt",'w'))
    mood_dict = json.load(open(filename))
    
    return mood_dict


def output_mood(filename):
    global current_mood
    mood_dict = read_mood_from_file(filename)
    while True:
        q.put(current_mood)

        for mood in mood_dict:
            config = mood_dict.get(int(mood))
            if config[0] <= accel_var_max < config[1] and config[2] <= photo_ewma < config[3] and config[4] <= temp_int_ewma < config[5] and config[6] <= temp_ext_ewma < config[7]:
                print("current mood is %s" % mood)
                current_mood = mood
                # update current mood globally
    time.sleep(0.5)


def alarm():
    while True:
        if q.get() != current_mood:
            os.system("pkill mpg123") 
            print("Mood Change: ", current_mood)
            time.sleep(0.1)
            playlist(current_mood)

def playlist(current_mood):
    if (current_mood == 0):
        os.system("mpg123 -Z ~/app/relax/*.mp3 &")
    elif (current_mood == 2):
        os.system("mpg123 -Z ~/app/upbeat/*.mp3 &")
    elif (current_mood == 3):
        os.system("mpg123 -Z ~/app/sad/*.mp3 &")
    else:
        os.system("mpg123 -Z ~/app/happy/*.mp3 &")
                
photo_ewma = 0
photo_alpha = 0.8

def read_photo(photo):
    global photo_ewma
    while True:
	    photo_val_new = photo.read(1)          
	    photo_ewma_new = photo_alpha*photo_ewma + (1-photo_alpha)*photo_val_new
	    photo_ewma = photo_ewma_new
	    time.sleep(0.1)

temp_int_ewma = 0
temp_ext_ewma = 0
temp_alpha = 0.8

def read_int(temp_int):
    global temp_int_ewma
    while True:
	    temp_int_new = temp_int.read_temp()[0][1]   
	    temp_int_ewma_new = temp_alpha*temp_int_ewma + (1-temp_alpha)*temp_int_new
	    temp_int_ewma = temp_int_ewma_new
	    time.sleep(0.1)

def read_ext(temp_ext):
    global temp_ext_ewma
    while True:
	    temp_ext_new = temp_ext.read_temp()[1][1]  
	    temp_ext_ewma_new = temp_alpha*temp_ext_ewma + (1-temp_alpha)*temp_ext_new
	    temp_ext_ewma = temp_ext_ewma_new
	    time.sleep(0.1)
# repeat something similar for temp, both int and ext

accelx_var = 0
accelx_ewma = 0
accely_var = 0
accely_ewma = 0
accelz_var = 0
accelz_ewma = 0
accel_alpha_mean = 0.8
accel_alpha_var = 0.8
accel_var_max = 0

def read_accel(accel):
    global accelx_ewma, accelx_var, accely_ewma, accely_var, accelz_ewma, accelz_var, accel_var_max
    while True:
        accel_val_new = accel.accelerometer_read()
	    #create/separate the read function from the init in library
        x_new =  accel_val_new[0]
        accelx_ewma_new = accel_alpha_mean*accelx_ewma + (1-accel_alpha_mean)*x_new
        accelx_ewma = accelx_ewma_new
        accelx_var_new = accel_alpha_var*accelx_var + (1-accel_alpha_var)*abs(accelx_ewma-x_new)
        accelx_var = accelx_var_new
        
        y_new =  accel_val_new[1]
        accely_ewma_new = accel_alpha_mean*accely_ewma + (1-accel_alpha_mean)*y_new
        accely_ewma = accely_ewma_new
        accely_var_new = accel_alpha_var*accely_var + (1-accel_alpha_var)*abs(accely_ewma-y_new)
        accely_var = accely_var_new

        z_new =  accel_val_new[2]
        accelz_ewma_new = accel_alpha_mean*accelz_ewma + (1-accel_alpha_mean)*z_new
        accelz_ewma = accelz_ewma_new
        accelz_var_new = accel_alpha_var*accelz_var + (1-accel_alpha_var)*abs(accelz_ewma-z_new)
        accelz_var = accelz_var_new

        accel_var_max = max(accelx_var, accely_var, accelz_var)
      
	    # repeat for three directions
        time.sleep(0.1)

def get_display_val():
    global current_mood, accel_var_max, photo_ewma, temp_int_ewma, temp_ext_ewma
    lst = [accel_var_max, photo_ewma, temp_int_ewma, temp_ext_ewma]
    return ((current_mood,lst))


#light is the main varibale that determines happy vs mellow
def main():
    #depends on what the name of the function is in moodmusic
    file_read = open("moodtracker.txt", 'r')
    mood_file(file_read)
    file_read.close()
    playlist(current_mood) #defaulted to 0 based on text file
    file_write = open("moodtracker.txt", 'w')
    
    # init photoresistor
    photo = moodmusic.MCP3002()
    # init temp sensor
    temp_class = moodmusic.Temperature() #init temp class
    #temp_tuple = temp_class.read_temp()
    #temp_int = temp_tuple[0] #base dir 1
   # temp_ext = temp_tuple[1] #base dir 2
    # init accelerometer
    accel_class = moodmusic.Accelerometer() #class initialization
    #accel = accel_class.accelerometer_read() #should return a tuple of 3 directions (xyz) m/s^2
    
    
    # launch a thread to read photoresistor
    photo_thread = Thread(target=read_photo, args=[photo])
    # launch thread to read temp sensor
    temp_int_thread = Thread(target=read_int, args=[temp_class])
    temp_ext_thread = Thread(target=read_ext, args=[temp_class])
    # launch thread to read accelerometer
    accel_thread = Thread(target=read_accel, args=[accel_class])
        
    # launch a thread to monitor and check mood
    mood_thread = Thread(target=output_mood)
    #check_thread = Thread(target=check_mood)
    alarm_thread = Thread(target=alarm)

    save_mood_thread = Thread(target = save_mood, args=[file_write])
    #reset_alarm_thread = Thread(target=reset_alarm)
    #including events to interrupt the mood_thread
    
    photo_thread.start()
    temp_int_thread.start()
    temp_ext_thread.start()
    accel_thread.start()
    mood_thread.start()
    #check_thread.start()
    alarm_thread.start()
    save_mood_thread.start()
    #reset_alarm_thread.start()
    
    photo_thread.join()
    temp_int_thread.join()
    temp_ext_thread.join()
    accel_thread.join()
    mood_thread.join()
    #check_thread.join()
    alarm_thread.join()
    save_mood_thread.join()
    #reset_alarm_thread.join()
    
    #print(("p: ", photo_ewma, "int_temp: ",temp_int_ewma, "ext_temp: ",temp_ext_ewma, "accel: ",accel_var_max))
    #print("Current Mood: ", current_mood)
               
#main()




#problems:


#implement 
#create a file that saves the last mood from last operation of code/ read when activate code
#display all songs (via a list call or smthin)
#mood change is still wonky, can detect first mood change but not any subsequential ones


#flask stuff
#include breaks-skip function?
#include functions to read in playlist for flask (return a list of songs)
#include add song(?)
#include way to read in song title for display
#include a way to delay song changing/detect only a moodshift



