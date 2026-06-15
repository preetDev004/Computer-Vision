import cv2
import numpy as np

def img_and_hsv(path):
    image = cv2.imread(path)
    if image is None:
        raise FileNotFoundError(f"Could not open or find the image: {path}")
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    return image, hsv

def empty(value):
    pass

def init_trackbars(window_name="Trackbars"):
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(window_name, 600, 400)

    cv2.createTrackbar("hue_min", window_name, 0, 179, empty)
    cv2.createTrackbar("hue_max", window_name, 179, 179, empty)
    cv2.createTrackbar("sat_min", window_name, 0, 255, empty)
    cv2.createTrackbar("sat_max", window_name, 255, 255, empty)
    cv2.createTrackbar("val_min", window_name, 0, 255, empty)
    cv2.createTrackbar("val_max", window_name, 255, 255, empty)

def get_trackbar_values(window_name="Trackbars"):
    h_min = cv2.getTrackbarPos("hue_min", window_name)
    h_max = cv2.getTrackbarPos("hue_max", window_name)
    s_min = cv2.getTrackbarPos("sat_min", window_name)
    s_max = cv2.getTrackbarPos("sat_max", window_name)
    v_min = cv2.getTrackbarPos("val_min", window_name)
    v_max = cv2.getTrackbarPos("val_max", window_name)
    return (h_min, h_max, s_min, s_max, v_min, v_max)

def segmented_image(image, mask):
    return cv2.bitwise_and(image, image, mask=mask)

def detector(path="./car.jpg"):
    # Load the image once before the loop starts
    img, hsv = img_and_hsv(path)
    
    init_trackbars()

    while True:
        h_min, h_max, s_min, s_max, v_min, v_max = get_trackbar_values()
        
        lower = np.array([h_min, s_min, v_min])
        upper = np.array([h_max, s_max, v_max])
        
        # Corrected: Use the HSV image here
        mask = cv2.inRange(hsv, lower, upper)

        result = segmented_image(img, mask)

        cv2.imshow("Original", img)
        cv2.imshow("Mask", mask)
        cv2.imshow("Segmented", result)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break 
            
    cv2.destroyAllWindows()

if __name__ == "__main__":
    detector()



