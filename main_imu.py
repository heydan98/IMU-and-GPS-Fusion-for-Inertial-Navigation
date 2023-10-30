######################################################
# Copyright (c) 2020 Maker Portal LLC
# Author: Joshua Hrisko
######################################################
#
# This code reads data from the MPU9250/MPU9265 board
# (MPU6050 - accel/gyro, AK8963 - mag) to verify its
# correct wiring to a Raspberry Pi and the functionality
# of the MPU9250_i2c.py library
#
#
######################################################
#
# import numpy as np
from Madgwick import *
import sysv_ipc
import pynmea2
import RPi.GPIO as GPIO
import serial




period = 1/100 #100Hz
import time
t0 = time.time()
start_bool = False # boolean for connection
while (time.time()-t0)<5: # wait for 5-sec to connect to IMU
    try:
        from mpu9250_i2c import *
        start_bool = True # True for forthcoming loop
        break 
    except:
        continue
#
#############################
# Strings for Units/Labs
#############################
#
imu_devs   = ["ACCELEROMETER","GYROSCOPE","MAGNETOMETER"]
imu_labels = ["x-dir","y-dir","z-dir"]
imu_units  = ["g","g","g","dps","dps","dps","uT","uT","uT"]
#
#############################
# Main Loop to Test IMU
#############################
#


# calib_factors =[ [ 1.00389342, -0.01671072],
# 	             [ 1.00844073, -0.0308995],
# 	             [0.6732579,  0.35341465],
# 	            [1, -0.9363937377929688],
# 	            [1, 0.9118270874023438],
# 	            [1, 0.6007766723632812],
# 	            [1, 1.8310546875],
# 	            [1, -10.546875],
# 	            [1, -20.5078125]]


calib_factors =[ [ 1.00257505, -0.01390942],
                  [-1.0004152,   0.03366062],
                  [-0.98767045, -0.03147396],
                  [1, -0.9867095947265625,],
                  [1, 0.9067535400390625],
                  [1, 1.1198806762695312],
                  [1, 2.490234375],
                  [1, -6.5185546875],
                  [1, -21.0205078125]]

import pynmea2
# import mariadb

# # mydb = mysql.connector.connect(
# mydb = mariadb.connect(
#   host="localhost",
#   user="admin_rasp2",
#   password="1",
#   database="admin"
# )

# mycursor = mydb.cursor()


pps=18

port="/dev/ttyS0"
ser=serial.Serial(port, baudrate=9600 ,   parity=serial.PARITY_NONE,

  stopbits=serial.STOPBITS_ONE,

  bytesize=serial.EIGHTBITS,)

ser.write(b"$PUBX,40,GLL,0,0,0,0*5D\r\n")

def PPS_interrupt(channel):
  print("PPS...")


GPIO.setmode(GPIO.BCM)
GPIO.setup(pps, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(pps, GPIO.FALLING, 
        callback=PPS_interrupt, bouncetime=100)



def calibrated_value(input, m ,b):
    return input*m - b
    
calibrated_data = [0,0,0,0,0,0,0,0,0]

tic=time.time()
toc = time.time()
elapse_time = toc-tic
count = 0
check_new_bool = 0
lat = 0 
lng = 0
memory = sysv_ipc.SharedMemory(112, flags = 512, size = 25*12, mode = 0o644)
memory_check_new_gps = sysv_ipc.SharedMemory(113, flags = 512, size = 4, mode = 0o666)

while True:
    if start_bool==False: # make sure the IMU was started
        print("IMU not Started, Check Wiring") # check wiring if error
        break
    ##################################
    # Reading and Printing IMU values
    ##################################
    #
    if elapse_time >= period:
        tic = time.time()
        # print(50*"-")
        # print("elapse time ",elapse_time)
        count += 1
        try:
            ax,ay,az,wx,wy,wz = mpu6050_conv() # read and convert mpu6050 data
            mx,my,mz = AK8963_conv() # read and convert AK8963 magnetometer data
        except:
            continue 
        #
        ##################################
        # Reading and Printing IMU values
        ##################################
        #
        # print(str_calibrated_data)
          
        # print ("elapse time: ", elapse_time)

        # time.sleep(1) # wait between prints
        if count >= 100:
            try:
                
                # count = 0   
                dataout = pynmea2.NMEAStreamReader()
                newdata=ser.readline()
                # print(50*"-")
                # print(newdata)

                # print(newdata[0:6] == "$GPRMC")
                if (newdata[0:6] == b"$GPGGA"):
                    newmsg=pynmea2.parse(newdata.decode("utf-8"))
                    lat=newmsg.latitude
                    # lat_deg= lat*np.pi//180
                    # alt = float(newmsg.altitude)


                    lng=newmsg.longitude
                    # lng_deg=lng*np.pi/180
                    write_command = f"update gps set kinhdo={lng}, vido={lat};"
                    # print(write_command)
                    # print("count", count )
                    count = 0
                    check_new_bool = 1
                    # mycursor.execute(write_command)
                    # mydb.commit()
                    # utc_time = newmsg.timestamp
                    # print(utc_time)
                # if (newdata[0:6] == b"$GPVTG"):
                #     # new = str(newdata).split(',')
                #     # print(new)
                #     newmsg=pynmea2.parse(newdata.decode("utf-8"))
                #     speed = newmsg.spd_over_grnd_kmph
                #     if speed < 1.5 : speed = 0
                #     speed = speed / 3.6
                #     write_command = f"update gps set vantoc={speed};"
                #     print(write_command)
                    # mycursor.execute(write_command)
                    # mydb.commit()
                    # print(speed)
                # if (newdata[0:6] == b"$GPRMC"):
                #         newmsg=pynmea2.parse(newdata.decode("utf-8"))
                #         utc_time = newmsg.timestamp
                #         print(type(utc_time))

            except :
                # count = 0

                port="/dev/ttyS0"
                ser=serial.Serial(port, baudrate=9600 ,   parity=serial.PARITY_NONE,

                stopbits=serial.STOPBITS_ONE,

                bytesize=serial.EIGHTBITS,)
                continue


        # print(calibrated_data )
        # print(50*"-")
        # print(sensor_data)
        # q = MadgwickAHRSupdate(calibrated_data[3]*np.pi/180,calibrated_data[4]*np.pi/180,calibrated_data[5]*np.pi/180,calibrated_data[0],calibrated_data[1],calibrated_data[2],calibrated_data[6]*0.01, calibrated_data[7]*0.01, calibrated_data[8]*0.01)
        # X = quaternion_to_euler(q[0],q[1],q[2],q[3])
        # # print("Q:",q[0],q[1],q[2],q[3])
        # # if  count >= 256:
        # #     count = 0
        # print("X,Y,Z:",X[0]*180/np.pi,X[1]*180/np.pi,X[2]*180/np.pi)
        sensor_data = [ax,ay,az,wx,wy,wz,mx,my,mz]
        for i in range(len(sensor_data)):
            calibrated_data[i] = calibrated_value(sensor_data[i], *calib_factors[i] )
        sensor_data_with_gps = calibrated_data + [lat, lng]

        str_calibrated_data = ' '.join(str(e) for e in sensor_data_with_gps)+'\0'

        byte_data = bytes(str_calibrated_data, "ascii")
        # print(byte_data)
        
        memory_value = memory.write(byte_data)

        # print(count)
        if (count == 0):
            byte_gps = bytes('1\0', "ascii")
            memrory_gps = memory_check_new_gps.write(byte_gps)        
            print(str_calibrated_data)


        # calibrated_data.append(check_new_bool)

        

    else:
        toc = time.time()
        elapse_time = toc-tic
    
