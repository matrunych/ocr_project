import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt


accuracies = []
with open("kraken_docs_accuracy.txt") as f:
    for line in f:
        accuracies.append(float(line.strip()))

accuracies = sorted(accuracies, reverse=True)

df = pd.DataFrame()
df["id"] = range(len(accuracies))
df["accuracy"] = accuracies


plt.rcParams["figure.figsize"] = (10, 3)

plot = sns.barplot(x="id", y="accuracy", data=df)
plot.set(xticklabels=[], xlabel="")
plt.show()

print(accuracies)