import moodmusic
import time

def photoresistor(): #adc
    init = moodmusic.MCP3002()
    timer = 0
    while timer<10:
        read = init.read(1)
        timer+=1
        print(read)
        time.sleep(1)
 
def heartrate():#adc
    pulse = moodmusic.Pulsesensor()
    pulse.startAsyncBPM()
    timer=0
    try:
        while timer<0:
            bpm = pulse.BPM
            if bpm>0:
                print("BPM: %d" % bpm)
            else:
                print("No heartbeat")
            time.sleep(1)
            timer+=1
    except:
        pulse.stopAsyncBPM()
    

def temperature():
    timer = 0
    while timer<10:
        temp = moodmusic.temperature_sensor()
        timer+=1
        print(temp)
        time.sleep(1)

def accelerometer():
    timer = 0
    while timer<10:
        accelerometer = moodmusic.accelerometer()
        print("%f %f %f"%accelerometer.acceleration)
        timer+=1
        time.sleep(1)


def speaker(): #pre-installed
    moodmusic.speaker()


photoresistor() #prints out 10 values of light reading (ranging decimal values of 10-50)
temperature() #prints both celsius and farenheit
heartrate() #prints heartrate, some problems still in code
speaker() #plays white noise
accelerometer() #should print out 3 dimensions of movement


