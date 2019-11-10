import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import picamera
import time
import cv2
import numpy as np
import serial
import sys

reader = SimpleMFRC522()


try:
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(40, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

        
        def action(pin):
            print('SMOKE DETECTED!!')
            #a=1
            return
        
        GPIO.add_event_detect(40, GPIO.RISING)
        a=GPIO.add_event_callback(40, action)
        
        while True:
                print('Taking Image')
                time.sleep(5)
                camera.capture('/home/pi/img.jpg')
                camera.vflip = True
                camera.brightness = 60
               
                image3 = cv2.imread("/home/pi/default.jpg")
                image4 = cv2.imread("/home/pi/img.jpg")

                difference = cv2.subtract(image3, image4)

                result =  not np.any(difference) #if difference is all zeros it will return False

                if result is True:
                    print ("The images are the same")

                else:
           # cv2.imwrite("/home/pi/result1.jpg", difference)
                    cv2.imwrite("/home/pi/result.jpg", difference)
                    print ("Dirt Detected")
                    
                    SERIAL_PORT = "/dev/serial0"
                    ser = serial.Serial(SERIAL_PORT, baudrate = 9600 , timeout = 5)

                    ser.write(str.encode("AT+CMGF=1\r"))
                    print("Text mode enabled...")
                    time.sleep(3)
                    ser.write(str.encode('AT+CMGS="9834369476"\r'))
                    msg=(str.encode("Calling Worker"))
                    print ("sending message ...")
                    time.sleep(3)
                    ser.write(msg+str.encode(chr(26)))
                    time.sleep(20)
                    print("message sent ...")
                    
                    time.sleep(5)
                    print("looking for cards")
                    print("press ctrl+c to stop")

                    id, text = reader.read()
                    print(id)
                    print(text)
                   
                    #camera = picamera.PiCamera()
                    time.sleep(5)
                    camera.capture('/home/pi/rfidbefore.jpg')
                    camera.vflip = True
                    camera.brightness = 60
                    
                    print("looking for cards")
                    id, text = reader.read()
                    print(id)
                    print(text)
                    
                    time.sleep(5)
                    camera.capture('/home/pi/rfidafter.jpg')
                    camera.vflip = True
                    camera.brightness = 60
                   
                    image1 = cv2.imread("/home/pi/rfidbefore.jpg")
                    image2 = cv2.imread("/home/pi/rfidafter.jpg")

                    difference = cv2.subtract(image1, image2)

                    result =  not np.any(difference) #if difference is all zeros it will return False

                    if result is True:
                        print ("The images are the same")

                    else:
               # cv2.imwrite("/home/pi/result1.jpg", difference)
                        cv2.imwrite("/home/pi/resultrfidd.jpg", difference)
                        print ("Worker completed the work")
                    break
                
        
finally:        
        GPIO.cleanup()


