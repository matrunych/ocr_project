import pytesseract
import cv2
import matplotlib.pyplot as plt
import googletrans
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import re
import os
from difflib import SequenceMatcher
from spellchecker import SpellChecker


custom_config = r'--oem 3 --psm 11'
translator = googletrans.Translator()
img = cv2.imread('training-dataset-images/img_245.png')

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
ret, thresh = cv2.threshold(gray, 180, 255, cv2.THRESH_BINARY)
image_final = cv2.bitwise_and(gray, gray, mask=thresh)
ret, new_img = cv2.threshold(image_final, 180, 255, cv2.THRESH_BINARY)


data = pytesseract.image_to_data(new_img, output_type=pytesseract.Output.DICT)
boxes = []
for i in range(len(data['level'])):
    (x, y, w, h) = (data['left'][i], data['top'][i], data['width'][i], data['height'][i])
    if (x, y, w, h) in boxes or (x == 0 and y == 0 and w == img.shape[1] and h == img.shape[0]):
        continue

    boxes.append((x, y, w, h))

spell = SpellChecker()

outputs = []
translations = []
valid_boxes = []
for box in boxes:
    x, y, w, h = box
    print(x, y, w, h)

    cropped = new_img[y:y + h, x:x + w]

    output = pytesseract.image_to_string(cropped, config=custom_config)
    output = re.sub(r'[^\x00-\x7f]', r'', output)
    output = os.linesep.join([s for s in output.splitlines() if s])

    print(output)

    similar_in_outputs = False
    for out in outputs:
        if SequenceMatcher(None, output, out).ratio() > 0.2:
            print("SIMILAR")
            similar_in_outputs = True
            break

    if similar_in_outputs:
        continue

    outputs.append(output)

    for word in output.split():
        print("CORRECTION " + word + " " + spell.correction(word))
        output = output.replace(word, spell.correction(word))

    if not output.strip() or len(output.strip()) < 4:
        print("removed")
        continue

    translation = translator.translate(output, dest='uk')
    translations.append(translation.text)
    print(translation.text.count("\n"))
    valid_boxes.append(box)

    cv2.rectangle(img, (x, y), (x + w, y + h), (255, 255, 255), -1)

pilimg = Image.fromarray(np.uint8(img)).convert('RGB')
draw = ImageDraw.Draw(pilimg)


print(len(valid_boxes), len(translations))

for i in range(len(valid_boxes)):
    x, y, w, h = valid_boxes[i]
    font = ImageFont.truetype('Code New Roman.otf', size=int((h / (translations[i].count("\n") + 1)) * 0.75))

    color = 'rgb(0, 0, 0)'

    print(translations[i])
    draw.text((x, y), translations[i], fill=color, font=font)

plt.imshow(pilimg)
plt.show()
