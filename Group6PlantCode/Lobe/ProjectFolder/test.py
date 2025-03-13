# mmal error:
# ps
# kill -KILL [id]

import RPi.GPIO as gpio
import time
import sys
from sensor1 import distance1
from sensor2 import distance2
import tkinter as tk
import random

#import Pi GPIO library button class
from gpiozero import Button, LED, PWMLED
from picamera import PiCamera
from time import sleep

from lobe import ImageModel

def init():
    #print("start init")
    gpio.setmode(gpio.BCM)
    gpio.setup(4, gpio.OUT)
    gpio.setup(17, gpio.OUT)
    gpio.setup(27, gpio.OUT)
    gpio.setup(22, gpio.OUT)
    #print("end init")

def forward(tf):
    gpio.output(4, False)
    gpio.output(17, True)
    gpio.output(27, True)
    gpio.output(22, False)
    time.sleep(tf)
    gpio.cleanup()

def reverse(tf):
    gpio.output(4, True)
    gpio.output(17, False)
    gpio.output(27, False)
    gpio.output(22, True)
    time.sleep(tf)
    gpio.cleanup()

def turn_right(tf):
    gpio.output(4, True)
    gpio.output(17, False)
    gpio.output(27, True)
    gpio.output(22, True)
    time.sleep(tf)
    gpio.cleanup()

def turn_left(tf):
    gpio.output(4, False)
    gpio.output(17, True)
    gpio.output(27, False)
    gpio.output(22, False)
    time.sleep(tf)
    gpio.cleanup()

def pivot_right(tf):
    gpio.output(4, True)
    gpio.output(17, False)
    gpio.output(27, True)
    gpio.output(22, False)
    time.sleep(tf)
    gpio.cleanup()

def pivot_left(tf):
    gpio.output(4, False)
    gpio.output(17, True)
    gpio.output(27, False)
    gpio.output(22, True)
    time.sleep(tf)
    gpio.cleanup()

def pause(tf):
    gpio.output(4, False)
    gpio.output(17, False)
    gpio.output(27, False)
    gpio.output(22, False)
    time.sleep(tf)
    gpio.cleanup()

def check_front():
    init()
    print('before distance calc')
    dist1 = distance1()
    print('1st dist cacl')
    dist2 = distance2()
    print('2nd dist calc')

    dist = dist1 if dist1 < dist2 else dist2

    if dist < 35:
        print('Too close,', dist)

        if(True):#button.is_pressed:
            take_photo()
            # Run photo through Lobe TF model
            result = model.predict_from_file('/home/plant/Lobe/ProjectFolder/image.jpg')
            # --> Change image path
            led_select(result.prediction)
            print('finished takinga pciture')
    
        init()
        print('after first init')
        pause(1)
        init()
        print('2nd init done')
        reverse(0.5)
        init()
        pivot_left(0.5)
        print('AAFTER REVERSE')
        dist1 = distance1()
        dist2 = distance2()
        dist = dist1 if dist1 < dist2 else dist2
        print('right before 2nd if statemtn')
        if dist < 25:
            print('Too close,', dist)
            init()
            pause(1)
            init()
            reverse(0.5)
            init()
            pivot_left(0.5)
            dist1 = distance1()
            dist2 = distance2()
            dist = dist1 if dist1 < dist2 else dist2
            if dist < 25:
                print('Too close,', dist)
                init()
                pause(1)
                init()
                pivot_left(0.5)
                init()
                reverse(0.5)
                dist1 = distance1()
                dist2 = distance2()
                dist = dist1 if dist1 < dist2 else dist2
                if dist < 25:
                    print('Too close, giving up', distance)
                    sys.exit()
    print('finishc heck front')

def autonomy():
    tf = 0.030
    x = random.randrange(0, 6)
    #print('before if')
    if x == 0:
        for y in range(30):
            check_front()
            init()
            forward(tf)
    elif x == 1:
        for y in range(30):
            check_front()
            init()
            pivot_left(tf)
    elif x == 2:
        for y in range(30):
            check_front()
            init()
            pivot_right(tf)
    elif x == 3:
        for y in range(30):
            check_front()
            init()
            turn_left(tf)
    elif x == 4:
        for y in range(30):
            check_front()
            init()
            turn_right(tf)
    elif x == 5:
        for y in range(30):
            check_front()
            init()
            forward(tf)
    #print('end of aut')

#Create input, output, and camera objects
#button = Button(2)

#yellow_led = LED(24) #garbage 9th
#blue_led = LED(25) #recycle 11th
#green_led = LED(22) #compost
#red_led = LED(23) #hazardous waste facility
#white_led = PWMLED(24) #Status light and retake photo

camera = PiCamera()

# Load Lobe TF model
# --> Change model file path as needed
model = ImageModel.load('/home/plant/Lobe/modelA')

# Take Photo
def take_photo():
    # Quickly blink status light
     #white_led.blink(0.1,0.1)
    sleep(2)
    print("Pressed")
     #white_led.on()
    # Start the camera preview
    camera.start_preview(alpha=200)
    # wait 2s or more for light adjustment
    sleep(3) 
    # Optional image rotation for camera
    # --> Change or comment out as needed
    camera.rotation = 180
    #Input image file path here
    # --> Change image path as needed
    camera.capture('/home/plant/Lobe/ProjectFolder/image.jpg')
    #Stop camera
    camera.stop_preview()
    #camera.close() # not in original code
     #white_led.off()
    sleep(1)

# Identify prediction and turn on appropriate LED
def led_select(label):
    gpio.setmode(gpio.BCM)
    gpio.setup(24, gpio.OUT)
    gpio.setup(25, gpio.OUT)
    print(label)
    if label == "Plant":
        print('plant detect, before led')
        #yellow_led.on()
        #blue_led.off()
        gpio.output(24, True)
        gpio.output(25, False)
        print('plant detect, after led')
        sleep(1)
    if label == "Not Plant":
        print('plant not, before led')
        #blue_led.on()
        #yellow_led.off()
        gpio.output(24, False)
        gpio.output(25, True)
        sleep(1)
        print('plant not, after led')
    #if label == "compost":
    #    green_led.on()
    #    sleep(5)
    #if label == "hazardous waste facility":
    #    red_led.on()
    #    sleep(5)
    #if label == "not trash!":
    #    white_led.on()
    #    sleep(5)
    else:
        #yellow_led.off()
        #blue_led.off()
        gpio.output(24, False)
        gpio.output(25, False)
        #green_led.off()
        #red_led.off()
        #white_led.off()
import cv2
cap = cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,480)

# Main Function
gpio.setwarnings(False)
while True:
    #success, img = cap.read()
    #cv2.imshow("Output",'/home/plant/Lobe/ProjectFolder/image.jpg')
    #cv2.waitKey(1)

    #while(cap.isOpened()):
     #   ret, frame = cap.read()
     #   if ret == True:

      #      cv2.imshow('Frame',frame)

       # if cv2.waitKey(25) & 0xFF == ord('q'):
        #    break

       # else: 
        #    break
    #if(True):#button.is_pressed:
     #   take_photo()
        # Run photo through Lobe TF model
      #  result = model.predict_from_file('/home/plant/Lobe/ProjectFolder/image.jpg')
        # --> Change image path
       # led_select(result.prediction)
    #else:
        # Pulse status light
    #    white_led.pulse(2,1)
    autonomy()
   # sleep(1)
    print('reached end')

#camera.close()
