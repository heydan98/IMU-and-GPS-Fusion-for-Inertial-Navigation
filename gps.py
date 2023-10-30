#!/usr/bin/env python
import serial
import numpy as np
import time
# import wiringpi as wp
import RPi.GPIO as GPIO
import sys
# import mysql.connector

import string

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


while True:
      #port="/dev/ttyAMA0"
  # try:
    #ser=serial.Serial(port, baudrate=9600, timeout=0.5)
  
  try:
    dataout = pynmea2.NMEAStreamReader()
    newdata=ser.readline()
    # print(50*"-")
    # print(newdata)

    # print(newdata[0:6] == "$GPRMC")
    if (newdata[0:6] == b"$GPGGA"):
            newmsg=pynmea2.parse(newdata.decode("utf-8"))
            lat=newmsg.latitude
            lat_deg= lat*np.pi//180
            alt = float(newmsg.altitude)


            lng=newmsg.longitude
            lng_deg=lng*np.pi/180
            write_command = f"update gps set kinhdo={lng}, vido={lat}, docao={alt}, goc=80;"
            print(write_command)
            # mycursor.execute(write_command)
            # mydb.commit()
            utc_time = newmsg.timestamp
            print(utc_time)
    if (newdata[0:6] == b"$GPVTG"):
            # new = str(newdata).split(',')
            # print(new)
            newmsg=pynmea2.parse(newdata.decode("utf-8"))
            speed = newmsg.spd_over_grnd_kmph
            if speed < 1.5 : speed = 0
            speed = speed / 3.6
            write_command = f"update gps set vantoc={speed};"
            print(write_command)
            # mycursor.execute(write_command)
            # mydb.commit()
            # print(speed)
    # if (newdata[0:6] == b"$GPRMC"):
    #         newmsg=pynmea2.parse(newdata.decode("utf-8"))
    #         utc_time = newmsg.timestamp
    #         print(type(utc_time))

  except :
      port="/dev/ttyS0"
      ser=serial.Serial(port, baudrate=9600 ,   parity=serial.PARITY_NONE,

        stopbits=serial.STOPBITS_ONE,

        bytesize=serial.EIGHTBITS,)
      continue
  # except KeyboardInterrupt:
  #   print("stop")
  #   break