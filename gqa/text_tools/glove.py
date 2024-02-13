import argparse
import json
import pickle 
from tqdm import tqdm
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
# from visual_genome import api as vg
from PIL import Image as PIL_Image
import requests
import io
# from models import Image, Object, Attribute, Relationship
# from models import Region, Graph, QA, QAObject, Synset
import json
# import utils
from nltk.corpus import wordnet as wn
import en
from progress.bar import Bar
from nltk.corpus import wordnet_ic
brown_ic = wordnet_ic.ic('ic-brown.dat')
import pprint
pp = pprint.PrettyPrinter(indent=2)
import os
from nltk.stem import WordNetLemmatizer
import numpy as np
import json
import argparse
from numpy import dot
from numpy.linalg import norm

wnl = WordNetLemmatizer()

def simFunc(a,b): 
    na = norm(a)
    nb = norm(b) 
    if na == 0 or nb == 0:
        return 0 
    return dot(a, b)/(na*nb)

# Initializes word embeddings to random uniform / random normal / GloVe. 
def initEmbRandom(num, dim):
    # uniform initialization
    # if config.wrdEmbUniform:
    #     lowInit = -1.0 * config.wrdEmbScale
    #     highInit = 1.0 * config.wrdEmbScale
    #     embeddings = np.random.uniform(low = lowInit, high = highInit, 
    #         size = (num, dim))
    # # normal initialization
    # else:
    #embeddings = config.wrdEmbScale * np.random.randn(num, dim)
    embeddings =  np.zeros((num, dim))
    return embeddings

def sentenceEmb(sentence, wordVectors):
    words = sentence.split(" ")
    wordEmbs = initEmbRandom(len(words), 300)
    for idx, word in enumerate(words):
        if word in wordVectors:
            wordEmbs[idx] = wordVectors[word]
    sentenceEmb = np.mean(wordEmbs, axis = 0)        
    return sentenceEmb

def initializeWordEmbeddings(dim, wordsDict):
    # embsFile = config.dictNpyFile(name)
    # if config.npy and os.path.exists(embsFile):
    #     embeddings = np.load(embsFile)
    #     print("loaded embs from file")
    # else: 
    #     embeddings = initEmbRandom(wordsDict.getNumSymbols(), dim)

        # if wrdEmbRandom = False, use GloVE
    wordVectors = {}
    with open("glove.6B.300d.txt", "r") as inFile:
        for line in inFile:
            line = line.strip().split()
            word = line[0].lower()
            vector = np.array([float(x) for x in line[1:]])
            # if config.wrdEmbNormalize:
            #     vector /= (numpy.linalg.norm(vector) 1e-6) 
            #     vector *= config.wrdEmbScale

            wordVectors[word] = vector
            # index = wordsDict.sym2id.get(word)
            # if index is not None:
            #     embeddings[index] = vector
            #     counter += 1

    embeddings = {} 
    # answordavg
    for sym in wordsDict:
        if " " in sym:
            symEmb = sentenceEmb(sym, wordVectors)
            embeddings[sym] = symEmb
        else:
            if sym in wordVectors:
                embeddings[sym] = wordVectors[sym]

        
        # print(counter)
        # # print(self.questionDict.sym2id)
        # print(len(self.questionDict.sym2id))
        # # print(self.answerDict.sym2id)      
        # print(len(self.answerDict.sym2id))
        # # print(self.qaDict.sym2id)      
        # print(len(self.qaDict.sym2id))
    
        # if config.npy:
        #     # np.save('/tmp/123', np.array([[1, 2, 3], [4, 5, 6]]))
        #     np.save(embsFile, embeddings)                               
    
    # if wordsDict.padding in wordsDict.sym2id and wordsDict != self.answerDict: #?? padding for answers?
    #     return embeddings[1:] # no embedding for padding symbol
    return embeddings    

oInterOut = {}
objList = [x.strip() for x in list(open("objs/objList.txt"))]
oEmbs = initializeWordEmbeddings(300, objList)
for i, o in enumerate(oEmbs):
	if i % 50 == 0:
		print(i)
	oInter = [(o2,simFunc(oEmbs[o],oEmbs[o2])) for o2 in oEmbs if o != o2] 
	interactions = sorted(oInter, key = lambda x: x[1], reverse = True)[:20]
	oInterOut[o] = interactions

json.dump(oInterOut, open("o2_Inters.json", "w"))

x = open("o2_Inters.txt", "w")
for o in oInterOut:
	x.write("+ "+o+"\n")
	for tup in oInterOut[o]:
		x.write("- "+str(tup)+"\n")
	x.write("\n")
