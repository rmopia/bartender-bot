
import numpy as np
import tensorflow
import tflearn as tf
import json
import random
from nltk import word_tokenize
from nltk.stem.lancaster import LancasterStemmer

from blacklist import BLACKLIST

corpus = json.load(open("corpus.json"))

words = []
description = []
token_list = []
label_stats = []

"""tokenizing and categorizing data obtained from json file"""
for stats in corpus["corpus"]:
    if stats["label"] not in description:
        description.append(stats["label"])
    for pattern in stats["patterns"]:
        tokens = word_tokenize(pattern)
        words.extend(tokens)
        token_list.append(tokens)
        label_stats.append(stats["label"])

"""processes tokens into stems/keywords and compares them to words from corpus"""
stemmer = LancasterStemmer()
words = [stemmer.stem(word.lower()) for word in words if word is not "?"]
training = []
result = []
row = [0] * len(description)

for n, t_list in enumerate(token_list):
    word_bag = []
    tokens = [stemmer.stem(word.lower()) for word in t_list]

    for w in words:
        if w in tokens:
            word_bag.append(1)
        else:
            word_bag.append(0)

    result_row = row[:]
    result_row[description.index(label_stats[n])] = 1
    training.append(word_bag)
    result.append(result_row)

training = np.array(training)
result = np.array(result)

tensorflow.reset_default_graph()
flow = tf.input_data(shape=[None, len(training[0])])
flow = tf.fully_connected(flow, 10)
flow = tf.fully_connected(flow, 10)
flow = tf.fully_connected(flow, len(result[0]), activation="softmax")
flow = tf.regression(flow)
model = tf.DNN(flow)
model.fit(training, result, n_epoch=500, batch_size=8,show_metric=False)

def prediction(s, words):
    possibilities = [0] * len(words)
    s_words = word_tokenize(s)
    s_words = [stemmer.stem(word.lower()) for word in s_words]

    for sw in s_words:
        for i, word in enumerate(words):
            if sw == word:
                possibilities[i] = 1
    return np.array(possibilities)

empty_responses = ["Huh.", "Interesting.", "Do tell.", "I didn't quite catch that.", "Hmm. A pity.", "Alrighty then.",
                   "That'll land you in the calaboose.", "Best skedaddle out of here."]

def bar_demo():
    print("Welcome to the Salty Spitoon. The only saloon for the next 60 miles north, east, south and west!")
    for _ in range(4):
        print("*" * 97)
    while True:
        user_input = input("> ")
        if user_input.lower() == "quit":
            quit(0)
        for inp in word_tokenize(user_input):
            for profanity in BLACKLIST:
                if inp == profanity:
                    print(random.choice(empty_responses))
                    quit(1)
        output = model.predict([prediction(user_input, words)])
        output_index = np.argmax(output)
        label = description[output_index]
        for lbl in corpus["corpus"]:
            if lbl["label"] == label:
                responses = lbl["responses"]

        print(random.choice(responses))


bar_demo()
