import cv2
import numpy as np

def empty(x):
    pass

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)
cap.set(10, 150)


myColors = [[69, 111, 36, 133, 241, 241]]
myColorValue = [[205, 0, 0]]
myPoints = [] #x, y, colorID

def findColor(img, myColors, myColorValue):
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    count = 0
    newPoints = []
    for color in myColors:
        lower = np.array(color[0:3])
        upper = np.array(color[3:6])
        mask = cv2.inRange(imgHSV, lower, upper)

        x, y = getContours(mask)
        cv2.circle(imgResult, (x, y), 10, myColorValue[count], cv2.FILLED)
        if x!=0 and y!=0:
            newPoints.append([x, y, count])

        count += 1

    return newPoints



def getContours(img):
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    x,y,w,h = 0,0,0,0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 400:
            cv2.drawContours(imgResult, cnt, -1, (255, 0, 0), 3)
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
            x,y,w,h = cv2.boundingRect(approx)

    return x+w//2, y


def drawOnCanvas(myPoints, myColorValues):
    for point in myPoints:
        cv2.circle(imgResult, (point[0], point[1]), 10, myColorValues[point[2]], cv2.FILLED)


while True:
    success, img = cap.read()
    imgResult = img.copy()
    newPoints = findColor(img, myColors, myColorValue)
    if len(newPoints) != 0:
        for newP in newPoints:
            myPoints.append(newP)
    if len(myPoints) != 0:
        drawOnCanvas(myPoints, myColorValue)

    cv2.imshow('result', imgResult)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    cv2.waitKey(1)



cap.release()
cv2.destroyAllWindows()





