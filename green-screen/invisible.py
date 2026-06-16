import cv2
import numpy as np

def apply_invisible_cloak(frame, background):
    # convert to HSV
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # define green color ranges and create masks
    #         H    S    V
    low_g1 = (25, 100, 100)
    up_g1  = (45, 255, 255)
    low_g2 = (45, 100, 100)
    up_g2  = (85, 255, 255)

    mask1 = cv2.inRange(hsv_frame, low_g1, up_g1)
    mask2 = cv2.inRange(hsv_frame, low_g2, up_g2)

    # combine masks and refine if needed
    mask = cv2.bitwise_or(mask1, mask2)
    kernel = np.ones((3, 3), np.uint8)

    # cv2.morphologyEx(): 
    #    - It is used to perform morphological transformations on the mask in order to remove noise and small imperfections. 
    #    - It works by applying/sliding a kernel over the image and performing choosen operations.
    #    - In this case, I'm using the MORPH_OPEN operation which removes small white noise and restores the size of the remaining objects.
    #    - I'm also applying the MORPH_DILATE operation to further enhance the mask.
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_DILATE, kernel)

    # create inverse mask and isolate cloak area
    inv_mask = cv2.bitwise_not(mask)
    
    bg = cv2.bitwise_and(background, background, mask=mask)
    fg = cv2.bitwise_and(frame, frame, mask=inv_mask)

    # combine background with current frame
    final_output = cv2.add(bg, fg)

    return final_output


cap = cv2.VideoCapture(0)

# capture background (press 'b' to save it)
# or ignore this and use the first 2 seconds of the camera as background
while True:
    ret, background = cap.read()
    cv2.imshow("Capture background (press 'b' to save it)", background) # added this line to show the background feed...
    if cv2.waitKey(1) & 0xFF == ord('b'):
        break

while True:
    ret, frame = cap.read()
    output = apply_invisible_cloak(frame, background)
    cv2.imshow("Cloak Effect", output)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
