import os, time
import pyautogui # capture image
from PIL import ImageChops # compare images
import cv2

# left image (original)
# starting point (0,158)
# right image (changed)
# starting point (1445,158)
# image size
# width = 1434
# height = 1145

while True:

    # to start or terminate the program
    result = pyautogui.confirm('Find Differences', buttons =('start', 'end'))
    if result == 'end':
        break # program terminated

    width, height = 1434, 1145
    y_pos = 158

    source = pyautogui.screenshot(region=(0, y_pos, width, height))
    # source.save('src.jpg')

    changed = pyautogui.screenshot(region=(1445, y_pos, width, height))
    # changed.save('changed.jpg')

    diff = ImageChops.difference(source,changed)
    diff.save('diff.jpg')

    # waiting for creating a file
    while not os.path.exists('diff.jpg'):
        time.sleep(2)

    # convert images from above to opencv images
    #source_img = cv2.imread('src.jpg')
    #changed_img = cv2.imread('changed.jpg')
    diff_img = cv2.imread('diff.jpg')

    # make images simple in order to work on images easily
    # convert color images to grayscale
    gray = cv2.cvtColor(diff_img, cv2.COLOR_BGR2GRAY) # BGR is used in Opencv (not RGB)
    gray = (gray > 25) * gray # to solve the problem that an outline is going to be the whole image
    # find outlines(contours) and junk var
    contours, _ = cv2.findContours(gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE) # retrieve external outline, save all the coordinate from differences

    # make the differences visible to be surrounded by a rectangle
    color = (0, 200, 0) # B,G,R
    for contour in contours:
        if cv2.contourArea(contour) > 100: # only if there is an outlier which is greater than 100, show the rectangle or just neglact
            x, y, width, height = cv2.boundingRect(contour) # to get coordinates for outline
            #cv2.rectangle(source_img, (x,y), (x+width, y+height), color, 2)
            #cv2.rectangle(changed_img, (x,y), (x+width, y+height), color, 2)
            cv2.rectangle(diff_img, (x,y), (x+width, y+height), color, 2)

            # click to automate finding differences
            to_x = x + (width // 2)
            to_y = y + (width // 2) + y_pos
            pyautogui.moveTo(to_x, to_y, duration=.3)
            pyautogui.click(to_x, to_y)
    
    #cv2.imshow('source', source_img)
    #cv2.imshow('changed', changed_img)
    cv2.imshow('diff', diff_img)

    #cv2.waitKey(0)
    #cv2.destroyAllWindows()