from PIL import Image
import pytesseract
import argparse
import cv2
import os

img = cv2.imread('img_28.png')

# Adding custom options 3 6
custom_config = r'--oem 3 --psm 11'
print(pytesseract.image_to_string(img, config=custom_config))