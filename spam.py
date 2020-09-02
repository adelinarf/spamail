import random
from math import floor

#test=[["gana dinero sin hacer nada",1], ["nuevas promociones",0],["gana 100 dolares sin hacer nada al dia",1],["trabaja desde ya",0]]

def compose(f,g):
        return lambda x: f(g(x))


def cleanString(message):
        return message.replace('W+',' ').replace('\s+',' ').lower().strip()


def naive_bayes(message):
        test = parseFile()
        cantidad_mensajes = len(test)
        train_data = random.sample(test, floor(cantidad_mensajes * 0.8))
        test_data = list(set(test) - set(train_data))
	vocabulary=[]
	words=[]
	for i in range(len(test)):
		w=list(map(cleanString,test[i][0].split()))
		words+=w
		#print (words)

        vocabulary = list(set(words))
	N_vocabulary = len(vocabulary)  # Number of unique words in the dataset
	
	words_not_spam=[]
	for i in range(len(test)):
		if test[i][1]==0:
			message=test[i][0].split()
			words_not_spam+=message
	#print (words_not_spam)
	N_not_spam=len(words_not_spam)
	
	
	words_spam=[]
	message_spam=[]
	for i in range(len(test)):
		if test[i][1]==1:
			message_spam.append(test[i][0])
			mes=test[i][0].split()
			words_spam+=mes
	#print (message_spam,words_spam)		
	
	N_spam=len(words_spam)  # Number of words in spam mails
	#print (N_spam)
	contador=0
	for i in range(len(message_spam)):
		for words in words_spam:
			if words in message_spam[i]:
					contador+=1	
	N_wi_spam=contador-N_spam  # Number of words that repeats in every spam mail
	#print (N_wi_spam)
	alpha=1
	P_spam=N_spam/N_vocabulary
	P_not_spam=N_not_spam/N_vocabulary
	
	q=classify(message,word,words_spam,words_not_spam,alpha,N_spam,N_vocabulary,N_wi_spam,P_spam,P_not_spam,N_not_spam)
	print (q)
	
def N_wi_spam(word,message_spam):
	contador=0
	for i in range(len(message_spam)):
		if word in message_spam[i]:
			w=message_spam[i].split()
			for i in range(len(w)):
				if word==w[i]:
					contador+=1
				else:
					i=i+1
	return contador	
	
def spam_(word,words_spam,alpha,N_spam,N_vocabulary,N_wi_spam,P_spam):
	if word in words_spam:
		return P_spam*(N_wi_spam+alpha)/(N_spam+(alpha*N_vocabulary))
	else:
		return 1
	
	
def not_spam_(word,words_not_spam,P_not_spam,N_wi_spam,alpha,N_vocabulary,N_not_spam):
	if word in words_not_spam:
		return P_not_spam*(N_wi_spam+alpha)/(N_not_spam+(alpha*N_vocabulary))
	else:
		return 1

def classify(message,word,words_spam,words_not_spam,alpha,N_spam,N_vocabulary,N_wi_spam,P_spam,P_not_spam,N_not_spam):
	p_spam_message=P_spam
	p_not_spam_message=P_not_spam
	for word in message:
		p_spam_message*=spam_(word,words_spam,alpha,N_spam,N_vocabulary,N_wi_spam,P_spam)
		p_not_spam_message*=not_spam_(word,words_not_spam,P_spam,N_wi_spam,alpha,N_vocabulary,N_not_spam)
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

def parseFile():
        f = open("SMSSpamCollection")
        messages = []
        for line in f:
                parse = line.split("\t")
                if (parse[0] == "spam"):
                        messages += [[parse[1],1]]
                else:
                        messages += [[parse[1],0]]
        f.close()
        return messages
        
#f=str(input("Introduce un mail:"))
#spam(f)

