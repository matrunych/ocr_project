accuracies = []
with open("kraken_docs_accuracy.txt") as f:
    for line in f:
        accuracies.append(float(line.strip()))

print(sum(accuracies) / len(accuracies))
