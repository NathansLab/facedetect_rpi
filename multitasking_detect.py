from multiprocessing import Process
import face_recognition
import picamera
import numpy as np
import requests

def detect(output):
    face_locations = face_recognition.face_locations(output)
    faces = len(face_locations)
    if faces != 0:
        facepos = ((320 - face_locations[0][1]) / 320) * 60
        print("Found {} faces in image.".format(faces))
        requests.get("http://localhost:8080/78ba576f1d0e47489a2368cc50678032/update/V6?value=255")
        requests.get("http://localhost:8080/78ba576f1d0e47489a2368cc50678032/update/V5?value=12")
        requests.get("http://localhost:8080/78ba576f1d0e47489a2368cc50678032/update/V7?value=%d" % facepos)
    else:
        print("No Face found")
        requests.get("http://localhost:8080/78ba576f1d0e47489a2368cc50678032/update/V5?value=1")
        requests.get("http://localhost:8080/78ba576f1d0e47489a2368cc50678032/update/V6?value=0")
    load = psutil.getloadavg()[0] * 100
    requests.get("http://localhost:8080/78ba576f1d0e47489a2368cc50678032/update/V10?value=%d" % load)

if __name__ == '__main__':
    camera = picamera.PiCamera()
    camera.resolution = (320, 240)
    output1 = np.empty((240, 320, 3), dtype=np.uint8)
    while True:
        camera.capture(output1, format="rgb")
        p = Process(target=detect, args=(output1,))
        p.start()
