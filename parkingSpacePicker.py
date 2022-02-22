import cv2
import pickle

width, height = 107, 48
try:
    with open("CarParkPos", "rb") as f:
        positionList =pickle.load(f)
except:

    positionList = list()

def mouseClick(events, x,y,flags,params):

    if events == cv2.EVENT_LBUTTONDOWN:
        positionList.append((x,y))
    if events == cv2.EVENT_RBUTTONDOWN:
        for i, pos in enumerate(positionList):
            x1,y1 = pos
            if x1 < x <x1+width and y1 <y<y1+height:
                positionList.pop(i)

    with open("CarParkPos","wb") as f:
        pickle.dump(positionList,f)

while True:
    img = cv2.imread("carParkImg.png")
    for position in positionList:
        cv2.rectangle(img,position, (position[0]+width, position[1]+height), (255, 0, 255), 2)  # measure the size of parking slots
    cv2.imshow("Image", img)
    cv2.setMouseCallback("Image",mouseClick)

    cv2.waitKey(1)
