import random
from functools import reduce
from math import floor

#from typing import Any
#from typing import List

#### Classes:
class testData:
        """Record type that holds all the important data. """
        def __init__(self):
                """Note: mq means message quantity"""
                self.test = parseFile()
                self.mq = getSubLength(self.test)
                self.train_data = list(map(lambda xs: getRandomSample(xs,0.8),self.test))
                self.mq_train = getSubLength(self.train_data)
                self.test_data = [list(set(self.test[0]) - set(self.train_data[0])),list(set(self.test[1]) - set(self.train_data[1]))]
                self.mq_test = getSubLength(self.train_data)


### Aux Functions:
#def concat(l: List[List[Any]]) -> List[Any]:
def concat(l):
        return [s for xs in l for s in xs]

def getSubLength(xs):
        return reduce(lambda x,y:x+y, map(len,xs))

def getRandomSample(xs, p):
        return random.sample(xs,int(floor(len(xs)*p)))

### Helper Functions:

#def cleanString(message: str) -> str:
def cleanString(message):
        """Returns a curated string without symbols, multiple spaces, leading/trealing 
        spaces and lowercased."""
        return message.replace('W+',' ').replace('\s+',' ').lower().strip()

#def parseFile() -> List[List[Any]]:
def parseFile():
        """" Reads the spam collection sample and 
        Returns a list whose first element contains all the spam messages
        and its second element contains all the non spam messages"""
        f = open("SMSSpamCollection")
        messages = [[],[]]
        for line in f:
                parse = line.split("\t")
                if (parse[0] == "spam"):
                        messages[0] += [parse[1]]
                else:
                        messages[1] += [parse[1]]
        f.close()
        return messages

#def N_wi_spam(word: str,message_spam: List[str]) -> int:
def N_wi_spam(word,message_spam):                                        
        words = concat(map(lambda s: s.split(),message_spam))
        f = lambda w: 1 if (w==word) else 0
        return reduce(lambda x,y: x+y,map(f,words))
                                        
### Main Functions:

def naive_bayes(message):
        data = testData() # Test data.
        words_not_spam = concat(map(lambda s: s.plit(),data.train_data[1]))
        words_spam = concat(map(lambda s: s.plit(),data.train_data[0]))
	words =  words_not_spam + words_spam
        vocabulary = list(set(words))
	N_vocabulary = len(vocabulary)  # Number of unique words in the dataset
	N_not_spam=len(words_not_spam)	
	N_spam=len(words_spam)  # Number of words in spam mails

	alpha=1
	P_spam = len(data.train_data[0])/data.mq_train
	P_not_spam = len(data.train_data[1])/data.mq_train
	
	for i in range(len(test)):
		if test[i][1]==0:
			message=test[i][0].split()
	
	
	message_spam=data.train_data[1]
	for i in range(len(test)):
		if test[i][1]==1:
			mes=test[i][0].split()	
	
	contador=0
	for i in range(len(message_spam)):
		for words in words_spam:
			if words in message_spam[i]:
					contador+=1	
	N_wi_spam=contador-N_spam  # Number of words that repeats in every spam mail
	
	q=classify(message,word,words_spam,words_not_spam,alpha,N_spam,N_vocabulary,N_wi_spam,P_spam,P_not_spam,N_not_spam,message_spam)
	print (q)
	
#def N_wi_spam(word,message_spam):
#	contador=0
#	for i in range(len(message_spam)):
#		if word in message_spam[i]:
#			w=message_spam[i].split()
#			for i in range(len(w)):
#				if word==w[i]:
#					contador+=1
#				else:
#					i=i+1
#	return contador	
	
def spam_(word,words_spam,alpha,N_spam,N_vocabulary,message_spam,P_spam):
	if word in words_spam:
		return P_spam*(N_wi_spam(word,message_spam)+alpha)/(N_spam+(alpha*N_vocabulary))
	else:
		return 1
	
	
def not_spam_(word,words_not_spam,P_not_spam,message_spam,alpha,N_vocabulary,N_not_spam):
	if word in words_not_spam:
		return P_not_spam*(N_wi_spam(word,message_spam)+alpha)/(N_not_spam+(alpha*N_vocabulary))
	else:
		return 1

def classify(message,word,words_spam,words_not_spam,alpha,N_spam,N_vocabulary,N_wi_spam,P_spam,P_not_spam,N_not_spam,message_spam):
	p_spam_message=P_spam
	p_not_spam_message=P_not_spam
	for word in message:
		p_spam_message*=spam_(word,words_spam,alpha,N_spam,N_vocabulary,message_spam,P_spam)
		p_not_spam_message*=not_spam_(word,words_not_spam,P_not_spam,message_spam,alpha,N_vocabulary,N_not_spam)
	if p_not_spam_message>p_spam_message:
		return "Not spam"
	elif p_not_spam_message<p_spam_message:
		return "Spam"
	else:
		"Can't be classified"
	
	
def spam(f):
	v=f.split()
	#print (v)
	naive_bayes(v)

#f=str(input("Introduce un mail:"))
#spam(f)
