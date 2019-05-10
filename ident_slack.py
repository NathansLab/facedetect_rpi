from PIL import Image
import glob
import os
import face_recognition
from multiprocessing import Process
import json
import numpy as np
import requests
import time

#other requirements: mpg123

#import picamera    #on raspi
import cv2          #on other devices

imagedir = "/home/nathan/Bilder/faces/some/*.jpg"
slackurl = "https://hooks.slack.com/services/****/**/***"

def detect(frame, images, encodings, names):
    face_locations = face_recognition.face_locations(frame)
    faces = len(face_locations)
    if faces != 0:
        print("Detected " + str(faces) + " face(s) on camera.")
        face_on_frame = face_recognition.face_encodings(frame, face_locations)
        for i in range(0, len(encodings)):
            if face_recognition.compare_faces([encodings[i][0]], face_on_frame[0]) == [True]:
                message = "Hallo " + str(names[i])
                payload = { "text" : message }
                requests.post(slackurl, data=json.dumps(payload))
                os.system("gtts-cli \"Hallo " + str(names[i]) + ".\" -l de | mpg123 -q -")
    else:
        print("No Face found")

if __name__ == '__main__':
    video_capture = cv2.VideoCapture(0)

    images = []
    encodings = []
    names = []

    for filename in glob.glob(imagedir):
        images.append(filename)

    print("Found " + str(len(images)) + " images.")

    for x in range(0, int(len(images))):
        print("Working on " + images[x])
        pic = face_recognition.load_image_file(images[x])
        encodings.append(face_recognition.face_encodings(pic))
        if len(encodings[x]) == 0:
            print("[ERROR]  No face detected.")
            os.remove(images[x])
        if len(encodings[x]) > 1:
            print("[ERROR]  More than one face on image.")
            os.remove(images[x])

    print("Classification done!")

    for x in range(0, len(images)):
        dir = images[x].split("/")
        pos = int(len(dir)) - 1
        names.append(dir[pos])
        names[x] = names[x].split(".")[0]

    print("These names are registered" + str(names))

    #camera = picamera.PiCamera()                       #on raspi
    #camera.resolution = (320, 240)                     #on raspi
    #frame = np.empty((240, 320, 3), dtype=np.uint8)    #on raspi
    while True:
        ret, frame = video_capture.read()               #on other devices
        frame = frame[:, :, ::-1]                       #on other devices
        #camera.capture(frame, format="rgb")            #on raspi
        p = Process(target=detect, args=(frame, images, encodings, names,))
        p.start()
        time.sleep(2)
    video_capture.release()
