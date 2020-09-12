import numpy as np
import cv2


def process_click(event, x, y,flags, params):
    # check if the click is within the dimensions of the button
    if event == cv2.EVENT_LBUTTONDOWN:
        if y > button[0] and y < button[1] and x > button[2] and x < button[3]:
        	cv2.destroyAllWindows()
        	exit() 



cv2.namedWindow('Control')
cv2.setMouseCallback('Control',process_click)

cap = cv2.VideoCapture(0)

button = [20,60,50,250]
while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Display the resulting frame
    cv2.imshow('frame',gray)
    cv2.setMouseCallback('Control',process_click)
    control_image = np.zeros((80,300), np.uint8)
    control_image[button[0]:button[1],button[2]:button[3]] = 180
    cv2.putText(control_image, 'Button',(100,50),cv2.FONT_HERSHEY_PLAIN, 2,(0),3)
    cv2.imshow('Control', control_image)
    if cv2.waitKey(1) & 0xFF == ord('q'):
    	break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()