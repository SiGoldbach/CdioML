import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt

import robotInfo

##When getting the circles array back the first 2 parameters are x and y coordinates and the third is radius.
sizeX=180
sizeY=120

print("hi")

videoCapture=cv.VideoCapture(1)
prevCircle=None
dist =lambda x1,x2,y1,y2: (x1-x2)**2+(y1-y2)**2
while True:
    ret,frame=videoCapture.read()
    if not ret:
        break
    grayFrame=cv.cvtColor(frame,cv.COLOR_BGR2GRAY)
    blurrFrame=cv.GaussianBlur(grayFrame,(17,17),0)

    circles=cv.HoughCircles(blurrFrame,cv.HOUGH_GRADIENT,1.2,100,param1=60,param2=20,minRadius=3,maxRadius=10)
    egdes=cv.Canny(grayFrame,50,150,apertureSize=3)

    ret,thresh = cv.threshold(grayFrame,50,255,0)
    contours, _ = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    xMAX=0
    yMAX=0
    for cnt in contours:
        x1,y1 = cnt[0][0]
        if(x1<xMAX):
            if(y1<yMAX):
                continue
        xMAX=x1
        yMAX=y1
        approx = cv.approxPolyDP(cnt, 0.01*cv.arcLength(cnt, True), True)
        if len(approx) == 4:
            x, y, w, h = cv.boundingRect(cnt)
            ratio = float(w)/h
            if ratio >= 0.9 and ratio <= 1.1:
                frame = cv.drawContours(frame, [cnt], -1, (0,255,255), 3)
                cv.putText(frame, 'Square', (x1, y1), cv.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)
            else:
                cv.putText(frame, 'Rectangle', (x1, y1), cv.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
                frame = cv.drawContours(frame, [cnt], -1, (0,255,0), 3)

    if circles is not None:
        circles=np.uint16(np.around(circles))
        chosen=None
        for i in circles[0,:]:
            if chosen is None: chosen=i
            if prevCircle is not None:
                if dist(chosen[0],chosen[1],prevCircle[0],prevCircle[1])<= dist(i[0],i[1],prevCircle[0],prevCircle[1]):
                    chosen=1
        cv.circle(frame,(i[0],i[1]),1,(0,100,100),3)
        cv.circle(frame,(i[0],i[1]),i[2],(255,0,255),3)

    cv.imshow("Shapes", frame)
    if cv.waitKey(1)& 0xFF ==ord('q'):
        break

print("Circles at: ")
print(circles)
videoCapture.release()
cv.destroyAllWindows()