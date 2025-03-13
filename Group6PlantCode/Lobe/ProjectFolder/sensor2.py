import RPi.GPIO as gpio
import time

def distance2(measure='cm'):
    gpio.setwarnings(False)
    #print('begin')
    try:
       # print('before setup')
        gpio.setmode(gpio.BOARD)
        gpio.setup(31, gpio.OUT)
        gpio.setup(33, gpio.IN)
       # print('after setup')

        gpio.output(31, False)

        while gpio.input(33) == 0:
            nosig  = time.time()
           # print('inside 0 while')
        while gpio.input(33) == 1:
            sig  = time.time()
           # print('inside 1 while')

        tl = sig - nosig

        if measure == 'cm':
            distance2  = tl / 0.000058
        elif measure == 'in':
            distance2 = tl / 0.000148
        else:
            print('improper choice of measurement: in or cm')
            distance2 = None

        gpio.cleanup()
        return distance2

    except:
        distance2 = 100
        gpio.cleanup()
        return distance2

#print(distance2('cm'))
