import cv2 as cv


def list_size_print(list_to_print):
    for lists in list_to_print:
        print(len(lists))
    print("hi")


videoCapture = cv.VideoCapture(1, cv.CAP_DSHOW)
list1 = [0]
circle_list = [0]
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
        print(type(contours))
        print("Length of tuple")
        print(len(contours))
        for i in contours:
            ob = i.tolist()
            # print(ob)
            list1.append(ob)
        for i in contours:
            approx = cv.approxPolyDP(i, 0.01 * cv.arcLength(i, True), True)
            area = cv.contourArea(i)
            if ((len(approx) > 8) & (len(approx) < 23) & (area > 30)):
                circle_list.append(i)
        break

videoCapture.release()
cv.destroyAllWindows()

list1.remove(0)
print(len(list1))
for i in list1:
    print(len(i))
print("I found "+str(len(circle_list))+" circles")
