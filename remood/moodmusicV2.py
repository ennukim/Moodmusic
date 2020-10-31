import spidev
import time
import board 
import busio
import adafruit_adxl34x
import os
import threading
import glob


class MCP3002: #adc class setup 
    def __init__(self, bus=0, port= 0):
        self.bus = bus
        self.port = port
        self.open()
        
    def open(self):
        self.spi = spidev.SpiDev()
        self.spi.open(self.bus,self.port)
        self.spi.max_speed_hz = 7629
        
    #photoresistor
    def read(self, adc_channel):
        resp = self.spi.xfer2([0b01100000 + (adc_channel << 4), 0b00000000]) 

        counter = 0;
        value = 0
        for b in resp:
            if counter == 0:
                value += (b<<8)
                counter+=1
            else: value+=b
        return value
    #from interfacing electronics lab #4
   
    
class Temperature():
    def __init__(self):
        # Initialize the GPIO Pins
        os.system('modprobe w1-gpio')  # Turns on the GPIO module
        os.system('modprobe w1-therm') # Turns on the Temperature module
        self.base_dir = '/sys/bus/w1/devices/' 
        self.device_folder = glob.glob(self.base_dir + '28*')[0] 
        self.device_folder2 = glob.glob(self.base_dir +'28*')[1]
        self.device_file = self.device_folder + '/w1_slave' 
        self.device_file2 = self.device_folder2 + '/w1_slave'

    #combined setup from https://blog.oddbit.com/post/2018-03-27-multiple-1-wire-buses-on-the-/ 
    # A function that reads the sensors data
    def read_temp_raw(self, file):
        f = open(file, 'r') # Opens the temperature device file
        lines = f.readlines() # Returns the text
        f.close()
        return lines
  # Convert the value of the sensor into a temperatur
    def read_temp_file(self, device):
        lines = self.read_temp_raw(device) # Read the temperature 'device file'
        # While the first line does not contain 'YES', wait for 0.2
        # and then read the device file again
        while lines[0].strip()[-3:] != 'YES':
            time.sleep(0.2)
            lines = self.read_temp_raw(device)
              # Look for the position of the '=' in the second line of the
              # device file.
        equals_pos = lines[1].find('t=')

        # If the '=' is found, convert the rest of the line after the
        # '=' into degrees Celsius, then degrees Fahrenheit
        if equals_pos != -1:
              temp_string = lines[1][equals_pos+2:]
              temp_c = float(temp_string) / 1000.0
              temp_f = temp_c * 9.0 / 5.0 + 32.0
              return temp_c, temp_f
          # code is from combined from the temperature sensor
    def read_temp(self):
        value1 = self.read_temp_file(self.device_file)
        value2 = self.read_temp_file(self.device_file2)
        return value1, value2
      

class Accelerometer:
    def __init__(self):
        i2c = busio.I2C(board.SCL, board.SDA)
        self.accelerometer = adafruit_adxl34x.ADXL345(i2c)
    def accelerometer_read(self):
        return self.accelerometer.acceleration

    #code and setup from https://pimylifeup.com/raspberry-pi-accelerometer-adxl345/
class Pulsesensor:
    def __init__(self, channel = 0, bus = 0, port = 0):
        self.channel = channel
        self.BPM = 0
        self.adc = MCP3002(bus, port)

    def getBPMLoop(self):
        # init variables
        rate = [0] * 10         # array to hold last 10 IBI values
        sampleCounter = 0       # used to determine pulse timing
        lastBeatTime = 0        # used to find IBI
        P = 512                 # used to find peak in pulse wave, seeded
        T = 512                 # used to find trough in pulse wave, seeded
        thresh = 525            # used to find instant moment of heart beat, seeded
        amp = 100               # used to hold amplitude of pulse waveform, seeded
        firstBeat = True        # used to seed rate array so we startup with reasonable BPM
        secondBeat = False      # used to seed rate array so we startup with reasonable BPM

        IBI = 600               # int that holds the time interval between beats! Must be seeded!
        Pulse = False           # "True" when User's live heartbeat is detected. "False" when not a "live beat". 
        lastTime = int(time.time()*1000)
        
        while not self.thread.stopped:
            Signal = self.adc.read(self.channel)
            currentTime = int(time.time()*1000)
            
            sampleCounter += currentTime - lastTime
            lastTime = currentTime
            
            N = sampleCounter - lastBeatTime

            # find the peak and trough of the pulse wave
            if Signal < thresh and N > (IBI/5.0)*3:     # avoid dichrotic noise by waiting 3/5 of last IBI
                if Signal < T:                          # T is the trough
                    T = Signal                          # keep track of lowest point in pulse wave 

            if Signal > thresh and Signal > P:
                P = Signal

            # signal surges up in value every time there is a pulse
            if N > 250:                                 # avoid high frequency noise
                if Signal > thresh and Pulse == False and N > (IBI/5.0)*3:       
                    Pulse = True                        # set the Pulse flag when we think there is a pulse
                    IBI = sampleCounter - lastBeatTime  # measure time between beats in mS
                    lastBeatTime = sampleCounter        # keep track of time for next pulse

                    if secondBeat:                      # if this is the second beat, if secondBeat == TRUE
                        secondBeat = False;             # clear secondBeat flag
                        for i in range(len(rate)):      # seed the running total to get a realisitic BPM at startup
                          rate[i] = IBI

                    if firstBeat:                       # if it's the first time we found a beat, if firstBeat == TRUE
                        firstBeat = False;              # clear firstBeat flag
                        secondBeat = True;              # set the second beat flag
                        continue

                    # keep a running total of the last 10 IBI values  
                    rate[:-1] = rate[1:]                # shift data in the rate array
                    rate[-1] = IBI                      # add the latest IBI to the rate array
                    runningTotal = sum(rate)            # add upp oldest IBI values

                    runningTotal /= len(rate)           # average the IBI values 
                    self.BPM = 60000/runningTotal       # how many beats can fit into a minute? that's BPM!

            if Signal < thresh and Pulse == True:       # when the values are going down, the beat is over
                Pulse = False                           # reset the Pulse flag so we can do it again
                amp = P - T                             # get amplitude of the pulse wave
                thresh = amp/2 + T                      # set thresh at 50% of the amplitude
                P = thresh                              # reset these for next time
                T = thresh

            if N > 2500:                                # if 2.5 seconds go by without a beat
                thresh = 512                            # set thresh default
                P = 512                                 # set P default
                T = 512                                 # set T default
                lastBeatTime = sampleCounter            # bring the lastBeatTime up to date        
                firstBeat = True                        # set these to avoid noise
                secondBeat = False                      # when we get the heartbeat back
                self.BPM = 0

            time.sleep(0.005)
            
        
    # Start getBPMLoop routine which saves the BPM in its variable
    def startAsyncBPM(self):
        self.thread = threading.Thread(target=self.getBPMLoop)
        self.thread.stopped = False
        self.thread.start()
        return
        
    # Stop the routine
    def stopAsyncBPM(self):
        self.thread.stopped = True
        self.BPM = 0
        return

    #code used from pulsesensor.com AND https://tutorials-raspberrypi.com/raspberry-pi-heartbeat-pulse-measuring/

def speaker():
    os.system('speaker-test -c2') #test run of white noise sound
    #set up from adafruit https://learn.adafruit.com/adafruit-i2s-stereo-decoder-uda1334a/raspberry-pi-usage



        

    

