import cv2
import time
import os
import Module
from Module import HandTrackingModule as htm
from pushbullet import PushBullet

wCam, hCam = 640, 480

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

folderPath = "FingerImages"
myList = os.listdir(folderPath)
print(myList)
overlayList = []

counter_1 = 0
counter_2 = 0
counter_3 = 0
counter_4 = 0
counter_5 = 0

API_KEY = "o.TXlHas7WTNYZvTWROrX2s88ZniNI759i"
folderPath2 = "PatientCallingHistory"
fileName = "Patient 1.txt"
file = os.path.join(folderPath2, fileName)

with open(file, mode='r') as f:
    text = f.read()
pb = PushBullet(API_KEY)

for imPath in myList:
    image = cv2.imread(f'{folderPath}/{imPath}')
    image = cv2.resize(image, (200, 300))
    # print(f'{folderPath}/{imPath}')
    overlayList.append(image)

print(len(overlayList))
pTime = 0

detector = htm.handDetector(detectionCon=0.75)

tipIds = [4, 8, 12, 16, 20]

while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmlist = detector.findPosition(img, draw=False)
    getHand = detector.findHandsPosition(img)

    if len(lmlist) != 0:
        fingers = []
        # Thumb
        if getHand == ['Right'] or getHand == ['Right', 'Right']:
            if lmlist[tipIds[0]][1] > lmlist[tipIds[0] - 1][1]:
                fingers.append(1)
            else:
                fingers.append(0)

            for id in range(1, 5):
                if lmlist[tipIds[id]][2] < lmlist[tipIds[id] - 2][2]:
                    fingers.append(1)
                else:
                    fingers.append(0)
        else:
            if lmlist[tipIds[0]][1] < lmlist[tipIds[0] - 1][1]:
                fingers.append(1)
            else:
                fingers.append(0)

            for id in range(1, 5):
                if lmlist[tipIds[id]][2] < lmlist[tipIds[id] - 2][2]:
                    fingers.append(1)
                else:
                    fingers.append(0)

        totalFingers = fingers.count(1)

        if totalFingers == 1:
            counter_1 += 1
            instruction = "Call Doctor"
        elif totalFingers == 2:
            counter_2 += 1
            instruction = "Want to go Toilet"
        elif totalFingers == 3:
            counter_3 += 1
            instruction = "Want to Eat"
        elif totalFingers == 4:
            counter_4 += 1
            instruction = "Want to Drink"
        elif totalFingers == 5:
            counter_5 += 1
            instruction = "Need Medicines"
        else:
            instruction = "No Instruction"

        if counter_1 >= 25:
            new_content = "Call Doctor"
            text += new_content
            with open(file, mode='w') as f:
                f.write(text)
            push = pb.push_note('Patient Calling', text)
            break
        elif counter_2 >= 25:
            new_content = "Want to go Toilet"
            text += new_content
            with open(file, mode='w') as f:
                f.write(text)
            push = pb.push_note('Patient Calling', text)
            break
        elif counter_3 >= 25:
            new_content = "Want to Eat"
            text += new_content
            with open(file, mode='w') as f:
                f.write(text)
            push = pb.push_note('Patient Calling', text)
            break
        elif counter_4 >= 25:
            new_content = "Want to Drink"
            text += new_content
            with open(file, mode='w') as f:
                f.write(text)
            push = pb.push_note('Patient Calling', text)
            break
        elif counter_5 >= 25:
            new_content = "Need Medicines"
            text += new_content
            with open(file, mode='w') as f:
                f.write(text)
            push = pb.push_note('Patient Calling', text)
            break

        cv2.putText(img, str(instruction), (45, 375), cv2.FONT_HERSHEY_PLAIN,
                    3, (255, 0, 0), 10)

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.putText(img, f'FPS: {int(fps)}', (400, 70), cv2.FONT_HERSHEY_PLAIN,
                3, (255, 0, 0), 3)

    if success:
        cv2.imshow('Camera', img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
