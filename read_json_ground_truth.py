import os
import json


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

dir_outputs = "doc-kraken-outputs"
output_files = sorted(os.listdir(dir_outputs))

for i in range(len(output_files)):
    output = []

    with open(dir_outputs + "/" + output_files[i]) as f:
        for line in f:
            output.extend(line.strip().split())

    count = 0
    for word in output:
        if word in words[i]:
            count += 1

    accuracy = count / len(words[i])

    print(output)
    print(words[i])
    print(accuracy)
    print("")

    with open("kraken_docs_accuracy.txt", "a") as f:
        f.write(str(accuracy) + "\n")

