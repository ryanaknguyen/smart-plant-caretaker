import RPi.GPIO as gpio
import time

def distance1(measure='cm'):
    #print('entry')
    try:
        gpio.setmode(gpio.BCM)
        gpio.setup(18, gpio.OUT)
        gpio.setup(23, gpio.IN)
        #print('after setup')
        gpio.output(18, False)
        #print('after output false')
        while gpio.input(23) == 0:
            nosig  = time.time()
            #print('0 while loop')

        while gpio.input(23) == 1:
            sig  = time.time()
            #print('1 wjhile loop')
       # print('after while')
        tl = sig - nosig

        if measure == 'cm':
            distance1  = tl / 0.000058
        elif measure == 'in':
            distance1 = tl / 0.000148
        else:
            print('improper choice of measurement: in or cm')
            distance1 = None
       # print('right before cleanup')
        gpio.cleanup()
        return distance1

    except:
        distance1 = 100
        gpio.cleanup()
        return distance1

#print(distance1('cm'))
#print('tester')
