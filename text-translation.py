import googletrans

# print(googletrans.LANGUAGES)

file = "line.pred.txt"

translator = googletrans.Translator()


original_text = ""
with open(file, "r") as f:
    for line in f:
        original_text += line.strip()

translation = translator.translate(original_text, dest='uk')


print(translation.text)