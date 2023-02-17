from pprint import pprint
import json
import random
import tensorflow
import tflearn
import numpy
import nltk
from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()

print("loading ai components...")
tensorflow.compat.v1.reset_default_graph()
with open('./static/wonjun.json', 'r', encoding="UTF-8") as pd:
    data = json.load(pd)

words = []
labels = []
nltk.download('punkt')
for intent in data['intents']:
    for pattern in intent['patterns']:
        wrds = nltk.word_tokenize(pattern)
        words.extend(wrds)
        if intent['tag'] not in labels:
            labels.append(intent['tag'])

words = [stemmer.stem(w.lower()) for w in words if w != "?"]
words = sorted(list(set(words)))
labels = sorted(labels)
net = tflearn.input_data(shape=[None, len(words)])
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, 11, activation="softmax")
net = tflearn.regression(net)
model = tflearn.DNN(net)
model.load('./static/model/model.tflearn')
print("loading ai components successfully")


def bag_of_words(s, words):
    bag = [0 for _ in range(len(words))]
    s_words = nltk.word_tokenize(s)
    s_words = [stemmer.stem(word.lower()) for word in s_words]
    for se in s_words:
        for i, w in enumerate(words):
            if w == se:
                bag[i] = 1
    return numpy.array(bag)


class OpenAI:
    def __init__(self, context, p1="사람", p2="AI"):
        self.context = context
        self.p1 = p1
        self.p2 = p2
        self.live_texts = []

    def to_text(self, backwords=True):
        result = "{0}\n\n{1}".format(self.context, "\n".join(
            f"{x}: {y}" for x, y in self.live_texts))
        if backwords:
            result += f"\n{self.p2}: "
        return result

    def create_response(self, text):
        self.live_texts.append((self.p1, text))
        execute = [bag_of_words(self.to_text(), words)]
        results = model.predict(execute)
        results_index = numpy.argmax(results)
        tag = labels[results_index]
        for tg in data["intents"]:
            if tg['tag'] == tag:
                responses = tg['responses']
        result = random.choice(responses)
        self.live_texts.append((self.p2, result))
        return result
