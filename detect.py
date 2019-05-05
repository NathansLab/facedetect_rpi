from multiprocessing import Process
import face_recognition
import picamera
import numpy as np

def detect(output):
    face_locations = face_recognition.face_locations(output)
    print("Found {} faces in image.".format(len(face_locations)))

if __name__ == '__main__':
    camera = picamera.PiCamera()
    camera.resolution = (320, 240)
    output = np.empty((240, 320, 3), dtype=np.uint8)
    While True:
        print("Capturing image.")
        camera.capture(output, format="rgb")
        p = Process(target=detect, args=(output,))
        p.start()
        p.join()
