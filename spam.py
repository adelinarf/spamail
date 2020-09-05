import random
import re
import string
from functools import reduce
from math import floor

# from typing import Any
# from typing import List


# --Classes:
class testData:
    """Record type that holds all the important data. """
    def __init__(self):
        """Note: mq means message quantity"""
        self.test = parseFile()
        self.mq = getSubLength(self.test)
        self.train_data = list(map(lambda xs: getRandomSample(xs, 0.8),
                                   self.test))
        self.mq_train = getSubLength(self.train_data)
        self.test_data = [list(set(self.test[0]) - set(self.train_data[0])),
                          list(set(self.test[1]) - set(self.train_data[1]))]
        self.mq_test = getSubLength(self.train_data)


# -- Aux Functions:
# def concat(l: List[List[Any]]) -> List[Any]:
def concat(li):
    return [s for xs in li for s in xs]


def getSubLength(xs):
    return reduce(lambda x, y: x+y, map(len, xs))


def getRandomSample(xs, p):
    return random.sample(xs, int(floor(len(xs)*p)))


# -- Helper Functions:
# def cleanString(message: str) -> str:
def cleanString(message):
    """Returns a curated string without symbols, multiple spaces, leading/trealing
    spaces and lowercased."""
    return re.sub('\s+', ' ', message).lower().strip().translate(None,
                                                                 string.punctuation)


# def parseFile() -> List[List[Any]]:
def parseFile():
    """" Reads the spam collection sample and
    Returns a list whose first element contains all the spam messages
    and its second element contains all the non spam messages"""
    f = open("SMSSpamCollection")
    messages = [[], []]
    for line in f:
        parse = line.split("\t")
        if (parse[0] == "spam"):
            messages[0] += [parse[1]]
        else:
            messages[1] += [parse[1]]
    f.close()
    return messages


def p_wi_(word, words, message_):
    f = lambda w: 1.0 if word in w.split() else 0.0
    if word in words:
        aux = (1.0+sum(map(f, message_)))/(len(message_)+2.0)
        return aux
    else:
        return 1.0


# --Main Functions:

def naive_bayes(message):
    data = testData()  # Test data.

    words_not_spam = list(set(concat(map(lambda s: s.split(), data.train_data[1]))))  # Words in all the not spam messages
    P_not_spam = len(data.train_data[1])/float(data.mq_train)
    message_not_spam = data.train_data[1]

    words_spam = list(set(concat(map(lambda s: s.split(), data.train_data[0]))))  # Words in all the spam messages
    P_spam = len(data.train_data[0])/float(data.mq_train)
    message_spam = data.train_data[0]

    q = classify(message, words_spam, words_not_spam,
                 P_spam, P_not_spam, message_spam, message_not_spam)
    print(q)
    return (q)


def classify(message, words_spam, words_not_spam,
             P_spam, P_not_spam, message_spam, message_not_spam):
    p_spam_message = P_spam
    p_not_spam_message = P_not_spam
    print(message)
    for word in set(message.split()):
        p_spam_message     *= p_wi_(word, words_spam, message_spam)
        p_not_spam_message *= p_wi_(word, words_not_spam, message_not_spam)
    p_spam_prob = p_spam_message / (p_spam_message + p_not_spam_message)
    p_not_spam_prob = p_not_spam_message / (p_not_spam_message + p_spam_message)
    print(p_spam_prob)
    print(p_not_spam_prob)

    if p_not_spam_prob > p_spam_prob:
        return "Not spam"
    elif p_not_spam_prob < p_spam_prob:
        return "Spam"
    else:
        return "Can't be classified"


def spam():
    data = testData()
    datas = [data.test_data[0][0:500], data.test_data[1][0:500]]
    mensajes = []
    spam = []
    notspam = []
    for i in range(len(datas)):
        a = datas[i]   # se toma la posicion i del data set
        for j in range(len(a)):
            resultado = naive_bayes(a[j])  # se aplica la funcion ahi
            if resultado == "Spam":
                spam.append(a[j])   # si es spam se mete en una lista
            else:
                notspam.append(a[j])  # si no es spam se mete en otra lista
        mensajes.append(spam)   # se unen las listas de no spam y spam
        mensajes.append(notspam)
        #if set(mensajes[0]) == set(datas[0]) and set(mensajes[1]) == set(datas[1]):
            #print("Is ok the classification")   # se evalua si son correctas o no
        #else:
            #print("Bad classification")
        good = 0
        goodnot = 0
        for i in range(len(mensajes[0])):
            if mensajes[0][i] in datas[0]:   # si la posicion de mensajes tiene el mismo texto que datas esta bien y suma 1
                good += 1
        for i in range(len(mensajes[1])):
            if mensajes[1][i] in datas[1]:
                goodnot += 1
        print(good, goodnot)


spam()
