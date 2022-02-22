import cv2
import pickle
import cvzone
import numpy as np

width, height = 107, 48
############              Video Feed     #########################
cap = cv2.VideoCapture("carPark.mp4")
with open("CarParkPos", "rb") as f:
    positionList = pickle.load(f)

def checkParkingSpace(imgProcessed):
    spaceCounter = 0
    for position in positionList:
        x,y = position

        imgCrop = imgProcessed[y:y+height, x: x+width]
        #cv2.imshow(str(x*y), imgCrop)
        count = cv2.countNonZero(imgCrop) #this gives count number of each images
        if count < 900:
            color=(0,255,0)
            thickness =5
            spaceCounter += 1
        else:
            color=(0,0,255)
            thickness = 2
        cv2.rectangle(img, position, (position[0] + width, position[1] + height), color,
                      thickness)
        cvzone.putTextRect(img, str(count), (x, y + height - 3), scale=1, thickness=2, offset=0, colorR=color)

        cvzone.putTextRect(img, f"Empthy: {spaceCounter}/{len(positionList)}", (100, 50), scale=3, thickness=5, offset=20, colorR=(0,200,0))
        #cvzone.putTextRect(img, "Empty Parking Slots", (190, 50), scale=3, thickness=5, offset=20, colorR=(0, 200, 0))


while True:
    #This ocde restart video when it comes to the last frame
    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES,0)
    success, img = cap.read()
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray,(3,3), 1)
    imgThreshold = cv2.adaptiveThreshold(imgBlur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                         cv2.THRESH_BINARY_INV,25,16)
    imgMedian = cv2.medianBlur(imgThreshold,5)
    kernel = np.ones((3,3), np.uint8)
    imgDilated = cv2.dilate(imgMedian,kernel, iterations=1)
    checkParkingSpace(imgDilated)
    #for position in positionList:
        # measure the size of parking slots

    cv2.imshow("Image", img)
    #cv2.imshow("ImgBLur",imgBlur)
    #cv2.imshow("ImgDilated",imgDilated)
    cv2.waitKey(10)