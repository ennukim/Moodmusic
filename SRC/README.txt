# MOODMUSIC

Moodmusic.py is the Python software library for running the sensors of the moodmusic device.
This device will use sensors to record the user's biometrics and surrounding environment into
an algorithm that determines the user's mood. From there the algorithm will select and play a
playlist according to its set mood value. 

The parts the code includes are: Heartbeat Pulse Sensor, MCP3002, ADXL345, DS18B20, UDA1334A, PDV-P8001


## Installation

The Heartbeat Pulse Sensor library and information is included [here](https://github.com/tutRPi/Raspberry-Pi-Heartbeat-Pulse-Sensor).
The Analog to Digital Converter example library can be found [here](https://github.com/tutRPi/Raspberry-Pi-Heartbeat-Pulse-Sensor/blob/master/MCP3008.py) 
pulled from the Heartbeat Pulse Sensor library.

Stereo Decoder (UDA1334A) installation command line. Additonal information on setup and installation can be found [here](https://learn.adafruit.com/adafruit-i2s-stereo-decoder-uda1334a/raspberry-pi-usage)

```bash
curl -sS https://raw.githubusercontent.com/adafruit/Raspberry-Pi-Installer-Scripts/master/i2samp.sh | bash
```
Accelerometer module installation lines. Addtional information on setup and installation can be found [here](https://pimylifeup.com/raspberry-pi-accelerometer-adxl345/)
Following the assumption that all previous I2C modules are already uploaded and tested for accuracy.
---bash
sudo pip3 install adafruit-circuitpython-ADXL34x
---

For the temperature sensor, the following line will have to be contributed to the source file of the Pi in /boot/config.txt
---
dtoverlay=w1-gpio
---
Additonally prior to usage, the software runs command lines to activiate the modules for the sensors. More information [here](https://blog.oddbit.com/post/2018-03-27-multiple-1-wire-buses-on-the-/)


## Special help Usage

```python
    base_dir = '/sys/bus/w1/devices/'
    device_folder = glob.glob(base_dir + '28*')[0]
    device_folder2 = glob.glob(base_dir+'28*')[1]
    device_file = device_folder + '/w1_slave'
    device_file2 = device_folder2 + '/w1_slave'
    value1 = read_temp(device_file)
    value2 = read_temp(device_file2)
    return value1, value2
```
The two device folder variables are defined because of the daisy chained temperature sensors used in the device.
If any additional sensors were to be added on the daisy chain, the code would have to be altered accordingly.


##Authors
Anthony Lam and Sally Kim


#Project Status
Still in production and testing, no algorithm has been devised yet and the sensory code is minimal for testing.
