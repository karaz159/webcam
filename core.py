#!/usr/bin/env python3
#Использует OpenCV для инициализации и работы с камерой
#Краткое описание: Создание снимка/видео с вебкамеры во время дейтсвия датчика света
#----------------------------------------------------------------------------------
import cv2 
import RPi.GPIO as GPIO
from time import sleep, asctime
from datetime import datetime
import os
#----------------------------------------------------------------------------------
#Настройка портов GPIO и задание констант
GPIO.setmode(GPIO.BCM)
GPIO.setup(25, GPIO.IN)
WHITE = (255,255,255)
os.system('echo 0 | sudo tee /sys/class/leds/led1/brightness') #выключаю светодиоды малинки
os.system('echo 0 | sudo tee /sys/class/leds/led0/brightness')
T = str(datetime.now())
NAME = '/home/pi/GoogleDrive/shit/python3/CAM/Video '+T+'.avi' # Путь для файлов
#----------------------------------------------------------------------------------
#def alarm():
	#ДОБАВИТЬ!кинуть в лог о включении света и указать имя файла
	#Было бы не плохо создать в кроне задачу на проверку лог файла или сделать это методом питона
	#которая будет оповещать каждое утро в 11 о новых событиях
	#return 1

def take_a_pic():
    cap = cv2.VideoCapture(-1) #задаю камеру
    fourcc = cv2.VideoWriter_fourcc(*'XVID') #формат
    out = cv2.VideoWriter(NAME,fourcc, 15.0, (640,480)) #Задание пути, формата, кадров и разрешения
    while(cap.isOpened()):
        a = asctime() # спрашиваю время
        sun2 = GPIO.input(25)# Еще раз задаю датчик света
        ret, frame = cap.read()
        if ret==True:
            cv2.putText(frame, a, (20,20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, WHITE,2) # вставляю время на кадр 
            out.write(frame)
            if sun2 == 0:# если датчик вернул ноль, то отпустить кадр
                cap.release()
                out.release()
                break
        else:
            break
def main():
    while True:
        now_time = datetime.now()
        cur_hour = now_time.hour
        sun = GPIO.input(25) # датчик света
        if cur_hour == 8:# если сейчас 8 часов утра, то прервать цикл
            print('its time to stop!')
            break
        elif sun == 1:# если датчик света возвращает единицу, то включается камера
            print('got sun!')
            take_a_pic()
        elif sun == 0:
            print('no sun!')
            print(sun)
        else: # если датчик дает что то кроме нуля и единицы, то прервать цикл(такого не может быть, но все же)
            break
        sleep(5)# ждать пять секунд и повторить цикл
#---------------------------------------------------------------------------------
main() #Запуск
