
import sys
import numpy as np
import cv2
import time
import os
import threading
import pytesseract
import imutils
import re
import matplotlib.pyplot as plt
from Api_ocr import fun






pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'






def get_string(img_path):
    img = cv2.imread(img_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    file_name = os.path.basename(img_path).split('.')[0]
    file_name = file_name.split()[0]
    output_path = os.path.join('output_path')
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    img = cv2.resize(img, None, fx=1.5, fy=1.5, interpolation=cv2.INTER_CUBIC)
    rgb_planes = cv2.split(img)
    result_planes = []
    result_norm_planes = []
    for plane in rgb_planes:
        dilated_img = cv2.dilate(plane, np.ones((7,7), np.uint8))
        bg_img = cv2.medianBlur(dilated_img, 21)
        diff_img = 255 - cv2.absdiff(plane, bg_img)
        result_planes.append(diff_img)
    img = cv2.merge(result_planes)
    kernel = np.ones((1, 1), np.uint8)
    img = cv2.dilate(img, kernel, iterations=1)
    img = cv2.erode(img, kernel, iterations=1)
    img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    save_path = os.path.join(output_path, file_name + "_filter_" + str('as') + ".png")
    
    cv2.imwrite(save_path, img)
    text = fun(save_path)
    result = pytesseract.image_to_string(
            img ,lang ='eng',config='--oem 3  --psm 3 -c tessedit_char_whitelist=abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
        )

    return text


# s = get_string(r"D:\helmet\OCR\inverted.jpg")

# t = s.split(sep='\n')

# for s in t:
#     print(s)



# import numpy as np

# def getSkewAngle(cvImage) -> float:
#     # Prep image, copy, convert to gray scale, blur, and threshold
#     newImage = cvImage.copy()
#     gray = cv2.cvtColor(newImage, cv2.COLOR_BGR2GRAY)
#     blur = cv2.GaussianBlur(gray, (9, 9), 0)
#     thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

#     # Apply dilate to merge text into meaningful lines/paragraphs.
#     # Use larger kernel on X axis to merge characters into single line, cancelling out any spaces.
#     # But use smaller kernel on Y axis to separate between different blocks of text
#     kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (30, 5))
#     dilate = cv2.dilate(thresh, kernel, iterations=2)

#     # Find all contours
#     contours, hierarchy = cv2.findContours(dilate, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
#     contours = sorted(contours, key = cv2.contourArea, reverse = True)
#     for c in contours:
#         rect = cv2.boundingRect(c)
#         x,y,w,h = rect
#         cv2.rectangle(newImage,(x,y),(x+w,y+h),(0,255,0),2)

#     # Find largest contour and surround in min area box
#     largestContour = contours[0]
#     print (len(contours))
#     minAreaRect = cv2.minAreaRect(largestContour)
#     cv2.imwrite("temp/boxes.jpg", newImage)
#     # Determine the angle. Convert it to the value that was originally used to obtain skewed image
#     angle = minAreaRect[-1]
#     if angle < -45:
#         angle = 90 + angle
#     return -1.0 * angle
# # Rotate the image around its center
# def rotateImage(cvImage, angle: float):
#     newImage = cvImage.copy()
#     (h, w) = newImage.shape[:2]
#     center = (w // 2, h // 2)
#     M = cv2.getRotationMatrix2D(center, angle, 1.0)
#     newImage = cv2.warpAffine(newImage, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
#     return newImage


# def deskew(cvImage):
#     angle = getSkewAngle(cvImage)
#     return rotateImage(cvImage, -1.0 * angle)


# img = cv2.imread('D:\helmet\OCR\image2.jpg')

def Preprocess(path):
    s =get_string(path)
    return s
# t = s.split(sep='\n')
# for s in t:
#     print(s)




