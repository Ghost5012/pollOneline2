import os
from django.shortcuts import render, redirect
import cv2
import numpy as np
import logging
from sklearn.model_selection import train_test_split
from . import dataset_fetch as df
from . import cascade as casc
from PIL import Image
from poll.views import *
from poll.models import *
from path import path
from time import time
from sklearn.decomposition import PCA
from sklearn.model_selection import GridSearchCV
from sklearn.svm import SVC
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
import pickle
import time as t
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def trainer(request,id):
    import os
    from PIL import Image
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    #Path of the samples
    path = BASE_DIR+'/ml/dataset/'
    if not os.path.exists(BASE_DIR+'/ml/recognizer'):
        os.makedirs(BASE_DIR+'/ml/recognizer')

    def getImagesWithID(path):
        imagePaths = [os.path.join(path,f) for f in os.listdir(path)]
        faces = []
        Ids = []
        for imagePath in imagePaths:
            faceImg = Image.open(imagePath).convert('L') 
            faceNp = np.array(faceImg, 'uint8')
            ID = int(os.path.split(imagePath)[-1].split('.')[1])
            faces.append(faceNp)
            Ids.append(ID)
            cv2.imshow("training", faceNp)
            cv2.waitKey(10)
        return np.array(Ids),faces
    ids, faces = getImagesWithID(path)
    recognizer.train(faces, ids)
    recognizer.save(BASE_DIR+'/ml/recognizer/trainingData.yml')
    cv2.destroyAllWindows()

def create_dataset(request):
    userId = request.POST['userId']
    if not os.path.exists((BASE_DIR+'/ml/dataset/')):
        os.makedirs((BASE_DIR+'/ml/dataset/'))
        os.makedirs((BASE_DIR+'/ml/dataset1/'))
    faceDetect = cv2.CascadeClassifier(BASE_DIR+'/ml/haarcascade_frontalface_default.xml')
    cam = cv2.VideoCapture(0)
    id = userId
    sampleNum = 0
    while(True):
        ret, img = cam.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = faceDetect.detectMultiScale(gray, 1.3, 5)
        for(x,y,w,h) in faces:
            sampleNum = sampleNum+1
            cv2.imwrite(BASE_DIR+'/ml/dataset/User.'+str(id)+'.'+str(sampleNum)+'.jpg', gray[y:y+h,x:x+w])
            cv2.rectangle(img,(x,y),(x+w,y+h), (0,255,0), 2)
            cv2.waitKey(100)
        cv2.imshow("Face",img)
        cv2.waitKey(1)
        if(sampleNum>15 or cv2.waitKey(1) == ord('q')):
            break
    cam.release()
    cv2.destroyAllWindows()
    #############################################
    trainer(request,id)
    image=BASE_DIR+'/ml/dataset/'+str(id)+'.'+str(1)+'.jpg'
    request.session['userId']=userId
    return redirect(reverse('poll:ap'))

def detect(request,id):
    frame=BASE_DIR+'/ml/recognizer/trainingData.yml'
    faceDetect = cv2.CascadeClassifier(BASE_DIR+'/ml/haarcascade_frontalface_default.xml')
    cam = cv2.VideoCapture(0)
    rec = cv2.face.LBPHFaceRecognizer_create()
    rec.read(frame)
    font = cv2.FONT_HERSHEY_SIMPLEX
    userId = 0
    while(True):
        ret, img = cam.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = faceDetect.detectMultiScale(gray, 1.3, 5)
        for(x,y,w,h) in faces:
            cv2.rectangle(img,(x,y),(x+w,y+h), (0,255,0), 3)
            getId,conf = rec.predict(gray[y:y+h, x:x+w])
            el=User.objects.get(username=getId)
            if conf<5:
                userId = getId
                cv2.putText(img, "Voter "+str(userId),(x+2,y+h-5), font, 1, (150,255,0),2)
            else:
                cv2.putText(img, "",(x+2,y+h-5), font, 1, (0,0,255),2)

        cv2.imshow("Face",img)
        c=cv2.waitKey(30) & 0xff
        if c==27:
            break
        elif(userId != 0):
            cv2.waitKey(1000)
            cam.release()
            cv2.destroyAllWindows()
            return True #redirect('/records/details/'+str(userId))
    #t.sleep(10)
    cam.release()
    cv2.destroyAllWindows()
    return False
