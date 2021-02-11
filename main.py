import cv2
import numpy as np
import imutils

cap= cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,480)

while True:
    _,frame = cap.read()
    hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)

    lower_green = np.array([40,70,80])
    upper_green = np.array([70,255,255])

    lower_red = np.array([0,50,120])
    upper_red = np.array([10,255,255])

    lower_blue = np.array([90,60,0])
    upper_blue = np.array([121,255,255])

    mask1 = cv2.inRange(hsv,lower_green,upper_green)
    mask2 = cv2.inRange(hsv,lower_red,upper_red)
    mask3 = cv2.inRange(hsv,lower_blue,upper_blue)
    

    cnts1 = cv2.findContours(mask1,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    cnts1 = imutils.grab_contours(cnts1)

    cnts2 = cv2.findContours(mask2,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    cnts2 = imutils.grab_contours(cnts2)

    cnts3 = cv2.findContours(mask3,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    cnts3 = imutils.grab_contours(cnts3)    
    
    for c in cnts1:
        area1 = cv2.contourArea(c)
        if area1>5000:
            cv2.drawContours(frame,[c],-1,(0,255,0),3)
            M = cv2.moments(c)
            cx = int(M["m10"]/M["m00"])
            cy = int(M["m01"]/M["m00"])
            
            # cv2.circle(frame,(cx,cy),7,(255,255,255),-1)
            cv2.putText(frame,"Green",(cx-20,cy-20),cv2.FONT_HERSHEY_SIMPLEX,2.5,(255,255,255),3)
            # cv2.putText(frame,"Green")

    for c in cnts2:
        area1 = cv2.contourArea(c)
        if area1>5000:
            cv2.drawContours(frame,[c],-1,(0,255,0),3)
            M = cv2.moments(c)
            cx = int(M["m10"]/M["m00"])
            cy = int(M["m01"]/M["m00"])
            
            # cv2.circle(frame,(cx,cy),7,(255,255,255),-1)
            cv2.putText(frame,"Red",(cx-20,cy-20),cv2.FONT_HERSHEY_SIMPLEX,2.5,(255,255,255),3)
            # cv2.putText(frame,"Green")

    for c in cnts3:
        area1 = cv2.contourArea(c)
        if area1>5000:
            cv2.drawContours(frame,[c],-1,(0,255,0),3)
            M = cv2.moments(c)
            cx = int(M["m10"]/M["m00"])
            cy = int(M["m01"]/M["m00"])
            
            # cv2.circle(frame,(cx,cy),7,(255,255,255),-1)
            cv2.putText(frame,"Blue",(cx-20,cy-20),cv2.FONT_HERSHEY_SIMPLEX,2.5,(255,255,255),3)
            # cv2.putText(frame,"Green")
        
    cv2.imshow("result",frame)
    k = cv2.waitKey(5)
    if k == 27:
        break
cap.release()
cv2.destroyAllWindows()


