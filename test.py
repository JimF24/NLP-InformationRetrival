import nltk
from nltk.stem import PorterStemmer

sen = "can a criterion be developed to show empirically the validity of flow\n\
solutions for chemically didn't reacting gas mixtures based on the simplifying\n\
assumption of instantaneous local chemical equilibrium ."
lista = sen.split()
listb = nltk.word_tokenize(sen)
print(listb[1])
# my_word = PorterStemmer.stem(listb[1])
for w in listb:
    w = PorterStemmer.stem(w)
print(lista)
print("----------")
print(listb)
print(a)