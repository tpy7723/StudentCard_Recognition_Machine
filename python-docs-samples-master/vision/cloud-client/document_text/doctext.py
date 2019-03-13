#!/usr/bin/env python
import argparse
from enum import Enum
import io
import json
from google.cloud import vision
from google.cloud.vision import types
from PIL import Image, ImageDraw
import cv2
import requests
from RPi import GPIO
import time
import os

GPIO.setmode(GPIO.BCM)

#GPIO.cleanup()


GPIO.setup(19,GPIO.OUT)  # red
GPIO.setup(18,GPIO.OUT)  # green 
GPIO.setup(17,GPIO.OUT)  # switch
GPIO.setup(16,GPIO.OUT)  # yellow



cap = cv2.VideoCapture(0)
flag = "false"

while cap.isOpened():
	ret, frame = cap.read()
	cv2.imshow('img', frame)

        GPIO.output(16,False)
        GPIO.output(18,False)
        GPIO.output(19,False)
	ID = ""
	paid=3
	answer=""
	json_data =""

	if GPIO.input(17)==0:
		print "Take Picture~!"
		cv2.imwrite('ID.jpg',frame)

		"""Returns document bounds given an image."""
		client = vision.ImageAnnotatorClient()

		with io.open('ID.jpg', 'rb') as image_file:
		     content = image_file.read()

		image = types.Image(content=content)

		response = client.document_text_detection(image=image)
		data = response

		for key in data.text_annotations:
		   if(len(key.description)== 8):
		     if(key.description[0]=="1") and (key.description[1]=="2"):
		       	flag = "true"
			ID = key.description
			print("key="+key.description)
		        print(flag) 

		if(flag == "true"):
		#   ID = key.description
		   print(ID)
		   URL = "http://www.inhaicesa.com:1666/users/" + ID + "?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdHVkZW50SWQiOiIxMjE1MTYxNiIsIm5hbWUiOiLsoITsiJjtmIQiLCJwYWlkIjoiMSIsInBob25lIjoiMDEwLTkyNzQtNTg5NyIsImF1dGhMZXZlbCI6NSwiZW1haWxBdXRoIjoxLCJwYXlEYXRlIjpudWxsLCJzY29yZSI6MTAsImlhdCI6MTU0NjI0NzkyOH0.va-yk-cmY-QQYw-W9byq5IOzVCY0GiNv_XZREJG2yTg"
		   try:
		   	answer = requests.get(URL)
		   	json_data = json.loads(answer.text)
		   	paid = json_data['payload']['paid']
		   except:
		        print("Not recognition")
	                GPIO.output(16,True)
        	        GPIO.output(18,False)
	                GPIO.output(19,False)
	                time.sleep(1)
			continue

		   if(paid =="1"):
		      print(ID + ":success")
		      GPIO.output(18,True)
		      GPIO.output(16,False)
		      GPIO.output(19,False)
		      os.system("mpg321 result2.mp3")
		      time.sleep(1)


		   elif(paid =="0"):
		      print(ID + ":fail")
		      GPIO.output(19,True)
		      GPIO.output(16,False)
		      GPIO.output(18,False)
		      os.system("mpg321 result1.mp3")
 		      time.sleep(1)

		else:
		   print("Not recognition")
		   GPIO.output(16,True)
		   GPIO.output(18,False)
	  	   GPIO.output(19,False)
		   time.sleep(1)



        if cv2.waitKey(1) & 0xFF == ord('q'):
		GPIO.output(16,False)
		GPIO.output(18,False)
		GPIO.output(19,False)
		GPIO.cleanup()
                break


cv2.destroyAllWindows()
cap.release()


