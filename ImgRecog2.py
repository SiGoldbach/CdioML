import cv2 as cv

videoCapture = cv.VideoCapture(1, cv.CAP_DSHOW)
while 1:
    ret, image = videoCapture.read()
    if not ret:
        break

    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

    edges = cv.Canny(gray, 30, 200)

    contours, hierarchy = cv.findContours(edges, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)

    cv.drawContours(image, contours, -1, (0, 255, 0), 3)

    cv.imshow('External Contours', image)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

videoCapture.release()
cv.destroyAllWindows()
