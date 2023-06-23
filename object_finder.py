import cv2
import numpy as np
import pandas as pd
import os
import pyautogui

def find_objects(image, objects_names, threshold=0.99, filename="locations.csv"):
    """Returns a list of coordinates of specified objects"""
    if not filename.endswith('.csv'):
        print("WRONG FILENAME!")
        return
    objects = []
    for obj_name in objects_names:
        path = str(os.path.dirname(os.path.abspath(__file__))) + "\\images\\" + obj_name
        loaded_obj = np.array(cv2.imread(path))
        objects.append(loaded_obj)

    image_modified = cv2.convertScaleAbs(image)
    middle_points = []

    #Looking for defined object type on a screenshot, we loop through every object passed into the 
    #function and append every middle point to the list
    for obj in objects:

        result = cv2.matchTemplate(image_modified, obj, cv2.TM_CCOEFF_NORMED)
        h, w, d = obj.shape

        #Thresholding (seeking best results)
        loc = np.where(result >= threshold)
        rectangles = []

        for (x, y) in zip(*loc[::-1]):
            rectangles.append([int(x), int(y), int(w), int(h)])

        # Destroying redundant results - algorithm finds multiple results in the proximity of an object

        rectangles, weights = cv2.groupRectangles(rectangles, 1, 0.2)
        for (x, y, w, h) in rectangles:
            cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
            middle_points.append([int(x + w / 2), int(y + h / 2)])

    cv2.imshow('Findings', image)
    cv2.waitKey()
    cv2.destroyAllWindows()
    objects_coords = pd.DataFrame(middle_points, columns=['X', 'Y'])
    objects_coords.to_csv("locations\\"+filename)
    cv2.imwrite("locations\\"+filename.replace(".csv",".png"), image)

def take_screenshot():
    screenshot = np.array(pyautogui.screenshot())
    screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGR2RGB)
    return screenshot
