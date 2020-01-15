import nltk
from nltk.stem import WordNetLemmatizer
import pickle
import numpy as np
from keras.models import load_model
import json
import click

ERROR_THRESHOLD = 0.01


class SmartEcho:
    def __init__(self):
        self.lemmatizer = WordNetLemmatizer()
        self.model = load_model("model/echo_model.h5")
        self.intents = json.loads(open("model/intents.json").read())
        self.words = pickle.load(open("model/words.pkl", "rb"))
        self.classes = pickle.load(open("model/classes.pkl", "rb"))

    def predict_command(self, command):
        p = self.bow(command, show_details=False)
        res = self.model.predict(np.array([p]))[0]
        results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]
        # sort by strength f probability
        results.sort(key=lambda x: x[1], reverse=True)
        return_list = []
        for r in results:
            return_list.append({"intent": self.classes[r[0]], "probability": str(r[1])})

        return return_list

    def bow(self, command, show_details=True):
        sentence_words = self.tokenize_command(command)
        print(sentence_words)
        bag = [0] * len(self.words)
        for s in sentence_words:
            for i, w in enumerate(self.words):
                if w == s:
                    bag[i] = 1
                    if show_details:
                        print("found in bag: %s" % w)
        return np.array(bag)

    def tokenize_command(self, command):
        sentence_words = nltk.word_tokenize(command)
        sentence_words = [
            self.lemmatizer.lemmatize(word.lower()) for word in sentence_words
        ]
        return sentence_words


@click.command()
@click.option("--command")
def parse_command(command):
    smart_echo = SmartEcho()

    print(f"Predicting command {command}")

    prediction = smart_echo.predict_command(command)

    print(f"My prediction is {prediction}")


if __name__ == "__main__":
    parse_command()

