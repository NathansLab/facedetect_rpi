from PIL import Image
import glob
import os
import face_recognition
from multiprocessing import Process
import time

imagedir = "/home/nathan/Bilder/faces/me/*.jpg"        #Path to your dataset of compare images
main_image = "/home/nathan/Bilder/faces/main.jpg"       #The image you want to find the most similar to

def compare(image, main_encoding):
    print("Working on " + image)
    pic = face_recognition.load_image_file(image)
    encoding = (face_recognition.face_encodings(pic))
    if len(encoding) == 0:
        print("[ERROR]  No face detected, deleting.")
        os.remove(image)
    elif len(encoding) > 1:
        print("[ERROR]  More than one face on image, deleting.")
        os.remove(image)
    else:
        dist = face_recognition.face_distance([encoding[0]], main_encoding[0])
        print("Distance: " + str(dist[0]))
        with open("dist.csv", "a") as file:
            file.write(str(int(dist[0] * 100000)) + ";" + image + "\n")

if __name__ == '__main__':
    images = []

    if os.path.isfile("dist.csv"):
        os.remove("dist.csv")

    print("Calculating main encoding.")
    pic = face_recognition.load_image_file(main_image)
    main_encoding = face_recognition.face_encodings(pic)

    if len(main_encoding) == 0:
        print("[ERROR]  No face detected on main images.")
        exit()
    if len(main_encoding) > 1:
        print("[ERROR]  More than one face on main image.")
        exit()

    for filename in glob.glob(imagedir):
        images.append(filename)

    print("Found " + str(len(images)) + " compare images.")

    for x in range(0 , len(images)):
        p = Process(target=compare, args=(images[x], main_encoding))
        p.start()
        time.sleep(0.15)

print("Classification done!")
