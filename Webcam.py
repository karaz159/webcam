#!/usr/bin/env python3
#Проект по слежки за бухлом!
#Использует OpenCV для инициализации и работы с камерой
#Краткое описание: Создание снимка/видео с вебкамеры во время дейтсвия датчика света
#----------------------------------------------------------------------------------
import cv2
import RPi.GPIO as GPIO
from time import sleep, asctime
from datetime import datetime
import os
#----------------------------------------------------------------------------------
GPIO.setmode(GPIO.BCM)
GPIO.setup(25, GPIO.IN)
WHITE = (255,255,255)
os.system('echo 0 | sudo tee /sys/class/leds/led1/brightness')
os.system('echo 0 | sudo tee /sys/class/leds/led0/brightness')
b = str(datetime.now())
#----------------------------------------------------------------------------------
#def alarm():
	#ДОБАВИТЬ!кинуть в лог о включении света и указать имя файла
	#Было бы не плохо создать в кроне задачу на проверку лог файла или сделать это методом питона
	#которая будет оповещать каждое утро в 11 о новых событиях
	#return 1

def take_a_pic():
    cap = cv2.VideoCapture(-1)
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter('/home/pi/GoogleDrive/shit/python3/CAM/Video '+b+'.avi',fourcc, 15.0, (640,480))
    while(cap.isOpened()):
        a = asctime()
        sun2 = GPIO.input(25)
        ret, frame = cap.read()
        if ret==True:
            cv2.putText(frame, a, (20,20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, WHITE,2)
            out.write(frame)
            if sun2 == 0:
                cap.release()
                out.release()
                break
        else:
            break
def main():
    while True:
        now_time = datetime.now()
        cur_hour = now_time.hour
        sun = GPIO.input(25)
        if cur_hour == 8:
            print('its time to stop!')
            break
        elif sun == 1:
            print('got sun!')
            take_a_pic()
        elif sun == 0:
            print('no sun!')
            print(sun)
        else:
            break
        sleep(5)
#---------------------------------------------------------------------------------
main()
