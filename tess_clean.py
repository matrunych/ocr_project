from PIL import Image
import pytesseract
import argparse
import cv2
import os
import numpy as np
import matplotlib.pyplot as plt


text_dir = "training-dataset-text"
text_files = os.listdir(text_dir)
text_files = sorted(text_files, key=lambda x: int(x[7:-4]))
print(text_files)

words = []
for file in text_files:
    with open(text_dir + "/" + file) as f:
        words_cur = []

        for line in f:
            words_cur.append(line.strip().split()[-1][1:-1])

        words.append(words_cur)

print(words)

img_dir = "training-dataset-images"
image_files = os.listdir(img_dir)
image_files = sorted(image_files, key=lambda x: int(x[4:-4]))

print(image_files)

custom_config = r'--oem 3 --psm 11'
for i in range(len(image_files)):
    if image_files[i].endswith("gif"):
        continue

    img = cv2.imread(img_dir + "/" + image_files[i])
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray, 180, 255, cv2.THRESH_BINARY)
    image_final = cv2.bitwise_and(gray, gray, mask=thresh)
    ret, new_img = cv2.threshold(image_final, 180, 255, cv2.THRESH_BINARY)

    output = pytesseract.image_to_string(new_img, config=custom_config)

    output = output.strip().split()

    count = 0
    for word in output:
        if word in words[i]:
            count += 1

    accuracy = count / len(words[i])

    with open("tesseract_accuracy.txt", "a") as f:
        f.write(str(accuracy) + "\n")

    print(output)
    print(words[i])
    print(accuracy)
    print("")



#
# print(words)
#
# img = cv2.imread('training-dataset-images/img_28.png')
# gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# ret, thresh = cv2.threshold(gray, 180, 255, cv2.THRESH_BINARY)
# image_final = cv2.bitwise_and(gray, gray, mask=thresh)
# ret, new_img = cv2.threshold(image_final, 180, 255, cv2.THRESH_BINARY)
#
#
# # plt.imshow(new_img)
# # plt.show()
#
# # Adding custom options 3 6
# custom_config = r'--oem 3 --psm 11'
# print(pytesseract.image_to_string(new_img, config=custom_config))