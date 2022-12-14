# importing libraries
import cv2
import time
import math

# x and y coordinates of basket 
basketx = 530
baskety = 300

# list holding trajectory centre positions
trajx = []
trajy = []

# defining the video
video = cv2.VideoCapture("bb3.mp4")

# Load tracker 
tracker = cv2.TrackerCSRT_create()

# Read the first frame of the video. First frame exists.
returned, img = video.read()

# Select the bounding box on the image. bbox storing x,y,width,height
bbox = cv2.selectROI("Tracking", img, False)

# Initialise the tracker on the img and the bounding box
tracker.init(img, bbox)

print(bbox)

def drawBox(img, bbox):
    x, y, w, h = int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3])

    cv2.rectangle(img,(x,y),((x+w),(y+h)),(255,0,255),3,1)

    cv2.putText(img,"Tracking",(75,90),cv2.FONT_HERSHEY_SIMPLEX,2,(0,255,0),2)

def goal_track(img, bbox):
    x, y,w, h = int(bbox[0]),int(bbox[1]),int(bbox[2]),int(bbox[3])

    # getting x-coordinate of centre of bbox
    cx = x + int(w/2)

    # getting y-coordinate of centre of bbox
    cy = y + int(h/2)
    
    # adding a circle on the points
    cv2.circle(img, (cx, cy), 2, (0, 0, 255), 2)

    # adding a circle to the basket
    cv2.circle(img, (int(basketx), int(baskety)), 2, (255, 0, 0), 2)

    # calculating distance between point and basket
    distance = math.sqrt(((cx-basketx)**2) + ((cy-baskety)**2))

    # if point is close to basket, say "scored"
    if (distance <= 20):
        cv2.putText(img, "POINT SCORED!", (500, 300), cv2.FONT_HERSHEY_COMPLEX, 2, (255, 0, 0), 2)

    # adding new trajectory points to list
    trajx.append(cx)
    trajy.append(cy)

    # drawing points on screen for trajectory
    for i in range(len(trajx) - 1):
        cv2.circle(img, (trajx[i], trajy[i]), 2, (255, 0, 255), 2)


while True:
    
    check, img = video.read()   

    # Update the tracker on the img and the bounding box
    success, bbox = tracker.update(img)

    if success:
        drawBox(img, bbox)
    else:
        cv2.putText(img,"Lost",(75,90),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,0,255),2)

    goal_track(img, bbox)

    cv2.imshow("result", img)
            
    key = cv2.waitKey(25)
    if key == 32:
        print("Stopped")
        break

video.release()
cv2.destroyALLwindows()