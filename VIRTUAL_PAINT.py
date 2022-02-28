import cv2
import numpy as np
cap=cv2.VideoCapture(0)
cap.set(3,640)#id=3 for width
cap.set(4,480)#id=4 for height
cap.set(10,150)#id=10 for brightness

myColors = [[90, 111, 21, 120, 211, 255],
            [133,56,0,156,156,255],
            [57,76,0,100,255,255]]
myColorsval=[[51,153,255],
             [255,0,255],
             [0,255,0]]

mypoints=[]##[x,y,color]

def drawonCANWAS(mypoints):
    for point in mypoints:
        cv2.circle(imgResult, (point[0],point[1]), 10, (255, 0, 0), cv2.FILLED)


def findcolor(img,myColors):
    imgHSv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    newpoint=[]
    lower = np.array(myColors[0][0:3])
    upper = np.array(myColors[0][3:6])
    mask = cv2.inRange(imgHSv, lower, upper)
    x,y=getContours(mask)
    cv2.circle(imgResult,(x,y),10,(255,0,0),cv2.FILLED)
    if x!=0 and y!=0:
        newpoint.append([x,y])
    cv2.imshow("img",mask)
    return newpoint


def getContours(img):
    contors,hierachy=cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    x, y, width, height=0,0,0,0
    for cnt in contors:
        area=cv2.contourArea(cnt)

        if area>500:
            cv2.drawContours(imgResult, cnt, -1, (255, 0, 0), 3)
            peri=cv2.arcLength(cnt,True)
            approx=cv2.approxPolyDP(cnt,0.02*peri,True)
            x, y, width, height=cv2.boundingRect(approx)
    return x+width//2,y
while True:
    sucsess,img=cap.read()
    imgResult=img.copy()
    newpoint=findcolor(img,myColors)
    if len(newpoint)!=0:
        for newp in newpoint:
            mypoints.append(newp)
    if len(mypoints)!=0:
        drawonCANWAS(mypoints)

    cv2.imshow("Video",imgResult)
    if cv2.waitKey(1)&0xff==ord("q"):
        break