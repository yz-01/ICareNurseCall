import cv2
import Module
from Module.FaceMeshModule import FaceMeshDetector
from Module.PlotModule import LivePlot
from pushbullet import PushBullet
import os

wCam, hCam = 640, 480

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
detector = FaceMeshDetector(maxFaces=1)
plotY = LivePlot(640, 360, [20, 50], invert=True)

idList = [22, 23, 24, 26, 110, 157, 158, 159, 160, 161, 130, 243]
ratioList = []
blinkCounter = 0
counter = 0
color = (255, 0, 255)

API_KEY = "o.TXlHas7WTNYZvTWROrX2s88ZniNI759i"
folderPath2 = "PatientCallingHistory"
fileName = "Patient 1.txt"
file = os.path.join(folderPath2, fileName)

with open(file, mode='r') as f:
    text = f.read()
pb = PushBullet(API_KEY)

while True:
    success, img = cap.read()
    img, faces = detector.findFaceMesh(img, draw=False)

    if faces:
        face = faces[0]
        for id in idList:
            cv2.circle(img, face[id], 5, color, cv2.FILLED)

        leftUp = face[159]
        leftDown = face[23]
        leftLeft = face[130]
        leftRight = face[243]
        lenghtVer, _ = detector.findDistance(leftUp, leftDown)
        lenghtHor, _ = detector.findDistance(leftLeft, leftRight)

        cv2.line(img, leftUp, leftDown, (0, 200, 0), 3)
        cv2.line(img, leftLeft, leftRight, (0, 200, 0), 3)

        ratio = int((lenghtVer / lenghtHor) * 100)
        print(ratio)
        ratioList.append(ratio)
        if len(ratioList) > 3:
            ratioList.pop(0)
        ratioAvg = sum(ratioList) / len(ratioList)

        if ratioAvg < 35:
            counter += 1
            if counter >= 25:
                blinkCounter += 1
                counter = 0
            color = (0, 200, 0)
        else:
            counter = 0
            color = (255, 0, 255)

        if blinkCounter >= 2:
            instruction = "Call Doctor"
            text += instruction
            with open(file, mode='w') as f:
                f.write(text)
            push = pb.push_note('Patient Calling', text)
            break
        else:
            instruction = "No Instruction"

        cv2.putText(img, str(instruction), (45, 375), cv2.FONT_HERSHEY_PLAIN,
                    3, (255, 0, 0), 10)

        imgPlot = plotY.update(ratioAvg, color)
        img = cv2.resize(img, (640, 360))
    else:
        img = cv2.resize(img, (640, 360))

    cv2.imshow("Image", img)
    cv2.waitKey(25)