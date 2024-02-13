import numpy as np
import json
import argparse
from numpy import dot
from numpy.linalg import norm

def simFunc(a,b): 
    na = norm(a)
    nb = norm(b) 
    if na == 0 or nb == 0:
        return 0 
    return dot(a, b)/(na*nb)
#simFunc2 = wn.synset(a).res_similarity(wn.synset(b), brown_ic)


parser = argparse.ArgumentParser()
parser.add_argument('--dir', default="objs", type = str)

# parser.add_argument('--inDir', required=True, type = str)
# parser.add_argument('--tier', required=True)
parser.add_argument('--outputName', default = "metadata", type = str)
# parser.add_argument('--cont', action = "store_true")
# parser.add_argument('--features', action = "store_true")
# parser.add_argument('--maxObjectNum', default = 100, type = int)
# parser.add_argument('--featuresDim', default = 2048, type = int)
# parser.add_argument('--inEnd', default = [""], nargs = "*")

# parser.add_argument('--imagesNum', default = _, type = int)

args = parser.parse_args()
out = "{dir}/{outputName}".format(dir = args.dir, outputName = args.outputName)
outTxt = lambda dictName: out + "_{dictName}.txt".format(dictName = dictName)
outJson = lambda dictName: out + "_{dictName}.json".format(dictName = dictName)


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
    embeddings = np.zeros((num, dim)) # config.wrdEmbScale * , random.randn
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
    zeros = np.zeros((1, 300))
    for sym in wordsDict:
        if " " in sym:
            symEmb = sentenceEmb(sym, wordVectors)
            embeddings[sym] = symEmb
        else:
            # if sym in wordVectors:
            embeddings[sym] = wordVectors.get(sym, zeros) 
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

# with open(outJson("objsNew"), "w") as outFile:

#cats = ["color", "size", "material", "height", "length", "weight", "age", "thickness", "shape", "activity", 
#"depth", "texture", "mood", "width", "orientation", "state", "gender"]

cats = ["toy", "appliance", "kitchenware", "utensil", "tableware", "furniture", "building", "person", 
"food", "snack", "dessert", "fruit", "baked", "pastry", "vegetable", "dairy", "meat", "plant", "tree", "flower", 
"vehicle", "watercraft", "aircraft", "clothing", "accessory", "bag", "animal", "bird", "insect", "reptile", 
"fish", "equipment", "ball", "tool", "container", "weapon", "drink", "location"] # beverage

with open(outJson("objsNew")) as f:
    words = json.load(f)

catsDict = {}
for cat in cats:
    catsDict[cat] = []
catsDict["none"] = []

vocab = cats + [w[0] for w in words]
glove = initializeWordEmbeddings(300, vocab)
print("loaded glove")

def addWord(word):
    # sims = 
    sim = max([(cat, simFunc(glove[word[0]], glove[cat])) for cat in cats], key = lambda x: x[1])
    if sim[1] > 0.3:
        catsDict[sim[0]].append(word)
    else:
        catsDict["none"].append(word)

for word in words:
    addWord(word)

with open(outJson("catsObjGlove"),"w") as f:
    json.dump(catsDict, f)

# with open(outTxt("catsObjGloveL"),"w") as fl, open(outTxt("catsObjGloveS"),"w") as fs:
for c in catsDict:
    with open(outTxt("catsObjGlove_O"+c),"w") as f: 
        wordsC = sorted(catsDict[c], reverse = True, key = lambda i: i[1])
        wordsL = [w for w in wordsC if w[1] > 100]
        wordsS = [w for w in wordsC if w[1] <= 100]
        f.write("\n"+ "- "+c+" -"+"\n")
        # fs.write("\n"+ "- "+c+" -"+"\n")
        for w in wordsL:
            f.write(",".join(map(str,w))+" "+c+"\n")
        # for w in wordsS:
        #     fs.write(",".join(map(str,w))+" "+c+"\n")


