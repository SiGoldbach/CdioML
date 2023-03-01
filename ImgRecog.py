import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt

##When getting the circles array back the first 2 parameters are x and y coordinates and the third is radius.
sizeX = 180
sizeY = 120

print("hi")

videoCapture = cv.VideoCapture(1, cv.CAP_DSHOW)
prevCircle = None
dist = lambda x1, x2, y1, y2: (x1 - x2) ** 2 + (y1 - y2) ** 2
while True:
    ret, frame = videoCapture.read()
    if not ret:
        break
    grayFrame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    blurrFrame = cv.GaussianBlur(grayFrame, (17, 17), 0)
    ##Defining the reds we are looking for when looking for the wall and distraction
    lower_red = np.array([20, 100, 100], dtype="uint8")

    upper_red = np.array([30, 255, 255], dtype="uint8")
    mask = cv.inRange(frame, lower_red, upper_red)
    detected_output = cv.bitwise_and(frame, frame, mask=mask)

    circles = cv.HoughCircles(blurrFrame, cv.HOUGH_GRADIENT, 1.2, 100, param1=60, param2=20, minRadius=3, maxRadius=10)
    egdes = cv.Canny(grayFrame, 50, 150, apertureSize=3)

    ret, thresh = cv.threshold(grayFrame, 50, 255, 0)

    if circles is not None:
        circles = np.uint16(np.around(circles))
        chosen = None
        for i in circles[0, :]:
            if chosen is None: chosen = i
            if prevCircle is not None:
                if dist(chosen[0], chosen[1], prevCircle[0], prevCircle[1]) <= dist(i[0], i[1], prevCircle[0],
                                                                                    prevCircle[1]):
                    chosen = 1
        cv.circle(frame, (i[0], i[1]), 1, (0, 100, 100), 3)
        cv.circle(frame, (i[0], i[1]), i[2], (255, 0, 255), 3)

    cv.imshow("Shapes", frame)
    cv.imshow("Red", detected_output)
    if cv.waitKey(1) & 0xFF == ord('q'):
        print("Circles at: ")
        print(circles)
        print("Masks: ")
        print(mask)
        print("First element in mask size: ")
        print(detected_output.size)
        red = 0
        for i in mask:
            if i.any != 0:
                red = red + 1
        print("Amount of red in the array: ")
        print(red)
        break

videoCapture.release()
cv.destroyAllWindows()
