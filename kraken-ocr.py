import os

# images = os.listdir("training-dataset-documents")
images = os.listdir("documents")
command = "kraken "

# binarize segment ocr -m en_best.mlmodel
for img in images:
    # command += "-i training-dataset-documents/" + img + " kraken-outputs/" + img + ".txt "
    command += "-i documents/" + img + " doc-kraken-outputs/" + img + ".txt "

command += "binarize --threshold 0.7 segment --scale 3.5 ocr -m en_best.mlmodel"

os.system(command)