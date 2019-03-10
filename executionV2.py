import re
import sys
import stop_list
import string
import math
import nltk
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
ps = PorterStemmer()
stop_words = stop_list.closed_class_stop_words
query_collection_name = "cran.qry"
query_file = open(query_collection_name,'r')
IDF_query_collection = {}
queries = query_file.read().replace("\n", " ")
queries = queries.split(".I")
queries = [phases for phases in queries if phases != ""]
non_repeating_list = []
# handling input
for i in range(len(queries)):
    queries[i] = nltk.word_tokenize(queries[i])
    queries[i].pop(0)
    queries[i].pop(0)
    queries[i] = [word for word in queries[i] if word not in stopwords.words('english') and word not in string.punctuation]
    non_repeating_list.append(list(set(queries[i])))
#print(queries)
# IDF calculation for queries
for query in non_repeating_list:
    for word in query:
        if word not in IDF_query_collection:
            IDF_query_collection[word] = 1
        else:
            IDF_query_collection[word] += 1

for word in IDF_query_collection:
    IDF_query_collection[word] = math.log((len(queries)/IDF_query_collection[word])+1)
# TF calculation for queries
vector_list_queries = []
for i in range(len(queries)):
    vector_list_queries.append({})
for i in range(len(queries)):
    for word in queries[i]:
        if word not in vector_list_queries[i]:
            # vector_list_queries[i][word] = 1/len(queries[i])
            vector_list_queries[i][word] = 1
        else:
            # vector_list_queries[i][word] += 1/len(queries[i])
            vector_list_queries[i][word] += 1

# TF*IDF
for vectors in vector_list_queries:
    for word in vectors:
        vectors[word] = math.log(vectors[word]+1) * IDF_query_collection[word]
#print(vector_list_queries)
query_file.close()
abstract_name = "cran.all.1400"
abstract_file = open(abstract_name, 'r')
abstract = abstract_file.read().replace("\n", " ").split(".I")
abstract = [document for document in abstract if document != ""]
for i in range(len(abstract)):
    abstract[i] = nltk.word_tokenize(abstract[i])


for i in range(len(abstract)):
    result = 0
    for j in range(len(abstract[i])):
        if abstract[i][j] == ".W":
            result = j
            break
    del(abstract[i][0:j+1])

non_repeating_list_abstract = []
for i in range(len(abstract)):
    abstract[i] = [word for word in abstract[i] if word not in stopwords.words('english') and word not in string.punctuation]
    non_repeating_list_abstract.append(list(set(abstract[i])))
# IDF calculation for abstracts
IDF_abstract_collection = {}
for document in non_repeating_list_abstract:
    for word in document:
        if word not in IDF_abstract_collection:
            IDF_abstract_collection[word] = 1
        else:
            IDF_abstract_collection[word] += 1

for word in IDF_abstract_collection:
    IDF_abstract_collection[word] = math.log((len(abstract)/IDF_abstract_collection[word])+1)

# TF calculation for abstracts
vector_list_documents = []
for i in range(len(abstract)):
    vector_list_documents.append({})
for i in range(len(abstract)):
    for word in abstract[i]:
        if word not in vector_list_documents[i]:
            # vector_list_documents[i][word] = 1/len(abstract[i])
            vector_list_documents[i][word] = 1
        else:
            # vector_list_documents[i][word] += 1/len(abstract[i])
            vector_list_documents[i][word] += 1
# TF*IDF
for vectors in vector_list_documents:
    for word in vectors:
        vectors[word] = math.log(vectors[word]+1) * IDF_abstract_collection[word]

output = open("output.txt",'w')

# Similarity calculation
ranking_list_all = []
for i in range(len(vector_list_queries)):
    queries_vec = vector_list_queries[i]
    ranking = []
    ranking.clear()
    for j in range(len(vector_list_documents)):
        document_vec = vector_list_documents[j]
        for word in queries_vec:
            if word not in document_vec:
                document_vec[word] = 0
        cosine_num = 0
        cosine_den = 0
        queries_square = 0
        document_square = 0
        for word in queries_vec:
            cosine_num += queries_vec[word]*document_vec[word]
        for word in queries_vec:
            queries_square += queries_vec[word]**2
            document_square += document_vec[word]**2
        cosine_den = math.sqrt(queries_square*document_square)
        if cosine_den == 0:
            cosine_ranking = 0
        else:
            cosine_ranking = cosine_num/cosine_den
        ranking.append((cosine_ranking, j))
    ranking.sort(key = lambda tup: tup[0], reverse = True)
    #print(ranking)
    for ranks in ranking:
        output.write(str(i+1))
        output.write(" ")
        output.write(str(ranks[1]+1))
        output.write(" ")
        output.write(str(ranks[0]))
        output.write("\n")
    #ranking_list_all.append(ranking)
# output = open("output.txt",'w')
# for i in range(len(ranking_list_all)):
#     for ranks in ranking_list_all[i]:
#         output.write(i + " " + ranks[1] + " " + ranks[0] + "\n")
