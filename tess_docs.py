import os
import json
import pytesseract
import cv2


dir = "annotations"
files = sorted(os.listdir(dir))

words = []
for file in files:
    words_cur = []

    with open(dir + "/" + file) as f:
        json_content = json.load(f)

        for box in json_content["form"]:
            words_cur.extend(box["text"].split())

    words.append(words_cur)
    # print(words_cur)

img_dir = "images"
image_files = os.listdir(img_dir)
image_files = sorted(image_files)

print(image_files)

custom_config = r'--oem 3 --psm 6'
for i in range(len(image_files)):
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

    with open("tesseract_docs_accuracy.txt", "a") as f:
        f.write(str(accuracy) + "\n")

    print(output)
    print(words[i])
    print(accuracy)
    print("")