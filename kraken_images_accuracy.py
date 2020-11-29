import os


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

dir_outputs = "kraken-outputs"
output_files = sorted(os.listdir(dir_outputs), key=lambda x: int(x[4:-8]))
print(output_files)

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

    with open("kraken_accuracy.txt", "a") as f:
        f.write(str(accuracy) + "\n")