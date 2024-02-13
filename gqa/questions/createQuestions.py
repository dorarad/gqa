from collections import defaultdict
import matplotlib.pyplot as plt
import argparse
import json
import random
import math
import pprint
pp = pprint.PrettyPrinter(indent = 2)
from patterns import *
import en
import copy
import re
import numpy as np
# import json
# import pickle 
# from tqdm import tqdm
# from matplotlib.patches import Rectangle
# from visual_genome import api as vg
# from PIL import Image as PIL_Image
# import requests
# import io
# import copy
# from models import Image, Object, Attribute, Relationship
# from models import Region, Graph, QA, QAObject, Synset

# import utils
# from nltk.corpus import wordnet as wn
# from progress.bar import Bar
# from nltk.corpus import wordnet_ic
# brown_ic = wordnet_ic.ic('ic-brown.dat')
# import os
# from nltk.stem import WordNetLemmatizer
#metadata_annotationsNew.json
# import utils 
# wnl = WordNetLemmatizer()
# import phrasefinder as pf

#pf.search(pf.Corpus.AMERICAN_ENGLISH, "that is followed by").phrases[0].match_count

parser = argparse.ArgumentParser()
# parser.add_argument('--dir', default="vg14", type = str)
# parser.add_argument('--inDir', required=True, type = str)
# parser.add_argument('--tier', required=True)
# parser.add_argument('--outputName', default = "metadata", type = str)
# parser.add_argument('--interThr', default=0.55, type = float)
# parser.add_argument('--interThrRelaxed', default=0.3, type = float)
# parser.add_argument('--sizeThr', default=1.5, type = float)
# parser.add_argument('--bigSizeThr', default=2.5, type = float)
# parser.add_argument('--margin', default=0.15, type = float)
# parser.add_argument('--hside', default=0.3, type = float)
# parser.add_argument('--vside', default=0.18, type = float)
# parser.add_argument('--distance', default=0.25, type = float)
# parser.add_argument('--mo', default=0.15, type = float)
# parser.add_argument('--mi', default=0.35, type = float)
# parser.add_argument('--isize', default=0.9, type = float)
# parser.add_argument('--normal', default=0.05, type = float)
parser.add_argument('--vis', action="store_true")
# parser.add_argument('--stats', default=500, type = int)
# parser.add_argument('--overlapSThr', default=0.85, type = float)
parser.add_argument('--overlapThr', default=0.7, type = float)
parser.add_argument('--interThr', default=0.55, type = float)
parser.add_argument('--interThrRelaxed', default=0.3, type = float)
parser.add_argument('--sizeThr', default=1.5, type = float)
parser.add_argument('--bigSizeThr', default=2.5, type = float)
parser.add_argument('--margin', default=0.15, type = float)
parser.add_argument('--hside', default=0.3, type = float)
parser.add_argument('--vside', default=0.18, type = float)
parser.add_argument('--distance', default=0.25, type = float)
# parser.add_argument('--distanceRelaxed', default=0.7, type = float)
parser.add_argument('--mo', default=0.15, type = float)
parser.add_argument('--mi', default=0.35, type = float)
parser.add_argument('--iSize', default=0.75, type = float)
parser.add_argument('--aSize', default=0.55, type = float)
parser.add_argument('--mSize', default=0.15, type = float) # ?????? 0.3
parser.add_argument('--pSize', default=0.125, type = float) # ???
parser.add_argument('--aProb', default=0.005, type = float) # ??? MAKE LARGER??????
parser.add_argument('--aLProb', default=0.05, type = float) # ???
parser.add_argument('--aCount', default=3, type = int) # ???
parser.add_argument('--oSize', default=0.002, type = float) # ??? 0.02
parser.add_argument('--cSize', default=0.1, type = float) # ?????? 0.09 05
parser.add_argument('--sameRefProb', default=0.5, type = float) # ?????? 0.09 05
# parser.add_argument('--shard', default="All", type = str) # ???
parser.add_argument('--equate', default=0.0, type = float) # ?????? 0.09 05
parser.add_argument('--rephrases', default = 1, type = int) # ???
parser.add_argument('--rephrasesBin', default = 0.25, type = float)
parser.add_argument('--rephrasesMax', default = 4, type = int)
parser.add_argument('--tier', default = 0.1, type = float)
parser.add_argument('--mturk1', default = 10, type = int)
parser.add_argument('--mturk2', default = 5, type = int)
parser.add_argument('--makeMturk', action="store_true")
parser.add_argument('--smallThr', default = 1, type = float)
parser.add_argument('--bigThr', default = 1, type = float)
parser.add_argument('--uniform', action="store_true")
parser.add_argument('--debug', action="store_true")
parser.add_argument('--gsmoothPrms', default = "", type = str)
parser.add_argument('--lsmoothPrms', default = "", type = str)
# parser.add_argument('--newnorm', action="store_true")
# parser.add_argument('--fix', action="store_true")
# parser.add_argument('--stats', action="store_true")
# parser.add_argument('--subsets', action="store_true")

# parser.add_argument('--cont', action = "store_true")
# parser.add_argument('--features', action = "store_true")
# parser.add_argument('--maxObjectNum', default = 100, type = int)
# parser.add_argument('--featuresDim', default = 2048, type = int)
# parser.add_argument('--inEnd', default = [""], nargs = "*")

# parser.add_argument('--imagesNum', default = _, type = int)

# ------------------------------------------------------------

parser.add_argument('--create', action="store_true")
parser.add_argument('--normalize', action="store_true")
parser.add_argument('--entailed', action="store_true")
parser.add_argument('--models', action="store_true")
parser.add_argument('--questionPrefix', default="final", type = str) # ???

parser.add_argument('--graphstats', action="store_true")
parser.add_argument('--histo', action="store_true")
parser.add_argument('--scores', action="store_true")
parser.add_argument('--scoresFiles', nargs = "*", type = str) # ???
parser.add_argument('--scoresSuffix', default="", type = str) # ???
parser.add_argument('--grounding', action="store_true")
parser.add_argument('--ds', default= "samQuestions", type = str) # default= "samgQuestions"

args = parser.parse_args()

def loadDicts(inDict):
    outDict = {}
    for k in inDict:
        with open(inDict[k]) as f:
            outDict[k] = json.load(f)
    return outDict

dataFilename = "graphDataFinal/info{}.json" # newData/info{}.json 00_{}
dataOutFilename1 = "finaliter1/info{}.json" # .format(args.shard) prefix = args.questionPrefix
dataOutFilename2 = "finaliter2/v{}info{}.json" # .format(args.shard)
dataOutFilename3 = "finaliter3/v{}info{}.json" # .format(args.shard)
dataOutFilename4 = "finaliter4/v{}info{}.json" # .format(args.shard)
dataOutFilename5 = "finaliter5/v{}info{}.json" # km{}
dataOutFilename7 = "finaliter6/info{}.json" # km{} am{}
dataOutFilename6 = "finaliter7/v{}info{}.json"
dataOutFilename8 = "finaliter8/v{}info{}.json"
counterFile = "finaliter2/v{}counter{}.json"
mturkFilename = "hits/hits{}.json"

shardsNum = 1 if args.debug else 20
# height: int, 'width': int, 'coco': id / None
# objects: obj Dict with ones from objList
# uobjects: obj Dict with all objs
# predObjects: obj Dict with predictions
# posRels: rel list. rel: {rel: left/right, obj: id, subj: id}, 
# name2obj: dict: name, list: [(id, score)]
# # refs

# Object:
# key: objId, structure:
# name: str, preds: [(name, score)]
# attributes: str list, predAttributes: [(name, score)]
# outRels / inRels: rels dict
# rel: {rel: name, obj: id, subj: id}
# pos: list: left, right, top, bottom, middle
# posRels: relId list
# rx0 ry0 rx1 ry1 rw rh
# x0 y0 x1 y1 xc yc w h
# size
# of <-- verify

###

x2imageFiles = { # x - > [imgIds...]
    "o": "vg14/oImg.json",
    "oo": "vg14/ooImg.json",
    "oor": "vg14/oorImg.json",
    "oon": "vg14/oonImg.json",
    # "oO": "vg14/oOImg.json", # TODO: filter with predObjects
    # "ooR": "vg14/ooRImg.json",
    # "ooN": "vg14/ooNImg.json",
    "O": "simImg.json"    
}

topFiles = { # x -> [(y,n),...]
    # "o2a": "vg14/oaList.json",  # GOOD, but bug..
    # "o1": "vg14/info_o1List.json", # GOOD
    # "o2": "vg14/info_o2List.json", # GOOD
    "sr2o": "vg14/info_sroList.json",
    "or2s": "vg14/info_orsList.json",
    # "so2r": "vg14/info_sorList.json", # GOOD
 #    "o2so": "o2_inters.json", # GOOD
 #    "ops": "vg14/opsList.json", # GOOD # (s,r,o), (sroDict[s][r][o] * sroDict[o][r][s], sroDict[s][r][o], orsDict[s][r][o]) 
 #    "ormulti": "vg14/srmultiList.json", # GOOD
 #    "srmulti": "vg14/ormultiList.json", # GOOD
 #    "srmulti": "vg14/ormultiList.json", # GOOD
 #    "ormulti": "vg14/ormultiList.json",  # GOOD   
 #    "oo": "vg14/topOO.json", # GOOD
 #    "coo": "vg14/topCOO.json", # GOOD
 #    "oo_Rr": "vg14/ooTFList.json", # GOOD
 #    "oo_rr": "vg14/oorrList.json", # GOOD
 #    "sor": "vg14/topSORList.json", # GOOD
 #    "oon": "vg14/topOonList.json", # GOOD
}

vocabFiles = {
    "o": "vg14/cObjsNV.json",
    "a": "vg14/cAttrsNV.json",
    "r": "vg14/cRelsNV.json"
}

# o
# "school bus": {
#     #"count": "45",
#     *"main": true,
#     *"cat": "vehicle"
# },

# r
# "across from": {
#     ?"cat": "spatial",
#     #"subcat": null,
#     #"simcat": null,
#     *"syms": [],
#     #"count": "179",
#     passive: None
#     stative: False
#     *"cases": [
#         "s",
#         "o"
#     ]
#     place
#     spatial
# },

# a 
# "rainbow colored": {
#     *"cat": "24",
#     #"subcat": null,
#     *"simcat": "colorful",
#     *"sims": [], <-- can't use sims for comparison or false candidates
#     *"syms": [
#         "rainbow-colored"
#     ],
#     *"adjForm": "rainbow colored", <-- adj form for questions
#     *"isAdj": true, <-- has to use adj form
#     #"count": "215",
#     #"named": false
# },

catsFiles = {
    "o": "vg14/cObjsCatsNV.json",
    "a": "vg14/cAttrsCatsNV.json",
}

# a keys: "", number, named
# "shape": [
#     "round",
#     "square",
#     "rectangular",
#     "triangular",
#     "octagonal"
# ],

# o keys: main, extra:
# "object": [
#     "floor tile",
#     "traffic sign",
#     "tank",
#     "pack",
#     "toilet tank",
#     "blocks",
#     "pole",
#     "antenna"
# ],

# TODO: get all words of some cat

countFiles = {
    "o": "vg14/info_oCount.json",
    "oa": "vg14/info_oaCount.json",
    "oo": "vg14/info_ooCount.json",
    "rc": "vg14/info_rcCount.json",  
    "rs": "vg14/info_rsCount.json",  
    "ro": "vg14/info_roCount.json",  
    "sro": "vg14/info_sroCount.json"
}

probFiles = {
    "oa": "vg14/info_oaProb.json",
    "oo2": "vg14/info_ooProb.json" # GOOD
    #"sro": "vg14/sroCount.json"
}

freqFiles = {
    "of": "ofFreqs.json",
    "oa": "oaFreqs.json",
    "ro": "roFreqs.json"
}

# outQuestions = open("questions/out_questions{}.txt".format(args.shard), "w")
# x2image = loadDicts(x2imageFiles)
# catInfo = loadDicts(catsFiles)
tops = loadDicts(topFiles)
vocab = loadDicts(vocabFiles)
freqs = loadDicts(freqFiles)
counts = loadDicts(countFiles)
probs = loadDicts(probFiles)

probs["oo1"] = defaultdict(dict)
for o1 in counts["oo"]:
    for o2 in counts["oo"][o1]:
        probs["oo1"][o1][o2] = float(counts["oo"][o1][o2]) / counts["o"][o1]

for o in probs["oo2"]:
    probs["oo2"][o][o] = counts["o"][o]

parent = {}
for p in objCats:
    for c in objCats[p]:
        parent[c] = p

def writeFile(s):
    pass
    # print(s)
    # outQuestions.write(str(s))
    # outQuestions.write("\n")

def addProp(hashTable, objId, name, score):
    if name not in hashTable:
        hashTable[name] = {}     
    hashTable[name][objId] = score
    # hashTable[name].append((objId, score))

def addObjCat(instance, hashTable, objId, name, score, obj):
    if name not in hashTable:
        hashTable[name] = {"objs": {}, "attr2obj": {}}
    hashTable[name]["objs"][objId] = score
    # hashTable[name]["objs"].append((objId, score))

    if "attributes" in obj:
        for attr in obj["attributes"]:
            addProp(hashTable[name]["attr2obj"], objId, attr, score) # -> prop

    if "pos" in obj:
        for pos in obj["pos"]:
            addProp(hashTable[name]["attr2obj"], objId, pos, score)

    if "predAttributes" in obj:
        for attr, attrScore in obj["predAttributes"]:
            addProp(hashTable[name]["attr2obj"], objId, attr, score * attrScore)

    for relId in obj["outRels"]:
        rel = obj["outRels"][relId]
        relo = instance["objects"][rel["obj"]]["name"]
        prop = "{}_{}".format(rel["rel"], relo)
        addProp(hashTable[name]["attr2obj"], objId, prop, score)            

    for relId in obj["inRels"]:
        rel = obj["inRels"][relId]
        srel = instance["objects"][rel["subj"]]["name"]
        prop = "{}_{}".format(srel, rel["rel"])
        addProp(hashTable[name]["attr2obj"], objId, prop, score)     

def addObj(instance, hashTable, objId, name, score, obj):
    name = singularOf(name) if isPlural(name) else name
    addObjCat(instance, hashTable, objId, name, score, obj)

    parents = ancestors(catOf(obj)) #name catn ["name"]
    for p in parents:
        addObjCat(instance, hashTable, objId, p, score, obj)

def hashObjs(instance, hashTable, objDict):
    for objId in objDict:
        obj = objDict[objId]
        if "name" in obj:
            addObj(instance, hashTable, objId, obj["name"], 1.0, obj)
        if "preds" in obj:
            for pred in obj["preds"]:
                addObj(instance, hashTable, objId, pred[0], pred[1], obj)

    return hashTable

def typeOf(a, o, retAll = False):
    if o is not None and a in o["senses"]:
        return o["senses"][a]
    if a in vocab["a"]:
        clist = vocab["a"][a]["cat"]
        if retAll:
            return clist
        if len(clist) == 1:
            clist[0] = "" if clist[0] is None else clist[0]
            return clist[0]
    return None

def catn(oname):
    if oname in vocab["o"]:
        return vocab["o"][oname]["cat"]
    return None

def how():
    return "what" if coin(0.72) else "how"

def mod(o):
    if o in vocab["o"]:
        return vocab["o"][o]["mod"]
    return None

def isPlural(o):
    return mod(o) == "plural"

def isSingular(o):
    return mod(o) == "singular"

def isMass(o):
    return mod(o) == "mass"

def singularOf(objname):
    ret = en.noun.singular(objname) if isPlural(objname) else objname
    if ret == "browny":
        ret = "brownie"    
    return ret
    # return en.noun.singular(objname)

def pluralOf(objname):
    ret = en.noun.plural(objname) if isSingular(objname) else objname
    if ret == "busses":
        return "buses"
    if ret == "kine":
        return "cows"
    if ret == "bread":
        return "breads"
    if ret == "pepperoni":
        return "pepperoni"
    if ret == "device":
        return "devices"
    if ret == "fruit":
        return "fruits"        
    return ret
    # return en.noun.plural(singularOf(objname))

def statOf(obj, attr, p):
    if attr == singularOf(obj):
        return 0
    ds = probs if p else counts
    if obj not in ds["oa"]:
        return 0
    return ds["oa"][obj].get(attr, 0)

def freqOf(d, k1, k2):
    if k1 not in freqs[d]:
        return None
    return freqs[d][k1].get(k2)

def objSims(obj, wide = False):
    sims = set()
    keys = vocab["o"][obj]["sims"] + [singularOf(obj)]

    for k in keys:
        for o in simGroups[k]:
            sims.add(o)
    
    if wide:
        cat = vocab["o"][obj]["cat"]
        if catInfo[cat]["similarity"]:
            for o in cat2objs[cat]:
                sims.add(o)   

    return sims        

def objAlts(obj, indicators = False):
    good = set()
    altscat = vocab["o"][obj]["altscat"]
    if altscat != "":
        for o in altGroups[altscat]:
            good.add(o)
    
    alts = vocab["o"][obj]["alts"]
    for o in alts:
        good.add(o)

    if indicators:
        inds = vocab["o"][obj]["indicators"]
        for o in inds:
            good.add(o)

        indCat = vocab["o"][obj]["catIndicator"]
        if indCat != "":
            objs = cat2objs[indCat]
            for o in objs:
                good.add(o)

    bad = objSims(obj)
    # bad.add(obj)
    ret = [a for a in good if a not in bad]
    return ret

def simType(a):
    if a in vocab["a"]:
        return vocab["a"][a]["simCat"]
    return None  

def ancestors(c):
    path = []
    if c is None:
        c = ""
    p = c
    while p != "None":
        path.append(p)
        p = parent[p]
    path.append(p)        

    path = path[::-1]
    return path

def specificAncestors(c):
    ans = ancestors(c)
    return [a for a in ans if a not in generalCats]

def commonAns(c1, c2):
    p1 = ancestors(c1)
    p2 = ancestors(c2)
    i = 0
    while i < min(len(p1), len(p2)) and p1[i] == p2[i]:
        i += 1
    i -= 1
    return p1[i]

def isA(o, cq):
    c = catOf(o)
    if c is None:
        return False
    ans = ancestors(c)
    return cq in ans #() or cq == o

def isAn(oname, cq):
    c = catn(oname)
    if c is None:
        return False
    ans = ancestors(c)
    return cq in ans #() or cq == o

def isAc(c, cq):
    if c is None:
        return False
    ans = ancestors(c)
    return cq in ans #() or cq == o

def isAlist(o, clist): # return sublist?
    c = catOf(o)
    if c is None:
        return False    
    ans = ancestors(c)
    for cq in clist:
        if cq in ans:
            return True
    return False

def isWeakExistObj(obj, strong = False):
    if isAn(obj, "place"):
        return False
    if strong:
        cat = vocab["o"][obj]["cat"]
        if not catInfo[cat]["standalone"]:
            return False
    return (vocab["o"][obj]["main"] == 0)

def parentOf(o1, o2):
    o1s = singularOf(o1)
    o2s = singularOf(o2)
    ans = ancestors(catn(o2s))
    return o1s in ans

def weakParentOf(o1, o2):
    o1c = catn(singularOf())
    o2s = singularOf(o2)
    ans = ancestors(catn(o2s))
    return o1c not in generalCats and o1p in ans

def isFamily(o1, o2):
    return parentOf(o1, o2) or parentOf(o2, o1) or singularOf(o1) == singularOf(o2)

def isWeakFamily(o1, o2):
    return weakParentOf(o1, o2) or weakParentOf(o2, o1) or singularOf(o1) == singularOf(o2)

def replace(old, new):
    if isFamily(old, new):
        return parentOf(old, new)
    return counts["o"][new] > counts["o"][old]
    # return vocab["o"][new]["count"] > vocab["o"][old]["count"]

# # GOOD
# for o in x2image["o"]:
#     x2image["o"][o] = set(x2image["o"][o])

# for o in x2image["O"]:
#     x2image["O"][o] = set(x2image["O"][o])

# for o1 in x2image["oo"]:
#     for o2 in x2image["oo"][o1]:
#         x2image["oo"][o1][o2] = set(x2image["oo"][o1][o2])

# for o1 in x2image["oor"]:
#     for o2 in x2image["oor"][o1]:
#         for r in x2image["oor"][o1][o2]:
#             x2image["oor"][o1][o2][r] = set(x2image["oor"][o1][o2][r])

# top["oo_rrv"] = [e for e in top["oo_rr"] if ((not vocab["r"][e[1][1][0][0]]["cat"] == "direct") and 
#                                              (not vocab["r"][e[1][1][1][0]]["cat"] == "direct"))]
# # GOOD

# patterns:
# - query pattern + answer
# - right verify pattern
# - false verify pattern + sources
# - pattern codes


# def captialLetter

# def questionMark:

# patterns = {
#     "exist": {

#     }
#     "queryAttr": [{
#         "pattern": [
#             "What {T> is/are <DO>?"
#         ]
#         "code":
#         "answer":
#         "constraint": [()]  
#     }]

#                 "what cat is o? subcat"
#                 "What type/kind"

def coords(o):
    return (o["x0"], o["y0"], o["x1"], o["y1"])

def close(c1, c2):
    for i in range(len(c1)):
        if abs(c1[i] - c2[i]) > 8:
            return False
    return True

def yrange(c):
    return (c[1], c[3])

def xrange(c):
    return (c[0], c[2])

def intersection(r1, r2):
    ir = (max(r1[0], r2[0]), min(r1[1], r2[1]))
    if ir[1] > ir[0]:
        return ir
    return None

def percent(r1, r2):
    if r2[1] - r2[0] == 0:
        return 1.0
    return float(r1[1]-r1[0]) / (r2[1] - r2[0])

def midpoint(r):
    return float(r[0] + r[1]) / 2

def leftrange(r1, r2):
    return r1[1] < midpoint(r2) and r2[0] > midpoint(r1)

def rightrange(r1, r2):
    return r1[0] > midpoint(r2) and r2[1] < midpoint(r1)

def closerange(r1, r2):
    return r2[0] - r1[1] < args.distance

def overlap(r1, r2):
    i = intersection(r1, r2)
    if i is None:
        return False
    p1 = percent(i, r1)
    p2 = percent(i, r2)
    p = max(p1,p2)
    return p > args.interThr

def relativeleft(c1, c2):
    return overlap(yrange(c1), yrange(c2)) and leftrange(xrange(c1), xrange(c2)) and closerange(xrange(c1), xrange(c2))

def relativeright(c1, c2):
    return overlap(yrange(c1), yrange(c2)) and rightrange(xrange(c1), xrange(c2)) and closerange(xrange(c2), xrange(c1))

def overlapRelaxed(r1, r2):
    i = intersection(r1, r2)
    if i is None:
        return False
    p1 = percent(i, r1)
    p2 = percent(i, r2)
    p = max(p1,p2)
    return p > args.interThrRelaxed

def relativeleftRelaxed(c1, c2):
    return overlapRelaxed(yrange(c1), yrange(c2)) and leftrange(xrange(c1), xrange(c2)) # and closerange(xrange(c1), xrange(c2))

def relativerightRelaxed(c1, c2):
    return overlapRelaxed(yrange(c1), yrange(c2)) and rightrange(xrange(c1), xrange(c2)) # and closerange(xrange(c2), xrange(c1))

def globalleft(c):
    return midpoint(xrange(c)) < args.hside

def globalright(c):
    return midpoint(xrange(c)) > 1 - args.hside

def globaltop(c):
    return midpoint(yrange(c)) < args.vside

def globalbottom(c):
    return midpoint(yrange(c)) > 1 - args.vside

def pinside(p, r):
    return p > r[0] and p < r[1]

def rinside(r1, r2):
    return r1[0] > r2[0] and r1[1] < r2[1]

def middlerange(r):
    i = pinside(midpoint(r), (args.mi, 1 - args.mi))
    o = rinside(r, (args.mo, 1 - args.mo))
    return i and o

def globalmiddle(c):
    return middlerange(xrange(c)) and middlerange(yrange(c))

def length(r):
    if r is None:
        return 0    
    return float(r[1] - r[0])

def size(c):
    return length(xrange(c)) * length(yrange(c))

def bigger(c1, c2):
    return size(c1) > args.sizeThr * size(c2)

def smaller(c1, c2):
    return bigger(c2, c1)

def main(c1, c2):
    return size(c1) > args.bigSizeThr * size(c2)

def minSize(obj):
    return size(coords(obj)) > args.oSize

def catSize(obj):
    return size(coords(obj)) > args.cSize

def allImage(c):
    return size(c) > args.aSize

def mainImage(c):
    return size(c) > args.mSize

def intersectionSize(c1, c2):
    return length(intersection(xrange(c1), xrange(c2))) * length(intersection(yrange(c1), yrange(c2)))
    # p1 = percent(i, r1)
    # p2 = percent(i, r2)
    # p = max(p1, p2)
    # return p > args.interThrRelaxed

def inside(c1, c2):
    if size(c1) == 0:
        return False
    return float(intersectionSize(c1, c2)) / size(c1) > args.isize

def overlapping(c1, c2):
    isize = float(intersectionSize(c1, c2))
    if size(c1) == 0 or size(c2) == 0:
        return False
    p1 = isize / size(c1)
    p2 = isize / size(c2)
    p = min(p1, p2)
    return p > args.overlapThr

def strongOverlapping(c1, c2):
    isize = float(intersectionSize(c1, c2))
    if size(c1) == 0 or size(c2) == 0:
        return False    
    p1 = isize / size(c1)
    p2 = isize / size(c2)
    p = min(p1, p2)
    return p

def onMargin(c):
    x = xrange(c)
    y = yrange(c)
    xm = x[1] < args.margin or x[0] > 1 - args.margin
    ym = y[1] < args.margin or y[0] > 1 - args.margin
    return xm or ym

def vis(imageId):   
    img = GetImageData(id = imageId)
    # print ("The url of the image is: %s" % image.url)

    fig, ax = plt.subplots()
    fig.set_size_inches(18.5, 10.5)

    # fig = plt.gcf()
    # fig.set_size_inches(18.5, 10.5)
    objs = list(data[imageId]["objects"].values())

    plt.imshow(img)
    # ax = plt.gca()
    # print(len(objs))
    for obj in objs:
        # if "relations" not in obj or len(obj["relations"]) == 0:
        #     continue        
        # print(obj)
        ax.add_patch(Rectangle((obj["rx0"], obj["ry0"]),
                               obj["rw"],
                               obj["rh"],
                               fill=False,
                               edgecolor='red',
                               linewidth=3))
        text = obj["name"]
        text += "\n"
        # text += " ".join(obj["attributes"]) + " "
        # if "predAttributes" in obj:
        #     text += " ".join([o[0] for o in obj["predAttributes"]])
        # text += "\n"
        # text += " ".join([str(1) for _ in obj["attributes"]]) + " "
        # if "predAttributes" in obj:
        #     text += " ".join([str(o[1])[:5] for o in obj["predAttributes"]])
        if "pos" in obj:
            text += "({})".format(str(obj["pos"]))
        for relId in obj["posRels"]:
            rel = data[imageId]["posRels"][relId]
            text += " " + "{}-{}".format(rel["rel"], data[imageId]["objects"][rel["obj"]]["name"])

        print(text)
                
        ax.text(obj["rx0"], obj["ry0"], text, style='italic', bbox={'facecolor':'white', 'alpha':0.5}) # , 'pad':10
        #text = obj["name"] + ("({})".format(", ".join([x["rel"]+"-"+x["subjN"]+"-"+x["objN"] for x in obj["relations"]])) if "relations" in obj and len(obj["relations"]) > 0 else "")
        #ax.text(obj["x"], obj["y"], text, style='italic', bbox={'facecolor':'white', 'alpha':0.7, 'pad':10})
        # i += 1
    # fig = plt.gcf()
    plt.tick_params(labelbottom='off', labelleft='off')
    #plt.show()
    plt.savefig("photos/"+imageId+"Data.jpg", dpi = 720) # +"_"+str(j)
    plt.close(fig)

# trivial = [] # if it's a question
parents2objs = defaultdict(set)
cat2objs = defaultdict(set)
simGroups = defaultdict(set)
altGroups = defaultdict(set)
for obj in vocab["o"]:
    #ancestors
    c = catn(obj)
    # if c is None:
    #     c = "None:
    cat2objs[c].add(obj)
    for ans in ancestors(c):
        parents2objs[ans].add(obj)
    singularObj = singularOf(obj)
    simGroups[singularObj].add(obj)
    keys = vocab["o"][obj]["sims"]
    for k in keys:
        simGroups[k].add(obj)

    altscat = vocab["o"][obj]["altscat"]
    if altscat != "":
        altGroups[altscat].add(obj)

typeGroups = defaultdict(set)
attrSimGroups = defaultdict(set)
for attr in vocab["a"]:
    ts = typeOf(attr, None, retAll = True)
    for t in ts:
        typeGroups[t].add(attr)
    # if t is not None:

for attr in vocab["a"]:
    attrSimGroups[attr].add(attr)
    keys = vocab["a"][attr]["simcats"]
    for k in keys:
        attrSimGroups[k].add(attr)

nProb = {} # defaultdict(dict) # lambda: defaultdict(
for obj in vocab["o"]:
    nProb[obj] = {}

    for t in typeGroups:
        attrs = typeGroups[t]
        attrsTypeCount = sum([statOf(obj, attr, p = False) for attr in attrs])

        for attr in attrs:
            nProb[obj][attr] = 0 if attrsTypeCount == 0 else (float(statOf(obj, attr, p = False)) / attrsTypeCount) # [t]

existanceObjs = set()
indToObjs = defaultdict(set)
# for obj in vocab["o"]:
#     indToObjs[obj] = set()
for obj in vocab["o"]:
    # obj = singularOf(obj) ???????????????????????????!?!?!?!?!?!?!?!?!?!!!?!?!?!?!?!?!?
    inds = objAlts(obj, indicators = True)
    if not isAn(obj, "place"):
        if len(inds) > 0:
            existanceObjs.add(obj)
        for ind in inds:
            indToObjs[ind].add(obj)

weakExistanceObjs = [obj for obj in vocab["o"] if isWeakExistObj(obj, strong = True)]

def objWeakAlts(obj):
    sims = objSims(obj, wide = True)
    return [alter for alter in weakExistanceObjs if (alter not in sims) and isWeakFamily(alter, obj)]

def kategory(cat):
    return "kind|type of {}".format(cat)

# TODO: update cat json to include all info
def catForms(cat, obj):
    # if cat in catNoncountable:
    #     return None
    if (cat in catMass) or (obj in ["headphones"]):
        return [cat], [cat], True
    return [cat], [toPlural[cat] if cat in toPlural else pluralOf(cat)], False

# def catPlural(cat):
#     if cat in catMass:
#         return cat, cat, False
#     return cat, (toPlural[cat] if cat in toPlural else pluralOf(cat)), True

def catNormalize(obj, cat, k = False):
    # c = catOf(obj)
    # if not catInfo[cat]["qspecific"]:
    #     return None
    if cat in catNoncountable:
        # ???????????????????????????!?!?!?!?!?!?!?!?!?!!!!?!?!?!?!!!!?!?!?!?!?!?!!?!?!?!?!
        # if not k:
        #     return None, "is"
        # ???????????????????????????!?!?!?!?!?!?!?!?!?!!!!?!?!?!?!!!!?!?!?!?!?!?!!?!?!?!?!
        prob = 0.8
        slist, plist, ptos = catNoncountable[cat]
    else:
        prob = 0.5
        slist, plist, ptos = catForms(cat, obj["name"])

    if k and coin(prob):
        s = kategory(cat)
        p = kategory(cat)
        ptos = True
    else:
        s = choice(slist)
        p = choice(plist)

    sing = not isPlural(obj["name"])
    catSing = sing or ptos
    return (s if sing else p), "is" if catSing else "are"

def coin(prob):
    if prob == 1:
        return True
    if prob == 0:
        return False
    return random.random() < prob

def choice(choices):
    if choices is None:
        return None
    return random.choice(choices) if len(choices) > 0 else None

def prioChoice(choices, weights = None): # 
    maxPrio = max([c["priority"] for c in choices])
    maxChoices = [c for c in choices if c["priority"] == maxPrio]
    return weightedChoice(maxChoices, weights) # choice(maxChoices) if weights is None else  choice(maxChoices) 

# subtypes?
# todo can merge dicts!
tfType2weight = {
    "logical": 0.75, # 0.54
    "verify": 0.25, # 0.46
    "compare": 10
}

oType2weight = {
    "choose": 0.28, # 0.28 0.2
    "query": 0.72, # 0.72 0.8
    "compare": 10
}

tfProb = 0.32 # 0.5 # 5 0.35

def weightedChoice(choices, weights, priority = False):
    if weights is None:
        return choice(choices)
    
    type2choices = defaultdict(list)
    for c in choices:
        type2choices[c["type"]].append(c)
    
    type2choice = {}
    for t in type2choices:
        # print([(q["group"], q["priority"], q["question"]) for q in type2choices[t]])
        c = sample([(q, q["priority"]) for q in type2choices[t]]) if priority else choice(type2choices[t]) # prioChoice
        type2choice[t] = c

    weightedChoices = [(c, weights[t]) for t,c in type2choice.items() if c is not None]
    return sample(weightedChoices)

def mostCommon(l):
    return max(set(l), key=l.count)

def sampleUniqueQuestions(questions):
    out = []
    if len(questions) == 0:
        return out

    tfQuestions = [q for q in questions if q["tf"]]
    oQuestions = [q for q in questions if not q["tf"]]
    
    tfLocalProb, tf2weightlocal, oType2weightlocal = tfProb, tfType2weight, oType2weight
    if questions[0]["newTf"] is not None:
        tfLocalProb = questions[0]["newTf"]
    if "weights" in questions[0]:
        tf2weightlocal = questions[0]["weights"]
        oType2weightlocal = questions[0]["weights"]
    
    if (coin(tfLocalProb) or len(oQuestions) == 0) and (len(tfQuestions) > 0) :
        tQuestions = [q for q in tfQuestions if q["answer"] == "yes"]
        fQuestions = [q for q in tfQuestions if q["answer"] == "no"]
        
        if len(tQuestions) == 0 or len(fQuestions) == 0:
            q = weightedChoice(tfQuestions, tf2weightlocal, priority = True)
            out.append(q)
        else:
            tQ = weightedChoice(tQuestions, tf2weightlocal, priority = True)
            fQ = weightedChoice(fQuestions, tf2weightlocal, priority = True)
            # qType = tQ["codeGroup"][-1] + "F"
            # sfQuestions = [q for q in fQuestions if q["codeGroup"] == qType]
            # if len(sfQuestions) > 0:
            #     fQ = sample([(q, q["priority"]) for q in sfQuestions])  # prioChoice
            # else:
            # 
            types = [q["group"] for q in tfQuestions]
            p = subtypeUbPreProb[subtypeOf[mostCommon(types)]]
            out.append(tQ if coin(p) else fQ)
            # out.append(choice([tQ, fQ]))
    else: # if len(oQuestions) > 0:
        q = weightedChoice(oQuestions, oType2weightlocal, priority = True)
        out.append(q)

    return out

def dedupQuestions(instance):
    questions2id = {}
    outIds = []

    for qid, question in instance["questions"].items():
        add = False
        if question["question"] not in questions2id:
            add = True
        else:
            preId = questions2id[question["question"]]
            preQuestion = instance["questions"][preId]
            if question["ansDist"] and (not preQuestion["ansDist"]):
                outIds.remove(preId)
                add = True

        if add:
            outIds.append(qid)
            questions2id[question["question"]] = qid

    instance["questions"] = {qid: q for (qid, q) in instance["questions"].items() if qid in outIds}
    instance["questions"] = {qid: q for (qid, q) in instance["questions"].items() if q["answer"] not in ansBlacklist}

    for key in instance["key2qids"]:
        instance["key2qids"][key] = [qid for qid in instance["key2qids"][key] if qid in instance["questions"]]
    for ccode in instance["ccode2qids"]:
        instance["ccode2qids"][ccode] = [qid for qid in instance["ccode2qids"][ccode] if qid in instance["questions"]]

def getDefault(dd, k1, k2, default):
    if k1 in dd:
        if k2 in dd[k1]:
            return dd[k1][k2]
    return default

def writeIdList(l, fname):
    with open(fname, "w") as f:
        for e in l: 
            epath = "vgi/{e}.jpg xml/{e}.xml".format(e = e)
            f.write("{}\n".format(epath))

def loadFromFile(fname):
    out = set()
    with open(fname) as f:
        l = list(f)
        for e in l:
            e = re.search(r"vgi/(.*)\.jpg", e).group(1)
            out.add(e)
    return out

def printD(d, title):
    print(title)
    print("------------")    
    for k in sorted(d.keys(), key = lambda c: d[c]):
        print(k, d[k])

def printDD(dd, title, edd = None):
    print(title)
    counter = 0
    print("------------")    
    for k1 in dd:
        print(k1)
        for k2 in sorted(dd[k1].keys(), key = lambda c: dd[k1][c]):
            out = dd[k1][k2]
            if edd is not None:
                out *= getDefault(edd, k1, k2, 1)
            counter += out
            print(k2, out)
    print(counter)

    with open(counterFile.format(args.questionPrefix, title), "w") as f:
        json.dump(dd, f)

def downsampleQuestions(gData, inField, outField, gProb): # , typeDict = None, toPrint = False
    # typeCounterU = defaultdict(int)
    # groupCounterU = defaultdict(int)
    for imageId in gData: 
        instance = gData[imageId]
        instance[outField] = [] # {}
        # print(len(instance["rQuestions"]))
        for qid in instance[inField]: # , question .items()
            question = instance["questions"][qid]
            # print("D2", question["key"], question["question"], question["fullAnswer"], question["answer"], "->".join(question["code"]))
            if (question["group"] not in gProb) or coin(gProb[question["group"]]):
                instance[outField].append(qid) # [qid] = question # out
                # if typeDict is not None:
                    # typeDict[question["type"]] += 1
                # groupCounterU[question["group"]] += 1
    # if toPrint:
    #     print(outField)
    #     print("------------")
    #     print(typeCounterU)
    #     for c in sorted(groupCounterU.keys()):
    #         print(c, groupCounterU[c])
# customSmoother(counts, b = 2, gamma = 1.3)
# typeSamples = {
#     "verify": 0.75, 
#     "choose": 0.865, 
#     "logical": 0.95
# }

def typesampleQuestions(gData, inField, outField, typeDict):

    newAll = float(typeDict["query"]) / 0.57
    newVerify = newAll * 0.18 * 1.4
    newChoose = newAll * 0.095 * 1.4
    newLogical = newAll * 0.125 * 1.4

    typeSamples = {
        "verify": min(newVerify / float(typeDict["verify"]), 1),#newAll * 0.17, #0.75, 
        "choose": min(newChoose / float(typeDict["choose"]), 1),#newAll * , #0.865, 
        "logical": min(newLogical / float(typeDict["logical"]), 1)#newAll, #0.95
    }
    print(typeSamples)

    for imageId in gData: 
        instance = gData[imageId]
        instance[outField] = [] # {}
        # print(len(instance["rQuestions"]))
        for qid in instance[inField]: # , question .items()
            question = instance["questions"][qid]
            # print("D2", question["key"], question["question"], question["fullAnswer"], question["answer"], "->".join(question["code"]))
            if (question["type"] not in typeSamples) or coin(typeSamples[question["type"]]):
                instance[outField].append(qid) # [qid] = question # out

def unbiasRatios(counters, smoother):
    ratios = {"open": defaultdict(dict), "boolean": defaultdict(dict)}
    for cond in counters["boolean"]:
        ansDist = counters["boolean"][cond]
        answers = list(ansDist.keys())
        if len(answers) == 1: # and cond not in ["age", ]
            print("removedBool", cond)
            ratios["boolean"][cond][answers[0]] = min(1, float(1) / ansDist[answers[0]]) # 0.0
        else:
            s = counters["boolean"][cond]["yes"] + counters["boolean"][cond]["no"]
            py = float(counters["boolean"][cond]["yes"]) / s
            pn = float(counters["boolean"][cond]["no"]) / s
            if max(py, pn) > 0.5: #0.51:# (max(py, pn) - 0.5) > 0.05:
                if py > pn:
                    ratios["boolean"][cond]["yes"] = min(1, (pn / py) ) #  * (0.51 / 0.49) max()ry # min(1, ry * max()) * (0.55 / 0.45)
                else:
                    ratios["boolean"][cond]["no"] = min(1, (py / pn) ) # * (0.51 / 0.49) rn # min(1, rn * max()) #  * (0.55 / 0.45)
            #rn = 1/ry
            #ry = pn / py # float(counters["boolean"][cond]["no"]) / counters["boolean"][cond]["yes"]

    for cond in counters["open"]:
        ansDist = counters["open"][cond]
        answers = list(ansDist.keys()) 
        if len(answers) == 1: # and cond not in ["age", ]
            print("removedOpen", cond)            
            ratios["open"][cond][answers[0]] = min(1, float(1) / ansDist[answers[0]]) # 0.0
        else:
            sansDist = list(ansDist.items())
            sansDist = sorted(sansDist, key = lambda x: x[1], reverse = True)
            counts = [float(c) for _,c in sansDist]
            newCounts = smoother(counts)
            for i,c in enumerate(newCounts):
                ratios["open"][cond][sansDist[i][0]] = float(c) / sansDist[i][1]

    return ratios

def unbiasOratios(counters, smoother):
    ratios = defaultdict(dict)
    for cat in counters:
        ansDist = counters[cat]
        answers = list(ansDist.keys()) 
        if len(answers) > 1:
            sansDist = list(ansDist.items())
            sansDist = sorted(sansDist, key = lambda x: x[1], reverse = True)
            counts = [float(c) for _,c in sansDist]
            newCounts = smoother(counts)
            for i,c in enumerate(newCounts):
                ratios[cat][sansDist[i][0]] = float(c) / sansDist[i][1]

    return ratios

def unbiasSelect(lists, counters, ratios):
    out = defaultdict(list)
    for atype in ["boolean", "open"]:
        for cond in lists[atype]:
            for ans in lists[atype][cond]:
                if cond in ratios[atype] and ans in ratios[atype][cond]:
                    newCount = int(round(counters[atype][cond][ans] * ratios[atype][cond][ans]))
                    newList = multichoice(lists[atype][cond][ans], newCount)
                else: 
                    newList = lists[atype][cond][ans]
                for qid, imgId in newList:
                    out[imgId].append(qid)

    for qid, imgId in lists["non"]:
        out[imgId].append(qid) 

    return out

def uniformSmoother(thr):
    def usmoother(counts):
        s = sum(counts)
        # ps = [float(sum(counts[:(i+1)])) for i in range(len(counts))]
        k = 1 
        for ck in range(1,len(counts))[::-1]:
            if ((ck + 1) * counts[ck]) / s > thr:
                k = ck
                break
        newCounts = [(counts[k] if i <= k else 0) for i in range(len(counts))]
        return newCounts
    return usmoother

# final:b = 1, gamma = 1.05, gup = 0.02 maxGamma = 1.38
# first?: b = 2, gamma = 1.3, gup = 0.05, maxGamma = 1.5
# smoothPrms b = 2, gamma = 1.25, gup = 0.03, maxGamma = 1.4
def customSmoother(b, gamma, gup, maxGamma): # gamma = 1.3, gup = 0.05  nts, b = 2, gamma = 1.3)
    def csmoother(counts):
    # gamma = 1.2 #1.3
        s = sum(counts)
        probs = [c/s for c in counts] 
        for i in range(len(counts)):
            # print(counts)
            if i == 0:
                continue
            s = sum(counts)
            tail = sum([c for c in counts[i:]])
            head = s - tail
            p = (min(0.1*(i+b),0.85))
            newHead = (p * tail / (1-p)) if i > 1 else 0 # (i-1) * tail # (1 - 1/i) * s
            # print((min(0.1*(i+1),0.85)), newHead, tail)
            if (sum(probs[i:]) > 0.099 or i == 1) and (head > newHead): # tail / s > 0.1
                newGamma = min(gamma + (i-1) * gup, maxGamma) # 1.38 1.5
                newProbs = [(probs[j]/sum(probs[:i])) for j in range(i)]
                for j in range(i-1)[::-1]:
                    newProbs[j] = min(newProbs[j], newGamma * newProbs[j+1])
                n = sum(newProbs)
                newProbs = [p/n for p in newProbs] 
                agamma = (1.1 if i > 1 else gamma)
                if newProbs[i-1] * newHead < agamma * counts[i]: # gamma * 
                    newHead = (agamma * counts[i]) / newProbs[i-1]
                    # print(newHead)
                for j in range(i): #[::-1]:
                    counts[j] = min(newProbs[j] * newHead, counts[j]) # max((probs[j]/sum(probs[:i])) * newHead, newGamma * counts[j+1])
        return counts
    return csmoother
# def customSmoother(counts):
#     gamma = 1.2 #1.3
#     s = sum(counts)
#     probs = [c/s for c in counts] 
#     for i in range(len(counts)):
#         # print(counts)
#         if i == 0:
#             continue
#         s = sum(counts)
#         tail = sum([c for c in counts[i:]])
#         head = s - tail
#         newHead = (min(0.1*(i+1),1) if i > 1 else 0) # (i-1) * tail # (1 - 1/i) * s
#         if (sum(probs[i:]) > 0.15 or i == 1) and (head > newHead): # tail / s > 0.1
#             # print(i, tail, s, head, newHead, gamma * counts[i])
#             for j in range(i):
#                 counts[j] = min(max((counts[j] / head) * newHead, gamma * counts[i]), counts[j])
#     return counts

lnF = lambda c, g: (np.log(g * c) + 1)
sqrtF = lambda c, g: math.sqrt(g * c)
def funcSmoother(sFunc, g):
    def smoother(counts):
        s = sum(counts)
        newCounts = [sFunc(c, g) for c in counts]
        newSum = sum(newCounts)
        newProbs = [c/newSum for c in newCounts]
        newCounts = [min(newProbs[i] * s, counts[i]) for i in range(len(counts))]
        return newCounts
    return smoother

def select(gData, outField, goodIds, outCounter = None, pretypeCounter = None): # inField, , outCounter = None
    # cdansCounter2 = defaultdict(lambda: defaultdict(int))    

    for imageId in gData: 
        instance = gData[imageId]
        # instance[outField] = [] # {}
        # print(len(instance["rQuestions"]))
        instance[outField] = goodIds[imageId]
        for qid in instance[outField]: # , question .items()
            question = instance["questions"][qid]
            # if qid in goodIds:
            #     instance[outField].append(qid) # [qid] = question # out
            if outCounter is not None: #  and cond is not None
                outCounter[question["group"]] += 1 # [ans]
            if pretypeCounter is not None:
                pretypeCounter[question["type"]] += 1
                # ans = question["answer"]
                # cans = catn(ans) or typeOf(ans, None)
                # if cans is not None:
                #     outCounter["cat"][cans][ans] += 1
            ans = question["answer"]
    #         canss = typeOf(ans, None, retAll = True) or [catn(ans)]
    #         if canss is not None:
    #             for cans in canss:
    #                 cdansCounter2[cans][ans] += 1

    # printDD(cdansCounter2, "finalGlobal")

def unbias(gData, inField, outField, ratios): # , outCounter = None , outCounter = None
    for imageId in gData: 
        instance = gData[imageId]
        instance[outField] = [] # {}
        # print(len(instance["rQuestions"]))
        for qid in instance[inField]: # , question .items()
            question = instance["questions"][qid]
            ans = question["answer"]
            cond = getConditional(instance, question)
            tans = "boolean" if ans in ["yes", "no"] else "open" 
            if cond is None or coin(getDefault(ratios[tans], cond, ans, 1)):
                #if (question["type"] not in ["verify", "choose", "logical"]):#: or coin(0.85): # 0.67 REMOVED????????
                instance[outField].append(qid) # [qid] = question # out

                # if outCounter is not None: #  and cond is not None
                    # outCounter[question["group"]] += 1 # [ans]

def unbiasCat(gData, inField, outField, ratios, toprint = False): # , outCounter = None , outCounter = None
    cdansCounter = defaultdict(lambda: defaultdict(int))

    for imageId in gData: 
        instance = gData[imageId]
        instance[outField] = [] # {}
        # print(len(instance["rQuestions"]))
        for qid in instance[inField]: # , question .items()
            question = instance["questions"][qid]
            ans = question["answer"]
            cans = choice(typeOf(ans, None, retAll = True)) or catn(ans)
            if cans is None or coin(getDefault(ratios, cans, ans, 1)):
                instance[outField].append(qid) # [qid] = question # out
                cdansCounter[cans][ans] += 1

    if toprint:
        printDD(cdansCounter, "afterGlobal")

def printStats(gdata, inField):
    typeCounter = defaultdict(int)
    groupCounter = defaultdict(int)

    for imgIndex, imageId in enumerate(gdata): 
        instance = gdata[imageId]
        # print(len(instance["rQuestions"]))
        for qid, question in instance[inField].items():
            typeCounter[question["type"]] += 1
            groupCounter[question["group"]] += 1

    # print(inField)
    # print("------------")    
    # print(typeCounter)
    # for c in sorted(groupCounter.keys()):
    #     print(c, groupCounter[c])

def multichoice(x, num, isDict = False):
    ret = x.keys() if isDict else x
    ret = [e for e in ret]
    random.shuffle(ret)
    ret = ret[:num]
    if isDict:
        ret = {k: x[k] for k in ret}
    return ret

def sortedchoice(l, num):
    sl = sorted(l, key = lambda x: x[1])
    return [e[0] for e in sl][:num]

def subselectQuestions(questions, num = None, prob = None):
    if num is None:
        num = int(math.ceil(prob * len(questions)))

    return multichoice(questions, num) # , isDict = True
   
    # inQuestions = [q for q in questions]
    # return random.shuffle(inQuestions)[:num]

def subuniqueQuestions(instance, qids, num = None, weak = False): # instance, 
    out = {}
    metakeys = set()
    # entailed = set()
    inQuestions = [instance["questions"][qid] for qid in qids] # .values()
    # inQuestions = sorted(inQuestions, key = lambda q: len(q["entailedQuestions"]), reverse = True)
    random.shuffle(inQuestions)
    # print([q["entailedQuestions"] for q in inQuestions])
    cond = lambda p,q: (p["id"] not in q["entailedQuestions"]) and (q["id"] not in p["entailedQuestions"])
    
    for q in inQuestions:
        if (weak or all([cond(pq, q) for pq in out.values()])) and q["metakey"] not in metakeys: # q["id"] not in entailed and 
            out[q["id"]] = q
            metakeys.add(q["metakey"])
            if num is not None and len(out) == num:
                break
    
    # print("!!!!")
    # print([q["entailedQuestions"] for q in out.values()])
    return out.keys()

    # entailed.add(q["id"])
    # for e in q["entailedQuestions"]:
    #     entailed.add(e)

def selectEntailedQuestions(instance, qids, num):
    entailed = {}# set()
    # ids = [question["id"] for question in questions]
    questions = [instance["questions"][qid] for qid in qids]
    for question in questions:
        i = 1
        for eq in question["entailedQuestions"]:
            if (eq in instance["questions"]) and (eq not in qids) and (eq not in entailed) :
                entailed[eq] = i # )
                i += 1

    entailed = [(eq, i) for (eq, i) in entailed.items()]
    ret = sortedchoice(entailed, num) # multichoice  multichoice
    # ret = {k: instance["questions"][k] for k in ks}
    return ret

    # for question in questions:
    #     if question["id"] in entailed:
    #         entailed.remove(question["id"])

    # out =
    # if len(out) < num:
    #     candidates = [q["id"] for q in instance["rQuestions"] if ((q["id"] not in questions) and (q["id"] not in out))]
    #     out += multichoice(candidates, num - len(out))
    
    # if len(out) < num:
    #     candidates = [q["id"] for q in instance["questions"] if ((q["id"] not in questions) and (q["id"] not in out))]
    #     out += multichoice(candidates, num - len(out))

def toRatios(counter):
    prob = {}
    for tlist, flist in questionSubtypes:
        tnum = float(sum([counter[t] for t in tlist]))
        fnum = float(sum([counter[f] for f in flist]))
        # allnum = tnum + fnum
        # ratio = float(fnum) / allnum if allnum > 0 else 0
        # print(tlist, ratio)
        if tnum == 0 or fnum == 0:
            continue
        ratio = fnum / tnum
        if ratio < 1:
            for t in tlist:
                prob[t] = ratio
        else:
            ratio = 1 / ratio
            for f in flist:
                prob[f] = ratio
    return prob

def equate(previous):
    if previous is None:
        return None
    if args.equate > 0.0 and coin(args.equate):
        return previous
    return None

def sample(choices, smoothing = False, index = False):
    if len(choices) == 0:
        return None
    if smoothing:
        choices = [(c, n ** 0.4) for c, n in choices] # math.sqrt(n)

    probsSum = 0.0
    limits = []
    for c in choices:
        prob = c[1]
        probsSum += prob
        limits.append(probsSum)

    if probsSum == 0:
        return None

    num = random.uniform(0, probsSum)
    for i, l in enumerate(limits):
        if num <= l:
            choice, prob = choices[i]
            if index:
                return choice, i 
            return choice

    print("STRANGE!")
    return choice([c for c, w in choices])

def multiSample(choices, num, smoothing = False):
    nchoices = [c for c in choices] # copy.deepcopy(choices)
    chosens = []
    for _ in range(num):
        chosen = sample(nchoices, smoothing)
        if chosen is not None:
            nchoices = [(c,w) for c,w in nchoices if c != chosen]         
            chosens.append(chosen)

    return chosens

def randSample(choices, nextF, smoothing = False):
    nchoices = [c for c in choices] # [c for c in choices] copy.deepcopy(choices)
    chosens = []
    while True:
        s = sample(nchoices, smoothing, index = True)
        if s is None:
            break
        chosen, index  = s
        nchoices = nchoices[:index] + nchoices[(index+1):]
        chosens.append(chosen)
        if not nextF(len(chosens)):
            break

    return chosens

def choiceSelect(choices, only = False):
    if len(choices) == 0:
        return None 
    allChoices = [c for c,b in choices]
    goodChoices = [c for c,b in choices if b]
    badChoices = [c for c,b in choices if not b]
    if only: #  or random.random() < 0.5
        return choice(goodChoices)
    return choice(allChoices)

toAns = {
    "{dobject}": "{aobject}", 
    "{cdobject}": "{caobject}",
    "{dsubject}": "{asubject}",
    "{cdsubject}": "{casubject}"
}

def getAnnotations(s):
    parts = s.split(" ")
    newParts = []
    annotations = {}
    for i, p in enumerate(parts):
        if "~" in p:
            p, a = p.split("~")
            annotations[i] = a
        newParts.append(p)
    newS = " ".join(parts)
    return annotations, newS

def generateQuestion(patterns, mapping, group, data, nonProb):
    questions = []
    
    if args.rephrases > 1:
        patterns = multiSample(patterns, args.rephrases)
    elif args.rephrasesBin > 0:
        nextF = lambda mnum: (coin(args.rephrasesBin) if mnum < args.rephrasesMax else False)
        patterns = randSample(patterns, nextF)
    else:
        patterns = [sample(patterns)]
    
    for pattern in patterns:
        genMapping = copy.deepcopy(mapping)
        genData = copy.deepcopy(data)

        question, fullAns, ans = pattern # [0], pattern[1]
        
        ans = ans.replace("{object}", "{objecta}")
        ans = ans.replace("{attribute}", "{attributea}")

        for r in toAns:
            fullAns = fullAns.replace(r, toAns[r])

        if "{dpobject}" in question:
            if genMapping["dpobject"] is None:
                question = question.replace("{dpobject}", "{dobject}")
            else:
                genMapping["dpobject"], genData["dobject"]["code"] = genMapping["dpobject"]

        if "{dpsubject}" in question:
            if genMapping["dpsubject"] is None:
                question = question.replace("{dpsubject}", "{dsubject}")
            else:
                genMapping["dpsubject"], genData["dobject"]["code"] = genMapping["dpsubject"]

        if "switchA" in genMapping:
            for s in [question, fullAns]:
                if "{a} {attribute}" in s and genMapping["a"] in ["a", "an"]:
                    genMapping["a"] = aPrefix("{} object".format(genMapping["attribute"]))

                if "{anya} {attribute}" in s and genMapping["anya"] in ["a", "an"]:
                    genMapping["anya"] = aPrefix("{} object".format(genMapping["attribute"]))

        if "switchCA" in genMapping:
            for s in [question, fullAns]:
                if "{a} {cAttribute}" in s and genMapping["a"] in ["a", "an"]:
                    genMapping["a"] = aPrefix("{} object".format(genMapping["cAttribute"]))

                if "{anya} {cAttribute}" in s and genMapping["anya"] in ["a", "an"]:
                    genMapping["anya"] = aPrefix("{} object".format(genMapping["cAttribute"]))

        question = question.format(**genMapping)
        fullAns = fullAns.format(**genMapping)
        ans = ans.format(**genMapping)

        question = normalizeString(question, question = True, nonProb = nonProb)
        fullAns = normalizeString(fullAns)
        annotations = {"question": {}, "fullAnswer": {}, "answer": {}}

        annotations["question"], question = getAnnotations(question)
        annotations["fullAnswer"], question = getAnnotations(fullAns)
        annotations["answer"], question = getAnnotations(ans)
        
        newQuestion = {"question": question, "fullAnswer": fullAns, "answer": ans, 
            "annotations": annotations, "group": group}
        # print(newQuestion)

        questions.append(newQuestion)
    return questions

def normalizeCode(code):
    # code = [c.replace("s!he", "person") for c in code]
    code = [re.sub(r" \d+:", ":", c) for c in code]
    code = [c.replace("lchoose", "choose") for c in code]
    return code

# def wnum(s):
#     parts = s.split(" ")
#     parts = [p for p in parts if p != ""]
#     return len(parts)

# def smartReplace(s, f, t, pointers):
#     parts = s.split(f)

#     newS = t.join(parts)
#     return newS

def toNumid(i):
    if i is None:
        return None
    if not i.isnumeric():
        print("??!?!?!?nonnumeric!?!?!?!?!!" + i)
    if i == "-":
        return None
    return i

def toRegex(ws):
    ws = ws.split(" ")
    inws, outws = [], []

    for w in ws:
        if w.endswith("~"):
            w = w[:-1]
            inw = r"{}([~0-9]*)".format(w)
            outw = r"{}\1".format(w)
        else:
            inw = w
            outw = w

        inws.append(inw)
        outws.append(outw) 

    inws = " ".join(inws)
    outws = " ".join(outws)
    return inws, outws

def annotate(s, i):
    i = toNumid(i)
    if i is None:
        return s
    return " ".join(["{}~{}".format(w, i) for w in s.split(" ")])

def smartReplace(s, i, o):
    i = toRegex(i)[0]
    o = toRegex(o)[1]
    return re.sub(i, o, s)

def normalizeString(s, question = False, cap = True, nonProb = False):
    if s.endswith("?"):
        s = s[:-1]
    s = s.lower()
    
    if question:
        s = sampleString(s)

    for word in withoutThe:
        for prefix in ["the", "a", "an"]: # , 
            wi, wo = toRegex(word)
            s = re.sub("{prefix} {word}".format(prefix = prefix, word = wi), wo, s)
        
    # for c in toCaps:
        # s = s.replace(c, toCaps[c])

    s = s.replace(" a other ", " another ")
    s = s.replace(" an other ", " another ")
    s = s.replace(" of or ", " or ")
    s = s.replace(" a image", " an image")
    s = s.replace("the_person", "the person")
    if "on where" in s:
        print(s)        
    s = s.replace("on where", "where")    
    # s = s.replace("is there salad ", "is there a salad")    
    # s = s.replace("is there soup ", "is there a soup")
    # s = s.replace("there is salad ", "there is a salad")
    # s = s.replace("there is soup ", "is there a soup")    
    # s = s.replace("s!he", "s/he")
    
    if not question:
        s = s.replace("[out]=0.03","")
        s = s.replace("kind|type of", "")
        for c in catAnswerReplace:
            s = smartReplace(s, c, catAnswerReplace[c])
        # s = s.replace(" of", "")

    if any(bad in s for bad in ["none", "[", "]", "|", "/" "=", "wooden is used", "made of wooden", "a apple"]): # , "what place", "which place"
        print("?!?!?!?!")
        print(s)

    for aFix in anFixes:
        s = smartReplace(s, aFix, anFixes[aFix])

    if nonProb and coin(0.5):
        s = s.replace("white or black", "black or white")

    if nonProb and coin(0.3):
        s = s.replace("blue or red", "red or blue")

    if nonProb and coin(0.7):
        if coin(0.5):
            s = s.replace("of a person", "of anyone")
        else:
            s = s.replace("of a person", "of someone")

    if nonProb and coin(0.7):
       s = s.replace("is a person", "is someone")

    if nonProb and coin(0.5):
        s = re.sub(r"Is the person([~0-9]*) ([a-z]*ing) ", r"Is someone\1 \2 ", s)

    if nonProb and coin(0.25):
        s = s.replace("what is ", "what's ")
    if nonProb and coin(0.25):
        s = s.replace("how is ", "how's ")
    if nonProb and coin(0.33):
        s = s.replace(" is not ", " isn't ")
    if nonProb and coin(0.33):
        s = s.replace(" are not ", " aren't ")                
    if nonProb and coin(0.5):
        s = s.replace("what type ", "which type ")
    if nonProb and coin(0.5):
        s = s.replace("what kind ", "which kind ")
    # if random.random() < 0.75:
    #     if s.startswith("what place"):
    #         s = s.replace("what place", "where", 1)
    # if random.random() < 0.75:
    #     if s.startswith("which place"):
    #         s = s.replace("which place", "where", 1)
    if nonProb and coin(0.5):
        s = s.replace("what kind ", "which kind ")

    if nonProb and coin(0.35):
        s = s.replace("do you see", "can you see")
    if nonProb and coin(0.65):
        s = s.replace("is seen through", "can be seen through")
        s = s.replace("are seen through", "can be seen through")
    
    if nonProb and coin(0.05):
        s = s.replace("in front of", "before")
    if nonProb and coin(0.1):
        s = s.replace("next to", "beside")
    
    if nonProb:
        if coin(0.5):
            s = s.replace("larger", "bigger")
        else:
            s = s.replace("bigger", "larger")

    if nonProb:
        x = random.random()
        if x < 0.03:
            s = s.replace("to the left of", "on the left of")
        elif x < 0.08:
            s = s.replace("to the left of", "left of")
        elif x < 0.085:
            s = s.replace("to the left of", "left to")

    if nonProb:
        x = random.random()
        if x < 0.03:
            s = s.replace("to the right of", "on the right of")
        elif x < 0.08:
            s = s.replace("to the right of", "right of")
        elif x < 0.085:
            s = s.replace("to the right of", "right to")

    s = " ".join([toCaps.get(w, w) for w in s.split(" ") if w != ""])
    s = s.replace(" ,", ",")
    # if random.random() < 0.2:
    #     slist = s.split(" ")
    #     if slist[-1] in ["at", "on", "in"] and slist[0] != "where":
    #         slist = [slist[-1]] + slist[:-1] 
    #     s = " ".join(slist)

    if cap:
        s = s[0].upper() + s[1:]
    
    if question:
        s = s + "?"
    
    return s

def sampleString(s):
    wordsIn = s.split(" ")
    wordsOut = []
    for w in wordsIn:
        if w.startswith("["):
            prob = 0.5
            if "]=" in w:
                w, prob = w.split("]=")
                w = w[1:]
                prob = float(prob)
            else:
                w = w[1:-1]
            if not coin(prob):
                continue
            if "/" in w:
                w = choice(w.split("/"))
        for sw in w.split("_"):
            if "|" in sw:
                sw = choice(sw.split("|"))
            wordsOut.append(sw)

    s = " ".join(wordsOut)
    return s

# tra

#fruit|vegetable
#baked

# rooms = {'bathroom': 't', 'kitchen': "k", 'dining room': "l", 'bedroom': "b", 'living room': "l", 'restroom': 'b'}
# places = ['ocean', 'shore', 'sea', 'farm', 'garden', 'restaurant', 'market', 'park', 'town', 'skate park', 'zoo', 
#     'yard', 'harbor', 'store', 'shop', 'train station', 'parking lot', 
#     'street', 'room', 'city', 'library', 'church', 'hotel',  'garage', 'stadium', 'outside', 
#     'hallway', 'office', 'station', 'beach', 'forest', 'airport', 'desert', 
#     'field', 'outfield', 'tunnel', 'coast'] + rooms.keys()

# 
# referRelBlacklist = [("playing", "o")]

def catOf(o):
    oname = o["name"] 
    if "senses" in o and "o_" + oname in o["senses"]:
        return o["senses"]["o_" + oname]
    if oname in vocab["o"]:
        return vocab["o"][oname]["cat"]
    raise Exception("nonvocab object")

# def isStandalone(o):
#     c = catOf(o)
#     # if c is None:
#     #     return False    
#     exception = vocab["o"][oname]["exception"]    
#     catStandalone = catInfo[c]["standalone"]
#     #standalone = (catStandalone and not exception) or (not catStandalone and exception)
#     standalone = catStandalone or exception
#     return standalone

# def sameSimcatOf(attribute, simCats):
#     for sc in vocab["a"][attribute]["simcat"]:
#         if sc in simCats:
#             return True
#     return False

def isAttrObj(obj):
    isMain = vocab["o"][obj]["main"] == 0
    isException = vocab["o"][obj]["exception"]
    return isMain or isException

    # isException = vocab["o"][oname]["exception"]
    # return isMain or isException

def toOp(obj, attr):
    if (attr, obj["name"]) in exceptAttrs:
        return None

    attrOp = None
    if attr in attrOps:
        attrOp = attrOps[attr]

    attrType = typeOf(attr, obj)
    if attrType is not None and attr in attrMultiOps:
        attrOp = attrMultiOps[attr][attrType]

    if attr == "small" and (not isA(obj, "person")):
        attrOp = "large"

    if attrOp is not None: # and statOf(obj["name"], attrOp, p = False) > 0:
        return attrOp
    return None

def attrNotTrivial(attr, obj):
    attrType = typeOf(attr, obj)
    attrs = [a for a in nProb[obj["name"]] if nProb[obj["name"]][a] > args.aLProb \
        and statOf(obj["name"], attr, p = False) > args.aCount and a not in attrSims(attr) # and a != attr 
        and typeOf(a, obj) == attrType] # [attrType]
    return (len(attrs) > 0) or toOp(obj, attr)

def isLikely(attr, obj):
    # nProb check?
    return statOf(obj, attr, p = True) > args.aProb and statOf(obj, attr, p = False) > args.aCount 

# def attrSameType(obj, attribute):
#     t = typeOf(attribute, obj) #vocab["a"][a]["cat"]
#     if t is None:
#         return []
#     sameType = [a for a in vocab["a"] if typeOf(a, None) == t and a != attribute]
#     return sameType

# def attrAlternatives(obj, attribute): # , attributes
#     sameType = attrSameType(obj, attribute)   
#     tooSimilarCats = vocab["a"][attribute]["simcat"]
#     diff = [a for a in sameType if a not in tooSimilar and not sameSimcatOf(a, tooSimilarCats)]
#     return diff 

def attrSims(attribute):
    simAtts = set()
    simAtts.add(attribute)
    simAttsR = vocab["a"][attribute]["sims"]
    for a in simAttsR:
        simAtts.add(a)
    keys = vocab["a"][attribute]["simcats"]
    for key in keys:
        simAttsR = attrSimGroups[key]
        for a in simAttsR:
            simAtts.add(a)
    # if attribute in simAtts:
    #     simAtts.remove(attribute)
    return simAtts       

def attrAlts(obj, attribute):
    t = typeOf(attribute, obj) #vocab["a"][a]["cat"]
    if t is not None:
        good = typeGroups[t]
        good = [a for a in good if isAdj(a) == isAdj(attribute)]
        bad = attrSims(attribute)
        ret = [a for a in good if (a not in bad)] #  and a != attribute
        return ret
    return []

def getColors(instance):
    return [otherA for otherA in otherObj["attributes"] for otherObj in instance["objects"].values() if typeOf(otherA, otherObj) == "color"]

def candidateAttr(instance, obj, attribute, smoothing = True, likely = True, extraObjs = None, nameof = lambda x: x, getAll = False): # likely = True?????
    if extraObjs is not None:
        if len(extraObjs) == 0:
            return None

    countOf = lambda o, a: statOf(o, a, p = False)
    probOf = lambda o, a: nProb[o].get(a, 0) # [t] , t

    # countLOf = lambda olist, a: max([(o, countOf(o, a)) for o in olist], key = lambda x: x[1])
    probLOf = lambda olist, a: max([(o, probOf(nameof(o), a)) for o in olist], key = lambda x: x[1]) # , t
    
    alts = attrAlts(obj, attribute)
    # attrType = typeOf(attr, obj)

    if obj is not None:
        alts = [a for a in alts if a not in obj["attributes"]]
        likelyAlts = [(a, countOf(obj["name"], a), probOf(obj["name"], a)) for a in alts] # , attrType
        likelyAlts = [(a, c) for a, c, pr in likelyAlts if pr > args.aProb and c > args.aCount] # c > 0
    
        likelyAlts =  [(a, c) for a, c in likelyAlts if (obj["name"] != "apple" or a not in ["white", "black", "dark"])]

        t = typeOf(attribute, obj)
        if t == "color":
            allColors = getColors(instance)
            allColors = [otherA for otherA in allColors if otherA != attribute] # not really needed
            factor = 3.25 if (extraObjs is None) else 1.6
            likelyAlts =  [(a, c * (factor if (a in allColors) else 1)) for a, c in likelyAlts]

        if extraObjs is not None:
            likelyAltsNew = []
            for a, c in likelyAlts:
                candObjs = [ea for ea in extraObjs if countOf(ea, a) > args.aCount]
                if len(candObjs) > 0:
                    o, p = probLOf(candObjs, a) # , attrType extraObjs extraObjs
                    # print(o, p, a, c)
                    if p > args.aProb:
                        likelyAltsNew.append(((a, o), c * p))

            likelyAlts = likelyAltsNew
            # likelyAlts = [(a, c * countOf(extraObj, a)) for a, c in likelyAlts if probOf(obj, a, attrType) > args.aProb]

        if len(likelyAlts) > 0:
            if getAll:
                return likelyAlts
            return sample(likelyAlts, smoothing = (extraObjs is None))
        if extraObjs is not None:
            return None

    # if attribute in ["healthy", "unhealthy"]: # ?????????????
    #     likely = False  
    if obj is not None:
        opAttr = toOp(obj, attribute)
        if opAttr is not None:
            return opAttr

    if getAll:
        return [(a, 1) for a in alts]

    return None if likely else choice(alts)
    # return candidate  

# def isMain(o):
#     if o in vocab["o"]:
#         return vocab["o"][o]["main"]
#     return False

def inclusionRate(c1, c2):
    if size(c1) == 0:
        return 0
    isize = length(intersection(xrange(c1), xrange(c2))) * length(intersection(yrange(c1), yrange(c2)))
    inclusionRate = float(isize) / size(c1)
    return inclusionRate

def partOfRate(o1, o2):
    # if (isA(o1, "body part") and isA(o2, "alive")) or \
    #     (isA(o1, "vehicle part") and isA(o2, "vehicle")):
    return inclusionRate(coords(o1), coords(o2))
    # return 0.0

# def objs(c, main = True):
#     objList = []
#     objList += catInfo["o"]["main" if main else "extra"]
#     for s in objCats[c]:
#         objList += objs(s, main)
#     return objList

# def allObjs(c):
#     return objs(c, True) + objs(c, False)

# attTypes = set('color', 'material', 'activity', 'size', 'shape', 'age', 'height', 'length', 'weight', 'tone', 'brightness'
#     'depth', 'texture', 'thickness', 'race', 'company', 'pattern', 'face expression', 'orientation', 'width', 
#     'state', 'gender', 'room', 'liquid', 'sport', 'cleanliness', 'weather', 'fatness', 'realism', 'hardness')

pos2phrase = { # 
    "left": "on the left", # [side]=0.25 of?
    "right": "on the right", # [side]=0.25
    "top": "at the top",
    "bottom": "at the bottom",
    "middle": "in the middle|center"
}

cPoses = {
    "left": "right", 
    "right": "left",
    "top": "bottom",
    "bottom": "top"
} 

def sideOf(pos):
    return ("side" if coin(0.8) else "part") if pos in ["left", "right"] else "part"

def probSideOf(pos):
    return 0 if pos in ["left", "right"] else 0.3

# pos2adj = {
#     "left": "to the left of", # of?
#     "right": "to the right of"
# }

def formsOf(objName, fltr = True):
    sObject = singularOf(objName)
    if fltr and sObject not in existanceObjs:
        sObject = None
    # sObject = sObject if sObject in existanceObjs else None # ?????
    pObject = None if isMass(objName) else pluralOf(objName)
    # if fltr and pObject not in vocab["o"]: # ???????? ???????????????????????????????????????????????
    #     pObject = None
    if fltr and objName == "glass":
        pObject = None
    return sObject, pObject

# def normalizeObj(objname):
    # return singularOf(objname) if isPlural(objname) else objname

# def gramsOf(objname):
#     grams = [objname]
#     if isSingular(objname) or isPlural(objname):
#         grams.append(pluralOf(objname) if isSingular(objname) else singularof(objname))
#     return grams

# def formsOf(objname):
#     return 
# pluralof

def uniqueL(instance, objId, objIds, among):
    if among != []:
        objIds = [oid for oid in among if oid in objIds]
    others = [oid for oid in objIds if oid != objId]
    # other = None
    # if len(objIds) == 2:
    #     other = others[0]
    return len(others) == 0, others

def uniqueO(instance, objId, objName, among = []):
    key = singularOf(objName)
    objIds = instance["name2obj"][key]["objs"]
    return uniqueL(instance, objId, objIds, among)

def uniquePO(instance, objId, objName, prop, among = []):
    key = singularOf(objName)
    objIds = instance["name2obj"][key]["attr2obj"].get(prop, []) # -> prop
    return uniqueL(instance, objId, objIds, among)

def isUnique(instance, objId, objName = None, prop = None):
    # ans = specificAncestors(catOf(obj))
    # if any(a in instance["objectSet"] for a in ans):
    #     return False
    if objName is None:
        objName = instance["objects"][objId]["name"]
    if prop is not None:
        return uniquePO(instance, objId, objName, prop)[0]
    return uniqueO(instance, objId, objName)[0]

def consistent(instance, objId, verifyFunc):
    others = uniqueO(instance, objId, instance["objects"][objId]["name"])[1]
    return all([verifyFunc(instance["objects"][o]) for o in others if o in instance["objects"]])

def sub(obj, cat):
    if isA(obj, cat):
        if catOf(obj) == cat:
            info = vocab["o"][obj["name"]]
            return (not info["noCat"]) and (not info["general"]) 
        return True
    return False

def refcatOf(obj, q = False, a = False):
    return ([None] + refCats(obj, q = q, a = a))[-1]

def refCats(obj, q = False, a = False):
    field = ("aspecific" if a else "qspecific") if q else "specific"
    ans = ancestors(catOf(obj))
    info = vocab["o"][obj["name"]]
    if info["noCat"] or (q and info["general"]):
        ans = ans[:-1]
    ans = [a for a in ans if catInfo[a][field]]
    return ans 

def uniqueCats(instance, objId, q = False):
    obj = instance["objects"][objId]
    ans = refCats(obj, q = q)
    ans = [a for a in ans if uniqueO(instance, objId, a)[0]]
    return ans

def uniqueACats(instance, objId, attr, q = False):
    obj = instance["objects"][objId]
    ans = refCats(obj, q = q, a = True)
    ans = [a for a in ans if uniquePO(instance, objId, a, attr)[0]]
    return ans

    # ans = specificAncestors(catOf(obj))
    # if any(a in instance["objectSet"] for a in ans):
    #     return False

# test with family func? 
def notexists(instance, objname):
    ans = specificAncestors(catn(objname))
    if any(a in instance["objectSet"] for a in ans):
        return False
    # print(objname)
    wideSims = objSims(objname, wide = True) 
    if any(a in instance["objectSet"] for a in wideSims):
        return False
    return not(singularOf(objname) in instance["name2obj"])

# def similarRel(rel1, rel2):
#     relList1 = rel1.split(" ")
#     relList2 = rel2.split(" ")
#     intersection = [w for w in relList1 if w in relList2]
#     return len(intersection) > 0

# edible 
# ref = {
#     "text": ""
#     "prob": num
#     "constraints": {
#         objId: [
#             "attributes": ["attr",...],
#             "pos": ["pos",...]
#             "rels": [relId,...],
#             "same": [("type", objId) ],
#             "name": bool
#         ]
#     }
# }

# add rel if not needed?
# 2 refs
def avg(l):
    if len(l) == 0:
        return 0
    return float(sum(l)) / len(l)

def countOfRel(s, r, o):
    if s in counts["sro"] and r in counts["sro"][s]:
        return counts["sro"][s][r].get(o, 0)
    return 0

def contextScore(instance, o, other):
    objNames = set([obj["name"] for obj in instance["objects"].values() if obj["name"] != other])
    sfreqOf = lambda x: math.sqrt(float(counts["o"][x]))
    sfreqSum = sum([sfreqOf(oname) for oname in objNames])
    weightOf = lambda x: 1.0 if sfreqSum == 0 else (sfreqOf(oname) / sfreqSum)
    contextProbs = [weightOf(oname) * probs["oo1"][oname].get(o, 0) for oname in objNames] # switch order????? oo2?
    score = avg(contextProbs)
    return score

def createAttrsDict(obj):
    typeToAttrs = defaultdict(list)
    for attr in obj["attributes"]:
        attrType = typeOf(attr, obj)
        if attrType is not None:
            typeToAttrs[attrType].append(attr)
    return typeToAttrs

def isMainObj(obj):
    return mainImage(coords(obj)) and not isA(obj, "part") and isWeakExistObj(obj["name"], strong = True) # ??????

def isPronoun(instance, objId):
    obj = instance["objects"][objId]
    return size(coords(obj)) > args.pSize and isA(obj, "person") and uniqueO(instance, objId, "person")[0]

def thisesBool(singular, main):
    if singular:
        prob = coin(0.8) if main else coin(0.6)
        if prob:
            return "this"
        else:
            return "that"
    else:
        if coin(0.95):
            return "these"
        else:
            return "those"

def thises(obj):
    return thisesBool(not isPlural(obj["name"]), isMainObj(obj))

def dPrefix(obj):
    main = isMainObj(obj)
    if main and coin(0.25):
        return thises(obj)
    cond = coin(0.9) or isPlural(obj["name"])
    return "the" if cond else "that"

    # ret = ["the"]
    # if isMainObj(obj):
    #     ret.append(thises(obj["name"]))
    # return ret

def aPrefix(objName):
    ret = en.noun.article(objName).split(" ")[0] # []
    return ret
    # if isMain(obj):
    #     if isSingular(obj):
    #         ret.append("this")
    #     else:
    #         ret.append("these")

def cany(first): # , firstAny
    if first:
        return "any" if coin(0.85) else "" 
    return "" # or firstAny != "any" 

def geta(word):
    if word in vocab["o"]:
        return getaIn(word)
    return aPrefix(word)

def getaIn(objName, aany = False, attr = None, first = True, firstAny = None): # firstAny = None
    name = objName
    if objName is None:
        return None
    # if "name" in objName and objName != ["name tag", "ornament", "ornaments"]:
        # objName = objName["name"]        
    if objName not in vocab["o"]:
        print(objName, "!!geta!!")        
    if attr is not None:
        name = "{attr} {obj}".format(attr = attr, obj = objName)
    if isSingular(objName):
        a = aPrefix(name)
        if aany:
            if firstAny == "any":
                return "" #"any"
            if first:
                return a if coin(0.75) else "any" 
        return a
    if isMass(objName):
        return cany(first) if aany else "" # , firstAny
    return ""

# prefixes = [aPrefix(objName)]
# if aany:
#     prefixes.append(cany(first, firstAny))
# return random.choice(prefixes) # + " "
# "any" if first or firstAny != "any" else ""
#return # "any" if aany and (first or firstAny != "any") else "" # " "

def lastWord(n):
    return n.split(" ")[-1]

def isare(objName):
    ret = "are" if isPlural(objName) else "is" # obj["name"]
    return ret

def wh(obj, where = True, rel = None, subj = None):
    if rel in whatWhereSpec:
        for whword in whatWhereSpec[rel]:
            if obj["name"] in whatWhereSpec[rel][whword]:
                return whword, ("place" if whword == "where" else None)

    whereRel, wherePlaces = False, False
    if rel is not None:
        whereRel = vocab["r"][rel]["where"]
        wherePlaces = vocab["r"][rel]["wherePlaces"]
    person = isA(obj, "person")
    if person or vocab["o"][obj["name"]]["who"]:
        return "who", "person"
    if isA(obj, "animal"):
        return "what animal", "animal"      
    if where:
        if (isA(obj, "place") or (obj["name"] in extraPlaces)) and wherePlaces: # ????
            return "where", "place"
        if subj is not None and isAlist(subj, ["animal", "person"]) and isAlist(obj, ["vehicle", "building"]) and wherePlaces:
            return "where", "place"
        if whereRel:
            return "where", None 
    return "what", None

def thatForm(subj):
    if subj is None:
        return "that"
    if isA(subj, "person"):
        return "who" if coin(0.07) else "that" # 14
    else:
        return "which" if coin(0.07) else "that" # 08

def thatOf(rel, subj, that = None, ithat = False, preRel = None): # lthat
    that = thatForm(subj)
    noThat = vocab["r"][rel]["noThat"]
    relType = vocab["r"][rel]["cat"]
    if relType != "direct":
        return that, True
    if preRel is not None:
        if lastWord(rel) == lastWord(preRel):
            return that, True             
    if noThat:
        return "", False
    if that is not None and that == False:
        return "", False  
    if ithat and rel == "in":
        return ("", False) if coin(0.75) else (that, True)
    if that is not None and that == True:
        return that, True 
    if rel in ["close to"]:
        return (that, True) if coin(0.85) else ("", False)          
    if coin(0.25):
        return that, True
    return "", False

def anRef(n, i):
    return "{pre} {obj}".format(pre = geta(n), obj = annotate(n, i)).strip()

def objRefRet(ref, code):
    return [(ref, code)], ref, None

def objRef(objId, objName, rel, q, loop = False): # , freq = False
    dirCode = [objDirCode(objId, objName)]

    relInfo = vocab["r"][rel]
    objOutName = choice([objName] + getSyms(objName, "o"))
    otherPrefix = loopPrefix(loop)
    aRef = "{pre} {other}{obj}".format(pre = geta(objName), other = otherPrefix, obj = annotate(objOutName, objId)).strip() # anRef(objOutName)
    dirRef = annotate(objName, objId)
    theRef = "the {other}{obj}".format(other = otherPrefix, obj = annotate(objName, objId))

    if rel in prefixSpec:
        for mod in prefixSpec[rel]:
            if objName in prefixSpec[rel][mod]:
                if mod == "a":
                    return objRefRet(aRef, dirCode)
                if mod == "direct" and (not loop):
                    return objRefRet(dirRef, dirCode)
                return objRefRet(theRef, dirCode)

    if rel == "playing with":
        if isAn(objName, "person") or isAn(objName, "animal"):
            return objRefRet(theRef, dirCode) # None

    if rel == "grazing on":
        if isAn(objName, "place"):
            return objRefRet(theRef, dirCode)

    if q and relInfo["questionThe"]:
        return objRefRet(theRef, dirCode)
    if vocab["o"][objName]["the"]:
        return objRefRet(theRef, dirCode)

    if rel in ["to the left of", "to the right of"]:
        return None
    if relInfo["aObjPrefix"]:
        return objRefRet(aRef, dirCode)
    if relInfo["noObjPrefix"] and (not loop):
        return objRefRet(dirRef, dirCode)

    if relInfo["freqBased"] and (not loop):
        l = freqOf("ro", rel, objName)
        if l is None:
            return None
        ref, freq = max(l, key = lambda p: p[1])
        ref = ref.replace(rel + " ", "", 1) #.strip() # .replace(objName, "")
        if freq == 0 or ref.startswith("the"):
            return None
        return objRefRet(annotate(ref, objId), dirCode)

    return None

def waswere(objName):
    ret = "were" if isPlural(objName) else "was" # obj["name"]
    return ret

def live(obj):
    return isAlist(obj, ["alive", "vehicle"]) # or isA(obj, "vehicle")

def liveC(cat):
    return isAc(cat, "alive") or isAc(cat, "vehicle")

def dodoes(objName):
    ret = "do" if isPlural(objName) else "does" # obj["name"]
    return ret

def hashave(objName):
    ret = "have" if isPlural(objName) else "has" # obj["name"]
    return ret

def getSyms(word, t):
    if word not in vocab[t]:
        return []
    return vocab[t][word]["syms"]

def similarRel(rel1, rel2):
    sims1 = ([rel1] + vocab["r"][rel1]["sims"]) if rel1 is not None else []
    sims2 = ([rel2] + vocab["r"][rel2]["sims"]) if rel2 is not None else []
    sims = [s for s in sims1 if s in sims2]
    return len(sims) > 0

def notlikely(rel):
    return False
    # r = rel["rel"]
    # s = instance["objects"][rel["subj"]]["name"]
    # o = instance["objects"][rel["obj"]]["name"]
    # if r not in counts["rs"] or r not in counts["ro"]:
    #     return True
    # return counts["rs"][r].get(s,0) <= 1 and counts["ro"][r].get(o,0) <= 1 # or or and??

def isloop(instance, rel):
    subjName = instance["objects"][rel["subj"]]["name"]
    objName = instance["objects"][rel["obj"]]["name"]
    return (singularOf(subjName) == singularOf(objName))

def loopPrefix(loop):
    return "other " if loop else ""

def bad(instance, rel, loopcheck = True):
    subjName = instance["objects"][rel["subj"]]["name"]
    objName = instance["objects"][rel["obj"]]["name"]
    if rel["rel"] in ["to the left of", "to the right of"]:
        if (not isWeakExistObj(subjName, strong = True)) or (not isWeakExistObj(objName, strong = True)):
            return True
    if rel["rel"] in ["to the left of", "to the right of", "near", "next to"]:
        if objName in tabletop and countOfRel(subjName, "on", objName) > 0:
            return True
        if subjName in tabletop and countOfRel(objName, "on", subjName) > 0:
            return True            
    return notlikely(rel) or (loopcheck and isloop(instance, rel)) or \
        isAn(subjName, "part") or isAn(objName, "part")

# def whereRel(rel):
#     r = rel["rel"]
#     s = instance["objects"][rel["subj"]]["name"]
#     o = instance["objects"][rel["obj"]]["name"]
#     return isAn(o,"place") or rel["rel"] == "at"

def isMultiSubj(instance, rel):
    r = rel["rel"]
    s = instance["objects"][rel["subj"]]
    o = instance["objects"][rel["obj"]]
    oname = o["name"]
    if r in multiRel:
        return True
    if isMainObj(s):
        return False
    if isA(o, "place") or r == "at":
        return True
    if r == "in" and vocab["o"][oname]["inBlacklist"]:
        return True
    if r in ["on", "on top of"] and vocab["o"][oname]["onBlacklist"]:
        return True
    if (r,o) in multiSubj:
        return True
    return False

def isMultiObj(instance, rel):
    r = rel["rel"]
    s = instance["objects"][rel["subj"]]
    o = instance["objects"][rel["obj"]]
    sname = s["name"]

    if r in multiRel:
        return True
    if isMainObj(o):
        return False
    if (s,r) in multiObj:
        return True
    return False

def badVerify(instance, rel):
    r = rel["rel"]
    s = instance["objects"][rel["subj"]]
    o = instance["objects"][rel["obj"]]
    oname = o["name"]

    if isA(o, "place") or rel["rel"] == "at":
        return True
    if rel["rel"] == "in" and vocab["o"][oname]["inBlacklist"]:
        return True
    if rel["rel"] == "on" and vocab["o"][oname]["onBlacklist"] and oname not in onWhitelist:
        return True
    return False

def tooGeneral(ans):
    # relInfo = vocab["r"][rel["rel"]]
    return vocab["o"][ans]["tooGeneral"]
    # return (relInfo["cat"] == "averb" and rel["subj"] == "person")

# def trivialO(rel):
#     relInfo = vocab["r"][rel["rel"]]
#     objInfo = vocab["o"][rel["info"]]
#     return objInfo["tooGeneral"]

# relate
objDirCode = lambda objId, objName: "select: {objName} ({objId})".format(objName = objName, objId = objId)
relObjCode = lambda func, objId, objName, rel, subj: "{func}: {obj},{rel},{so} ({objId})".format( \
    func = func, obj = "_" if objName is None else objName, #+ ","), 
    rel  = rel, so = "_" if subj is None else ("s" if subj else "o"), objId = objId) # ,s
filterByAttrCode = lambda attr, ta: "filter{t}: {a}".format(t = (" " + ta) if ta is not None else "", a = attr)
filterByNotAttrCode = lambda attr, ta: "filter{t}: not({a})".format(t = (" " + ta) if ta is not None else "", a = attr)
orelsCode = lambda sourceId, sourceName, rel, targetId, targetName, subj: \
   [objDirCode(sourceId, sourceName), relObjCode("relate", targetId, targetName, rel, subj)] # code

# def adRefs(refs):
#     ret = [["the {}".format(ref)] for ref in refs]
#     aans = [geta(ref) for ref in refs]
#     if all([a != "" for a in aans]) and random.random() < 0.5:
#         return [["{a} {ref}".format(a = geta(ref), ref = ref)] for ref in refs]
#     return ret

def adRefs(refs):
    ret = ["the {}".format(ref) for ref in refs]
    aans = [geta(ref) for ref in refs]
    if all([a != "" for a in aans]) and (coin(0.5) or (any([vocab["o"][ref]["placeA"] for ref in refs]))):
        return ["{a} {ref}".format(a = geta(ref), ref = ref) for ref in refs]
    return ret

def inImg(shown = False, oIs = None):
    if shown:
        val = random.random()
        if val < 0.13:
            return "that_{oIs}_shown_in_the_picture|image".format(oIs = oIs)
        elif val < 0.4:
            return "in_the_picture|image"
        elif val < 0.47:
            return "that_{oIs}_shown_in_this_picture|image".format(oIs = oIs)
        elif val < 0.6:
            return "in_this_picture|image"
        elif val < 0.63:
            return "that_{oIs}_presented_in_this|the_picture|image".format(oIs = oIs)
        elif val < 0.69:
            return "that_{oIs}_shown|presented_in_the|this_photo".format(oIs = oIs)
        elif val < 0.8:
            return "in_the|this_photo"            
        elif val < 0.87:
            return "that_{oIs}_shown|presented_in_the|this_scene|photograph".format(oIs = oIs)
        else:
            return "in_the|this_scene|photograph"
    else:
        val = random.random()
        if val < 0.4:
            return "in_the_picture|image"
        elif val < 0.6:
            return "in_this_picture|image"
        elif val < 0.8:
            return "in_the|this_photo"
        else:
            return "in_the|this_scene|photograph"

        # if obj is not None and instance is None:
        #     isFood = isA(obj, "food")
        #     for rel in obj["outRels"]:
        #         if rel["rel"] in ["on", "above"]:
        #             if rel["obj"] == "plate" and isFood:
        #                 ret += "\on_the_plate"
        #             if rel["obj"] == "pizza":
        #                 ret += "\on_the_pizza"
        #             if rel["obj"] == "table" and obj["name"] == "tablecloth":
        #                 ret += "\on_the_table"
        #             if rel["obj"] in ["sofa", "bed", "couch"] and obj["name"] == "pillow"
        # return ret

def getObjCode(objId, obj, objName, attr = None, nt = False, clean = False, attrType = None):
    code = {"dobject": {"code": [objDirCode(objId, objName)]}}
    if attrType is None:
        attrType = typeOf(attr, obj)
    if attr is not None:
        filterFunc = filterByNotAttrCode if nt else filterByAttrCode
        code["dobject"]["code"].append(filterFunc(attr, attrType))
    if clean:
        return code["dobject"]["code"]
    return code

def addAttrFilter(code, attr, nt = False, attrType = None)
    if attrType is None:
        attrType = typeOf(attr, obj)
    filterFunc = filterByNotAttrCode if nt else filterByAttrCode
    code.append(filterFunc(attr, attrType))
    return code

def definedSubjAlt(instance, objs, subjo, subj, r, o, cat = None):
    return None
    # inSubjs = instance["ro"][r][singularOf(o)].keys() 
    # simsSubj = objSims(subj)
    # catCond = lambda s: True if cat is None else isAn(s, cat)    
    # cond = lambda s, sj: (singularOf(s) not in inSubjs) and (s not in simsSubj) \
    #     and catCond(s) and (mod(s) == mod(subj)) and (s not in blacklistObjs) \
    #     and singularOf(s) != singularOf(o) and (not overlapping(coords(sj), coords(subjo))) \
    #     and (s not in tooCommon) and (not isFamily(s, subj)) # need isFamily check????

    # candidates = []
    
    # for sid in objs:
    #     sj = instance["objects"][sid]
    #     s = sj["name"]
    #     c = countOfRel(s, r, o)
    #     if c > 10 and cond(s, sj):
    #         candidates.append(sid) # (sid, c)
    
    # chosen = choice(candidates) # sample True ????????????? , smoothing = False
    # return chosen

def definedObjAlt(instance, objs, objo, s, r, obj, cat = None):
    return None
    # inObjs = instance["sr"][singularOf(s)][r].keys()  
    # simsObj = objSims(obj)
    # catCond = lambda o: True if cat is None else isAn(o, cat)
    # cond = lambda o, oj: (singularOf(o) not in inObjs) and (o not in simsObj) \
    #     and catCond(o) and (mod(o) == mod(obj)) and (o not in blacklistObjs) \
    #     and (singularOf(s) != singularOf(o)) and (not overlapping(coords(oj), coords(objo))) \
    #     and (o not in tooCommon) and (not isFamily(o, obj))  # need isFamily check????

    # candidates = []
    
    # for oid in objs:
    #     oj = instance["objects"][oid]
    #     o = oj["name"]
    #     c = countOfRel(s, r, o)
    #     if c > 10 and cond(o, oj):
    #         candidates.append(oid) # (oid, c)
    
    # chosen = choice(candidates) # sample True ????????????? , smoothing = False
    # return chosen

# return id if exists?
def undefinedSubjAlt(instance, subj, r, o, cat = None, getAll = False):    
    inSubjs = instance["ro"][r][singularOf(o)].keys() # [] # 
    simsSubj = objSims(subj)
    catCond = lambda s: True if cat is None else isAn(s, cat)    
    lrCond = lambda s: isWeakExistObj(s, strong = True) if r in ["to the left of", "to the right of"] else True
    cond = lambda s: (singularOf(s) not in inSubjs) and (s not in simsSubj) \
        and catCond(s) and (mod(s) == mod(subj)) and (s not in blacklistObjs) \
        and (singularOf(s) != singularOf(o)) and (s not in tooCommon) \
        and (not isFamily(s, subj)) and lrCond(s)

    likelySubjs = [(s,c) for s,c in tops["or2s"][o].get(r, []) if \
        (c > 10 and isWeakExistObj(s) and cond(s))][:10] # ??????
    leastLikely = likelySubjs[-1][1] if len(likelySubjs) > 0 else 0
    similarSubjs = objAlts(subj)
    similarSubjs = [(s, countOfRel(s, r, o) + (float(leastLikely) / 2)) for s in similarSubjs if cond(s)]
    
    subjs = likelySubjs + similarSubjs
    subjs = [(s, c * (contextScore(instance, s, o) + 0.01)) for s, c in subjs]

    if getAll:
        return subjs

    chosen = sample(subjs, smoothing = True) # True/False ????????????????????????????????????????????????????????????????? likelySubjs
    # chosenB = choice(similarSubjs)

    # if chosenA is None or chosenB is None:
    #     return chosenA or chosenB
    return chosen #chosenA if random.random() < 0.75 else chosenB

# Add nonexistent or ops!
def undefinedObjAlt(instance, s, r, obj, cat = None, getAll = False):    
    inObjs = instance["sr"][singularOf(s)][r].keys() # [] # 
    simsObj = objSims(obj)
    catCond = lambda o: True if cat is None else isAn(o, cat)
    lrCond = lambda o: isWeakExistObj(o, strong = True) if r in ["to the left of", "to the right of"] else True
    cond = lambda o: (singularOf(o) not in inObjs) and (o not in simsObj) \
        and catCond(o) and (mod(o) == mod(obj)) and (o not in blacklistObjs) \
        and (singularOf(s) != singularOf(o)) and (o not in tooCommon) \
        and (not isFamily(o, obj)) and lrCond(o)

    likelyObjs = [(o,c) for o,c in tops["sr2o"][s].get(r, []) if \
        (c > 10 and isWeakExistObj(o) and cond(o))][:10] # ??????
    leastLikely = likelyObjs[-1][1] if len(likelyObjs) > 0 else 0
    similarObjs = objAlts(obj)
    similarObjs = [(o, countOfRel(s, r, o) + (float(leastLikely) / 2)) for o in similarObjs if cond(o)]
    
    objs = likelyObjs + similarObjs 
    objs = [(o, c * (contextScore(instance, o, s) + 0.01)) for o, c in objs]

    objs = [(o, c) for o, c in objs if o not in trivial]

    if getAll:
        return objs # multiSample(choices, num, smoothing = False)

    chosen = sample(objs, smoothing = True) # True/False ???????????????????????????????????????????????????????????????????? likelyObjs chosenA
    # chosenB = choice(similarObjs)

    # if chosenA is None or chosenB is None:
    #     return chosenA or chosenB
    return chosen # chosenA if random.random() < 0.75 else chosenB

# TODO: change to weightedChoice
def indirectRef(instance, objId, short, that, ithat, blackAType, blackObjIds, blackRS, blackRO, simple, cat = None, onlyPrefix = False):
    if cat is not None:
        catC, catN, catIs = cat
        # catP = (catIs == "are")
        # catC, catN, catP = cat

    sims = []
    for oid in blackObjIds:
        obj = instance["objects"][oid]
        # objSims =  # ??? wide?????
        sims += list(objSims(obj["name"])) # ??? wide?????

    # names = [instance["objects"][oid]["name"] for oid in blackObjIds]
    coordSet = [coords(instance["objects"][oid]) for oid in blackObjIds] 

    cond = lambda xid, x: (xid not in blackObjIds) and x["name"] not in sims \
        and not (any([overlapping(coords(x), c) for c in coordSet])) #\
        # and not (any([isFamily(o["name"], n) for n in names]))
    badIn = lambda rel: rel["rel"] in ["on top of", "on"] \
        and isAlist(instance["objects"][rel["subj"]], ["food", "sauce"]) \
        and isA(instance["objects"][rel["obj"]], "food")

    obj = instance["objects"][objId]    
    objName = obj["name"] if cat is None else catN
    objCode = objName if cat is None else catC
    objIs = isare(objName) if cat is None else catIs

    if cat is None:
        objLooks = "look" if isPlural(objName) else "looks"
    else:
        objLooks = "looks" if catIs == "is" else "look"

    refs = []
    # if simple is None:
        # simple = (random.random() < 0.2)
    # objIs = "" if simple else 
    # synonym for attr or obj??

    attrRefs = []
    matRefs = []
    colorRefs = []
    notRefs = []
    c2Refs = []
    for attr in obj["attributes"]:
        
        attrType = typeOf(attr, obj)
        if attr == "black and white":
            attrType = "color"

        if attrType not in blackAType and isUnique(instance, objId, objName = objCode, prop = attr):
            code = getObjCode(objId, obj, objCode, attr = attr, clean = True)
            c = freqOf("oa", objName, attr)
            if c is None:
                c = 0
            if c > 300:
                attrRef = "the {a} {o}".format(a = annotate(attr, objId), o = annotate(objName, objId))
                attrRefs.append(((attrRef, code), c))

            if attrType == "material":
                matRef = "the {o} [that_{ois}]=0.3 made [out]=0.03 of {m}".format(o = annotate(objName, objId), 
                    ois = objIs, m = annotate(attr, objId))
                matRefs.append((matRef, code))

            if attrType in attrRefTypes:
                ois = objLooks if ((attrType not in ["pose", "activity", "sportActivity"]) and coin(0.85)) else objIs
                colorRef = "the {o} that {ois} {a}".format(o = annotate(objName, objId), ois = ois, a = annotate(attr, objId))
                colorRefs.append((colorRef, code))

            aop = toOp(obj, attr)
            if aop is not None:
                codeNot = getObjCode(objId, obj, objCode, attr = attr, nt = True, clean = True)
                notRef = "the {o} that {ois} not {a}".format(o = annotate(objName, objId), ois = objIs, a = annotate(attr, objId))
                notRefs.append((notRef, codeNot))

    if "color" not in blackAType:
        objColors = [otherAttr for otherAttr in obj["attributes"] if typeOf(otherAttr, obj) == "color"]
        for c1 in objColors:
            for c2 in objColors:
                if c1 == c2: 
                    continue
                ois = objLooks if coin(0.85) else objIs
                colorRef = "the {o} that {ois} {c1} and {c2}".format(o = annotate(objName, objId), ois = ois, 
                    c1 = annotate(c1, objId), c2 = annotate(c2, objId))
                colorRefs.append((colorRef, code))  

    attrRef = sample(attrRefs, smoothing = False) # if len(attrRefs) > 0 else None # smoothing?
    refs.append((attrRef, 2))

    if not onlyPrefix:

        matRef = choice(matRefs)
        refs.append((matRef, 2.5))

        colorRef = choice(colorRefs)
        refs.append((colorRef, 0.4))    

        notRef = choice(notRefs)
        refs.append((notRef, 0.7))

        c2Ref = choice(c2Refs)
        refs.append((c2Ref, 0.3))    
        # add unique check?????

        outRelRefs = []
        lroutRelRefs = []
        aoutRelRefs = []
        alroutRelRefs = [] 
        coutRelRefs = []
        clroutRelRefs = []        
        for relId in obj["outRels"]:
            rel = obj["outRels"][relId]
            if bad(instance, rel, loopcheck = False):
                continue

            sId = rel["subj"]
            oId = rel["obj"]
            s = instance["objects"][sId]
            o = instance["objects"][oId]
            sName = s["name"] if cat is None else catN
            sCode = sName if cat is None else catC
            oName = o["name"]
            loop = isloop(instance, rel)

            if cond(oId, o) and (rel["rel"] != blackRO) and (not similarRel(rel["rel"], blackRO)) \
                    and isUnique(instance, objId, objName = objCode, prop = "{}_{}".format(rel["rel"], oName)): # (rel["obj"] not in blackObjIds) # ??????
                shouldS = shouldBeSimple(rel, s) if cat is None else shouldBeSimpleC(rel, catC)
                toS = toSimple(rel["rel"], sName) if cat is None else toSimpleP(rel["rel"], personOf(catIs))
                sIs = isare(sName) if cat is None else catIs #("are" if catP else "is")

                relSimple = simple or shouldS
                thatWord, thatB = thatOf(rel["rel"], subj = s, that = True if that else (False if short else None), ithat = ithat, preRel = blackRS) # that(rel, that = None)
                subjIs = "" if (relSimple or (not thatB)) else sIs
                relName = toS if relSimple else rel["rel"]
                ref = objRef(oId, oName, rel["rel"], q = False, loop = loop)
                if ref is not None and loop: continue
                otherPrefix = loopPrefix(loop)
                oRef = "the {other}{o}".format(o = annotate(oName, oId), other = otherPrefix) if ref is None else ref[0][0][0]

                oCode = oName
                if isPronoun(instance, oId):
                    if coin(0.3 if oName == "person" else 0.18):
                        if loop: continue
                        p = pronounOf(o, person = "obj")
                        if p is not None:
                            oCode, oRef = p

                code = orelsCode(oId, oCode, rel["rel"], sId, sCode, True)
                if relName == "with" and (sName, oName) in withPhrases:
                    if loop: continue
                    outRelRef = "the {obj} {subj}".format(subj = annotate(sName, sId), obj = annotate(oName, oId))
                else:
                    outRelRef = "the {subj} {that} {sIs} {rel} {obj}".format( \
                        subj = annotate(sName, sId), that = thatWord, sIs = subjIs, rel = relName, obj = oRef)

                outList = lroutRelRefs if rel["rel"] in ["to the left of", "to the right of"] else outRelRefs
                outList.append(((outRelRef, code), not thatB))
                
                if not (relName == "with" and (sName, oName) in withPhrases):
                    for attr in obj["attributes"]:
                        if attrType not in blackAType:
                            c = freqOf("oa", sName, attr)
                            if c is None:
                                c = 0
                            if c > 300:
                                code = orelsCode(oId, oCode, rel["rel"], sId, sCode, True)
                                code = addAttrFilter(code, attr)

                                aoutRelRef = "the {attr} {subj} {that} {sIs} {rel} {obj}".format( \
                                    attr = annotate(attr, sId), subj = annotate(sName, sId), that = thatWord, 
                                    sIs = subjIs, rel = relName, obj = oRef)

                                aoutList = alroutRelRefs if rel["rel"] in ["to the left of", "to the right of"] else aoutRelRefs
                                aoutList.append(((aoutRelRef, code), not thatB))

                            if attrType == "color" and isAlist(s, ["object", "thing"]) and (not isPlural(sName)):
                                newName = "object|thing" if isA(s, "object") else "thing"
                                code = orelsCode(oId, oCode, rel["rel"], sId, sCode, True)
                                code = addAttrFilter(code, attr)

                                coutRelRef = "the {attr} {subj} {that} {sIs} {rel} {obj}".format( \
                                    attr = annotate(attr, sId), subj = annotate(newName, sId), that = thatWord, 
                                    sIs = subjIs, rel = relName, obj = oRef)

                                coutList = clroutRelRefs if rel["rel"] in ["to the left of", "to the right of"] else coutRelRefs
                                coutList.append(((coutRelRef, code), not thatB))   

        lroutRelRef = choiceSelect(lroutRelRefs) # choose
        outRelRef = choiceSelect(outRelRefs, only = short) # that = True if that False/None
        alroutRelRef = choiceSelect(alroutRelRefs) # choose
        aoutRelRef = choiceSelect(aoutRelRefs, only = short) # that = True if that False/None
        clroutRelRef = choiceSelect(clroutRelRefs) # choose
        coutRelRef = choiceSelect(coutRelRefs, only = short) # that = True if that False/None

        refs.append((outRelRef, 3))
        refs.append((lroutRelRef, 0.75))
        refs.append((aoutRelRef, 0.4))
        refs.append((alroutRelRef, 0.1))
        refs.append((coutRelRef, 0.24))
        refs.append((clroutRelRef, 0.06))

        if not short:
            posRefs = []
            img = "of_the_image|photo|picture"
            if "pos" in obj and isWeakExistObj(obj["name"], strong = True) and (obj["name"] not in tabletop): # , strong = True
                for pos in obj["pos"]:
                    posType = "hposition" if pos in ["left", "right"] else "vposition"
                    if isUnique(instance, objId, objName = objCode, prop = pos):
                        posRef = "the {obj} [that_{ois}]=0.15 {pos} [{side}]=0.3 [{img}]=0.3".format(obj = annotate(objName, objId), 
                            pos = pos2phrase[pos], ois = objIs, side = sideOf(pos), img = img)
                        code = getObjCode(objId, obj, objCode, attr = pos, clean = True, attrType = posType)
                        posRefs.append((posRef, code))

            posRef = choice(posRefs)
            refs.append((posRef, 0.75))

            inRelRefs = []
            lrinRelRefs = []
            pRelRefs = []
            for relId in obj["inRels"]:
                rel = obj["inRels"][relId]
                if bad(instance, rel):
                    continue

                sId = rel["subj"]
                oId = rel["obj"]
                s = instance["objects"][sId]
                o = instance["objects"][oId]
                sName = s["name"]
                oName = o["name"] if cat is None else catN
                oCode = oName if cat is None else catC
                relInfo = vocab["r"][rel["rel"]]

                if cond(sId, s) and (rel["rel"] != blackRS) and (not similarRel(rel["rel"], blackRS)) \
                        and isUnique(instance, objId, objName = objCode, prop = "{}_{}".format(sName, rel["rel"])): # ????????????? (rel["subj"] not in blackObjIds)
                    if not relInfo.get("notobj", False) and not badIn(rel):
                        relSimple = simple or shouldBeSimple(rel, s)
                        subjIs = "" if relSimple else isare(sName)
                        relName = toSimple(rel["rel"], sName) if relSimple else rel["rel"]
                        if relInfo["of"]:
                            relName += " of"
                        if relInfo["by"]:
                            relName = " ".join(relName.split(" ")[:-1]) + " by"
                        sOut = sCode = sName
                        the = "the "
                        if isPronoun(instance, sId):
                            if coin(0.7 if sName == "person" else 0.4):
                                p = pronounOf(s, person = "subj")
                                if p is not None:
                                    sCode, sOut = p
                                    the = ""

                        code = orelsCode(sId, sCode, rel["rel"], oId, oCode, False)
                        inRelRef = "the {obj} [that]=0.28 {the}{subj} {sIs} {rel}".format( # ???
                            obj = annotate(oName, oId), the = the, subj = annotate(sOut, sId), sIs = subjIs, rel = relName)

                        ref = (inRelRef, code)
                        weight = 1

                        islr = rel["rel"] in ["to the left of", "to the right of"]
                        inList = lrinRelRefs if islr else inRelRefs
                        weight = 2.5 if (isA(s, "person") and relInfo["cat"] == "averb") else 1
                        if islr:
                            weight = 0.25
                        inList.append((ref, weight))

                    passiveRel = relInfo["passive"]
                    if passiveRel is not None:
                        # shouldS = shouldBeSimple(rel, s) if cat is None else shouldBeSimpleC(rel, catC)
                        # toS = toSimple(rel["rel"], sName) if cat is None else toSimpleP(rel["rel"], personOf(catIs))
                        oIs = isare(oName) if cat is None else catIs #("are" if catP else "is")
                        # relSimple = simple or shouldS
                        # thatWord, thatB = thatOf(rel["rel"], subj = s, that = True if that else (False if short else None), ithat = ithat, preRel = blackRS) # that(rel, that = None)
                        
                        # objIs = "" if (relSimple or (not thatB)) else oIs
                        # passiveRelName = toS if relSimple else passiveRel
                        # ref = objRef(sId, sName, passiveRel, q = False)
                        sRef = "the {}".format(sName) # if ref is None else ref[0][0][0]

                        sCode = sName
                        if isPronoun(instance, oId):
                            if coin(0.3 if sName == "person" else 0.18):
                                p = pronounOf(s, person = "obj")
                                if p is not None:
                                    sCode, sRef = p

                        code = orelsCode(sId, sCode, rel["rel"], oId, oCode, True)

                        if coin(0.75):
                            pRelRef = "the {subj} that {oIs} [being]=0.05 {rel} {obj}".format( \
                                subj = annotate(oName, oId), oIs = oIs, rel = passiveRel, obj = annotate(sRef, sId)) # Name objIs
                        else:
                            pRelRef = "the {subj} {rel} {obj}".format( \
                                subj = annotate(oName, oId), oIs = oIs, rel = passiveRel, obj = annotate(sRef, sId)) # Name objIs

                        weight = 0.09 if isAlist(s, ["person", "animal"]) else 1
                        pRelRefs.append(((pRelRef, code), weight))
                        # if : else:
                        #     pRelRefs.append(((pRelRef, code), 1)) # not thatB

            lrinRelRef = choice(lrinRelRefs)
            inRelRef = choice(inRelRefs) # that = True if that False/None
            pRelRef = choice(pRelRefs)

            # weight = 3 if 
            # if  pRelRef is not None:
            #     weight = 0.75
            if inRelRef is not None:
                refs.append(inRelRef) # ((1 if pRelRef is None else 0.75) 0.75
            if lrinRelRef is not None:
                refs.append(lrinRelRef)
            if pRelRef is not None:
                refs.append(pRelRef) # , 1 0.75
            # if "color" not in blackAType: todo???

    return sample([(r,c) for r,c in refs if r is not None])

#this|shown|pictured|presented = 0.42 0.42 0.08 0.08
def definedRef(instance, objId, direct, short = False, answer = False, that = False, ithat = False, simple = False, # addShort = False, 
    onlyPrefix = False, blackAType = [], blackObjIds = [], blackRS = None, blackRO = None, isSubj = True): # simple = None? # inImg = True, of = True, 
    obj = instance["objects"][objId]
    objName = obj["name"]
    objIs = isare(objName)
    unique = isUnique(instance, objId)
    # prefixes = dPrefixes(obj)
    # prefix = random.choice(prefixes)
    prefix = dPrefix(obj)
    name = choice([objName] + getSyms(objName, "o"))
    name = annotate(name, objId)
    stheRef = "the {}".format(name)
    theRef = stheRef

    updated = False
    if blackRS is not None and blackRS in ops:
        blackRO = ops[blackRS]
        updated = True
    if not updated and (blackRO is not None) and (blackRO in ops):
        blackRS = ops[blackRO] 

    pronoun = None
    if isPronoun(instance, objId):
        p = None
        if objName == "person":
            if coin(0.75): #:
                p = pronounOf(obj, person = "subj" if isSubj else "obj")
        else:
            if isSubj and coin(0.4): #:
                p = pronounOf(obj, person = "subj")
            if (not isSubj) and coin(0.22): #:
                p = pronounOf(obj, person = "obj")
        
        if p is not None:
            pCode, pRef = p
            pronoun = (annotate(pRef, objId), [objDirCode(objId, pCode)])

    ref = {"ref": ([], stheRef, pronoun), "the": ([], stheRef, pronoun)} # ref = {"ref": ([], theRef), "the": ([], theRef)} # , "this": []
    
    if (not direct) and (not noSuffix) and coin(0.04):
        theRef += " {}".format(inImg(shown = not short, oIs = objIs))
    
    objCode = [objDirCode(objId, objName)]
    if unique or answer: # or addShort:
        ref["ref"] = ([("{} {}".format(prefix, name), objCode)], stheRef, pronoun) # .append
        ref["the"] = ([(theRef, objCode)], stheRef, pronoun) # .append
        # ref["this"].append(("{} {}".format(thises(name), name), objCode))

    if "of" in obj and obj["of"] in instance["objects"] and not noSuffix: # TODO: synonyms for that case???
        otherId = obj["of"]
        other = instance["objects"][otherId]
        otherName = other["name"]
        l = freqOf("of", otherName, objName) 
        if l is not None:
            ofName, freq = max(l, key = lambda p: p[1])
            ofName = annotate(ofName, objId)
        else:
            ofName = "{obj} of the {other}".format(other = annotate(otherName, otherId), obj = annotate(objName, objId))
            freq = 101 
        count = counts["rc"]["of"].get("{obj}_{other}".format(obj = objName, other = otherName), 0)

        if isA(obj, "body part") or obj["name"] in ["hair", "fur", "feathers"]:
            endS = "" if otherName.endswith("s") else "s"
            ofName = "{other}'{s}{cid} {obj}".format(other = otherName, s = endS, obj = annotate(objName, objId), cid = toAnn(otherId))

        ofName = "the {}".format(ofName)
        outCode = otherName
        if isPronoun(instance, otherId):
            if coin(0.75 if objName == "person" else 0.4):
                p = pronounOf(other, person = "of")
                if p is not None:
                    outCode, his = p
                    ofName = "{his} {obj}".format(his = his, obj = objName)

        ofCode = orelsCode(otherId, outCode, "of", objId, objName, True)

        if (obj["strongOf"] or freq > 100 or count > 100) and (singularOf(objName) != singularOf(otherName)):
            if coin(0.35):
                ref["ref"] = ([(ofName, ofCode)], stheRef, pronoun) #.append((ofName, ofCode)) 
                ref["the"] = ([(ofName, ofCode)], stheRef, pronoun) #.append((ofName, ofCode))

        # if isA(obj, "part"):
        #     ref["ref"] = ([(ofName, ofCode)], stheRef, pronoun)
        #     ref["the"] = ([(ofName, ofCode)], stheRef, pronoun)

    if (not direct) or onlyPrefix:
        nonDirectRef = indirectRef(instance, objId, short = short, that = that,
            ithat = ithat, blackAType = blackAType, blackObjIds = blackObjIds,
            blackRS = blackRS, blackRO = blackRO, simple = simple, onlyPrefix = onlyPrefix)

        if (nonDirectRef is not None):
            # if addShort:
            #     ref["ref"][0].append(nonDirectRef)
            #     ref["the"][0].append(nonDirectRef)            
            if (not unique) or coin(0.5): #  el and (nonDirectRef is not None)
                ref["ref"] = ([nonDirectRef], stheRef, pronoun)
                ref["the"] = ([nonDirectRef], stheRef, pronoun)

        cat = refcatOf(obj) 
        if unique and (cat is not None):
            catInfo = catNormalize(obj, cat)
            catInfo = cat, catInfo[0], catInfo[1]
            # catPlural(cat) if isPlural(obj["name"]) else (cat, cat, False) # ????? catnormalize??????
            catRef = indirectRef(instance, objId, short = short, that = that,
                ithat = ithat, blackAType = blackAType, blackObjIds = blackObjIds,
                blackRS = blackRS, blackRO = blackRO, simple = simple, cat = catInfo, onlyPrefix = onlyPrefix)        

            if catRef is not None:
                ref["ref"][0].append(catRef)
                ref["the"][0].append(catRef)

    return ref

def pronounOf(obj, person = "subj"):
    retDict = {
        "it": {"subj": "it", "obj": "it", "of": "its"},
        "she": {"subj": "she", "obj": "her", "of": "her"},
        "he": {"subj": "he", "obj": "him", "of": "his"},
        "they": {"subj": "they", "obj": "them", "of": "their"},
    }
    objName = obj["name"] 
    singular = not isPlural(objName)
    hasGender = ("gender" in obj["mAttributes"])
    isPerson = isA(obj, "person")
    isFemale = False
    if hasGender:
        isFemale = (obj["mAttributes"]["gender"] == "female")
    if singular:
        if hasGender:
            ret = "she" if isFemale else "he"
        elif isPerson:
            return ("person", "the_person") if person == "subj" else None # s!he
        else:
            ret = "it"
    else:
        ret = "they"
    return ret, retDict[ret][person]

stativeList = ["contain", "belong", "have"]

def toSimpleP(verb, person):
    ignore = ["meeting", "balding"]

    wordsIn = verb.split(" ")
    wordsOut = []
    for v in wordsIn:
        # word = []
        # subwordlist = v.split("-")
        # for s in subwordlist:
        if (v.endswith("ing") or v in stativeList) and v not in ignore:
            try:
                v = en.verb.present(v, person = person, negate = False)
            except:
                pass
                # word.append(newS)
            # else:
                # word.append(s)

        # word = "-".join(word)
        wordsOut.append(v)
    ret = " ".join(wordsOut)
    return ret

def personOf(isr):
    return "3" if isr == "is" else "plural"

def toSimple(verb, objName):
    return toSimpleP(verb, personOf(isare(objName))) # isPlural(objName)

def toBasic(verb):
    return toSimpleP(verb, "plural")

def shouldBeSimple(rel, obj):
    return vocab["r"][rel["rel"]]["cat"] == "averb" and \
        (rel["rel"] in stativeList or coin(0.14 if live(obj) else 0.18)) # 08

def shouldBeSimpleC(rel, cat):
    return vocab["r"][rel["rel"]]["cat"] == "averb" and \
        (rel["rel"] in stativeList or coin(0.14 if liveC(cat) else 0.18)) # 08 (not liveC(cat)) or random.random() < 0.16)

# def newRef(objId, name, text, isName, isCont, thatCont, unique, others, prob):
#     newRef = {
#         "text": text,
#         # "definition"
#         "objId": objId,
#         "prob": prob,
#         "name": name,
#         "constraints": {
#             "objs": {objId: {"attributes": [], "pos": [], "same": [], "name": isName}},
#             "rels": {} # "rels": [], 
#         } 
#         "directCont": isCont, "thatCont": thatCont, 
#         "unique": unique, "others": others,
#         "prefix": None
#     }
#     return newRef

# def adjRefs(instance, objName, objId, isName, defined, nonAttr):
#     obj = instance[objId]
#     refs = []
#     prefixes = dPrefixes(obj) if defined else aPrefixes(obj)
#     for p in prefixes:
#         if nonAttr:
#             cont = p not in ["this", "these"]
#             uniqueObj, others = uniqueO(instance, objId, objName, among = [])
#             text = "{prefix} {obj}".format(prefix = p, obj = objName)
#             prob = 1.0 
#             ref = newRef(objId, objName, text, isName, isCont = cont, thatCont = cont, 
#                 unique = uniqueObj, others = others, prob = prob)
#             refs.append(ref)

#         attrList = vocab["a"][attr]["syms"] + [attr]
#         if vocab["a"][attr]["adjForm"] != "":
#             attrList.append(vocab["a"][attr]["adjForm"])
#         attrText = "|".join(["({})".format(a) for a in attrList])

#         for attr in obj["attributes"]:
#             common = True
#             prefix = vocab["a"][attr]["isPrefix"]
#             prior = 0.5 if uniqueObj else 1.0
#             unique, others = uniqueAO(instance, objId, objName, attr, among = [])
#             if args.stats > 0:
#                 common = pf.search(pf.Corpus.AMERICAN_ENGLISH, "{attr} {obj}".format(attr = attr, obj = objName)).phrases[0].match_count > args.stats:
#             if prefix and common:
#                 text = "{prefix} {attr} {obj}".format(prefix = p, attr = attrText, obj = objName)
#                 prob = 1.0 * prior
#                 ref = newRef(objId, objName, text, isName, isCont = cont, thatCont = cont, 
#                     unique = unique, others = others, prob = prob)
#                 ref["constraints"]["objs"][objId]["attributes"].append(attr)
#                 refs.append(ref)

#             # test valid?
#             if (p == "the" and vocab["a"][attr]["isAdj"]) or 
#                 ((p not in ["this", "these"]) and (not prefix)): # (typeOf(attr, obj) == "material")
#                 if vocab["a"][attr]["adjForm"] != "":
#                     attrList = vocab["a"][attr]["syms"] + [vocab["a"][attr]["adjForm"]]
#                     attrText = "|".join(["({})".format(a) for a in attrList])
#                 if typeOf(attr, obj) == "material":
#                     text = "{prefix} {obj} that {isr} made [out]=0.03 of {attr}".format(prefix = p, attr = attrText, obj = objName, isr = isare(objName))
#                 else:
#                     text = "{prefix} {obj} that {isr} {attr}".format(prefix = p, attr = attrText, obj = objName, isr = isare(objName))
#                 prob = (0.2 if prefix else 1.0) * prior
#                 ref = newRef(objId, objName, text, isName, isCont = False, thatCont = False, 
#                     unique = unique, others = others, prob = prob)
#                 ref["constraints"]["objs"][objId]["attributes"].append(attr)
#                 refs.append(ref)

#             simpleAttr = toSimple(attr, objName)
#             hasSimple = (rel != simpleAttr)
            
#             if hasSimple and (p not in ["this", "these"]):
#                 if attr in ["sitting","lying"]
#                     simpleAttr = "({a1})|({a2}-down)|({a3} down)".format(a1 = simpleAttr, a2 = simpleAttr, a3 = simpleAttr)
                
#                 text = "{prefix} {obj} that {attr}".format(prefix = p, attr = simpleAttr, obj = objName, isr = isare(objName))
#                 prob = prior
#                 ref = newRef(objId, objName, text, isName, isCont = False, thatCont = False, 
#                     unique = unique, others = others, prob = prob)
#                 ref["constraints"]["objs"][objId]["attributes"].append(attr)
#                 refs.append(ref)                   
    
#     return refs

# #if defined: # TODO!!!!! ????????
# def posRefs(instance, refs):
#     newRefs = []
#     for ref in refs:
#         objId = ref["objId"]
#         obj = instance[objId]
#         prior = 0.3 if ref["unique"] else 1.0
#         #if ref["unique"] 
#         for pos in obj["pos"]:
#             if ref["directCont"]:
#                 newRef1 = copy.deepcopy(ref)
#                 newRef1["text"] += " {pos}".format(pos2phrase[pos])
#                 newRef1["prob"] *= prior # 0.6 
#                 newRef1["constraints"]["objs"][objId]["pos"].append(pos)
#                 newRef1["directCont"] = False
#                 newRef1["unique"], newRef1["others"] = uniqueAO(instance, objId, newRef1["name"], pos, among = newRef1["others"])
#                 newRefs.append(newRef1)  
            
#             if ref["thatCont"]:
#                 newRef2 = copy.deepcopy(ref)
#                 newRef2["text"] += " that {isr} {pos}".format(isr = isare(newRef2["name"]), pos = pos2phrase[pos])
#                 newRef2["prob"] *= prior #(0.3 if ref["unique"] else 1.0) # 0.4
#                 newRef2["constraints"]["objs"][objId]["pos"].append(pos)
#                 newRef2["directCont"] = False
#                 newRef2["thatCont"] = False
#                 newRef2["unique"], newRef2["others"] = uniqueAO(instance, objId, newRef2["name"], pos, among = newRef2["others"])
#                 newRefs.append(newRef2)

#     return newRefs

# newRef = {
#     "text": text,
#     "objId": objId,
#     "prob": prob,
#     "name": name,
#     "constraints": {
#         "objs": {objId: {"attributes": [], "pos": [], "same": [], "name": isName}},
#         "rels": [] # "rels": [], 
#     },
#     "directCont": isCont, "thatCont": thatCont, 
#     "unique": unique, "others": others
#     "prefix": None
# }

# # TODO? add article like? the cat next to a tree instead of the??
# # refs for active? 0?
# # 
# def modProb(hasSimple, stative, direct):
#     if hasSimple:
#         if stative:
#             directProb, relProb, srelProb = 0.0, 0.0, 1.0
#         else:
#             directProb, relProb, srelProb = 0.0, 0.8, 0.2
#     else:
#         if direct:
#             if rel in ["of", "with"]:
#                 directProb, relProb, srelProb = 1.0, 0.0, 0.0
#             else:
#                 directProb, relProb, srelProb = 0.65, 0.35, 0.0
#         else:
#             directProb, relProb, srelProb = 0.0, 1.0, 0.0

#     return directProb, relProb, srelProb

# def relRefs(instance, objId, refs, maxCount):
#     obj = instance[objId]
#     outObjsRefs = {}
#     for relId in obj["outRels"]:
#         rel = obj["outRels"][relId]
#         relWord = rel["rel"]
#         otherObjId = rel["obj"]
#         objRefs = objRef(instance, otherObjId, True, maxCount - 1)
#         newInfoObjRefs = [ref for ref in objRefs if objId not in ref["constraints"]["objs"]]  
#         outObjsRefs[otherObjId] = newInfoObjRefs

#     inObjsRefs = {}
#     for relId in obj["inRels"]:
#         rel = obj["outRels"][relId]
#         relWord = rel["rel"]
#         otherObjId = rel["obj"]
#         objRefs = objRef(instance, otherObjId, True, 0)
#         newInfoObjRefs = [ref for ref in objRefs if objId not in ref["constraints"]["objs"]]  
#         inObjsRefs[otherObjId] = newInfoObjRefs

#     newRefs = []
#     # for ref in refs:
#     for relId in obj["outRels"]:
#         rel = obj["outRels"][relId]
#         relP = rel["rel"]

#         direct = vocab["r"][relP]["cat"] == "direct" 
#         simpleRel = toSimple(relP, obj["name"])
#         hasSimple = (relP != simpleRel) or (relP in stativeRel)
#         stative = relP in stativeRel
        
#         otherObjId = rel["obj"]
#         otherObj = instance[otherObjId]
#         inObjs = [r["subj"] for r in otherObj["inRels"] if similarRel(r["rel"], rel["rel"])]  
#         # just with this rel or any rel?????????????????????

#         for ref in refs:
#             if ref["thatCont"]:
#                 directProb, relProb, srelProb = modProb(hasSimple, stative, direct and ref["directCont"])

#                 prior = 0.2 if ref["unique"] else 1.0
#                 for otherObjRef in outObjsRefs[otherObjId]:
#                     if directProb > 0:
#                         newRef = copy.deepcopy(ref)
#                         newRef["text"] = "{obj} {rel} {otherObj}".format( \
#                             obj = ref["text"], isr = isare(obj["name"]), rel = relP, otherObj = otherObjRef["text"])
#                         newRef["prob"] *= (prior * directProb) 
#                         newRef["directCont"] = False
#                         ############ ?????????????????????? that? the X on the ... that is .... ???                        
#                         newRef["unique"], newRef["others"] = uniqueL(instance, objId, newRef["others"], inObjs)
#                         newRef["constraints"]["objs"].update(otherObjRef["constraints"]["objs"])
#                         newRef["constraints"]["rels"].append(relId)
#                         newRefs.append(newRef)

#                     if relProb > 0:
#                         newRef = copy.deepcopy(ref)
#                         newRef["text"] = "{obj} that {isr} {rel} {otherObj}".format( \
#                             obj = ref["text"], isr = isare(obj["name"]), rel = relP, otherObj = otherObjRef["text"])
#                         newRef["prob"] *= (prior * relProb) 
#                         newRef["directCont"] = False
#                         newRef["thatCont"] = False
#                         newRef["unique"], newRef["others"] = uniqueL(instance, objId, newRef["others"], inObjs)
#                         newRef["constraints"]["objs"].update(otherObjRef["constraints"]["objs"])
#                         newRef["constraints"]["rels"].append(relId)
#                         newRefs.append(newRef)

#                     if srelProb > 0:
#                         newRef = copy.deepcopy(ref)
#                         newRef["text"] = "{obj} that {rel} {otherObj}".format( \
#                             obj = ref["text"], isr = isare(obj["name"]), rel = simpleRel, otherObj = otherObjRef["text"])
#                         newRef["prob"] *= (prior * srelProb) 
#                         newRef["directCont"] = False
#                         newRef["thatCont"] = False
#                         newRef["unique"], newRef["others"] = uniqueL(instance, objId, newRef["others"], inObjs)
#                         newRef["constraints"]["objs"].update(otherObjRef["constraints"]["objs"])
#                         newRef["constraints"]["rels"].append(relId)
#                         newRefs.append(newRef)

#     for relId in obj["outRels"]:
#         rel = obj["outRels"][relId]
#         relP = rel["rel"]

#         direct = vocab["r"][relP]["cat"] == "direct" 
#         simpleRel = toSimple(relP, obj["name"])
#         hasSimple = (relP != simpleRel) or (relP in stativeRel)
#         stative = relP in stativeRel
        
#         otherObjId = rel["obj"]
#         otherObj = instance[otherObjId]
#         inObjs = [r["subj"] for r in otherObj["inRels"] if similarRel(r["rel"], rel["rel"])]  
#         # just with this rel or any rel?????????????????????

#         for ref in refs:
#             if ref["thatCont"]:
#                 directProb, relProb, srelProb = modProb(hasSimple, stative, direct and ref["directCont"])

#                 prior = 0.2 if ref["unique"] else 1.0
#                 for otherObjRef in inObjsRefs[otherObjId]:
#                     if directProb > 0:
#                         newRef = copy.deepcopy(ref)
#                         newRef["text"] = "{obj} {rel} {otherObj}".format( \
#                             obj = ref["text"], isr = isare(obj["name"]), rel = relP, otherObj = otherObjRef["text"])
#                         newRef["prob"] *= (prior * directProb) 
#                         newRef["directCont"] = False
#                         ############ ?????????????????????? that? the X on the ... that is .... ???                        
#                         newRef["unique"], newRef["others"] = uniqueL(instance, objId, newRef["others"], inObjs)
#                         newRef["constraints"]["objs"].update(otherObjRef["constraints"]["objs"])
#                         newRef["constraints"]["rels"].append(relId)
#                         newRefs.append(newRef)

#                     if relProb > 0:
#                         newRef = copy.deepcopy(ref)
#                         newRef["text"] = "{obj} that {isr} {rel} {otherObj}".format( \
#                             obj = ref["text"], isr = isare(obj["name"]), rel = relP, otherObj = otherObjRef["text"])
#                         newRef["prob"] *= (prior * relProb) 
#                         newRef["directCont"] = False
#                         newRef["thatCont"] = False
#                         newRef["unique"], newRef["others"] = uniqueL(instance, objId, newRef["others"], inObjs)
#                         newRef["constraints"]["objs"].update(otherObjRef["constraints"]["objs"])
#                         newRef["constraints"]["rels"].append(relId)
#                         newRefs.append(newRef)

#                     if srelProb > 0:
#                         newRef = copy.deepcopy(ref)
#                         newRef["text"] = "{obj} that {rel} {otherObj}".format( \
#                             obj = ref["text"], isr = isare(obj["name"]), rel = simpleRel, otherObj = otherObjRef["text"])
#                         newRef["prob"] *= (prior * srelProb) 
#                         newRef["directCont"] = False
#                         newRef["thatCont"] = False
#                         newRef["unique"], newRef["others"] = uniqueL(instance, objId, newRef["others"], inObjs)
#                         newRef["constraints"]["objs"].update(otherObjRef["constraints"]["objs"])
#                         newRef["constraints"]["rels"].append(relId)
#                         newRefs.append(newRef)

#     return newRefs

# def sameRefs(instance, refs):
#     newRefs = []
#     for ref in refs:
#         objId = ref["objId"]
#         obj = instance[objId]

#     return newRefs

# def twoRefs(instance, refs):
#     newRefs = []
#     for ref in refs:
#         objId = ref["objId"]
#         obj = instance[objId]

#     return newRefs

# def objRefs(instance, objId, defined, maxCount = 2, objCount = 2):
#     obj = instance["objects"][objId]
#     objName = obj["name"]
#     if not isMain(objName):
#         return None
#     cats = []
#     c = catOf(obj)
#     if c is not None:
#         cats = ancestors(c)
#     refs = adjRefs(instance, objName, objId, True, defined, True)
#     for cat in cats:
#         refs += adjRefs(instance, cat, objId, False, defined, catInfo[cat]["specific"])
    
#     refs += posRefs(instance, refs)

#     sourceRefs = refs
#     for _ in range(objCount):
#         sourceRefs = relRefs(instance, objId, sourceRefs, maxCount)
#         refs += sourceRefs
    
#     refs += twoRefs(instance, refs)
#     refs += sameRefs(instance, refs)

#     uniqueRefs = [ref for ref in refs if ref["unique"]]

#     return uniqueRefs

 # = {"objs": [], "attr2obj": {}} 

# TODO: that for object: A O, O Rel, O that is, O that is [not] A, O that is rel O2, O that O2 is rel (for case when other are), C instead of O,
# O that is both X and Y, that is made of..., O that is X but not Y, C that is not O
# different for that and a? a c that is not a more common than the c that is not o
# (that is), prefix Ther is... it.
# same as relate that is|has the same <type> as 
# not
# o that is not rel, 
# on the left/right (global)
# rel/posrel
# this, it, prefix... 

# verify -> yes / no
# choose -> list
# query -> type
# attr nouns: liquid, sport, material, company
# generateAll = ["chooseAttr"]
# TODO:!!! different probs for choose, query, verify
def verifyAttrs(data):
    data["attributes"] = sorted(data["attributes"])
    ret = data["dobject"]["code"]
    l = len(ret) - 1
    ret.append("verify {type}: {attr}".format(type = data["type"][0], attr = data["attributes"][0]))
    ret.append("verify {type}: {attr} [{backref}]".format(type = data["type"][1], attr = data["attributes"][1], backref = l))
    ret.append("and: {s1}+{s2}".format(s1 = l + 1, s2 = l + 2))
    # args = range(len(ret), len(ret) + len(data["attributes"]))
    # ret += ["verify: {attr} [{step}]".format(attr = attr, step = len(ret) - 1) for attr in data["attributes"]]
    # ret.append("and [{}]".format(",".join(map(str, args))))
    return ret

def binaryOp(parts, op): 
    ret = copy.deepcopy(parts[0])
    parts[1][0] += " []"
    ret += parts[1]
    ret.append("{op}: {s1}+{s2}".format(op = op, s1 = len(parts[0]) - 1, s2 = len(ret) - 1))
    return ret

codes = {
    "verifyState": lambda data: ["select: scene"] + ["verify {}: {}".format(data["type"], data["attribute"])],
    "queryState": lambda data: ["select: scene"] + ["query: {}".format(data["type"])],
    "chooseState": lambda data: ["select: scene"] + ["choose {}: {}".format(data["type"],"|".join(data["candidates"]))],
    "queryAttr": lambda data: data["dobject"]["code"] + ["query: {}".format(data["type"])],
    "verifyAttr": lambda data: data["dobject"]["code"] + ["verify{}: {}".format("" if data["type"] is None else (" " + data["type"]), data["attribute"])],
    "verifyAttrs": verifyAttrs, # lambda data:  + [] + ["and": data["attrs"]#["verify: {}".format(",".join(data["candidates"]))] 
    "chooseAttr": lambda data: data["dobject"]["code"] + ["choose{}: {}".format("" if data["type"] is None else (" " + data["type"]),"|".join(data["candidates"]))],
    "exist": lambda data: data["dobject"]["code"] + ["exist"],# query:  (c.replace("select", "exist") for c in data["dobject"]["code"])
    "existRel": lambda data: data["dobject"]["code"] + [data["rel"], "exist"],#  query: (c.replace("select", "exist") for c in data["dobject"]["code"])
    "logicOr": lambda data: binaryOp(data["parts"], "or"), # lambda data: data["dobject"]["code"].replace("select", "exist")
    "logicAnd": lambda data: binaryOp(data["parts"], "and"), 
    "queryObject": lambda data: data["dobject"]["code"] + ["query: name"],
    "chooseObject": lambda data: data["dobject"]["code"] + ["choose name: {}".format("|".join(data["candidates"]))],
    "queryRel": lambda data: data["dobject"]["code"] + [relObjCode("relate", data["tId"], data["tName"], data["rel"], data["subj"]), "query: name"],
    "verifyRel": lambda data: data["dobject"]["code"] + [relObjCode("verify rel", data["tId"], data["tName"], data["rel"], data["subj"])],
    "chooseRel": lambda data: data["dobject"]["code"] + [relObjCode("choose rel", data["tId"], data["tName"], "|".join(data["candidates"]), data["subj"])],
    "chooseObjRel": lambda data: data["dobject"]["code"] + [relObjCode("relate", data["tId"], data["tName"], data["rel"], data["subj"]), "choose name: {}".format("|".join(data["candidates"]))],
    "allSame": lambda data: data["dobject"]["code"] + ["same: {}".format(data["type"])],
    "allDiff": lambda data: data["dobject"]["code"] + ["different: {}".format(data["type"])],
    "compare": lambda data: binaryOp(data["parts"], "lchoose {}".format(data["comparative"])),
    "common": lambda data: binaryOp(data["parts"], "common"),
    "same": lambda data: binaryOp(data["parts"], "same {}".format(data["type"])),
    "diff": lambda data: binaryOp(data["parts"], "different {}".format(data["type"]))
    # "compare": lambda data: data["dobject"]["code"] + [relObjCode("verify", data["tId"], data["tName"], data["rel"], data["subj"])]
}

def verifyAttrs(data):
    data["attributes"] = sorted(data["attributes"])
    ret = data["dobject"]["code"]
    l = len(ret) - 1
    ret.append("verify {type}: {attr}".format(type = data["type"][0], attr = data["attributes"][0]))
    ret.append("verify {type}: {attr} [{backref}]".format(type = data["type"][1], attr = data["attributes"][1], backref = l))
    ret.append("and: {s1}+{s2}".format(s1 = l + 1, s2 = l + 2))
    # args = range(len(ret), len(ret) + len(data["attributes"]))
    # ret += ["verify: {attr} [{step}]".format(attr = attr, step = len(ret) - 1) for attr in data["attributes"]]
    # ret.append("and [{}]".format(",".join(map(str, args))))
    return ret

# "verifyState":  "select: scene", "verify {type}: {attr}" | "scene.verify {type}: {attr}"
# "queryState": "select: scene", "query: {type}" | "scene.query: {type}"
# "chooseState": "select: scene", "choose {type}: {|candidates}" | "scene.choose {type}: {|candidates}"
# "queryAttr": "select: DOBJECT", "query: {type}" | "oid.query: {type}"
# "verifyAttr": "select: DOBJECT", "verify {type}: {attr}" | "oid.verify {type}: {attr}"
# "verifyAttrs": "select: DOBJECT", "verify {type}: {attr}", "verify {type}: {attr}", "and: {s1}, {s2}" | "oid.verify {type}: {attr}.verify {type}: {attr}.and"
# "chooseAttr": "select: DOBJECT", "choose {type}: {|candidates}" | "oid.choose {type}: {|candidates}"
# "exist": "select: OBJECT", "query: exist" | "oid.[filter {t}: not({a}).]exist"
# "existRel": "select: DOBJECT", "relate: REL", "query: exist" | "oid.@rel,d@ oid.exist"
# "logicOr": "select: DOBJECT1", "select: DOBJECT2" | "oid1.oid.2[filter {t}: not({a}).]or"
# "logicAnd": "select: DOBJECT1", "select: DOBJECT2" | "oid1.oid.2[filter {t}: not({a}).]and"
# "queryObject": "select: DOBJECT", "query: name" | "oid.query: name"
# "chooseObject": "select: DOBJECT", "choose name: {|candidates}" | "oid.choose name: {|candidates}"
# "queryRel": "select: DOBJECT", "relate: REL", "query: name" | "oid.@rel,d@ oid.query: name"
# "verifyRel": "select: DOBJECT", "verify rel: REL" | "oid.verify rel: @rel,d@ oid"
# "chooseRel": "select: DOBJECT", "choose rel: REL {|candidates}" | "oid.choose rel: (|candidates,d) oid"
# "chooseObjRel": "select: DOBJECT", "relate: REL", "choose name: {|candidates}" | "oid.@rel,d@ oid.choose name: {|candidates}"
# "allSame": "select: DOBJECT", "same: {type}" | "{cat}.same: {type}"
# "allDiff": "select: DOBJECT", "different: {type}" | "{cat}.different: {type}"
# "compare": "select: DOBJECT1", "select: DOBJECT2", "lchoose {comparative}: {s1}, {s2}" | "oid.oid.{comparative}"
# "common": "select: DOBJECT1", "select: DOBJECT2", "common: {s1}, {s2}" | "oid.oid.common"
# "same": "select: DOBJECT1", "select: DOBJECT2", "same {type}: {s1}, {s2}" | "oid.oid.same {type}"
# "diff": "select: DOBJECT1", "select: DOBJECT2", "different {type}: {s1}, {s2}" | "oid.oid.different {type}"
# "REL": "@rel,d@ oid"

# DOBJECT: "select: {objName} ({objId})"
# REL: "{obj},{rel},{so} ({objId})"

# "filter {t}: {a}"
# "filter {t}: not#{a}"

pattern = {
    "o": r"!o:[a-z0-9\-\\\[\]\* ]*!", # () ()
    "a": r"!a:[a-z0-9\-\\\[\]\* ]*!", # () ()
    "t": r"!t [a-z0-9\-\\\[\]\* ]*!", # ()
    "obj": r"select: (.*) \((.*)\)",
    "oattr": r".* (.*): (.*)", # lambda func: (func + 
    "attr": r".* (!t .*!): (!a:.*!)", # lambda func: (func + 
    "attrnot": r".* (!t .*!): not#(!a:.*!)", # lambda func: (func + 
    "rel": r"(.*): (.*),(.*),(.*) \((.*)\)",
    "onot": r"not\((.*)\)",
    "not": r"not#(.*)",
    "choices": r"(.*)\|(.*)", # ","
    "arg": r".*: (.*)", # lambda func: (func + 
    "r": r"@.*@ (.*)"
}

def match(pattern, ccode):
    ret = re.match(pattern + "$", ccode)
    return (ret is not None)

def compactCode(code, answer, codeGroup, group):
    # TODO: fix to right form!
    for i, c in enumerate(code):
        for op in ["filter", "verify", "choose"]:
            if "{}:".format(op) in c:
                a = re.match("{}: (.*)".format(op), c).group(1)
                if a.startswith("not("):
                    a = a[4:-1]
                a = a.split("[")[0]
                # print(a)
                t = typeOf(a, None, retAll = True)
                t = t[0] if (t is not None and len(t) > 0) else None
                # print(c, code[i])
                if t is None:
                    if op in ["verify", "choose"]:
                        # print("none")                    
                        return None
                    else:
                        t = "ph"
                code[i] = re.sub("{}:".format(op), "{} !t {}!:".format(op, t), c)
            # if "{}:".format(op) in c:
            #     print("HERE", code)
            #     return None

    normalizedCode = []
    for i, c in enumerate(code):
        if c.startswith("relate"):
            if codeGroup not in ["existRelT", "existRelF", "queryRel", "chooseObjRel"] or (i < len(code) - 2):
                oname, oid = re.match(pattern["rel"], c).group(2,5)
                o = oname if oid == "-" else "id{}".format(oid)
                normalizedCode[-1] = "!o:{}!".format(o)# "select {} ({})".format(oname, oid)
                continue
            if i != len(code) - 2:
                continue
        if c.startswith("filter"):
            if not ((codeGroup.startswith("exist") or codeGroup.endswith("Object")) and (not codeGroup.startswith("existRel"))):
                continue

        if re.search(r" \[[0-9]*\]", c):
            c = re.sub(r" \[[0-9]*\]", r"", c)

        if c.startswith("select"):
            if c == "select: scene":
                nc = "scene"
            else:
                content = re.match(pattern["obj"], c) # .group(2) c.split("(")[1][:-1]
                oname, oid = content.group(1, 2) 
                o = oname if oid == "-" else "id{}".format(oid)
                if codeGroup.startswith("all"):
                    o = "allpeople" if oname == "person" else "allanimals"
                nc = "!o:{}!".format(o)
        elif c.startswith("filter"):
            t, a = re.match(pattern["oattr"], c).group(1, 2)#  ("filter") c.split(": ")[1] # "[a:{}]".format()
            if a.startswith("not("):
                a = re.match(pattern["onot"], a).group(1)
                nc = "filter !t {}!: not#!a:{}!".format(t, a) # a[4:-1]
            else: 
                nc = "filter !t {}!: !a:{}!".format(t, a)
        elif c.startswith("verify") and (not c.startswith("verify rel")):
            op, a = re.match(pattern["oattr"], c).group(1, 2) # ("filter")#, content.group(2)# c.split(": ")
            nc = "verify !t {}!: !a:{}!".format(op, a)
        elif c.startswith("choose") and (not c.startswith("choose rel")):
            op, content = re.match(pattern["oattr"], c).group(1, 2) # ("choose")#, content.group(2)# c.split(": ") [content.group(2), content.group(3)]
            content = re.match(pattern["choices"], content)
            alist = content.group(1, 2) # , content.group(2)
            #alist = alist.split("|")
            alist = ["!a:{}!".format(a) for a in alist]
            alist = "&".join(alist)
            nc = "choose !t {}!: {}".format(op, alist)
        elif any([c.startswith(mod) for mod in ["or", "and", "lchoose", "common", "same", "different"]]):
            if (not c.startswith("same:")) and (not c.startswith("different:")):
                c = c.split(":")[0]
            c = c.replace("same ", "same: ")
            c = c.replace("different ", "different: ")
            nc = c.replace("lchoose ", "")
            if nc.startswith("same") or nc.startswith("different"):
                nc = re.sub(r"(.*): (.*)", r"\1: !t \2!", nc)
        elif c.startswith("relate") or "rel:" in c:
            relOp, oname, relName, relDir, oid = re.match(pattern["rel"], c).group(1,2,3,4,5) # relContent =  # ("choose") rel
            relOp = "" if relOp == "relate" else (relOp + ":")
            # if "relate" in relOp:
            #     relContent = c.split("relate: ")[1]
            #     op = ""
            # else:
            #     op, relContent = c.split("rel: ")
            #     op += "rel: "

            # relInfo, oid = relContent.split("(")
            # _, relName, relDir = relInfo.split(",")
            o = "!o:{}!".format(oname if oid == "-" else "id{}".format(oid))
            rel = "{},{}".format(relName, relDir)
            # oid = oid[:-1]
            nc = relOp + "@{}@ {}".format(rel, o)
            nc = nc.replace("|", "&")            
        elif c.startswith("query"):
            nc = re.sub(r"(.*): (.*)", r"\1: !t \2!", c)
        else:
            nc = c
        normalizedCode.append(nc)

    if normalizedCode[-1] in ["or", "and"] and (not codeGroup.startswith("verifyAttrs")):
        if any(["filter" in nc for nc in normalizedCode]):
            normalizedCode = [normalizedCode[0]] + normalizedCode[2:]
        if any(["verify" in nc for nc in normalizedCode]):
            normalizedCode = [normalizedCode[0]] + normalizedCode[2:]
        if any(["exist" in nc for nc in normalizedCode]):
            normalizedCode = [normalizedCode[0]] + normalizedCode[2:]

    if group in ["logicOr", "logicAnd", "common", "same", "diff"]: # "compare", 
        normalizedCode[0:2] = sorted(normalizedCode[0:2])    
    
    if codeGroup.startswith("verifyAttrs"):
        normalizedCode[-3:-1] = sorted(normalizedCode[-3:-1])

    normalizedCode = "/".join(normalizedCode)

    if answer in ["yes", "no"]:
        normalizedCode += ";" + ("T" if answer == "yes" else "F")

    if codeGroup == "common":
        normalizedCode += " {}".format(answer)

    return normalizedCode

def compactCodeFix(ccode, code, answer, codeGroup, group):
    # TODO: fix to right form!
    if ccode is None or codeGroup not in ["existRelT", "existRelF", "queryRel", "chooseObjRel"]:
        return ccode
    right = ccode.split("/")[0]
    for i, c in enumerate(code):
        if c.startswith("relate"):
            if i < len(code) - 2:
                oname, oid = re.match(pattern["rel"], c).group(2,5)
                o = oname if oid == "-" else "id{}".format(oid)
                right = "!o:{}!".format(o)# "select {} ({})".format(oname, oid)
    ccode = "/".join([right] + ccode.split("/")[1:])
    return ccode

# entailed = set()
def entailed(ccode, codeGroup, es = None):
    if es is None:
        es = []       
    if ccode not in es:
        es.append(ccode)
    newEs = directEntailed(ccode, codeGroup)
    for e, ct in newEs:
        if e not in es:
            es.append(e)
            sons = entailed(e, ct, es = es)
            for s in sons:
                if s not in es:
                    es.append(s)
    return es

def vat2qa(vat):
    vat = vat[:-2].split("/")
    t = re.match(pattern["attr"], vat[-1]).group(1) # t = vst[-1][7:].split(":")[0]
    qs = vat[:-1] + ["query: {}".format(t)]
    return "/".join(qs)

def vaf2ca(vaf):
    ca = vaf[:-2].split("/")
    t, fa = re.match(pattern["attr"], ca[-1]).group(1, 2)
    choices = "&".join([pattern["a"], fa])
    ca = ca[:-1] + ["choose {}: {}".format(t, choices)]
    return "/".join(ca)

def qa2va(qa, b):
    qa = qa.split("/")
    t = re.match(pattern["arg"], qa[-1]).group(1) # t = vst[-1][7:].split(":")[0]
    vat = qa[:-1] + ["verify {}: {}".format(t, pattern["a"])]
    return "/".join(vat) + ";{}".format("T" if b else "F")

def qa2ca(qa):
    ca = qa.split("/")
    t = re.match(pattern["arg"], ca[-1]).group(1) # t = vst[-1][7:].split(":")[0]
    choices = "&".join([pattern["a"], pattern["a"]])
    ca = ca[:-1] + ["choose {}: {}".format(t, choices)]
    return "/".join(ca)

def ca2qa(ca):
    qa = ca.split("/")
    t = re.match(r"choose (.*): .*", qa[1]).group(1)
    a1, a2 = re.search(r": !a:(.*)!&!a:(.*)!", qa[1]).group(1, 2)
    if a1 not in attrOpsList and a2 not in attrOpsList:
        return None
    qa[1] = "query: {}".format(t)
    return "/".join(qa)

def va2vas(va, index, op):
    vas = va[:-2].split("/")
    t = re.match(pattern["attr"], vas[-1]).group(1)
    vas.append("verify {}: {}".format(pattern["t"], pattern["a"]))
    if index == 0:
        vas[-2], vas[-1] = vas[-1], vas[-2]
    vas.append(op)
    return "/".join(vas) + va[-2:]

def vas2va(va, index):
    vas = va[:-2].split("/")[:-1]
    vas = [vas[0], vas[1 + index]]
    return "/".join(vas) + va[-2:]

def c2cc(c, index, op):
    code = c[:-2].split("/")
    newC = [pattern["o"]] #[pattern["o"]] + code[1:]# code[1:1+length] # "exist"
    cc = code[:index] + newC + code[(index+1):]
    # cc = (code + newC) if index == 0 else (newC + code)
    cc.append(op)
    return "/".join(cc) + c[-2:]

def cc2c(cc, index, partLength):
    code = cc[:-2].split("/")
    c = code[:index] + code[(index+1):-1]
    # startPoint = index * partLength
    # c = code[startPoint:(startPoint + partLength)]
    return "/".join(c) + cc[-2:]

def ert2et(ert):
    code = ert[:-2].split("/")
    o = re.match(pattern["r"], code[1]).group(1)
    et = [o, code[-1]]
    return "/".join(et) + ert[-2:]

def ent2et(ent):
    et = ent[:-2].split("/")
    et = [c for c in et if (not c.startswith("filter"))]
    return "/".join(et) + ent[-2:]

def e2en(e):
    en = e[:-2].split("/")
    en = [en[0], "filter {}: not#{}".format(pattern["t"], pattern["a"]), en[1]]
    return "/".join(en) + e[-2:]

def e2er(e):
    en = e[:-2].split("/")
    en = [pattern["o"], "@.*,.*@ {}".format(en[0]), en[1]]
    return "/".join(en) + e[-2:]

def ea2en(ea):
    acode = ea[:-2].split("/")
    ncode = []
    for c in acode:
        if c.startswith("filter"):
            t = re.match(pattern["attr"], c).group(1)
            c = "filter {}: not#{}".format(t, pattern["a"])
        ncode.append(c)
    return "/".join(ncode) + ea[-2:]

def en2ea(en):
    ncode = en[:-2].split("/")    
    acode = []
    for c in ncode:
        if c.startswith("filter"):
            t = re.match(pattern["attrnot"], c).group(1)
            c = "filter {}: {}".format(t, pattern["a"])
        acode.append(c)
    return "/".join(acode) + en[-2:]

def co2cn(acode):
    ncode = acode.split("/")
    t, a = re.match(pattern["attr"], ncode[1]).group(1, 2)
    ncode[1] = "verify {}: not#{}".format(t, a)
    ncode[-1] = re.sub(r": (.*)&(.*)$", r": \2&\1", ncode[-1])
    return "/".join(ncode)

def cn2co(ncode):
    acode = ncode.split("/")
    t, a = re.match(pattern["attrnot"], acode[1]).group(1, 2)
    # a = re.match(pattern["not"], a).group(1)
    acode[1] = "verify {}: {}".format(t, a)
    acode[-1] = re.sub(r": (.*)&(.*)$", r": \2&\1", acode[-1])
    return "/".join(acode)

def q2et(q):
    et = q.split("/")[:-1]
    et.append("exist")
    return "/".join(et) + ";T"

def cr2vrt(cr):
    orig = re.search(r"@(.*)&", cr).group(1)
    if ".*" in orig:
        return None
    cr = re.sub(r"@(.*)&(.*),", r"@\1,", cr)
    cr = cr.replace("/choose", "/verify")
    return cr + ";T"

def vrt2vrf(vrt):
    rel = re.search(r"@(.*),(.*)", vrt).group(1)
    if rel not in negative:
        return None
    nrel = negative[rel][0][0]
    # nrel = "&".join(["({})".format(nrel) for nrel in nrels])
    vrf = re.sub(r"@(.*),", "@{},".format(nrel), vrt)
    return vrf[:-1] + "F"

def vrt2vct(vrt):
    rel, d = re.search(r"@(.*),(.*)@", vrt).group(1, 2)
    # d = "o" if d == "s" else "s"
    if rel not in ops:
        return None
    orel = ops[rel]
    vct = re.sub(r"@(.*),", "@{},".format(orel), vrt) # (.*)@ {}@ , d
    vct = re.sub(r"(!o:[a-z0-9\-\\\[\]\* ]*!)(.*)(!o:[a-z0-9\-\\\[\]\* ]*!)", r"\3\2\1", vct)
    return vct

def qr2vrt(qr):
    vrt = qr.split("/")[:-1]
    vrt[1] = "verify rel: " + vrt[1]
    return "/".join(vrt) + ";T"

def qr2cmp(qr):
    rel = re.search(r"@(.*),", qr).group(1)
    if not rel.endswith(" than"):
        return None
    oid1, oid2 = re.search(r"(!o:[a-z0-9\-\\\[\]\* ]*!).*(!o:[a-z0-9\-\\\[\]\* ]*!)", qr).group(1, 2)
    cmpc = [oid1, oid2, rel[:-5]]
    return "/".join(cmpc) 

def qr2smt(qr):
    rel = re.search(r"@(.*),", qr).group(1)
    if not rel.startswith("same "):
        return None
    oid1, oid2 = re.search(r"(!o:[a-z0-9\-\\\[\]\* ]*!).*(!o:[a-z0-9\-\\\[\]\* ]*!)", qr).group(1, 2)
    oids = "/".join(sorted([oid1, oid2]))
    smt = oids + "/" + rel
    return smt

def smdiff(ccode):
    if "/different" in ccode:
        newCcode = ccode.replace("/different", "/same")       
    else:
        newCcode = ccode.replace("/same", "/different")
    newCcode = newCcode[:-1] + ("F" if ccode[-1] == "T" else "T")
    return newCcode

def cmn2same(cmn):
    ret = cmn.replace("/common", "/same")
    ret += ";T"
    return ret

def cmp2t(cmpc):
    cmpc = cmpc.split("/")
    if cmpc[-1] not in oppositeComp:
        return None
    cmpc[-1] = oppositeComp[cmpc[-1]]
    cmpc[0], cmpc[1] = cmpc[1], cmpc[0]
    return "/".join(cmpc)

def cmp2vr(cmpc):
    cmpc = cmpc.split("/")
    if cmpc[-1] not in oppositeComp:
        return None    
    cmpc[1] = "verify rel: @{} than,o@ ".format(cmpc[-1]) + cmpc[1]
    return "/".join(cmpc[:-1]) + ";T"    

def ert2qr(ert):
    qr = ert.split("/")[:-1]
    qr.append("query: !t name!")
    return "/".join(qr)

def qr2cr(qr):
    cr = qr.split("/")[:-1]
    cr[-1] = "choose rel: {}".format(cr[-1])
    cr[-1] = re.sub(r"@(.*),", r"@\1&(.*),", cr[-1])
    return "/".join(cr)

def q2cor(q):
    cor = q.split("/")[:-1]
    cor.append(r"choose: !t name!: (.*)&(.*)")
    return "/".join(cor)

def cor2vrt(cor):
    vrt = cor.split("/")[:-1]
    vrt[-1] = "verify rel: {}".format(vrt[-1])
    return "/".join(vrt) + ";T"

def vrt2qr(vrt, side):
    qr = vrt[:-2].replace("verify rel: ", "") + "/query: !t name!"
    if side == "s":
        if ",s@" in qr:
            qr = qr.replace(",s@", ",o@")
        else:
            qr = qr.replace(",o@", ",s@")
        qr = re.sub(r"(!o:[a-z0-9\-\\\[\]\* ]*!)(.*)(!o:[a-z0-9\-\\\[\]\* ]*!)", r"\3\2\1", qr)
    
    return qr

def erf2cr(erf):
    cr = erf[:-2].split("/")[:-1]
    cr[-1] = "choose rel: {}".format(cr[-1])
    cr[-1] = re.sub(r"@(.*),", r"@(.*)&\1,", cr[-1])    
    return "/".join(cr)

# def erf2cor(ccode): TODO!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

def vrf2cr(vrf):
    cr = re.sub(r"@(.*),", r"@(.*)&\1,", vrf[:-2])
    cr = cr.replace("/verify", "/choose")
    return cr

def vr2vr(vr):
    if ",s@" in vr:
        vr = vr.replace(",s@", ",o@")
    else:
        vr = vr.replace(",o@", ",s@")
    vr = re.sub(r"(!o:[a-z0-9\-\\\[\]\* ]*!)(.*)(!o:[a-z0-9\-\\\[\]\* ]*!)", r"\3\2\1", vr)
    return vr

def vr2er(vr):
    er = vr[:-2].replace("verify rel: ", "") + "/exist" + vr[-2:]
    return er

def er2vr(er):
    vr = er.split("/")[:-1]
    vr[-1] = "verify rel: {}".format(vr[-1])
    return "/".join(vr) + er[-2:]

# def vrf2cor(ccode): TODO!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

# "verifyState": "scene.verify {type}: {attr}"
# "queryState": "scene.query: {type}"
# "chooseState": "scene.choose {type}: {|candidates}"
# "queryAttr": "oid.query: {type}"
# "verifyAttr": "oid.verify {type}: {attr}"
# "verifyAttrs": "oid.verify {type}: {attr}.verify {type}: {attr}.and"
# "chooseAttr": "oid.choose {type}: {|candidates}"
# "exist": "oid.[filter {t}: not#{a}.]exist"
# "existRel": "oid.@rel,d@ oid.exist"
# "logicOr": "oid1.oid2.[filter {t}: not#{a}.]or"
# "logicAnd": "oid1.oid2.[filter {t}: not#{a}.]and"
# "queryObject": "oid.query: name"
# "chooseObject": "oid.choose name: {|candidates}"
# "queryRel": "oid.@rel,d@ oid.query: name"
# "verifyRel": "oid.verify rel: @rel,d@ oid"
# "chooseRel": "oid.choose rel: @|candidates,d@ oid"
# "chooseObjRel": "oid.@rel,d@ oid.choose name: {|candidates}"
# "allSame": "{cat}.same: {type}"
# "allDiff": "{cat}.different: {type}"
# "compare": "oid.oid.{comparative}"
# "common": "oid.oid.common {type}"
# "same": "oid.oid.same {type}"
# "diff": "oid.oid.different {type}"

def directEntailed(ccode, codeGroup):
    es = []
    if codeGroup in ["chooseState", "verifyAttrsF", "existAttrF", "existOrT", #  "existRelF", 
        "existAndF", "verifyAttrAndF", "chooseObject", "chooseObjRel"]: # , "chooseObjRel" , "verifyRelF"
        return es
    elif codeGroup == "chooseAttr":
        newCcode = ca2qa(ccode)
        if newCcode is not None:
            es.append((newCcode, "queryAttr"))
    elif codeGroup in ["verifyStateT", "verifyAttrT"]:
        ct = codeGroup[:-1].replace("verify", "query")
        es.append((vat2qa(ccode), ct))
    elif codeGroup in ["verifyStateF", "verifyAttrF"]:
        ct = codeGroup[:-1].replace("verify", "choose")
        es.append((vaf2ca(ccode), ct))
        if codeGroup == "verifyAttrF":
            es.append((va2vas(ccode, 0, "and"), "verifyAttrsF"))
            es.append((va2vas(ccode, 1, "and"), "verifyAttrsF"))
            es.append((c2cc(ccode, 0, "and"), "verifyAttrAndF"))
            es.append((c2cc(ccode, 1, "and"), "verifyAttrAndF"))
    elif codeGroup in ["queryState", "queryAttr"]:
        ct = codeGroup.replace("query", "verify")
        es.append((qa2va(ccode, True), ct + "T"))
        es.append((qa2va(ccode, False), ct + "F"))
        es.append((qa2ca(ccode), codeGroup.replace("query", "choose")))
    elif codeGroup == "verifyAttrsT":
        es.append((vas2va(ccode, 0), "verifyAttrT")) 
        es.append((vas2va(ccode, 1), "verifyAttrT"))
    elif codeGroup == "existT":
        es.append((c2cc(ccode, 0, "or"), "existOrT"))
        es.append((c2cc(ccode, 1, "or"), "existOrT"))
    elif codeGroup == "existF":
        es.append((c2cc(ccode, 0, "and"), "existAndF"))
        es.append((c2cc(ccode, 1, "and"), "existAndF"))
        es.append((e2en(ccode), "existNotF"))
        es.append((e2er(ccode), "existRelF"))
    elif codeGroup == "existNotF":
        es.append((en2ea(ccode), "existAttrF"))
    elif codeGroup == "existNotOrF":
        es.append((en2ea(ccode), "existAttrOrF"))
        es.append((cc2c(ccode, 0, 3), "existNotF"))
        es.append((cc2c(ccode, 1, 3), "existNotF"))       
    elif codeGroup == "existAttrT": 
        es.append((ea2en(ccode), "existNotT"))
        es.append((c2cc(ccode, 0, "or"), "existAttrOrT"))
        es.append((c2cc(ccode, 1, "or"), "existAttrOrT"))
    elif codeGroup == "existAttrOrT":
        es.append((ea2en(ccode), "existNotOrT"))
    elif codeGroup in ["existOrF", "existAndT", "verifyAttrAndT"]:
        ct = codeGroup.replace("Or", "").replace("And", "")
        es.append((cc2c(ccode, 0, 2), ct))
        es.append((cc2c(ccode, 1, 2), ct))
    elif codeGroup == "existAttrOrF":
        es.append((cc2c(ccode, 0, 3), "existAttrF"))
        es.append((cc2c(ccode, 1, 3), "existAttrF"))
    elif codeGroup in ["existNotT", "existNotOrT"]:
        ct = codeGroup.replace("Not", "")
        es.append((ent2et(ccode), ct))
    elif codeGroup == "existRelT":
        es.append((ert2et(ccode), "existT"))
        es.append((er2vr(ccode), "verifyRelT"))
        # es.append((ert2qr(ccode), "queryRel"))
    elif codeGroup == "chooseAttrObject": 
        es.append((co2cn(ccode), "chooseNotObject")) # , choose = True
    elif codeGroup == "chooseNotObject":
        es.append((cn2co(ccode), "chooseAttrObject")) # , choose = True
    elif codeGroup in ["queryObject", "queryAttrObject", "queryNotObject"]:
        ct = codeGroup.replace("query", "exist").replace("Object", "") + "T"
        es.append((q2et(ccode), ct))
    elif codeGroup == "queryRel":
        es.append((q2et(ccode), "existRelT"))
        es.append((qr2vrt(ccode), "verifyRelT"))
        es.append((qr2cr(ccode), "chooseRel"))
        es.append((q2cor(ccode), "chooseObjRel")) # *****
        newCcode = qr2cmp(ccode)
        if newCcode is not None:
            es.append((newCcode, "compare"))
        newCcode = qr2smt(ccode)
        if newCcode is not None:
            es.append((newCcode, "sameT"))
    elif codeGroup == "chooseRel":
        newCcode = cr2vrt(ccode)
        if newCcode is not None:
            es.append((newCcode, "verifyRelT"))
    # elif codeGroup == "chooseObjRel":
        # es.append((cor2vrt(ccode), "verifyRelT"))    
    elif codeGroup == "verifyRelT":
        # es.append((vr2vr(ccode), "verifyRelT"))
        # es.append((vr2er(ccode), "existRelT"))
        # es.append((vrt2qr(ccode, "o"), "queryRel"))
        # es.append((vrt2qr(ccode, "s"), "queryRel"))
        newCcode = vrt2vrf(ccode)
        if newCcode is not None:
            es.append((newCcode, "verifyRelF"))
        newCcode = vrt2vct(ccode)
        if newCcode is not None:
            es.append((newCcode, "verifyRelT"))
    elif codeGroup == "existRelF":
        es.append((erf2cr(ccode), "chooseRel"))
        es.append((er2vr(ccode), "verifyRelF"))        
        # es.append(q2cor(ccode), "chooseObjRel")   *****
    elif codeGroup == "verifyRelF":
        # es.append((vr2vr(ccode), "verifyRelF"))        
        es.append((vrf2cr(ccode), "chooseRel"))
        es.append((vr2er(ccode), "existRelF"))
        # es.append(vrf2cor(ccode), "chooseObjRel")   *****
    elif codeGroup in ["allSameT", "allSameF", "allDiffT", "allDiffF", "sameT", "sameF", "diffT", "diffF" ]:
        if "same" in codeGroup.lower():
            ct = codeGroup.replace("Same", "Diff").replace("same", "diff")
        else:
            ct = codeGroup.replace("Diff", "Same").replace("diff", "same")
        ct = ct[:-1] + ("F" if ct[-1] == "T" else "T")
        es.append((smdiff(ccode), ct))
    elif codeGroup == "common":
        es.append((cmn2same(ccode), "sameT"))
    elif codeGroup == "compare":
        newCcode = cmp2t(ccode)
        if newCcode is not None:
            es.append((newCcode, "compare"))
        newCcode = cmp2vr(ccode)
        if newCcode is not None:
            es.append((newCcode, "verifyRelT"))

    return es

# ADD OBJECT ID
# MARK NOT IN THE IMG SUFFIX

# questions = {}
idCounter = 0
pidCounter = 0

def adjForm(attr):
    if attr in vocab["a"]:
        return vocab["a"][attr]["adjForm"]
    return attr

def isAdj(attr):
    if typeOf(attr, None) == "material" and coin(0.3):
        return False
    return vocab["a"][attr]["isAdj"]

def isPrefix(attr):
    return vocab["a"][attr]["isPrefix"]

def lookOf(isP):
    return "look" if (isP and coin(0.78)) else "seem|appear to be"

def personKey(person):
    return person["mAttributes"].get("gender")
    # if "gender" not in person["mAttributes"]:
    #     return None
    # for key in ["male", "female"]:
    #     if key in person["attributes"]:
    #         return key
    # return None

def animalKey(animal):
    animalType = singularOf(animal["name"])
    if animalType == "animal":
        return None
    return animalType

# attribute that related
# def ctoa(comparative):
# {
# "taller than": "height",
# "larger than": "size",
# "smaller than": "size",
# "higher than": "height",
# "bigger than": "size",
# "shorter than": "length",
# "longer than": "length",
# }

def createComparative(instance, subjId, subjName, objId, objName, comparative, qk):
    # ids = [subjId, objId]
    subj = instance["objects"][subjId]
    obj = instance["objects"][objId]
    subjIs = isare(subjName)
    s = "s" if not isPlural(subjName) else ""
    which = "which"
    if isA(subj, "person") and isA(obj, "person"):
        which += "|who" 
    mapping = {"which": which, "is": subjIs, "s": s, "comparative": comparative, "subject": subjName}
    mapping["dsubject"], mapping["asubject"], mapping["dpsubject"] = definedRef(instance, subjId, direct = True)["the"] # , blackObjIds = ids, blackRS = [comparative], , blackRO = [comparative]
    mapping["dobject"], mapping["aobject"], mapping["dpobject"] = definedRef(instance, objId, direct = True)["the"] # , blackObjIds = ids, blackRS = [comparative], , blackRO = [comparative]

    data = {"parts": [getObjCode(subjId, subj, subjName, clean = True), getObjCode(objId, obj, objName, clean = True)], "comparative": comparative}
    data["pointer"] = [subjId]
    gen(instance, "comparativeChoose", "compare", "compare", mapping, data, qk) 

    if comparative in oppositeComp:
        mapping["subject"] = objName
        mapping["dsubject"], mapping["dobject"] = mapping["dobject"], mapping["dsubject"] 
        mapping["asubject"], mapping["aobject"] = mapping["aobject"], mapping["asubject"] 
        data["comparative"] = oppositeComp[comparative]
        data["pointer"] = [objId]
        gen(instance, "comparativeChoose", "compare", "compare", mapping, data, qk)

def groupByKey(objs, gFunc):
    retDict = defaultdict(list)
    allMarked = True
    for obj in objs:
        k = gFunc(obj)
        if k is not None:
            retDict[k].append(obj)
        else:
            allMarked = False

    return retDict, allMarked

def createAllQ(objs, keyFync, cat, ctype, patternType, qk):
    if len(objs) == 0:
        return

    ids = [objId for objId,_ in objs]
    objs = [obj for _,obj in objs]

    type2objs, allMarked = groupByKey(objs, keyFync)

    if allMarked:
        multiple = (len(objs) > 1 or any([isPlural(obj["name"]) for obj in objs]))
        if multiple:
            two = (len(objs) == 2 and all([isSingular(obj["name"]) for obj in objs]))
            subgroups = [(t, g) for t, g in type2objs.items() if len(g) > 0] 
            same = (len(subgroups) == 1)
            if same and subgroups[0][0] == "male":
                return
            kname = "gender" if ctype == "gender" else "pObject" 
            mapping = {"two": two, kname: pluralOf(subgroups[0][0])}
            if not same:
                mapping["pObject2"] = subgroups[1][0]

            sameP = "same" + patternType
            diffP = "diff" + patternType

            data = {"dobject": {"code": [objDirCode(",".join(ids), cat)]}, "type": ctype}
            data["pointer"] = ids
            mapping["inImg"] = inImg()
            gen(instance, sameP if same else (sameP + "C"), "allSame", "allSame{}".format("T" if same else "F"), mapping, data, qk)
            mapping["inImg"] = inImg()        
            gen(instance, (diffP + "C") if same else diffP, "allDiff", "allDiff{}".format("F" if same else "T"), mapping, data, qk)

def createSmdiffQ(instance, type2obj, c1, c2, ctype, qk):
    same = (c1 == c2)
    t1 = type2obj[c1]
    t2 = type2obj[c2]
    tsize = len(t1)
    for obj1Id in t1:
        for obj2Id in t2:
            ids = [obj1Id, obj2Id]
            obj1 = instance["objects"][obj1Id]
            obj2 = instance["objects"][obj2Id]
            obj1name = obj1["name"]
            obj2name = obj2["name"]

            if obj1Id != obj2Id and mod(obj1name) == mod(obj2name) and singularOf(obj1name) != singularOf(obj2name) \
                    and not isA(obj1, "part") and not isA(obj2, "part"): #:
                objIs = isare(obj1name)
                objDoes = dodoes(obj1name)
                objHas = hashave(obj1name)                
                mapping = {"attribute": c1, "attribute2": c2, "type": ctype, 
                    "is": objIs, "does": objDoes, "has": objHas}

                mapping["dsubject"], mapping["asubject"], mapping["dpsubject"] = definedRef(instance, obj1Id, direct = True)["the"]
                mapping["dobject"], mapping["aobject"], mapping["dpobject"] = definedRef(instance, obj2Id, direct = True)["the"]

                # data = {"dobject": {"code": None, "s": True}, "rel": "same {}".format(ctype), "tId": obj1Id, "tName": obj1name, "subj": None}
                data = {"parts": [getObjCode(obj1Id, obj1, obj1name, clean = True), getObjCode(obj2Id, obj2, obj2name, clean = True)]}
                data["type"] = ctype
                data["pointer"] = ids

                if ctype == "material":
                    gen(instance, "twoSameMaterial" if same else "twoSameC", "same", "same{}".format("T" if same else "F"), mapping, data, qk) # "verifyRel"
                else:
                    gen(instance, "twoSame" if same else "twoSameC", "same", "same{}".format("T" if same else "F"), mapping, data, qk) # "verifyRel"
                    data["rel"] = "different {}".format(ctype)
                    gen(instance, "twoDifferentC" if same else "twoDifferent", "diff", "diff{}".format("F" if same else "T"), mapping, data, qk) # "verifyRel"

                if same and tsize == 2:
                    data = {"parts": [getObjCode(obj1Id, obj1, obj1name, clean = True), getObjCode(obj2Id, obj2, obj2name, clean = True)]}
                    data["pointer"] = ids
                    gen(instance, "twoCommon", "common", "common", mapping, data, qk)

                    cat = refcatOf(obj1, q = True)
                    if cat is not None:
                        mapping["dsubject"], mapping["asubject"], mapping["dpsubject"] = definedRef(instance, obj1Id, direct = True, answer = True)["the"]
                        mapping["dobject"], mapping["aobject"], mapping["dpobject"] = definedRef(instance, obj2Id, direct = False, blackAType = [ctype], blackObjIds = [obj1Id, obj2Id])["the"]
                        mapping["category"], mapping["cis"] = catNormalize(obj, cat, k = False)
                        mapping["kategory"], mapping["kis"] = catNormalize(obj, cat, k = True)
                        mapping["khas"] = "has" if mapping["kis"] == "is" else "have" # obj["name"]
                        mapping["chas"] = "has" if mapping["cis"] == "is" else "have"
                        mapping["subject"] = obj1name
                        mapping["a"] = geta(obj1name)

                        data = {"dobject": {"code": None, "s": True}, "rel": "same {}".format(ctype), "tId": obj1Id, "tName": cat, "subj": None}
                        data["pointer"] = [obj1Id]

                        if ctype == "material" and c1 in basicMats:
                            gen(instance, "sameMaterialRelate", "queryRel", "queryRel", mapping, data, qk + "o")
                        else:
                            gen(instance, "sameRelate", "queryRel", "queryRel", mapping, data, qk + "o")

flavorAnsPattern = "{this} {is} a {attribute} {object}."
def getPatterns(group, mapping):
    # if group == "verifyAttr":
    patterns = []
    for p in templates[group]["list"]:
        if len(p) == 4:
            patterns.append(p)
        else:
            # if group in ["verifyAttr", "verifyAttrC", "verifyAttrs", "verifyAttrs", 
            #     "directOf", "directWhich", "how"]:
            bad = False
            if p[4] in ["have", "typed", "of", "pattern", "direct"]:
                condKey = p[4]
                condGroup = templates[group]["extra"][condKey]
                if not all(t in condGroup for t in mapping["types"]):
                    bad = True # *patterns.append(p)
            elif p[4] in ["place", "room"]:
                # if  p[4] in ["room", "notroom"]:
                cond = isAn(mapping["place"], "room") if p[4] == "room" else not isA(mapping["place"], "room")
                if not cond:
                    bad = True # *patterns.append(p)
                # else:
                #     patterns.append(p)
            elif p[4] in ["singular", "plural"]:
                if p[4] == "plural":
                    if not all(mapping.get(p,"") is not None for p in ["pObject", "cpObject", "pSubject", "cpSubject"]):
                        bad = True # *patterns.append(p)
                else:
                    if not all(mapping.get(p,"") is not None for p in ["sObject", "csObject", "sSubject", "csSubject"]):
                        bad = True # *patterns.append(p)
            elif p[4] in ["2", ">2"]:
                if p[4] == "2":
                    if not mapping["two"]:
                        bad = True # *patterns.append(p)                    
                else:
                    if mapping["two"]:
                        bad = True # *patterns.append(p)
            elif p[4] == "countable":
                if not mapping["category"] is not None:
                    bad = True # *patterns.append(p)
            # elif p[4] == "leftright":
            #     if mapping["pos"] not in ["left", "right"]:
            #         bad = True
            # elif p[4] == "where":
            #     if 

            if p[-1] == "short":
                if not (mapping["dobject"] == mapping["aobject"]):
                    bad = True # *patterns.append(p)                    
            
            if group in ["directOf", "directWhich"] and mapping["type"] == "flavor":
                p = (p[0], flavorAnsPattern) + p[2:] 
                
            if not bad:
                patterns.append(p)
            # elif p[4] == "both":
            #     if all(mapping[p] is not None for p in ["object", "cObject"]):
            #         patterns.append(p)
            #     else:
            #         patterns.append(p)
            # else:
            #     patterns.append(p)

    patterns = [(p[:3], p[3]) for p in patterns]
    return patterns

def isTf(questionAns):
    return questionAns in ["yes", "no"]

def genQuestionRep(instance, patterns, group, codeSturcture, codeGroup, mapping, data, key, 
        priority, select = 1.0, ansDist = False, newTf = None, nonProb = False, weights = None):
    global idCounter
    global pidCounter

    # generation
    newQuestions = generateQuestion(patterns, mapping, group, data, nonProb)
    for question in newQuestions:
        code = codes[codeSturcture](data)
        question["ocode"] = code
        question["code"] = normalizeCode(code)
        question["ccode"] = compactCode(code, question["answer"], codeGroup, group)
        question["entailed"] = [] if question["ccode"] is None else entailed(question["ccode"], codeGroup)
        question["pointer"] = data["pointer"]
        question["tf"] = isTf(question["answer"])
        question["codeGroup"] = codeGroup
        question["group"] = group
        question["type"] = gInfo[codeSturcture]["type"]
        question["codeSturcture"] = codeSturcture
        question["priority"] = priority
        question["isPos"] = mapping.get("isPos", False)
        question["select"] = min(select, (0.33 if question["isPos"] else 1.0)) # * (0.75 if question["type"] in ["verify", "logical"] else 1.0)
        question["ansDist"] = ansDist # if (coin(0.33)  else True) else False

        if "relData" in mapping:
            question["rel"] = mapping["relData"]

        if "catData" in mapping:
            question["cat"] = mapping["catData"]

        if question["isPos"]:
            if coin(0.66):
                question["ansDist"] = False
        # min([select, (0.33 if question["isPos"] else 1.0), (0.55 if question["type"] in ["verify", "logical"] else 1.0)])

        question["id"] = str(idCounter)
        question["pid"] = str(pidCounter)
        question["newTf"] = newTf
        if weights is not None:
            question["weights"] = weights
        question["key"] = key
        question["metakey"] = key.split("_")[0]

        instance["questions"][str(idCounter)] = question
        if not ansDist: # question["ansDist"]:
            instance["key2qids"][question["key"]].append(str(idCounter)) # question
        if question["ccode"] is not None:
            instance["ccode2qids"][question["ccode"]].append(str(idCounter))

        # print(question)
        # writeFile(question)
        # print(question)
        # print("O", question["key"], question["question"], question["fullAnswer"], question["answer"], "->".join(question["code"]))
        idCounter += 1

    pidCounter += 1

def gen(instance, group, codeSturcture, codeGroup, mapping, data, key, priority = 1, select = 1.0, 
        newTf = None, weights = None): # , weight
    dobjects = mapping.get("dobject", [None]) #  and "{dobject}" in :
    cdobjects = mapping.get("cdobject", [None])
    dsubjects = mapping.get("dsubject", [None]) #  and "{dobject}" in :
    cdsubjects = mapping.get("cdsubject", [None])
    
    if "object" in mapping:
        mapping["objecta"] = mapping["object"]
    if "attribute" in mapping:
        mapping["attributea"] = mapping["attribute"]

    for dobject in dobjects:
        for cdobject in cdobjects:
            for dsubject in dsubjects:
                for cdsubject in cdsubjects:

                    genMapping = copy.deepcopy(mapping)
                    genData = copy.deepcopy(data)

                    # if "type" in genData and unicode(genData["type"]).isnumeric(): # , 'utf-8'
                    #     genData["type"] = None

                    if dobject is not None:
                        genMapping["dobject"] = dobject[0]
                        if "dobject" in genData and "code" in genData["dobject"] and genData["dobject"]["code"] is None and "s" not in genData["dobject"]:
                            genData["dobject"]["code"] = dobject[1]
            
                    if cdobject is not None:
                        genMapping["cdobject"] = cdobject[0]
                        
                    if dsubject is not None:
                        genMapping["dsubject"] = dsubject[0]
                        if "dobject" in genData and "code" in genData["dobject"] and genData["dobject"]["code"] is None and "s" in genData["dobject"]:
                            genData["dobject"]["code"] = dsubject[1] # dsubject

                    if cdsubject is not None:
                        genMapping["cdsubject"] = cdsubject[0]

                    # attr normalization
                    attrFields = ["attribute", "attribute2", "cAttribute", "cAttribute2"]
                    for a in attrFields:
                        if a in genMapping:
                            if adjForm(genMapping[a]) != "" and ("material" not in group.lower()) \
                                    and ("material" not in mapping): # Attr in
                                genMapping[a] = adjForm(genMapping[a])
                            else: # if len(getSyms(mapping[a], "a")) > 0:
                                noSyms = (not isAn(genMapping["object"], "alive")) and (genMapping[a] in ["sitting", "lying"])
                                candidates = [genMapping[a]] + (if nosysms [] else getSyms(genMapping[a], "a"))
                                genMapping[a] = choice(candidates)
                                if a in ["attribute", "cAttribute"]:
                                    genMapping["switch{}".format("A" if a == "attribute" else "CA")] = True

                    # obj normalization
                    objFields = ["sObject", "pObject", "csObject", "cpObject"]    
                    for o in objFields:
                        if o in genMapping and genMapping[o] is not None:
                            #if len(getSyms(mapping[o], "o")) > 0:
                            oid = o.split(" ")[0].split("~")
                            oid = oid[1] if len(oid) > 1 else ""
                            candidates = [genMapping[o]] + getSyms(genMapping[o], "o")
                            genMapping[o] = choice(candidates)
                            if oid != "":
                                genMapping[o] = annotate(genMapping[o], oid)

                    patterns = getPatterns(group, genMapping)
                    if len(patterns) > 0:
                        genQuestionRep(instance, patterns, group, codeSturcture, codeGroup, genMapping, 
                            genData, key, priority, select = select, newTf = newTf, weights = weights)

    ck = group
    if "type" in mapping:
        if mapping["type"] in ofTypes:
            ck += "O"
        if mapping["type"] in directTypes:
            ck += "2"
    if ck in shortTemplates:
        pattern, mod = shortTemplates[ck]
        genMapping = copy.deepcopy(mapping)
        genData = copy.deepcopy(data)

        unique = True
        if mod is not None:
            oid = genMapping["oid"]
            oname = instance["objects"][oid]["name"]
            ocode = [objDirCode(oid, oname)]            
            genData["dobject"]["code"] = ocode
            genMapping["d{}bject".format(mod)] = "the {}".format(oname)
            unique = isUnique(instance, oid)

        if unique:
            genQuestionRep(instance, [(pattern, 1)], group, codeSturcture, codeGroup, genMapping, 
                genData, key, priority, ansDist = True, newTf = newTf, nonProb = True, weights = weights)

def printGraph(gdata, imageId):
    writeFile(imageId)
    for oId in gdata[imageId]["objects"]:
        o = gdata[imageId]["objects"][oId]
        objLine = o["name"]
        objLine += " A: ["
        objLine += ",".join(o["attributes"])    
        objLine += "]"
        objLine += " P: ["
        if "pos" in o:
            objLine += ",".join(o["pos"])    
        objLine += "]"        
        objLine += " R: ["
        for relId in o["outRels"]:
            rel = o["outRels"][relId]
            if rel["rel"] not in ["to the right of", "to the left of"]:
                other = gdata[imageId]["objects"][rel["obj"]]
                objLine += "({}, {})".format(rel["rel"], other["name"])
        objLine += "]"
        if "of" in o and o["of"] in instance["objects"]:
            objLine += " Of: "
            objLine += gdata[imageId]["objects"][o["of"]]["name"]         # objLine += " RL: ["
        for relId in o["outRels"]:
            rel = o["outRels"][relId]
            if rel["rel"] in ["to the right of", "to the left of"]:
                other = gdata[imageId]["objects"][rel["obj"]]
                objLine += "({}, {})".format(rel["rel"], other["name"])
        objLine += "]"        
        writeFile(objLine)
    writeFile("________________________________________________________________________")

# vgData = {}
# for s in range(1): args.shard
with open(dataFilename.format("Keys")) as f:
   vgKeys = json.load(f)
   vgKeys = [k for k in vgKeys]
   # vgData = json.load(f)
   # vgData.update(json.load(f))

# trainPercent = 1 - (3 * args.tier)
# trainMax = int(trainPercent * len(vgKeys))
# valMax = trainMax + (args.tier * len(vgKeys))
# testMax = valMax + (args.tier * len(vgKeys))
# ttestMax = len(vgKeys)
# trainPercent = 1 - (3 * args.tier)
# trainMax = int(float(1)/3 * len(vgKeys))

trainkeys = loadFromFile("trainkeys.txt")
valkeys = [k for k in vgKeys if k not in trainkeys]
random.shuffle(valkeys)

valMax = int(float(1)/3 * len(valkeys))
testMax = valMax + int(float(2)/3 * len(valkeys))
ttestMax = len(valkeys)

def tierOf(index):
    lims = [("val", valMax), ("test", testMax), ("ttest", ttestMax)] # ("train", trainMax), 
    for tier, lim in lims:
        if index < lim:
            return tier
    return "ttest"

key2tier = {}
for k in trainkeys:
    key2tier[k] = "train"
for i, k in enumerate(valkeys):
    key2tier[k] = tierOf(i)

# trainKeys = []
#     # if key2tier[k] == "train":
#     #     trainKeys.append(k)

sk = multichoice(trainkeys, 37500)
ssk = multichoice(sk, 7500)
subsets2 = {
    "10k": set(ssk),
    "50k": set(sk)
}

keyrel = lambda relId: "{rel}:{oid}".format(rel = rel["rel"], oid = rel["obj"])

k = 0

def resetKey():
    global k
    k = 0

def getKey():
    global k
    ret = k
    k += 1
    return str(ret)

redo = []

if args.create:
    # keylist = list(vgData.keys()) #["2365465"]
    # random.shuffle(keylist)
    #### questions
    typeCounter = defaultdict(int)
    groupCounter = defaultdict(int)
    typeCounterG = defaultdict(int)
    groupCounterG = defaultdict(int)

    for shardIndex in range(shardsNum):
        with open(dataFilename.format(shardIndex)) as f:
            vgData = json.load(f)

        for imgIndex, imageId in enumerate(vgData):
            instance = vgData[imageId]
            for obj in instance["objects"].values():
                for i, relId in enumerate(obj["outRels"]):
                    rel = obj["outRels"][relId]
                    o = instance["objects"][rel["obj"]]
                    o["inRels"][relId] = rel

            for name, s in subsets2.items():
                if imageId in s:
                    instance["subset{}".format(name)] = True

        for imgIndex, imageId in enumerate(vgData): 
            instance = vgData[imageId]
            instance["questions"] = {}
            instance["key2qids"] = defaultdict(list)
            instance["ccode2qids"] = defaultdict(list)

            resetKey()

            # if True:
            try:
                for objId in instance["objects"]:
                    obj = instance["objects"][objId]
                    krels = set()
                    toDel = []

                    for relId in obj["outRels"]:
                        rel = obj["outRels"][relId]
                        krel = keyrel(rel)
                        if krel in krels:
                            toDel.append(relId)
                        krels.add(krel)

                    for relId in toDel:
                        obj["outRels"].pop(relId, None)
                        o = instance["objects"][rel["obj"]]
                        o["inRels"].pop(relId, None)

                newObjs = {}
                for newId in instance["objects"]:
                    new = instance["objects"][newId]
                    toDel = []
                    add = True

                    for attr in new["attributes"]:
                        if (attr, new["name"]) in toDelAttrs:
                            new["attributes"].remove(attr)

                    for oldId in newObjs:
                        old = newObjs[oldId]
                        p = strongOverlapping(coords(old), coords(new))
                        if (p > 0.87) or (p > 0.84 and \
                                (isWeakFamily(old["name"], new["name"]) or new["name"] in objSims(old["name"], wide = True))):
                            if replace(old["name"], new["name"]):
                                toDel.append(oldId)
                            else:
                                add = False
                            print(old["name"], new["name"])

                    if add:
                        for d in toDel:
                            newObjs.pop(d, None)

                        newObjs[newId] = new

                instance["objects"] = newObjs

                instance["objects"] = {oId: o for oId, o in instance["objects"].items() if o["name"] in vocab["o"]}
                for objId in instance["objects"]:
                    obj = instance["objects"][objId]        
                    obj["outRels"] = {relId: rel for relId, rel in obj["outRels"].items() if rel["obj"] in instance["objects"]}
                    obj["inRels"] = {relId: rel for relId, rel in obj["inRels"].items() if rel["subj"] in instance["objects"]}

                instance["name2obj"] = hashObjs(instance, {}, instance["objects"])

                bodyParts = [obj for obj in instance["objects"].values() if (isA(obj, "body part") or obj["name"] in ["hair", "fur", "feathers"])]
                personals = [(objId, obj) for objId, obj in instance["objects"].items() if (isAlist(obj, ["animal", "person", "toy"] or obj["name"] in toys)) and isSingular(obj["name"])]
                if len(personals) > 0:
                    for bp in bodyParts:
                        candidates = [(objId, partOfRate(bp, obj)) for objId, obj in personals]
                        contain = max(candidates, key = lambda x: x[1])
                        if contain[1] > args.iSize:
                            bp["of"] = contain[0]
                            bp["strongOf"] = True
                # printGraph(vgData, imageId)

                objs = [oid for oid in instance["objects"] if minSize(instance["objects"][oid])] # ??????

                # templates["directOf"]["extra"][
                instance["objectSet"] = defaultdict(list)
                instance["ro"] = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
                instance["sr"] = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))

                for objId in instance["objects"]:
                    obj = instance["objects"][objId]
                    objname = obj["name"]
                    instance["objectSet"][singularOf(objname)].append(objId)

                    for relId in obj["outRels"]:
                        rel = obj["outRels"][relId]
                        sid = rel["subj"]
                        oid = rel["obj"]
                        s = singularOf(instance["objects"][sid]["name"])
                        o = singularOf(instance["objects"][oid]["name"])
                        r = rel["rel"]
                        instance["ro"][r][o][s].append(sid)
                        instance["sr"][s][r][o].append(oid)

                printGraph(vgData, imageId)

                if "place" in instance and instance["place"][1] > 0.25 and instance["place"][0] not in notPlaces:
                    placek = getKey()
                    weights = {
                        "verify": 1.0,
                        "choose": 0.9, # 0.28
                        "query": 0.1, # 0.72
                    }

                    place = instance["place"][0]
                    isAroom = isAn(place, "room")
                    placeroom = "room" if isAn(place, "room") else "place" 
                    baseMapping = {"placeroom": placeroom, "place": place, "dPlace": "the {}".format(place),
                        "aPlace": "{} {}".format(geta(place), place), "how": how()} 

                    # place
                    mapping = copy.deepcopy(baseMapping)
                    mapping["adPlace"] = adRefs([place])[0]
                    data = {"type": placeroom, "attribute": place, "pointer": ["scene"]}
                    gen(instance, "place", "queryState", "queryState", mapping, data, placek, newTf = 0.7, weights = weights)

                    alts = objAlts(place)
                    if len(alts) > 0:

                        # placeVerify
                        mapping["adPlace"] = adRefs([place])[0]        
                        gen(instance, "placeVerify", "verifyState", "verifyStateT", mapping, data, placek, newTf = 0.7, weights = weights)
                        
                        # placeChoose
                        cPlace = choice(alts)
                        refs = adRefs([place, cPlace])
                        mapping["adPlace"], mapping["cadPlace"] = refs[0], refs[1]
                        data["candidates"] = [place, cPlace]
                        data["type"] = "place"
                        gen(instance, "placeChoose", "chooseState", "chooseState", mapping, data, placek, newTf = 0.7, weights = weights)

                        # placeVerifyC
                        mapping = copy.deepcopy(baseMapping)
                        cPlace = equate(cPlace) or choice(alts)
                        refs = adRefs([place, cPlace])
                        mapping["adPlace"], mapping["cadPlace"] = refs[0], refs[1]
                        data["attribute"] = cPlace
                        gen(instance, "placeVerifyC", "verifyState", "verifyStateF", mapping, data, placek, newTf = 0.7, weights = weights)
                    else:
                        print(place, "NON ALTS!!")
                if "weather" in instance and instance["weather"] in weathers:
                    weatherk = getKey()

                    weather = instance["weather"]
                    mapping = {"weather": weather}
                    if mapping["weather"] == "snowy":
                        mapping["weather"] = "snowing"
                    data = {"type": "weather", "attribute": weather, "pointer": ["scene"]}
                    
                    # weather
                    mapping["inImg"] = inImg()
                    gen(instance, "weather", "queryState", "queryState", mapping, data, weatherk, newTf = 0.5)
                    
                    # weatherVerify
                    mapping["inImg"] = inImg()
                    gen(instance, "weatherVerify", "verifyState", "verifyStateT", mapping, data, weatherk, newTf = 0.5)

                    # weatherChoose
                    mapping["inImg"] = inImg()
                    pcWeather = cWeather = candidateAttr(instance, None, weather, likely = False)
                    if weather == "clear":
                        cWeather = choice(["cloudy", "foggy", "overcast", "partly cloudy", "stormy", "rainy"])
                    mapping["cWeather"] = cWeather
                    data["candidates"] = [weather, cWeather]
                    gen(instance, "weatherChoose", "chooseState", "chooseState", mapping, data, weatherk, newTf = 0.5)
                    # if weather is None or cWeather is None:
                        # print("!!!!!!")
                        # print(weather, cWeather)

                    # weatherVerifyC
                    mapping["inImg"] = inImg()
                    cWeather = candidateAttr(instance, None, weather, likely = False)
                    if weather == "clear":
                        cWeather = choice(["cloudy", "foggy", "overcast", "partly cloudy", "stormy", "rainy"])        
                    cWeather = equate(pcWeather) or cWeather

                    mapping["cWeather"] = cWeather
                    mapping["weather"] = "snowing" if mapping["weather"] == "snowy" else mapping["weather"]
                    data["attribute"] = cWeather
                    gen(instance, "weatherVerifyC", "verifyState", "verifyStateF", mapping, data, weatherk, newTf = 0.5)

                if "location" in instance:
                    lock = getKey()

                    location = instance["location"]
                    mapping = {"location": location}
                    data = {"type": "location", "attribute": location, "pointer": ["scene"]}

                    # locationVerify
                    mapping["inImg"] = inImg()
                    gen(instance, "locationVerify", "verifyState", "verifyStateT", mapping, data, lock, newTf = 0.7)
                    
                    # locationChoose
                    mapping["inImg"] = inImg()
                    data["candidates"] = [location, "outdoors" if location == "indoors" else "indoors"] # ["indoors", "outdoors"]
                    gen(instance, "locationChoose", "chooseState", "chooseState", mapping, data, lock, newTf = 0.7)

                    # locationVerifyC
                    mapping["inImg"] = inImg()
                    cLocation = "indoors" if location == "outdoors" else "outdoors"
                    mapping["cLocation"] = cLocation
                    data["attribute"] = cLocation
                    gen(instance, "locationVerifyC", "verifyState", "verifyStateF", mapping, data, lock, newTf = 0.7)

                
                allobjs = [(objId, instance["objects"][objId]) for objId in instance["objects"]]
                people = [(objId, obj) for objId, obj in allobjs if isA(obj, "person")]
                animals = [(objId, obj) for objId, obj in allobjs if isA(obj, "animal")]
                foods = [(objId, obj) for objId, obj in allobjs if isA(obj, "food")]
                allGenderk = getKey()
                createAllQ(people, personKey, "person", "gender", "Gender", allGenderk)
                allAnimalk = getKey()
                createAllQ(animals, animalKey, "animal", "type","Animals", allAnimalk)
                
                byAge, _ = groupByKey(people, lambda person: person[1]["mAttributes"].get("age"))
                byHealth, _ = groupByKey(foods, lambda food: food[1]["mAttributes"].get("healthiness"))        
                youngk = [getKey() for _ in range(4)]
                if "young" in byAge and "old" in byAge:
                    for young in byAge["young"]:
                        for old in byAge["old"]:
                            yId, yObj = young
                            oId, oObj = old
                            createComparative(instance, yId, yObj["name"], oId, oObj["name"], "younger", choice(youngk))
                
                healthk = [getKey() for _ in range(4)] # getKey()
                if "healthy" in byHealth and "unhealthy" in byHealth:
                    for healthy in byHealth["healthy"]:
                        for uhealthy in byHealth["unhealthy"]:
                            hId, hObj = healthy
                            uId, uObj = uhealthy
                            createComparative(instance, hId, hObj["name"], uId, uObj["name"], "healthier", choice(healthk))

                uobjByColor = {c: [] for c in basicColors}
                uobjByMaterial = {m: [] for m in basicMaterials}
                uobjByShape = {s: [] for s in basicShapes}

                uObjs = [oid for oid in objs if isUnique(instance, oid)]
                for objId in uObjs:
                    obj = instance["objects"][objId]
                    objColors = [c for c in basicColors if c in obj["attributes"]] 
                    objMaterials = [m for m in basicMaterials if m in obj["attributes"]]
                    objShapes = [s for s in basicShapes if s in obj["attributes"]] 

                    if len(objColors) == 1:
                        uobjByColor[objColors[0]].append(objId)
                    if len(objMaterials) == 1:
                        uobjByMaterial[objMaterials[0]].append(objId) 
                    if len(objShapes) == 1:
                        uobjByShape[objShapes[0]].append(objId) 
                
                for c in uobjByColor:
                    colork = [getKey() for _ in range(3)] # getKey()
                    createSmdiffQ(instance, uobjByColor, c, c, "color", choice(colork))
                for m in uobjByMaterial:
                    matk = [getKey() for _ in range(3)] # getKey()
                    createSmdiffQ(instance, uobjByMaterial, m, m, "material", choice(matk))                
                for s in uobjByShape:
                    shapek = [getKey() for _ in range(3)] # getKey()
                    createSmdiffQ(instance, uobjByShape, s, s, "shape", choice(shapek))
                
                for c1, c2 in colorPairs:
                    colork = [getKey() for _ in range(3)] # getKey()
                    createSmdiffQ(instance, uobjByColor, c1, c2, "color", choice(colork))
                for m1, m2 in materialPairs:
                    matk = [getKey() for _ in range(3)] # getKey()
                    createSmdiffQ(instance, uobjByMaterial, m1, m2, "material", choice(matk))           
                shapek = [getKey() for _ in range(3)] # getKey()
                createSmdiffQ(instance, uobjByShape, "round", "square", "shape", choice(shapek))

                for objId in objs:
                    obj = instance["objects"][objId]
                    objName = obj["name"]

                    if objName in blacklistObjs:
                        continue
                    ##### object questions
                    # exist
                    objIs = isare(objName)
                    a = geta(objName)
                    sObject, pObject = formsOf(objName)
                    aany = geta(sObject, aany = True)
                    # objPrintName = random.choise([objName] + getSyms(objName, "o")) ???

                    baseMapping = {"object": objName, "sObject": sObject, "pObject": pObject, 
                        "is": objIs, "a": a, "any": aany, "oid": objId, "how": how()}

                    existk = getKey()
                    # existCk = getKey()
                    existAttrk = getKey()
                    # existLogick = getKey()
                    attrPrio = (2 if coin(0.15) else 1)
                    notPrio = (2 if coin(0.15) else 1)
                    matPrio = (2.5 if coin(0.65) else attrPrio)
                    # mat1Prio = (2 if coin(0.9) else 1)
                    if objName in existanceObjs:

                        mapping = copy.deepcopy(baseMapping)
                        mapping["inImg"] = inImg()
                        data = getObjCode(objId, obj, objName)
                        data["pointer"] = [objId]
                        gen(instance, "exist", "exist", "existT", mapping, data, existk, priority = 0.25, select = 0.4) # 0.7

                        alts = objAlts(objName)
                        alts = [a for a in alts if isMass(a) == isMass(objName)]

                        contextScoreOf = lambda x: math.sqrt(10 * (contextScore(instance, x, objName) + 0.01))
                        weightedOthers = [(ot, contextScoreOf(ot)) for ot in alts] # prob or count???? nProb[alt].get(attr, 0) 3 * 
                        other = sample(weightedOthers)
                        # done = []
                        # for other in alts: # done
                        if other is not None:
                            mapping = copy.deepcopy(baseMapping)
                            mapping["inImg"] = inImg()
                            mapping["csObject"], mapping["cpObject"] = formsOf(other)
                            mapping["cAny"] = geta(mapping["csObject"], aany = True)
                            mapping["eAny"] = "[either]=0.8" if mapping["any"] == "" else "[either]=0.3 {}".format(mapping["any"]) 
                            mapping["ecAny"] = "[either]=0.8" if mapping["cAny"] == "" else "[either]=0.3 {}".format(mapping["cAny"]) 
                            mapping["any2"] = geta(mapping["sObject"], aany = True, first = False, firstAny = mapping["cAny"])
                            mapping["cAny2"] = geta(mapping["csObject"], aany = True, first = False, firstAny = mapping["any"])
                            mapping["ca"] = geta(mapping["csObject"])
                            
                            otherId, otherObj = "-", None
                            if singularOf(other) in instance["objectSet"]:
                                otherId = instance["objectSet"][singularOf(other)][0]
                                otherObj = instance["objects"][otherId]
                            mapping["cid"] = toNumid(otherId)

                            # existOr
                            data = {"parts": []}
                            data["parts"].append(codes["exist"](getObjCode(objId, obj, objName)))
                            data["parts"].append(codes["exist"](getObjCode(otherId, otherObj, other)))
                            data["pointer"] = [objId, otherId]
                            gen(instance, "existOr", "logicOr", "existOrT", mapping, data, existk, priority = 0.3, select = 0.55) #  existLogick

                        other = equate(other) or sample(weightedOthers)
                        if other is not None:
                            mapping = copy.deepcopy(baseMapping)
                            mapping["inImg"] = inImg()
                            mapping["csObject"], mapping["cpObject"] = formsOf(other)
                            mapping["cAny"] = geta(mapping["csObject"], aany = True)
                            mapping["any2"] = geta(mapping["sObject"], aany = True, first = False, firstAny = mapping["cAny"])
                            mapping["cAny2"] = geta(mapping["csObject"], aany = True, first = False, firstAny = mapping["any"])
                            mapping["ca"] = geta(mapping["csObject"])

                            otherId, otherObj = "-", None
                            if singularOf(other) in instance["objectSet"]:
                                otherId = instance["objectSet"][singularOf(other)][0]
                                otherObj = instance["objects"][otherId]
                            mapping["cid"] = toNumid(otherId)

                            data = {"parts": []}
                            data["parts"].append(codes["exist"](getObjCode(objId, obj, objName)))
                            data["parts"].append(codes["exist"](getObjCode(otherId, otherObj, other)))
                            data["pointer"] = [objId, otherId]
                            # newMapping = copy.deepcopy(mapping)
                            # existAnd
                            if otherId != "-":
                                mapping["inImg"] = inImg()
                                mapping["a"] = geta(mapping["sObject"])                    
                                gen(instance, "existAnd", "logicAnd", "existAndT", mapping, data, existk, priority = 2) # , priority = 3 !!!!!!! TODO add back prio!!!! existLogick, 
                            # existAndC
                            elif notexists(instance, other):
                                mapping["inImg"] = inImg()
                                mapping["cpsObject"] = mapping["cpObject"] or mapping["csObject"]
                                gen(instance, "existAndC", "logicAnd", "existAndF", mapping, data, existk, priority = 2) # , priority = 3 !!!!!!! TODO add back prio!!!! existLogick, 

                        # done = []
                        for attr in obj["attributes"]:
                            weightedAlts = [(alt, statOf(alt, attr, p = False)) for alt in alts if isLikely(attr, alt)] # prob or count???? nProb[alt].get(attr, 0)
                            other = sample(weightedAlts)
                            attrType = typeOf(attr, obj)
                            isAj = isAdj(attr)
                            isP = isPrefix(attr)
                            if attrType is not None and other is not None: #\                    
                                #and (attrNotTrivial(attr, obj) or attrNotTrivial(attr, other)):
                                mapping = copy.deepcopy(baseMapping)                        
                                mapping["inImg"] = inImg()
                                mapping["csObject"], mapping["cpObject"] = formsOf(other)
                                mapping["cAny"] = geta(mapping["csObject"], aany = True)
                                mapping["any2"] = geta(mapping["sObject"], aany = True, first = False, firstAny = mapping["cAny"])
                                mapping["cAny2"] = geta(mapping["csObject"], aany = True, first = False, firstAny = mapping["any"])
                                mapping["ca"] = geta(mapping["csObject"])

                                otherId, otherObj = "-", None
                                if singularOf(other) in instance["objectSet"]:
                                    otherId = instance["objectSet"][singularOf(other)][0]
                                    otherObj = instance["objects"][otherId]
                                mapping["cid"] = toNumid(otherId)

                                data = {"parts": []}
                                data["parts"].append(codes["exist"](getObjCode(objId, obj, objName, attr = attr)))
                                data["parts"].append(codes["exist"](getObjCode(otherId, otherObj, other, attr = attr)))
                                data["pointer"] = [objId, otherId]

                                if isAj and isP: 
                                    newMapping = copy.deepcopy(mapping)
                                    newMapping["a"] = geta(objName, attr = attr)
                                    newMapping["attribute"] = attr
                                    # if "existAttrOr" not in done:
                                    gen(instance, "existAttrOr", "logicOr", "existAttrOrT", newMapping, data, existAttrk) # existk , priority = attrPrio existLogick
                                        # done.append("existAttrOr")

                                if attrType == "material" and attr in basicMats:
                                    mapping["material"] = True
                                    mapping["prop"] = "made [out]=0.03 of {attr}".format(attr = attr)
                                    mapping["cprop"] = "made [out]=0.03 of {attr}".format(attr = attr)
                                    # if "existMatOr" not in done:
                                    gen(instance, "existThatOr", "logicOr", "existAttrOrT", mapping, data, existAttrk, priority = 3) # existk existLogick
                                        # done.append("existMatOr")

                            cattro = candidateAttr(instance, obj, attr, extraObjs = alts)
                            if cattro is not None:
                                cattr, other = cattro
                                mapping = copy.deepcopy(baseMapping)                        
                                mapping["csObject"], mapping["cpObject"] = formsOf(other)
                                mapping["cAny"] = geta(mapping["csObject"], aany = True)
                                mapping["any2"] = geta(mapping["sObject"], aany = True, first = False, firstAny = mapping["cAny"])
                                mapping["cAny2"] = geta(mapping["csObject"], aany = True, first = False, firstAny = mapping["any"])
                                mapping["ca"] = geta(mapping["csObject"])

                                otherId, otherObj = "-", None
                                if singularOf(other) in instance["objectSet"]:
                                    otherId = instance["objectSet"][singularOf(other)][0]
                                    otherObj = instance["objects"][otherId]
                                mapping["cid"] = toNumid(otherId)

                                data = {"parts": []}
                                data["parts"].append(codes["exist"](getObjCode(objId, obj, objName, attr = cattr, nt = True)))
                                data["parts"].append(codes["exist"](getObjCode(otherId, otherObj, other, attr = cattr, nt = True)))
                                data["pointer"] = [objId, otherId]

                                if isAj: # and isP: 
                                    mapping["prop"] = attr
                                    mapping["cprop"] = "not {attr}".format(attr = cattr)
                                    # if "existNotOr" not in done:
                                    gen(instance, "existThatOr", "logicOr", "existNotOrT", mapping, data, existAttrk) # existk, priority = notPrio existLogick existk
                                        # done.append("existNotOr")

                                if attrType == "material" and attr in basicMats:
                                    mapping["material"] = True
                                    mapping["prop"] = "made [out]=0.03 of {attr}".format(ois = objIs, attr = attr)
                                    mapping["cprop"] = "not made [out]=0.03 of {attr}".format(ois = objIs, attr = cattr)
                                    # if "existNotMatOr" not in done:
                                    gen(instance, "existThatOr", "logicOr", "existNotOrT", mapping, data, existAttrk, priority = 3) # existk matPrio existLogick
                                        # done.append("existNotMatOr")

                        attrs = [a for a in obj["attributes"]]
                        random.shuffle(attrs)
                        # done = []
                        for attr in attrs:
                            attrType = typeOf(attr, obj)
                            isAj = isAdj(attr)
                            isP = isPrefix(attr)
                            if attrType is not None and attrNotTrivial(attr, obj):
                                if isAj and (attr[:4] != obj["name"][:4]): # (attr != "surfing") or (obj["name"] != "surfer"
                                    # existAttr
                                    mapping = copy.deepcopy(baseMapping)
                                    mapping["inImg"] = inImg()
                                    mapping["attribute"] = attr
                                    mapping["a"] = geta(objName, attr = attr)
                                    mapping["anya"] = geta(sObject, aany = True, attr = attr)
                                    data = getObjCode(objId, obj, objName, attr = attr)
                                    data["pointer"] = [objId]
                                    # if "existAttr" not in done:
                                    if isP: #  and coin(0.85)
                                        gen(instance, "existAttr", "exist", "existAttrT", mapping, data, existAttrk) # , existk priority = attrPrio , existAttrk
                                    else:
                                        mapping["a"] = geta(objName)
                                        gen(instance, "existThat", "exist", "existAttrT", mapping, data, existAttrk)
                                        # done.append("existAttr")

                                    # existAttrNot
                                    cattr = candidateAttr(instance, obj, attr)
                                    if cattr is not None:
                                        mapping["inImg"] = inImg()
                                        mapping["cAttribute"] = cattr                        
                                        mapping["a"] = geta(objName, attr = cattr)                        
                                        data = getObjCode(objId, obj, objName, attr = cattr, nt = True)
                                        data["pointer"] = [objId]
                                        # if "existAttrNot" not in done:
                                        if isP: #  and coin(0.85)
                                            gen(instance, "existAttrNot", "exist", "existNotT", mapping, data, existAttrk) #existk , priority = notPrio existAttrk, priority = (1.5 if coin(0.15) else 1)
                                        else:
                                            mapping["a"] = geta(objName)
                                            gen(instance, "existThatNot", "exist", "existNotT", mapping, data, existAttrk)                                            
                                            # done.append("existAttrNot")

                                if attrType == "material" and attr in basicMats:
                                    # existMaterial
                                    mapping = copy.deepcopy(baseMapping)
                                    mapping["inImg"] = inImg()
                                    mapping["attribute"] = attr
                                    data = getObjCode(objId, obj, objName, attr = attr)
                                    data["pointer"] = [objId]
                                    # if "existMaterial" not in done:
                                    gen(instance, "existMaterial", "exist", "existAttrT", mapping, data, existAttrk, priority = 3) #existk mat1Prio existAttrk
                                        # done.append("existMaterial")

                                    # existMaterialNot
                                    cattr = candidateAttr(instance, obj, attr)
                                    if cattr is not None:
                                        mapping["inImg"] = inImg()
                                        mapping["cAttribute"] = cattr                        
                                        data = getObjCode(objId, obj, objName, attr = cattr, nt = True)
                                        data["pointer"] = [objId]
                                        # if "existMaterialNot" not in done:
                                        gen(instance, "existMaterialNot", "exist", "existNotT", mapping, data, existAttrk, priority = 3) # existk mat1Prio existAttrk
                                            # done.append("existMaterialNot")

                                # if attrType in ["pose", "activity"]:
                                #     # existActivity
                                #     mapping = copy.deepcopy(baseMapping)
                                #     mapping["inImg"] = inImg()
                                #     mapping["attribute"] = attr
                                #     data = {"dobject": {"code": [objDirCode(objId, objName), filterByAttrCode(attr)]}}
                                #     gen(instance, "existActivity", "exist", mapping, data)

                                #     # existActivityNot
                                #     cattr = candidateAttr(obj, attr)
                                #     mapping["cAttribute"] = cattr                        
                                #     mapping["inImg"] = inImg()
                                #     data = {"dobject": {"code": [objDirCode(objId, objName), filterByNotAttrCode(cattr)]}}
                                #     gen(instance, "existActivityNot", "exist", mapping, data)

                    others = [(o, 1.3) for o in indToObjs[objName]] + [(o, 1) for o in objWeakAlts(objName)]
                    others = [(o, c) for (o, c) in others if notexists(instance, o)]
                    contextScoreOf = lambda x: ((10 * (contextScore(instance, x, objName) ** 0.4) + 0.01))
                    # mcontextScoreOf = lambda x: math.sqrt(10 * ((0.35 * probs["oo1"][objName].get(x, 0) + 0.65 * contextScore(instance, x, objName)) + 0.01))
                    weightedOthers = [(ot, contextScoreOf(ot) * c) for (ot, c) in others] # prob or count???? nProb[alt].get(attr, 0) 3 * 
                    # moreOthers = 
                    # allOthers
                    other = sample(weightedOthers)

                    if other is not None:# len(others) > 0:
                        # other = choice(others)
                        sObject, pObject = formsOf(other)
                        psObject = pObject or sObject

                        aany = geta(sObject, aany = True)
                        isp = isare(psObject)

                        existMapping = {"object": other, "sObject": sObject, "pObject": pObject, 
                            "psObject": psObject, "any": aany, "isp": isp}
                        
                        mapping = copy.deepcopy(existMapping)
                        mapping["inImg"] = inImg()
                        data = getObjCode("-", None, other)
                        data["pointer"] = ["-"]
                        gen(instance, "existC", "exist", "existF", mapping, data, existk, priority = 0.25, select = 0.4) # existCk

                        # # alts = objAlts(objName)
                        # for another in alts:
                        #     if notexists(instance, another) and :
                        # other = sample(weightedOthers)
                        others = [o for o in others if singularOf(o) != singularOf(other) and catn(o) == catn(other)] # ?????????????????????
                        weightedOthers = [(ot, contextScoreOf(ot)) for ot in others] # prob or count???? nProb[alt].get(attr, 0)
                        another = sample(weightedOthers)

                        if another is not None: # len(others) > 0:
                            another = choice(others)
                            mapping = copy.deepcopy(existMapping)
                            mapping["inImg"] = inImg()
                            mapping["csObject"], mapping["cpObject"] = formsOf(another)
                            mapping["cpsObject"] = mapping["cpObject"] or mapping["csObject"]
                            mapping["cAny"] = geta(mapping["csObject"], aany = True)
                            mapping["eAny"] = "[either]=0.8" if mapping["any"] == "" else "[either]=0.3 {}".format(mapping["any"])
                            mapping["ecAny"] = "[either]=0.8" if mapping["cAny"] == "" else "[either]=0.3 {}".format(mapping["cAny"]) 
                            mapping["any2"] = geta(mapping["sObject"], aany = True, first = False, firstAny = mapping["cAny"])
                            mapping["cAny2"] = geta(mapping["csObject"], aany = True, first = False, firstAny = mapping["any"])                
                            mapping["cid"] = None

                            data = {"parts": []}
                            data["parts"].append(codes["exist"](getObjCode(objId, obj, objName)))
                            data["parts"].append(codes["exist"](getObjCode("-", None, other)))
                            data["pointer"] = ["-", "-"]
                            gen(instance, "existOrC", "logicOr", "existOrF", mapping, data, existk, priority = 3, select = 0.55) # existCk

                    if catSize(obj):
                        seed = getKey()

                        isMain = isMainObj(obj)
                        cats = uniqueCats(instance, objId, q = True)
                        weights = [1,3,4,4,4,4,4]
                        if len(cats) > 1 and cats[0] == "food":
                            weights[0] = 0
                        cat = sample([(cats[i], weights[i]) for i in range(len(cats))])
                        # for cat in cats:
                        if cat is not None:
                            catk = seed + "_1"

                            mapping = copy.deepcopy(baseMapping)
                            mapping["catData"] = cat
                            mapping["inImg"] = inImg()
                            mapping["othis"] = thises(obj)
                            mapping["ois"] = mapping["is"]
                            mapping["category"], mapping["is"] = catNormalize(obj, cat, k = False)
                            mapping["kategory"], mapping["kis"] = catNormalize(obj, cat, k = True)
                            mapping["kit"] = "it" if mapping["kis"] else "these"
                            data = getObjCode(objId, obj, cat)
                            data["pointer"] = [objId]
                            gen(instance, "category", "queryObject", "queryObject", mapping, data, catk)

                            mapping = copy.deepcopy(baseMapping)
                            mapping["catData"] = cat
                            mapping["othis"] = thises(obj)
                            mapping["ois"] = mapping["is"]
                            mapping["category"], mapping["is"] = catNormalize(obj, cat, k = False)
                            mapping["kategory"], mapping["kis"] = catNormalize(obj, cat, k = True)
                            mapping["this"] = thisesBool(mapping["kis"], isMainObj(obj))
                            
                            if isMain:
                                data = getObjCode(objId, obj, cat)
                                data["pointer"] = [objId]
                                gen(instance, "categoryThis", "queryObject", "queryObject", mapping, data, catk, priority = 2) # (2 if coin(0.3) else 1)

                            alts = objAlts(objName)
                            alts = [a for a in alts if isAn(a, cat)]
                            nAlts = [a for a in alts if notexists(instance, a)] # ??????????????????
                            contextScoreOf = lambda x: math.sqrt(10 * (contextScore(instance, x, objName) + 0.01))
                            weightedOthers = [(ot, contextScoreOf(ot)) for ot in alts] # prob or count???? nProb[alt].get(attr, 0) 3 * 
                            other = sample(weightedOthers)
                            # other = choice(alts)
                            # for other in alts:
                            if other is not None:
                                s, p = formsOf(other)
                                mapping["cObject"] = s if mapping["ois"] == "is" else p
                                mapping["ca"] = geta(mapping["cObject"])
                                mapping["cid"] = None
                                data["candidates"] = [objName, other]
                                data["pointer"] = [objId]
                                gen(instance, "categoryThisChoose", "chooseObject", "chooseObject", mapping, data, catk) 

                        catAttrk = seed + "_2"
                        catAttrChoosek = seed + "_3"
                        # catAttrNotk = getKey()
                        catMatPrio = (2 if coin(0.9) else 1)
                        # catcPrio = (0.5 if coin(0.35) else 1)
                        for attr in obj["attributes"]:
                            attrType = typeOf(attr, obj)
                            isAj = isAdj(attr)
                            cats = uniqueACats(instance, objId, attr, q = True)
                            weights = [1,3,4,4,4,4,4]
                            if len(cats) > 1 and cats[0] == "food":
                                weights[0] = 0                
                            cat = sample([(cats[i], weights[i]) for i in range(len(cats))])                
                            if cat is not None:    
                                mapping = copy.deepcopy(baseMapping)
                                mapping["catData"] = cat
                                mapping["inImg"] = inImg()
                                mapping["category"], mapping["is"] = catNormalize(obj, cat, k = False)
                                mapping["kategory"], mapping["kis"] = catNormalize(obj, cat, k = True)
                                data = getObjCode(objId, obj, cat, attr = attr)
                                data["pointer"] = [objId]

                                if isAj:
                                    mapping["attribute"] = attr
                                    gen(instance, "categoryAttr", "queryObject", "queryAttrObject", mapping, data, catAttrk) 
                                if attrType == "material" and attr in basicMats:
                                    mapping["material"] = True
                                    mapping["prop"] = "made of {}".format(attr)
                                    gen(instance, "categoryThat", "queryObject", "queryAttrObject", mapping, data, catAttrk, priority = 3)  # catMatPrio

                            for cat in cats[::-1]:
                                _, otherIds = uniqueO(instance, objId, cat)
                                
                                otherIdsR = [(xid, instance["objects"][xid]) for xid in otherIds if xid in instance["objects"]]
                                simsObj = objSims(objName)
                                otherCond = lambda x: sub(x, cat) and mod(x["name"]) == mod(objName) and \
                                    (x["name"] not in simsObj) and (singularOf(x["name"]) != singularOf(objName)) and \
                                    (not overlapping(coords(x), coords(obj)))
                                otherIds = [xid for xid, x in otherIdsR if otherCond(x)]

                                asims = attrSims(attr)
                                aalts = attrAlts(obj, attr)
                                otherss = [(i, instance["objects"][i]) for i in otherIds if i in instance["objects"]]
                                otherss = [(i,o) for i, o in otherss if not(any([a in o["attributes"] for a in asims]))]
                                goodOtherss = [i for i, o in otherss if any([a in o["attributes"] for a in aalts])]
                                if len(goodOtherss) > 0:
                                    otherId = choice(goodOtherss)
                                else:
                                    weightedAlts = [(i, statOf(o["name"], attr, p = False)) for i,o in otherss] # prob or count???? nProb[alt].get(attr, 0)
                                    otherId = sample(weightedAlts)

                                if otherId is not None:
                                # for otherId in otherIds:
                                    other = instance["objects"][otherId]
                                    # if sub(other, cat) and mod(other["name"]) == mod(objName): #  isPlural(other["name"]) == isPlural(objName)
                                    mapping = {"object": objName, "is": isare(objName)}
                                    mapping["catData"] = cat
                                    mapping["inImg"] = inImg()
                                    mapping["kategory"], mapping["kis"] = catNormalize(obj, cat, k = True)
                                    mapping["category"], mapping["is"] = catNormalize(obj, cat, k = False)
                                    mapping["dobject"], mapping["aobject"], mapping["dpobject"] = definedRef(instance, objId, direct = True, answer = True)["the"]
                                    mapping["cdobject"], mapping["caobject"], mapping["cdpobject"] = definedRef(instance, otherId, direct = True, answer = True)["the"]
                                    # data["candidates"] = [objName, other["name"]]

                                    if isAj:
                                        mapping["prop"] = attr
                                        if adjForm(mapping["prop"]) != "":
                                            mapping["prop"] = adjForm(mapping["prop"])
                                        data = getObjCode(objId, obj, cat, attr = attr)
                                        data["candidates"] = [objName, other["name"]]
                                        data["pointer"] = [objId]
                                        # if "categoryThatChoose" not in done:
                                        gen(instance, "categoryThatChoose", "chooseObject", "chooseAttrObject", mapping, data, catAttrChoosek)
                                        # done.append("categoryThatChoose")

                                        altMapping = copy.deepcopy(mapping)
                                        altMapping["dobject"], altMapping["cdobject"] = \
                                            altMapping["cdobject"], altMapping["dobject"]
                                        altMapping["aobject"], altMapping["caobject"] = \
                                            altMapping["caobject"], altMapping["aobject"]
                                        altMapping["dpobject"], altMapping["cdpobject"] = \
                                            altMapping["cdpobject"], altMapping["dpobject"]                                                                        
                                        altMapping["object"] = other["name"]
                                        altMapping["prop"] = "not {}".format(altMapping["prop"])
                                        data = getObjCode(otherId, other, cat, attr = attr, nt = True)                                
                                        data["candidates"] = [objName, other["name"]]
                                        data["pointer"] = [objId]
                                        gen(instance, "categoryThatChoose", "chooseObject", "chooseNotObject", altMapping, data, catAttrChoosek) # , priority = catcPrio
                                        altMapping["a"] = geta(other["name"])                            
                                        gen(instance, "categoryThat", "queryObject", "queryNotObject", altMapping, data, catAttrk) # catAttrNotk

                                        # categoryThat

                                    if attrType == "material" and attr in basicMats:
                                        mapping["material"] = True
                                        mapping["prop"] = "made of {}".format(attr)
                                        data = getObjCode(objId, obj, cat, attr = attr)
                                        data["candidates"] = [objName, other["name"]]
                                        data["pointer"] = [objId]
                                        gen(instance, "categoryThatChoose", "chooseObject", "chooseAttrObject", mapping, data, catAttrChoosek, priority = 3) # catMatPrio

                                        # altMapping = copy.deepcopy(mapping)
                                        # altMapping["dobject"], altMapping["cdobject"] = \
                                        #     altMapping["cdobject"], altMapping["dobject"]
                                        # altMapping["aobject"], altMapping["caobject"] = \
                                        #     altMapping["caobject"], altMapping["aobject"]
                                        # altMapping["dpobject"], altMapping["cdpobject"] = \
                                        #     altMapping["cdpobject"], altMapping["dpobject"]                                    
                                        # altMapping["object"] = other["name"]
                                        # altMapping["prop"] = "not {}".format(altMapping["prop"])
                                        # data = getObjCode(otherId, other, cat, attr = attr, nt = True)
                                        # data["candidates"] = [objName, other["name"]]
                                        # gen(instance, "categoryThatChoose", "chooseObject", altMapping, data, catAttrChoosek, priority = (2 if coin(0.9) else 1))
                                        # gen(instance, "categoryThat", "queryObject", mapping, data, catAttrk, priority = (2 if coin(0.9) else 1))

                    if isMainObj(obj):
                        maink = getKey()
                        mapping = copy.deepcopy(baseMapping)
                        alts = objAlts(objName)
                        nAlts = [a for a in alts if notexists(instance, a) and isMass(a) == isMass(objName)]
                        other = choice(nAlts)
                        # for other in alts:
                            # if notexists(instance, other):
                        if other is not None:
                            s, p = formsOf(other, fltr = False)
                            mapping["this"] = thises(obj)
                            mapping["cObject"] = s if mapping["is"] == "is" else p
                            if mapping["cObject"] is None or mapping["cObject"] not in vocab["o"]:
                                print(other, mapping["cObject"]) 
                            mapping["ca"] = geta(mapping["cObject"]) # geta(mapping["cObject"])
                            mapping["what"], _ = wh(obj, where = False)
                            mapping["cid"] = None
                            data = getObjCode(objId, obj, "this")
                            data["candidates"] = [objName, other]
                            data["pointer"] = [objId]
                            gen(instance, "objThisChoose", "chooseObject", "chooseObject", mapping, data, maink) 

                    posk = getKey()
                    # done = []
                    pre = None
                    if "pos" in obj and isWeakExistObj(obj["name"], strong = True) and (obj["name"] not in tabletop): #  and isUnique(instance, objId)
                        for pos in obj["pos"]:
                            if pos != "middle" and consistent(instance, objId, lambda obj: pos in obj.get("pos", [])):
                                position = pos2phrase[pos]
                                cPos = cPoses[pos]
                                cPosition = pos2phrase[cPos]
                                objIs = isare(objName)
                                side = sideOf(pos)
                                prob = probSideOf(pos)
                                posType = "hposition" if pos in ["left", "right"] else "vposition"

                                mapping = {"is": objIs, "pos": pos, "position": position, "cPosition": cPosition, "side": side}
                                
                                pre = definedRef(instance, objId, direct = True, answer = True, onlyPrefix = True)["the"]
                                mapping["dobject"], mapping["aobject"], mapping["dpobject"] = pre
                                data = {"dobject": {"code": None}, "attribute": pos, "type": posType, "pointer": [objId]}

                                # if "positionVerify" not in done:
                                mapping["prob"] = str(0.35 + prob)
                                gen(instance, "positionVerify", "verifyAttr", "verifyAttrT", mapping, data, posk)
                                    # done.append("positionVerify")

                                mapping["dobject"], mapping["aobject"], mapping["dpobject"] = equate(pre) or definedRef(instance, objId, direct = True, answer = True, onlyPrefix = True)["the"]
                                data = {"dobject": {"code": None}, "attribute": cPos, "type": posType, "pointer": [objId]}
                                # if "positionVerifyC" not in done:
                                gen(instance, "positionVerifyC", "verifyAttr", "verifyAttrF", mapping, data, posk)
                                    # done.append("positionVerifyC")

                                mapping["dobject"], mapping["aobject"], mapping["dpobject"] = equate(pre) or definedRef(instance, objId, direct = True, answer = True, onlyPrefix = True)["the"]
                                mapping["inImg"] = inImg()                    
                                data = {"dobject": {"code": None}, "candidates": [pos, cPos], "type": posType, "pointer": [objId]}
                                # if "positionChoose" not in done:
                                mapping["prob"] = str(0.5 + prob)
                                gen(instance, "positionChoose", "chooseAttr", "chooseAttr", mapping, data, posk)
                                    # done.append("positionChoose")

                                mapping["dobject"], mapping["aobject"], mapping["dpobject"] = equate(pre) or definedRef(instance, objId, direct = True, answer = True, onlyPrefix = True)["the"]
                                mapping["inImg"] = inImg()
                                data = {"dobject": {"code": None}, "attribute": pos, "type": posType, "pointer": [objId]}                        
                                mapping["prob"] = str(0.65 + prob)
                                gen(instance, "positionQuery", "queryAttr", "queryAttr", mapping, data, posk)

                    mattrk = getKey()
                    pre = None
                    if "type" in obj["mAttributes"] and isUnique(instance, objId):
                        attr = obj["mAttributes"]["type"]
                        cattr = choice([a for a in subtypes[objName] if a != attr]) 
                        attrType = "flavor" if (attr in flavors) else None
                        objIs = isare(objName)
                        objDoes = dodoes(objName)
                        objHas = hashave(objName)
                        objThis = thises(obj)
                        ref = pronounOf(obj)[1]
                        if ref == "the_person":
                            ref = "he"

                        mapping = {"is": objIs, "does": objDoes, "has": objHas, "ref": ref, "this": objThis, 
                           "attribute": attr, "cAttribute": cattr, "type": attrType, "types": [attrType], 
                           "object": objName, "oid": objId}
                        pre = definedRef(instance, objId, direct = False, short = True)["the"] # , direct = True
                        mapping["dobject"], mapping["aobject"], mapping["dpobject"] = pre
                        data = {"dobject": {"code": None}, "attribute": attr, "type": "type" if attrType is None else attrType, "pointer": [objId]}

                        if attrType == "flavor":
                            gen(instance, "directOf", "queryAttr", "queryAttr", mapping, data, mattrk)
                            cattr = equate(cattr) or choice([a for a in subtypes[objName] if a != attr]) 
                            mapping["dobject"], mapping["aobject"], mapping["dpobject"] = equate(pre) or definedRef(instance, objId, direct = False, short = True)["the"] # , direct = True
                            gen(instance, "directWhich", "queryAttr", "queryAttr", mapping, data, mattrk)

                        cattr = equate(cattr) or choice([a for a in subtypes[objName] if a != attr]) 
                        mapping["dobject"], mapping["aobject"], mapping["dpobject"] = equate(pre) or definedRef(instance, objId, direct = False, short = True)["the"] # , direct = True            
                        gen(instance, "typeVerify", "verifyAttr", "verifyAttrT", mapping, data, mattrk)

                        cattr = equate(cattr) or choice([a for a in subtypes[objName] if a != attr]) 
                        mapping["dobject"], mapping["aobject"], mapping["dpobject"] = equate(pre) or definedRef(instance, objId, direct = False, short = True)["the"] # , direct = True            
                        data = {"dobject": {"code": None}, "attribute": cattr, "type": attrType, "pointer": [objId]}
                        gen(instance, "typeVerifyC", "verifyAttr", "verifyAttrF", mapping, data, mattrk)

                        cattr = equate(cattr) or choice([a for a in subtypes[objName] if a != attr]) 
                        mapping["dobject"], mapping["aobject"], mapping["dpobject"] = equate(pre) or definedRef(instance, objId, direct = False, short = True)["the"] # , direct = True            
                        data = {"dobject": {"code": None}, "candidates": [attr, cattr], "type": attrType, "pointer": [objId]}
                        gen(instance, "typeChoose", "chooseAttr", "chooseAttr", mapping, data, mattrk)

                    if "mRels" in obj and isAlist(obj, ["person", "animal"]):
                        for mrel in obj["mRels"]:
                            seed = getKey()
                            mrelsk = seed + "_1"
                            mrelok = seed + "_2"
                            mrelvk = seed + "_3"
                            if mrel != "casting":
                            # relName = srelName = mrel
                            # ois = qis = isare(objName)
                            # sIs = "is"
                            # if shouldBeSimple(mrel, obj):
                            #     relName = toSimple(mrel, obj["name"])
                            #     srelName = toSimpleP(mrel, "is")
                            #     ois = sIs = ""
                            #     subjQis = dodoes(sName)
                            # qattr = "{r} {a}".format(r = srelName, a = obj["mRels"][mrel])
                            # , "srel": mrel

                                ois = isare(objName)
                                attr = "{r} {a}".format(r = mrel, a = obj["mRels"][mrel])
                                mapping = {"is": ois, "sis": "is", "qis": ois, "object": objName, 
                                    "attribute": attr, "qattribute": attr, "rel": mrel, "qrel": mrel, 
                                    "relq": mrel, "what": "what", "of": "", "suffix": "", "oid": objId}
                                    
                                mapping["dobject"], mapping["aobject"], mapping["dpobject"] = definedRef(instance, objId, direct = False, short = True)["the"] # direct = True

                                mapping["inImg"] = inImg()
                                data = getObjCode(objId, obj, "person", attr = attr)
                                data["pointer"] = [objId]
                                gen(instance, "activityWho", "queryObject", "queryObject", mapping, data, mrelsk)

                                if mrel in mRelActivity:
                                    data = {"dobject": {"code": None}, "type": attrType, "pointer": [objId]}     
                                    gen(instance, "activity", "queryAttr", "queryAttr", mapping, data, mrelok)

                                if (mrel in mRelWhere):
                                    mapping["rel"] = mapping["qrel"] = mapping["relq"] = mRelWhere[mrel]
                                    mapping["dsubject"], mapping["asubject"], mapping["dpsubject"] = definedRef(instance, objId, direct = False, short = True)["the"] 
                                    mapping["dobject"], mapping["aobject"] = [(obj["mRels"][mrel], None)], obj["mRels"][mrel]
                                    mapping["object"] = obj["mRels"][mrel] 
                                    data = {"dobject": {"code": None, "s": True}, "rel": mRelWhere[mrel], "tId": "-", "tName": obj["mRels"][mrel], "subj": False, "pointer": [objId]} # dsubject
                                    gen(instance, "dir", "queryRel", "queryRel", mapping, data, mrelok)

                                    gen(instance, "relVerify", "verifyRel", "verifyRelT", mapping, data, mrelvk)
                                    other = choice([d for d in mRelWhereDir[mrel] if d != obj["mRels"][mrel]])
                                    mapping["cdobject"] = [(other, None)]
                                    data = {"dobject": {"code": None, "s": True}, "rel": mrel, "tId": "-", "tName": other, "subj": False, "pointer": [objId]} # dsubject
                                    gen(instance, "relVerifyCo", "verifyRel", "verifyRelF", mapping, data, mrelvk)

                                if mrel in mRelWhat:
                                    mapping["dsubject"], mapping["asubject"], mapping["dpsubject"] = definedRef(instance, objId, direct = True)["the"] 
                                    mapping["dobject"], mapping["aobject"] = [(obj["mRels"][mrel], None)], obj["mRels"][mrel]
                                    mapping["object"] = obj["mRels"][mrel].replace("the ", "").replace("a ", "") # lastWord(attr) # " ".join(attr #
                                    data = {"dobject": {"code": None, "s": True}, "rel": mrel, "tId": "-", "tName": obj["mRels"][mrel], "subj": False, "pointer": [objId]} # dsubject
                                    gen(instance, "relO", "queryRel", "queryRel", mapping, data, mrelok)

                                    if mapping["object"] in games:
                                        gen(instance, "relVerify", "verifyRel", "verifyRelT", mapping, data, mrelvk)
                                        other = choice([g for g in games if g != obj["mRels"][mrel]])
                                        mapping["cdobject"] = [(other, None)]
                                        data = {"dobject": {"code": None, "s": True}, "rel": mrel, "tId": "-", "tName": other, "subj": False, "pointer": [objId]} # dsubject
                                        gen(instance, "relVerifyCo", "verifyRel", "verifyRelF", mapping, data, mrelvk)

                    typeToAttrs = createAttrsDict(obj)
                    attrAndk1 = getKey()
                    attrAndk2 = getKey()

                    for attr in obj["attributes"]:
                        seed = getKey()
                        attrk = seed + "_1"
                        # attrOAndk = getKey()
                        attrkWho = seed + "_2" # getKey()

                        ##### attribute questions
                        attrType = typeOf(attr, obj)
                        isAj = isAdj(attr)
                        isP = isPrefix(attr)
                        look = lookOf(isP)
                        # alts = attrAlts(obj, attr)
                        cattr = None
                        if isAttrObj(obj["name"]) and attrType is not None and len(typeToAttrs[attrType]) == 1:
                            # TODO: more refined handling
                            # all(a not in alts for a in obj["attributes"])
                            #############  and isUnique(instance, objId) ????????????????
                            objIs = isare(objName)
                            objWas = waswere(objName)
                            objDoes = dodoes(objName)
                            objHas = hashave(objName)
                            objThis = thises(obj)
                            ref = pronounOf(obj)[1]
                            if ref == "the_person":
                                ref = "he"                
                            a = geta(objName)
                            sObject, pObject = formsOf(objName)
                            aany = geta(objName, aany = True)                  

                            ###### MORE INTERESTING REFS!!
                            baseMapping = {"is": objIs, "was": objWas, "does": objDoes, "has": objHas, "ref": ref,
                                "a": a, "any": aany, "this": objThis, "type": attrType, "types": [attrType], "attribute": attr, 
                                "sObject": sObject, "pObject": pObject, "object": objName, "oid": objId, "look": look, "how": how()}

                            for attr2 in obj["attributes"]:
                                attrType2 = typeOf(attr2, obj)
                                isA2 = isAdj(attr2)
                                isP2 = isPrefix(attr2)
                                # alts2 = attrAlts(obj, attr2)
                                if attr2 != attr and attrType2 is not None and attrType2 != attrType \
                                    and len(typeToAttrs[attrType2]) == 1:
                                    if ("color" in [attrType, attrType2]) and ("24" in [attrType, attrType2]):
                                        continue
                                    # all(attr2 not in alts2 for attr in obj["attributes"]):
                                    
                                    if isAj and isA2 and isP and isP2: #\
                                        #    and attrNotTrivial(attr, obj) or attrNotTrivial(attr2, obj): 
                                        # verifyAttrs
                                        mapping = copy.deepcopy(baseMapping)
                                        mapping["types"].append(attrType2)
                                        mapping["dobject"], mapping["aobject"], mapping["dpobject"] = definedRef(instance, objId, direct = False, short = True, blackAType = mapping["types"])["ref"] # False, short = True
                                        mapping["attribute2"] = attr2
                                        mapping["type2"] = attrType2
                                        data = {"dobject": {"code": None}, "attributes": [attr, attr2], "type": mapping["types"], "pointer": [objId]}
                                        gen(instance, "verifyAttrs", "verifyAttrs", "verifyAttrsT", mapping, data, attrAndk1)

                                        # verifyAttrsC
                                        cattr2 = candidateAttr(instance, obj, attr2) # , likely = False
                                        if cattr2 is not None:
                                            mapping = copy.deepcopy(baseMapping)
                                            mapping["types"].append(attrType2)
                                            mapping["dobject"], mapping["aobject"], mapping["dpobject"] = definedRef(instance, objId, direct = False, short = True, blackAType = mapping["types"])["ref"] #direct = True,  
                                            mapping["attribute2"] = attr2
                                            mapping["type2"] = attrType2
                                            mapping["cAttribute2"] = cattr2
                                            data = {"dobject": {"code": None}, "attributes": [attr, cattr2], "type": mapping["types"], "pointer": [objId]}
                                            gen(instance, "verifyAttrsC", "verifyAttrs", "verifyAttrsF", mapping, data, attrAndk1)

                            # singularOf(other) in instance["objectSet"]:
                            # objAlts(other, indicators = False) ##### ALTS or same cat???
                            sameCat = cat2objs[catOf(obj)] 
                            # done = []
                            for otherId in objs:
                                otherObj = instance["objects"][otherId]
                                other = otherObj["name"]
                                otherTypeToAttrs = createAttrsDict(otherObj)
                                if otherId != objId and other in sameCat and isAttrObj(other) and \
                                    mod(other) == mod(objName) and attr in otherObj["attributes"] and \
                                    isWeakExistObj(other) and isWeakExistObj(objName) and \
                                    len(otherTypeToAttrs[attrType]) == 1: # isPlural(other) == isPlural(objName)
                                        #and isUnique(instance, otherId) and isLikely(attr, other): # if isAttrObj(obj) and 
                                        # ????????????????????? weakly exist???????????????????

                                    mapping = copy.deepcopy(baseMapping)
                                    # DO NOT CHANGE to short without fixing code for that!!!!
                                    mapping["dobject"], mapping["aobject"], mapping["dpobject"] = definedRef(instance, objId, direct = False, short = True, blackAType = [attrType])["the"]
                                    mapping["cdobject"], mapping["caobject"], _ = definedRef(instance, otherId, direct = False, short = True, blackAType = [attrType])["the"]
                                    data = {"parts": []}
                                    dataT = getObjCode(objId, obj, objName) # , clean = True
                                    dataT.update({"attribute": attr, "type": attrType})
                                    data["parts"].append(codes["verifyAttr"](dataT))
                                    dataT = getObjCode(otherId, otherObj, other)
                                    dataT.update({"attribute": attr, "type": attrType})
                                    data["parts"].append(codes["verifyAttr"](dataT))
                                    data["pointer"] = [objId, otherId]
                                    # if attr in other["attributes"]:
                                    if isAj:
                                        # if "verifyAttrAnd" not in done:
                                        gen(instance, "verifyAttrAnd", "logicAnd", "verifyAttrAndT", mapping, data, attrAndk2) # attrOAndk
                                            # done.append("verifyAttrAnd")
                                    if attrType == "material":
                                        # if "verifyMaterialAnd" not in done:
                                        gen(instance, "verifyMaterialAnd", "logicAnd", "verifyAttrAndT", mapping, data, attrAndk2, priority = 3) # matPrio attrOAndk
                                            # done.append("verifyMaterialAnd")
                                    # else: 
                                    #     if isAj:
                                    #         gen(instance, "verifyAttrAndC", "logicAnd", mapping, data)
                                    #     if attrType == "material":
                                    #         gen(instance, "verifyMaterialAndC", "logicAnd", mapping, data)

                            ##### FIX!! not attr/material
                            pre = None
                            if isUnique(instance, objId):
                                alts = objAlts(objName)
                                goodAlts = [alt for alt in alts if notexists(instance, alt) and isLikely(attr, alt)]
                                weightedAlts = [(alt, statOf(alt, attr, p = False)) for alt in goodAlts] # prob or count???? nProb[alt].get(attr, 0)
                                other = sample(weightedAlts)

                                if other is not None:
                                    # for other in alts: # done
                                    #     if notexists(instance, other) and isLikely(cattr, other):
                                    mapping = copy.deepcopy(baseMapping)
                                    mapping["inImg"] = inImg()
                                    mapping["csObject"], mapping["cpObject"] = formsOf(other)
                                    mapping["cAny"] = geta(mapping["csObject"], aany = True)
                                    mapping["any2"] = geta(mapping["sObject"], aany = True, first = False, firstAny = mapping["cAny"])
                                    mapping["cAny2"] = geta(mapping["csObject"], aany = True, first = False, firstAny = mapping["any"])                

                                    otherId, otherObj = "-", None
                                    mapping["cid"] = None
                                    # if singularOf(other) in instance["objectSet"]:
                                    #     otherId = instance["objectSet"][singularOf(other)][0]
                                    #     otherObj = instance["objects"][otherId]

                                    data = {"parts": []}
                                    data["parts"].append(codes["exist"](getObjCode(objId, obj, objName, attr = attr, nt = True)))                            
                                    data["parts"].append(codes["exist"](getObjCode(otherId, otherObj, other, attr = attr, nt = True)))
                                    data["pointer"] = [objId, otherId]

                                    if isAj and isP:
                                        mapping["prop"] = attr
                                        mapping["cprop"] = "not {attr}".format(attr = attr)
                                        
                                        gen(instance, "existThatOrC", "logicOr", "existNotOrF", mapping, data, existAttrk) # ,existk  priority = notPrio existLogick

                                    if attrType == "material" and attr in basicMats:
                                        mapping["material"] = True
                                        mapping["prop"] = "made [out]=0.03 of {attr}".format(attr = attr)
                                        mapping["cprop"] = "not made [out]=0.03 of {attr}".format(attr = attr)
                                        gen(instance, "existThatOrC", "logicOr", "existNotOrF", mapping, data, existAttrk) # existk, priority = matPrio existLogick 

                            # verifyAttr
                            if isAj: # and attrNotTrivial(attr, obj):  # ??????????????????????????????                                      
                                mapping = copy.deepcopy(baseMapping)
                                pre = definedRef(instance, objId, direct = False, short = True, blackAType = [attrType])["ref"] # direct = True
                                mapping["dobject"], mapping["aobject"], mapping["dpobject"] = pre
                                data = {"dobject": {"code": None}, "attribute": attr, "type": attrType, "pointer": [objId]}
                                gen(instance, "verifyAttr", "verifyAttr", "verifyAttrT", mapping, data, attrk, newTf = 0.35)

                                mapping = copy.deepcopy(baseMapping)
                                pre = definedRef(instance, objId, direct = False, short = True, blackAType = [attrType])["ref"] # direct = True
                                mapping["dobject"], mapping["aobject"], mapping["dpobject"] = pre
                                data = {"dobject": {"code": None}, "attribute": attr, "type": attrType, "pointer": [objId]}
                                gen(instance, "verifyAttrT", "verifyAttr", "verifyAttrT", mapping, data, attrk, newTf = 0.35)                                

                            # materialVerify
                            if attrType == "material":
                                mapping = copy.deepcopy(baseMapping)
                                pre = definedRef(instance, objId, direct = False, short = True, blackAType = [attrType])["ref"]
                                mapping["dobject"], mapping["aobject"], mapping["dpobject"] = pre
                                data = {"dobject": {"code": None}, "attribute": attr, "type": attrType, "pointer": [objId]}
                                gen(instance, "materialVerify", "verifyAttr", "verifyAttrT", mapping, data, attrk, newTf = 0.35)

                            # materialVerify
                            if attrType == "company":
                                mapping = copy.deepcopy(baseMapping)
                                pre = definedRef(instance, objId, direct = False, short = True, blackAType = [attrType])["ref"]
                                mapping["dobject"], mapping["aobject"], mapping["dpobject"] = pre
                                data = {"dobject": {"code": None}, "attribute": attr, "type": attrType, "pointer": [objId]}
                                gen(instance, "companyVerify", "verifyAttr", "verifyAttrT", mapping, data, attrk, newTf = 0.35)

                            # directOf
                            which = attrType in attrWhich and coin(0.5)
                            if isAj and isP: #?????? 
                                mapping = copy.deepcopy(baseMapping)
                                mapping["dobject"], mapping["aobject"], mapping["dpobject"] = equate(pre) or definedRef(instance, objId, direct = False, blackAType = [attrType])["ref"]
                                if attrType in templates["directOf"]["extra"]["synonyms"]:
                                    typeNames = [attrType] + templates["directOf"]["extra"]["synonyms"][attrType]
                                    mapping["type"] = choice(typeNames)
                                data = {"dobject": {"code": None}, "type": attrType, "pointer": [objId]}            
                                if not which:
                                    gen(instance, "directOf", "queryAttr", "queryAttr", mapping, data, attrk, newTf = 0.35)

                                # if attrType not in ["color", "texture", "pattern"]: #  or coin(0.25)
                                # directWhich
                                # if isAj and isP:                
                                mapping = copy.deepcopy(baseMapping)
                                mapping["dobject"], mapping["aobject"], mapping["dpobject"] = equate(pre) or definedRef(instance, objId, direct = False, blackAType = [attrType])["ref"]
                                if attrType in templates["directWhich"]["extra"]["synonyms"]:
                                    typeNames = [attrType] + templates["directWhich"]["extra"]["synonyms"][attrType]
                                    mapping["type"] = choice(typeNames)
                                data = {"dobject": {"code": None}, "type": attrType, "pointer": [objId]}
                                if which:
                                    gen(instance, "directWhich", "queryAttr", "queryAttr", mapping, data, attrk, newTf = 0.35)

                                # how
                                # if isAj and isP:                                
                                mapping = copy.deepcopy(baseMapping)
                                howDict = templates["how"]["extra"]["aDict"]
                                if attrType in howDict:
                                    mapping["dobject"], mapping["aobject"], mapping["dpobject"] = equate(pre) or definedRef(instance, objId, direct = False, blackAType = [attrType])["ref"]
                                    mapping["adjType"] = howDict[attrType]
                                    data = {"dobject": {"code": None}, "type": attrType, "pointer": [objId]}
                                    gen(instance, "how", "queryAttr", "queryAttr", mapping, data, attrk, priority = 4, newTf = 0.35) # (2 if coin(0.2) else 1)

                            # material
                            mapping = copy.deepcopy(baseMapping)
                            if attrType == "material" and attr in basicMats:
                                mapping["dobject"], mapping["aobject"], mapping["dpobject"] = equate(pre) or definedRef(instance, objId, direct = False, short = True, blackAType = [attrType])["ref"]             
                                data = {"dobject": {"code": None}, "type": attrType, "pointer": [objId]}            
                                gen(instance, "material", "queryAttr", "queryAttr", mapping, data, attrk, priority = 3, newTf = 0.35) # (2 if coin(0.6) else 1)

                            if attrType in ["activity", "pose", "sportActivity"] and (attr[:4] != obj["name"][:4]):
                                # activity
                                if isA(obj, "alive"):
                                    mapping = copy.deepcopy(baseMapping)
                                    mapping["dobject"], mapping["aobject"], mapping["dpobject"] = equate(pre) or definedRef(instance, objId, direct = False, short = True, blackAType = [attrType])["ref"]             
                                    mapping["qis"] = mapping["is"]
                                    data = {"dobject": {"code": None}, "type": attrType, "pointer": [objId]}            
                                    gen(instance, "activity", "queryAttr", "queryAttr", mapping, data, attrk, newTf = 0.35)
                           
                                if isA(obj, "person"):
                                    mapping = copy.deepcopy(baseMapping)                        
                                    mapping["inImg"] = inImg()
                                    mapping["dobject"], mapping["aobject"], mapping["dpobject"] = definedRef(instance, objId, direct = True, answer = True)["the"]             
                                    mapping["sis"] = "is"
                                    mapping["qattribute"] = mapping["attribute"]
                                    data = getObjCode(objId, obj, "person", attr = attr)
                                    data["pointer"] = [objId]
                                    gen(instance, "activityWho", "queryObject", "queryObject", mapping, data, attrkWho)

                                # if attrType in ["activity", "pose"]:
                                #     # existActivityC
                                #     mapping = copy.deepcopy(baseMapping)
                                #     cattr = candidateAttr(obj, attr)
                                #     mapping["cAttribute"] = cattr                    
                                #     mapping["inImg"] = inImg()
                                #     data = {"dobject": {"code": [objDirCode("-", objName), filterByAttrCode(cattr)]}}
                                #     gen(instance, "existActivityC", "exist", mapping, data)

                                #     # existActivityNotC
                                #     mapping = copy.deepcopy(baseMapping)
                                #     mapping["inImg"] = inImg()
                                #     data = {"dobject": {"code": [objDirCode(objId, objName), filterByNotAttrCode(attr)]}}
                                #     gen(instance, "existActivityNotC", "exist", mapping, data)

                            # company
                            mapping = copy.deepcopy(baseMapping)
                            if attrType == "company":
                                mapping["dobject"], mapping["aobject"], mapping["dpobject"] = equate(pre) or definedRef(instance, objId, direct = False, short = True, blackAType = [attrType])["ref"]             
                                data = {"dobject": {"code": None}, "type": attrType, "pointer": [objId]}            
                                gen(instance, "company", "queryAttr", "queryAttr", mapping, data, attrk, newTf = 0.35)

                            if attrType == "state" and objName in waters:
                                mapping["dobject"], mapping["aobject"], mapping["dpobject"] = equate(pre) or definedRef(instance, objId, direct = True)["ref"]             
                                data = {"dobject": {"code": None}, "type": attrType, "pointer": [objId]}            
                                gen(instance, "state", "queryAttr", "queryAttr", mapping, data, attrk, newTf = 0.35)        

                            if isAj:
                                # verifyAttrC                 
                                mapping = copy.deepcopy(baseMapping)
                                cattr = candidateAttr(instance, obj, attr) # ????????????????????????????????
                                if cattr is not None:
                                    mapping["cAttribute"] = cattr
                                    mapping["dobject"], mapping["aobject"], mapping["dpobject"] = equate(pre) or definedRef(instance, objId, direct = False, short = True, blackAType = [attrType])["ref"]                          
                                    data = {"dobject": {"code": None}, "attribute": cattr, "type": attrType, "pointer": [objId]}
                                    gen(instance, "verifyAttrC", "verifyAttr", "verifyAttrF", mapping, data, attrk, newTf = 0.35)

                                    mapping["cAttribute"] = cattr
                                    mapping["dobject"], mapping["aobject"], mapping["dpobject"] = equate(pre) or definedRef(instance, objId, direct = False, short = True, blackAType = [attrType])["ref"]                          
                                    data = {"dobject": {"code": None}, "attribute": cattr, "type": attrType, "pointer": [objId]}
                                    gen(instance, "verifyAttrTC", "verifyAttr", "verifyAttrF", mapping, data, attrk, newTf = 0.35)

                                # verifyAttrAndC
                                if isUnique(instance, objId):
                                    sameCat = cat2objs[catOf(obj)] 
                                    
                                    goodAlts = []
                                    for otherId in objs:
                                        other = instance["objects"][otherId]["name"]
                                        if otherId != objId and other in sameCat and isAttrObj(other) \
                                            and isWeakExistObj(other) and isWeakExistObj(objName) \
                                            and mod(other) == mod(objName): # isPlural(other) == isPlural(objName)
                                                goodAlts.append((otherId, other))
                                                #and isUnique(instance, otherId): # if isAttrObj(obj) and 
                                                # ?????????? weakly??????????????????????????????????????????
                                                 #and isLikely(cattr, other) \

                                    cattro = candidateAttr(instance, obj, attr, extraObjs = goodAlts, nameof = lambda x: x[1])
                                    # weightedAlts = [(otherId, statOf(other, cattr, p = False)) for otherId, other in goodAlts] # prob or count???? nProb[alt].get(attr, 0)
                                    # otherId = sample(weightedAlts)
                                    if cattro is not None:
                                        cattr, (otherId, other) = cattro
                                        # print(cattr, other)
                                        mapping = copy.deepcopy(baseMapping)
                                        mapping["dobject"], mapping["aobject"], mapping["dpobject"] = definedRef(instance, objId, direct = False, short = True)["the"]
                                        mapping["cdobject"], mapping["caobject"], _ = definedRef(instance, otherId, direct = False, short = True)["the"]
                                        mapping["cAttribute"] = cattr # candidateAttr(obj, attr)

                                        otherId, otherObj = "-", None
                                        if singularOf(other) in instance["objectSet"]:
                                            otherId = instance["objectSet"][singularOf(other)][0]
                                            otherObj = instance["objects"][otherId]

                                        data = {"parts": []} # , "attrType": cattr, "type": attrType
                                        dataT = getObjCode(objId, obj, objName)
                                        dataT.update({"attribute": cattr, "type": attrType})
                                        data["parts"].append(codes["verifyAttr"](dataT)) # 
                                        dataT = getObjCode(otherId, otherObj, other)
                                        dataT.update({"attribute": cattr, "type": attrType})                      
                                        data["parts"].append(codes["verifyAttr"](dataT)) # , attr = cattr, clean = True
                                        data["pointer"] = [objId, otherId]

                                        gen(instance, "verifyAttrAndC", "logicAnd", "verifyAttrAndF", mapping, data, attrAndk2) # attrOAndk

                                    # existAttrOrC
                                    alts = objAlts(objName)
                                    goodAlts = [alt for alt in alts if notexists(instance, alt)] # and isLikely(cattr, alt)
                                    cattro = candidateAttr(instance, obj, attr, extraObjs = goodAlts)
                                    # weightedAlts = [(alt, statOf(alt, cattr, p = False)) for alt in goodAlts] # prob or count???? nProb[alt].get(attr, 0)
                                    # other = sample(weightedAlts)

                                    if cattro is not None:
                                    # for other in alts:
                                        # if notexists(instance, other) and isLikely(cattrn, other):
                                        cattrn, other = cattro
                                        mapping = copy.deepcopy(baseMapping)
                                        mapping["cAttribute"] = cattrn # candidateAttr(obj, attr)     
                                        mapping["inImg"] = inImg()
                                        mapping["csObject"], mapping["cpObject"] = formsOf(other)
                                        mapping["cAny"] = geta(mapping["csObject"], aany = True)
                                        mapping["any2"] = geta(mapping["sObject"], aany = True, first = False, firstAny = mapping["cAny"])
                                        mapping["cAny2"] = geta(mapping["csObject"], aany = True, first = False, firstAny = mapping["any"])                

                                        otherId, otherObj = "-", None
                                        mapping["cid"] = None
                                        # if singularOf(other) in instance["objectSet"]:
                                        #     otherId = instance["objectSet"][singularOf(other)][0]
                                        #     otherObj = instance["objects"][otherId]

                                        data = {"parts": []}
                                        data["parts"].append(codes["exist"](getObjCode(objId, obj, objName, attr = cattrn)))
                                        data["parts"].append(codes["exist"](getObjCode(otherId, otherObj, other, attr = cattrn)))
                                        data["pointer"] = [objId, otherId]
                                        gen(instance, "existAttrOrC", "logicOr", "existAttrOrF", mapping, data, existAttrk) # existk, priority = attrPrio existLogick

                                if isUnique(instance, objId):
                                    if isP and objName in existanceObjs:
                                        # existAttrC
                                        mapping = copy.deepcopy(baseMapping)
                                        cattr = equate(cattr) or candidateAttr(instance, obj, attr)
                                        if cattr is not None:
                                            mapping["cAttribute"] = cattr                    
                                            mapping["anya"] = geta(sObject, aany = True, attr = cattr)
                                            mapping["inImg"] = inImg()
                                            data = getObjCode(objId, obj, objName, attr = cattr)
                                            data["pointer"] = [objId]
                                            if isP: #  and coin(0.85)
                                                gen(instance, "existAttrC", "exist", "existAttrF", mapping, data, existAttrk) # existk , priority = attrPrio existAttrk
                                            else:
                                                gen(instance, "existThatC", "exist", "existAttrF", mapping, data, existAttrk) # existk , priority = attrPrio existAttrk

                                            # existAttrNotC
                                            mapping = copy.deepcopy(baseMapping)
                                            mapping["inImg"] = inImg()
                                            data = getObjCode(objId, obj, objName, attr = attr, nt = True)
                                            data["pointer"] = [objId]
                                            if isP: #  and coin(0.85)
                                                gen(instance, "existAttrNotC", "exist", "existNotF", mapping, data, existAttrk) # existk, priority = notPrio existAttrk
                                            else:
                                                gen(instance, "existThatNotC", "exist", "existNotF", mapping, data, existAttrk) # existk, priority = notPrio existAttrk

                            if attrType == "material":
                                # materialVerifyC
                                mapping = copy.deepcopy(baseMapping)
                                cattr = candidateAttr(instance, obj, attr) # ????????????????????????????
                                if cattr is not None:
                                    mapping["cAttribute"] = cattr
                                    mapping["dobject"], mapping["aobject"], mapping["dpobject"] = equate(pre) or definedRef(instance, objId, direct = False, short = True, blackAType = [attrType])["ref"]  
                                    data = {"dobject": {"code": None}, "attribute": cattr, "type": attrType, "pointer": [objId]}
                                    gen(instance, "materialVerifyC", "verifyAttr", "verifyAttrF", mapping, data, attrk, newTf = 0.35)

                                if isUnique(instance, objId):
                                    # verifyMaterialAndC
                                    sameCat = cat2objs[catOf(obj)] 
                                    
                                    goodAlts = []
                                    for otherId in objs:
                                        other = instance["objects"][otherId]["name"]
                                        if otherId != objId and other in sameCat and isAttrObj(other) \
                                            and mod(other) == mod(objName): # and isLikely(cattr, other): # isPlural(other) == isPlural(objName)
                                                #and isUnique(instance, otherId): # if isAttrObj(obj) and 
                                                goodAlts.append((otherId, other))

                                    # weightedAlts = [(otherId, statOf(other, cattr, p = False)) for otherId, other in goodAlts] # prob or count???? nProb[alt].get(attr, 0)
                                    # otherId = sample(weightedAlts)
                                    cattro = candidateAttr(instance, obj, attr, extraObjs = goodAlts, nameof = lambda x: x[1])
                                    if cattro is not None:
                                        catttr, (otherId, other) = cattro
                                        mapping = copy.deepcopy(baseMapping)
                                        mapping["dobject"], mapping["aobject"], mapping["dpobject"] = definedRef(instance, objId, direct = False, short = True)["the"]
                                        mapping["cdobject"], mapping["caobject"], _ = definedRef(instance, otherId, direct = False, short = True)["the"]
                                        mapping["cAttribute"] = cattr # candidateAttr(obj, attr)

                                        otherId, otherObj = "-", None
                                        if singularOf(other) in instance["objectSet"]:
                                            otherId = instance["objectSet"][singularOf(other)][0]
                                            otherObj = instance["objects"][otherId]

                                        data = {"parts": []}
                                        dataT = getObjCode(objId, obj, objName)
                                        dataT.update({"attribute": cattr, "type": attrType})
                                        data["parts"].append(codes["verifyAttr"](dataT)) # 
                                        dataT = getObjCode(otherId, otherObj, other)
                                        dataT.update({"attribute": cattr, "type": attrType})
                                        data["parts"].append(codes["verifyAttr"](dataT))                            
                                        data["pointer"] = [objId, otherId]
                                        # data["parts"].append(getObjCode(objId, obj, objName, attr = cattr, clean = True))
                                        # data["parts"].append(getObjCode(otherId, otherObj, other, attr = cattr, clean = True))

                                        gen(instance, "verifyMaterialAndC", "logicAnd", "verifyAttrAndF", mapping, data, attrAndk2, priority = 3) # matPrio attrOAndk
                                
                                    # existThatOrC
                                    alts = objAlts(objName)
                                    goodAlts = [alt for alt in alts if notexists(instance, alt)] #  and isLikely(cattr, alt)
                                    cattro = candidateAttr(instance, obj, attr, extraObjs = goodAlts)
                                    # weightedAlts = [(alt, statOf(alt, cattr, p = False)) for alt in goodAlts] # prob or count???? nProb[alt].get(attr, 0)
                                    # other = sample(weightedAlts)
                                    # other = choice(goodAlts)
                                    if cattro is not None:
                                    # for other in alts:
                                        # if notexists(instance, other) and isLikely(cattrn, other):
                                        cattrn, other = cattro
                                        mapping = copy.deepcopy(baseMapping)
                                        mapping["inImg"] = inImg()
                                        mapping["csObject"], mapping["cpObject"] = formsOf(other)
                                        mapping["cAny"] = geta(mapping["csObject"], aany = True)
                                        mapping["any2"] = geta(mapping["sObject"], aany = True, first = False, firstAny = mapping["cAny"])
                                        mapping["cAny2"] = geta(mapping["csObject"], aany = True, first = False, firstAny = mapping["any"])                
                                        
                                        mapping["prop"] = "made [out]=0.03 of {attr}".format(attr = attr)
                                        mapping["cprop"] = "made [out]=0.03 of {attr}".format(attr = cattrn)

                                        otherId, otherObj = "-", None
                                        mapping["cid"] = None
                                        # if singularOf(other) in instance["objectSet"]:
                                        #     otherId = instance["objectSet"][singularOf(other)][0]
                                        #     otherObj = instance["objects"][otherId]

                                        data = {"parts": []}
                                        data["parts"].append(codes["exist"](getObjCode(objId, obj, objName, attr = cattrn)))
                                        data["parts"].append(codes["exist"](getObjCode(otherId, otherObj, other, attr = cattrn)))
                                        data["pointer"] = [objId, otherId]
                                        mapping["material"] = True
                                        gen(instance, "existThatOrC", "logicOr", "existAttrOrF", mapping, data, existAttrk, priority = 3) #existk matPrio  existLogick

                                if isUnique(instance, objId) and (objName in existanceObjs) and (attr in basicMats):
                                    # existMaterialC
                                    mapping = copy.deepcopy(baseMapping)
                                    cattr = equate(cattr) or candidateAttr(instance, obj, attr)
                                    if cattr is not None:
                                        mapping["cAttribute"] = cattr                    
                                        mapping["inImg"] = inImg()
                                        data = getObjCode(objId, obj, objName, attr = cattr)
                                        data["pointer"] = [objId]
                                        gen(instance, "existMaterialC", "exist", "existAttrF", mapping, data, existAttrk, priority = 3) #existk matPrio mat1Prio existAttrk

                                    # existMaterialNotC
                                    mapping = copy.deepcopy(baseMapping)
                                    mapping["inImg"] = inImg()
                                    data = getObjCode(objId, obj, objName, attr = attr, nt = True)
                                    data["pointer"] = [objId]
                                    gen(instance, "existMaterialNotC", "exist", "existNotF", mapping, data, existAttrk, priority = 3) # existk matPrio mat1Prio existAttrk

                            # companyVerifyC
                            if attrType == "company":
                                mapping = copy.deepcopy(baseMapping)
                                cattr = candidateAttr(instance, obj, attr, likely = False)
                                if cattr is not None:
                                    mapping["cAttribute"] = cattr
                                    mapping["dobject"], mapping["aobject"], mapping["dpobject"] = equate(pre) or definedRef(instance, objId, direct = False, short = True, blackAType = [attrType])["ref"]  
                                    data = {"dobject": {"code": None}, "attribute": cattr, "type": attrType, "pointer": [objId]}
                                    gen(instance, "companyVerifyC", "verifyAttr", "verifyAttrF", mapping, data, attrk, newTf = 0.35)

                            # chooseAttr
                            if isAj:                                      
                                mapping = copy.deepcopy(baseMapping)
                                cattr = equate(cattr) or candidateAttr(instance, obj, attr)
                                if cattr is not None:
                                    mapping["cAttribute"] = cattr
                                    mapping["dobject"], mapping["aobject"], mapping["dpobject"] = equate(pre) or definedRef(instance, objId, direct = False, short = True, blackAType = [attrType])["ref"] # , direct = True
                                    data = {"dobject": {"code": None}, "candidates": [attr, cattr], "type": attrType, "pointer": [objId]}
                                    gen(instance, "chooseAttr", "chooseAttr", "chooseAttr", mapping, data, attrk, newTf = 0.35)

                            # materialChoose
                            mapping = copy.deepcopy(baseMapping)
                            if attrType == "material":
                                cattr = equate(cattr) or candidateAttr(instance, obj, attr)
                                if cattr is not None:
                                    mapping["cAttribute"] = cattr
                                    mapping["dobject"], mapping["aobject"], mapping["dpobject"] = equate(pre) or definedRef(instance, objId, direct = False, short = True, blackAType = [attrType])["ref"]
                                    data = {"dobject": {"code": None}, "candidates": [attr, cattr], "type": attrType, "pointer": [objId]}
                                    gen(instance, "materialChoose", "chooseAttr", "chooseAttr", mapping, data, attrk, newTf = 0.35)

                            # activityChoose
                            mapping = copy.deepcopy(baseMapping)
                            if attrType in ["activity", "pose", "sportActivity"]:
                                if isA(obj, "alive"):
                                    cattr = candidateAttr(instance, obj, attr)
                                    if cattr is not None:
                                        mapping["cAttribute"] = cattr
                                        mapping["dobject"], mapping["aobject"], mapping["dpobject"] = equate(pre) or definedRef(instance, objId, direct = False, short = True, blackAType = [attrType])["ref"]
                                        data = {"dobject": {"code": None}, "candidates": [attr, cattr], "type": attrType, "pointer": [objId]}
                                        gen(instance, "activityChoose", "chooseAttr", "chooseAttr", mapping, data, attrk, newTf = 0.35)

                            # companyChoose
                            mapping = copy.deepcopy(baseMapping)
                            if attrType == "company":
                                cattr = equate(cattr) or candidateAttr(instance, obj, attr)
                                if cattr is not None:
                                    mapping["cAttribute"] = cattr
                                    mapping["dobject"], mapping["aobject"], mapping["dpobject"] = equate(pre) or definedRef(instance, objId, direct = False, short = True, blackAType = [attrType])["ref"]
                                    data = {"dobject": {"code": None}, "candidates": [attr, cattr], "type": attrType, "pointer": [objId]}
                                    gen(instance, "companyChoose", "chooseAttr", "chooseAttr", mapping, data, attrk, newTf = 0.35)

                            if attrType == "state" and objName in waters:
                                cattr = equate(cattr) or candidateAttr(instance, obj, attr)
                                if cattr is not None:
                                    mapping["cAttribute"] = cattr
                                    mapping["dobject"], mapping["aobject"], mapping["dpobject"] = equate(pre) or definedRef(instance, objId, direct = True)["ref"]
                                    data = {"dobject": {"code": None}, "candidates": [attr, cattr], "type": attrType, "pointer": [objId]}
                                    gen(instance, "stateChoose", "chooseAttr", "chooseAttr", mapping, data, attrk, newTf = 0.35)


                            if isMainObj(obj) and isUnique(instance, objId):
                                thisPrio = (2 if coin(0.2) else 1)
                                if isAj and isP and attrNotTrivial(attr, obj):     
                                    # "verifyAttrThis"                                                     
                                    mapping = copy.deepcopy(baseMapping)
                                    # objOutName, objRef, objCode = definedRef(instance, objId, of = False)                        
                                    # mapping["sobject"] = mapping["object"] = objOutName
                                    mapping["a"] = geta(objName, attr = attr)
                                    data = getObjCode(objId, obj, objName)
                                    data["attribute"] = attr
                                    data["type"] = attrType
                                    data["pointer"] = [objId]
                                    gen(instance, "verifyAttrThis", "verifyAttr", "verifyAttrT", mapping, data, attrk, priority = 1.5, newTf = 0.35) # thisPrio

                                    # "verifyAttrCThis"
                                    mapping = copy.deepcopy(baseMapping)
                                    cattr = equate(cattr) or candidateAttr(instance, obj, attr)
                                    if cattr is not None:
                                        mapping["cAttribute"] = cattr
                                        # objOutName, objRef, objCode = definedRef(instance, objId, of = False)
                                        # mapping["sobject"] = mapping["object"] = objOutName 
                                        mapping["a"] = geta(objName, attr = attr)
                                        mapping["ca"] = geta(objName, attr = cattr)
                                        data = getObjCode(objId, obj, objName)
                                        data["attribute"] = cattr
                                        data["type"] = attrType
                                        data["pointer"] = [objId]
                                        # data = {"dobject": {"code": objCode}, "attribute": cattr}                                
                                        gen(instance, "verifyAttrCThis", "verifyAttr", "verifyAttrF", mapping, data, attrk, priority = 1.5) # thisPrio   

                    for relId in obj["outRels"]:
                        seed = getKey()
                        relsk = seed + "_1"
                        relok = seed + "_2"
                        relck = seed + "_3"
                        relvk = seed + "_4" # choice([relsk, relok])#getKey()
                        relcck = seed + "_5"
                        # relr1k = getKey()
                        relr2k = seed + "_6"
                        cmpk = seed + "_7"

                        rel = obj["outRels"][relId]
                        relInfo = vocab["r"][rel["rel"]]
                        if relInfo["noQuestion"] or bad(instance, rel): #or trivial(rel):
                            continue  

                        sId = rel["subj"]
                        oId = rel["obj"]
                        ids = [sId, oId]
                        s = instance["objects"][sId]
                        o = instance["objects"][oId]
                        sName = s["name"]
                        oName = o["name"]
                        sCat = refcatOf(s, q = True)
                        oCat = refcatOf(o, q = True)
                        subjQis = subjIs = isare(sName)
                        subjA = geta(sName)
                        direct = (relInfo["cat"] == "direct")
                        isPos = (rel["rel"] in ["to the left of", "to the right of"])

                        if sName in blacklistObjs or oName in blacklistObjs:
                            continue

                        relName = qrelName = srelName = rel["rel"]
                        sIs = "is"
                        simple = False
                        if shouldBeSimple(rel, s):
                            relName = toSimple(relName, sName)
                            qrelName = toBasic(rel["rel"])
                            srelName = toSimpleP(rel["rel"], personOf("is"))
                            subjIs = ""
                            sIs = ""
                            subjQis = dodoes(sName)
                            simple = True

                        baseMapping = {"subject": sName, "object": oName, "a": subjA, "is": subjIs, 
                        "qis": subjQis, "rel": relName, "qrel": qrelName, "relq": relName, "ois": subjIs,
                        "srel": srelName, "sis": sIs, "suffix": "", "sid": sId, "oid": oId, "isPos": isPos, "relData": (relId, rel), "how": how()}

                        ##### subject
                        if "s" in relInfo["cases"] and (not tooGeneral(sName)):
                            smapping = copy.deepcopy(baseMapping)
                            smapping["oid"] = oId

                            if relInfo["located"] and (not isA(s, "alive")):
                                smapping["srel"] = "located {}".format(smapping["srel"])

                            if (not relInfo["catS"]) and (not isMultiSubj(instance, rel)):
                                mapping = copy.deepcopy(smapping)
                                mapping["dsubject"], mapping["asubject"], mapping["dpsubject"] = definedRef(instance, sId, direct = True, answer = True, simple = simple, noSuffix = True)["the"]
                                ref = objRef(oId, oName, rel["rel"], q = True)
                                mapping["dobject"], mapping["aobject"], mapping["dpobject"] = ref or definedRef(instance, oId, direct = False, that = direct, ithat = True, simple = simple, isSubj = False, blackObjIds = ids, blackRS = rel["rel"])["the"] # ["ref"] noSuffix = True, 
                                mapping["what"], catwh = wh(s, where = False)
                                # "sId": oId, "sName": oName, 
                                data = {"dobject": {"code": None}, "rel": rel["rel"], "tId": sId, "tName": catwh, "subj": True, "pointer": [sId]}
                                gen(instance, "relS", "queryRel", "queryRel", mapping, data, relsk)

                            if sCat is not None:
                                mapping = copy.deepcopy(smapping)
                                mapping["catData"] = sCat
                                mapping["dsubject"], mapping["asubject"], mapping["dpsubject"] = definedRef(instance, sId, direct = True, answer = True, simple = simple, noSuffix = True)["the"]
                                ref = objRef(oId, oName, rel["rel"], q = True)
                                mapping["dobject"], mapping["aobject"], mapping["dpobject"] = ref or definedRef(instance, oId, direct = False, that = direct, ithat = True, simple = simple, isSubj = False, blackObjIds = ids, blackRS = rel["rel"])["the"] # ["ref"] noSuffix = True,  lthat = direct, ithat = True, depends on that
                                
                                mapping["category"], mapping["cis"] = catNormalize(s, sCat, k = False)
                                mapping["kategory"], mapping["kis"] = catNormalize(s, sCat, k = True)
                                mapping["is"] = mapping["cis"]
                                mapping["a"] = geta(sName)
                                mapping["that"], that = thatOf(rel["rel"], subj = None)                    
                                mapping["krel"] = mapping["crel"] = rel["rel"]
                                
                                if simple:
                                    mapping["crel"] = toSimpleP(rel["rel"], personOf(mapping["cis"]))
                                    mapping["krel"] = toSimpleP(rel["rel"], personOf(mapping["kis"]))
                                    mapping["is"] = ""
                                    mapping["kis"] = ""

                                if not that:
                                    mapping["is"] = ""

                                # "sId": oId, "sName": oName, 
                                data = {"dobject": {"code": None}, "rel": rel["rel"], "tId": sId, "tName": sCat, "subj": True, "pointer": [sId]}
                                gen(instance, "categoryRelS", "queryRel", "queryRel", mapping, data, relck)
                                
                                csid = definedSubjAlt(instance, objs, s, sName, rel["rel"], oName, cat = sCat)
                                if csid is not None:
                                    cSubj = instance["objects"][csid]["name"]

                                    mapping["cdsubject"], mapping["casubject"], _ = definedRef(instance, csid, direct = True, answer = True, simple = simple, noSuffix = True)["the"]
                                    mapping["dobject"], mapping["aobject"], mapping["dpobject"] = ref or definedRef(instance, oId, direct = False, simple = simple, isSubj = False, blackObjIds = ids + [csid], blackRS = rel["rel"])["the"] # ["ref"] noSuffix = True, 
                                    data["candidates"] = [sName, cSubj + " ({})".format(csid)]
                                    gen(instance, "categoryRelSChoose", "chooseObjRel", "chooseObjRel", mapping, data, relck) 

                        ##### object
                        if "o" in relInfo["cases"] and (not tooGeneral(oName)):
                            omapping = copy.deepcopy(baseMapping)
                            omapping["of"] = "of" if relInfo["of"] else ""
                            if relInfo["by"]:
                                mapping["qrel"] = " ".join(mapping["qrel"].split(" ")[:-1]) + " by"
                                mapping["rel"] = " ".join(mapping["rel"].split(" ")[:-1]) + " by"

                            if relInfo["suffix"] or relInfo["suffixLast"]:
                                if coin(0.04):
                                    if relInfo["suffix"]:
                                        omapping["suffix"] = omapping["qrel"]
                                        omapping["qrel"] = ""
                                    else:
                                        words = omapping["qrel"].split(" ")
                                        omapping["suffix"] = words[-1]
                                        omapping["qrel"] = " ".join(words[:-1])
                                    omapping["of"] = ""

                            if (not relInfo["catO"]) and (not isMultiObj(instance, rel)):
                                mapping = copy.deepcopy(omapping)
                                
                                if rel["rel"] in ["on", "at", "in"]:
                                    mapping["qrel"] = rel["rel"]
                                    mapping["suffix"] = ""

                                mapping["dsubject"], mapping["asubject"], mapping["dpsubject"] = definedRef(instance, sId, direct = direct, short = (not direct), simple = simple, noSuffix = direct, blackObjIds = ids, blackRO = rel["rel"])["ref"]
                                ref = objRef(oId, oName, rel["rel"], q = False)
                                mapping["dobject"], mapping["aobject"], mapping["dpobject"] = ref or definedRef(instance, oId, direct = True, answer = True, simple = simple, noSuffix = True, isSubj = False)["the"]

                                mapping["what"], catwh = wh(o, where = True, rel = rel["rel"], subj = s) # False?????
                                # mapping["qrel"] = mapping["rel"] 
                                if rel["rel"] in whereRemove and mapping["what"] == "where":
                                    mapping["qrel"] = " ".join(mapping["qrel"].split(" ")[:-1])
                                    mapping["relq"] = " ".join(mapping["relq"].split(" ")[:-1])

                                # "sId": sId, "sName": sName, 
                                data = {"dobject": {"code": None, "s": True}, "rel": rel["rel"], "tId": oId, "tName": catwh, "subj": False, "pointer": [oId]} # dsubject
                                gen(instance, "relO", "queryRel", "queryRel", mapping, data, relok) 
                                # if whereRel(rel):
                                #     mapping = copy.deepcopy(omapping)
                                #     mapping["dsubject"], mapping["asubject"], mapping["dpsubject"] = definedRef(instance, sId, direct = True, answer = True, noSuffix = True)["ref"]
                                #     mapping["dobject"], mapping["aobject"], mapping["dpobject"] = definedRef(instance, oId, direct = True, answer = True, noSuffix = True)["the"] # , simple = simple, noSuffix = True

                                #     # "sId": sId, "sName": sName, 
                                #     placeO = "where" if isA(o, "place") else None
                                #     data = {"dobject": {"code": None}, "rel": rel["rel"], "tId": oId, "tName": placeO, "subj": False} # dsubject
                                #     gen(instance, "where", "queryRel", mapping, data)                         

                            if oCat is not None:
                                mapping = copy.deepcopy(omapping)
                                mapping["catData"] = oCat
                                mapping["a"] = geta(oName)
                                mapping["dsubject"], mapping["asubject"], mapping["dpsubject"] = definedRef(instance, sId, direct = direct, short = (not direct), simple = simple, noSuffix = direct, blackObjIds = ids, blackRO = rel["rel"])["ref"]
                                ref = objRef(oId, oName, rel["rel"], q = False)
                                mapping["dobject"], mapping["aobject"], mapping["dpobject"] = ref or definedRef(instance, oId, direct = True, answer = True, simple = simple, noSuffix = True, isSubj = False)["the"]

                                mapping["category"], mapping["cis"] = catNormalize(o, oCat, k = False)
                                mapping["kategory"], mapping["kis"] = catNormalize(o, oCat, k = True)

                                data = {"dobject": {"code": None, "s": True}, "rel": rel["rel"], "tId": oId, "tName": oCat, "subj": False, "pointer": [oId]} # dsubject
                                # "sId": sId, "sName": sName, 
                                gen(instance, "categoryRelO", "queryRel", "queryRel", mapping, data, relck, priority = 3)  

                                # ????
                                ref = objRef(oId, oName, rel["rel"], q = True)
                                if isWeakExistObj(oName): # (ref is None)
                                    # the = False
                                    # if not isWeakExistObj(oName):
                                    #     the = True
                                    cObj1, coid1 = undefinedObjAlt(instance, sName, rel["rel"], oName, cat = oCat), "-"
                                    coid2 = definedObjAlt(instance, objs, o, sName, rel["rel"], oName, cat = oCat)
                                    cObj2 = None if coid2 is None else instance["objects"][coid2]["name"]
                                    
                                    if cObj1 is None:
                                        cObj, coid, a = cObj2, coid2, False
                                    elif cObj2 is None:
                                        cObj, coid, a = cObj1, coid1, True
                                    else:
                                        cObj, coid, a = (cObj1, coid1, True) if coin(0.5) else (cObj2, coid2, False)

                                    if cObj is not None:
                                        if a:
                                            mapping["dobject"], mapping["aobject"], mapping["dpobject"] = [(anRef(oName, oId), objDirCode(oId, oName))], anRef(oName, oId), None
                                            mapping["cdobject"], mapping["caobject"] = [(anRef(cObj, coid), objDirCode("-", cObj))], anRef(cObj, coid)
                                        else:
                                            mapping["cdobject"], mapping["caobject"], _ = [("the {}".format(cObj), objDirCode(coid, cObj))], "the {}".format(cObj)

                                        mapping["dsubject"], mapping["asubject"], mapping["dpsubject"] = definedRef(instance, sId, direct = direct, short = (not direct), simple = simple, noSuffix = direct, blackObjIds = ids + ([coid] if coid != "-" else []), blackRO = rel["rel"])["ref"]
                                        data["candidates"] = [oName, cObj + ("" if a else " ({})".format(coid))]
                                        gen(instance, "categoryRelOChoose", "chooseObjRel", "chooseObjRel", mapping, data, relck, priority = 3) 

                            if relInfo["cat"] == "comparative" and mod(sName) == mod(oName) \
                                    and isUnique(instance, sId) and isUnique(instance, oId):
                                comparative = rel["rel"].split(" ")[0]
                                createComparative(instance, sId, sName, oId, oName, comparative, cmpk)

                        if isWeakExistObj(sName, strong = True) and \
                                (((relInfo["cat"] == "direct") and ("s" in relInfo["cases"])) or \
                                    relInfo["existQuestionOnly"] or rel["rel"] == "at"): # ? unique????
                            mapping = copy.deepcopy(baseMapping)
                            mapping["sSubject"], mapping["pSubject"] = formsOf(sName)
                            mapping["any"] = geta(mapping["sSubject"], aany = True)
                            mapping["dobject"], mapping["aobject"], mapping["dpobject"] = definedRef(instance, oId, direct = False, that = direct, ithat = True, simple = simple, isSubj = False, blackObjIds = ids, blackRS = rel["rel"])["the"] # , short = True noSuffix = True,  that = True, 

                            data = {"dobject": {"code": None}, "rel": relObjCode("relate", sId, sName, rel["rel"], True), "pointer": [sId, oId]}
                            gen(instance, "existRelS", "existRel", "existRelT", mapping, data, relvk, select = 0.8) # 0.5 

                            if rel["rel"] in negative:
                                alts, prefixSize = negative[rel["rel"]]
                                orels = [op for op in alts if countOfRel(sName, op, oName) > 10]
                                orel = choice(orels)
                                # for orel in alts: 
                                if orel is not None:
                                    mapping["dobject"], mapping["aobject"], mapping["dpobject"] = definedRef(instance, oId, direct = False, that = direct, ithat = True, simple = simple, isSubj = False, blackObjIds = ids, blackRS = rel["rel"])["the"] # , short = True noSuffix = True,  that = True, 
                                    mapping["nrel"] = orel
                                    data = {"dobject": {"code": None}, "rel": relObjCode("relate", sId, sName, orel, True), "pointer": [sId, oId]}
                                    gen(instance, "existRelSRC", "existRel", "existRelF", mapping, data, relvk) 

                            cSubj = undefinedSubjAlt(instance, sName, rel["rel"], oName)
                            if cSubj is not None:
                                # cSubj = instance["objects"][csid]
                                mapping = copy.deepcopy(baseMapping)
                                mapping["csSubject"], mapping["cpSubject"] = formsOf(cSubj)
                                mapping["any"] = geta(mapping["csSubject"], aany = True)
                                mapping["dobject"], mapping["aobject"], mapping["dpobject"] = definedRef(instance, oId, direct = False, that = direct, ithat = True, simple = simple, isSubj = False, blackObjIds = ids, blackRS = rel["rel"])["the"] # , short = True noSuffix = True, that = True, 

                                data = {"dobject": {"code": None}, "rel": relObjCode("relate", "-", cSubj, rel["rel"], True), "pointer": [oId]}
                                gen(instance, "existRelSC", "existRel", "existRelF", mapping, data, relvk, select = 0.8) # 0.5

                        # and isMultiSubj(rel):
                        if not relInfo["existQuestionOnly"] and not badVerify(instance, rel): # ???????? and isMultiSubj????
                            mapping = copy.deepcopy(baseMapping)
                            mapping["dsubject"], mapping["asubject"], mapping["dpsubject"] = definedRef(instance, sId, direct = direct, short = (not direct), onlyPrefix = direct, simple = simple, blackObjIds = ids, blackRO = rel["rel"])["the"] # noSuffix = True, 

                            ref = objRef(oId, oName, rel["rel"], q = False) # , q = True
                            dRef = definedRef(instance, oId, direct = False, that = direct, ithat = True, blackObjIds = ids, blackRS = rel["rel"], isSubj = False)["the"] # short = (not direct), ,  that = True
                            # oIsDefined = (ref is None)
                            if isWeakExistObj(oName) and isSingular(oName) and coin(0.4): # 0.35???? 
                                dRef = [(anRef(oName, oId), getObjCode(oId, o, oName, clean = True))], anRef(oName, oId), (dRef[2] if dRef is not None else None)
                                # oIsDefined = False
                            mapping["dobject"], mapping["aobject"], mapping["dpobject"] = ref or dRef
                            
                            # oIsDefined = (mapping["dobject"][0][0].startswith("th")) if len(mapping["dobject"]) > 0 else False
                            # "sId": sId, "sName": sName, 
                            # if oIsDefined: ????????????????????????????????????????????????????????????????????????????????????????????
                            #     data = {"dobject": {"code": None}, "rel": rel["rel"], "tId": sId, "tName": sName, "subj": True, "pointer": [sId, oId]}
                            # else:
                            data = {"dobject": {"code": None, "s": True}, "rel": rel["rel"], "tId": oId, "tName": oName, "subj": False, "pointer": [sId, oId]}

                            # only for rels in ops? otherwise bias
                            gen(instance, "relVerify", "verifyRel", "verifyRelT", mapping, data, relvk, priority = 3)  # , select = 0.65

                            # if not isMultiSubj(isntance, rel):
                            csid = definedSubjAlt(instance, objs, s, sName, rel["rel"], oName)
                            if csid is not None:
                                cSubj = instance["objects"][csid]["name"]

                                mapping["cdsubject"], mapping["casubject"], mapping["dpsubject"] = definedRef(instance, csid, direct = True, answer = True, onlyPrefix = True, simple = simple)["the"] # , noSuffix = True
                                mapping["dobject"], mapping["aobject"], mapping["dpobject"] = ref or definedRef(instance, oId, direct = False, that = direct, ithat = True, simple = simple, isSubj = False, blackObjIds = ids + [csid], blackRS = rel["rel"])["the"] # that = True noSuffix = True, 

                                data = {"dobject": {"code": None}, "rel": rel["rel"], "tId": csid, "tName": cSubj, "subj": True, "pointer": [sId, oId]}
                                gen(instance, "relVerifyCs", "verifyRel", "verifyRelF", mapping, data, relvk, priority = 3) # , select = 0.65 

                            # if not isMultiObj(isntance, rel):
                            if isWeakExistObj(oName): # (ref is None)
                                cObj1, coid1 = undefinedObjAlt(instance, sName, rel["rel"], oName), "-" # , cat = oCat
                                coid2 = definedObjAlt(instance, objs, o, sName, rel["rel"], oName) # , cat = oCat
                                cObj2 = None if coid2 is None else instance["objects"][coid2]["name"]
                                
                                if cObj1 is None:
                                    cObj, coid, a = cObj2, coid2, False
                                elif cObj2 is None:
                                    cObj, coid, a = cObj1, coid1, True
                                else:
                                    cObj, coid, a = (cObj1, coid1, True) if coin(0.5) else (cObj2, coid2, False)

                                if cObj is not None:
                                    if a:
                                        mapping["cdobject"], mapping["caobject"] = [(anRef(cObj, coid), objDirCode(coid, cObj))], anRef(cObj, coid)
                                    else:
                                        mapping["cdobject"], mapping["caobject"] = [("the {}".format(cObj), objDirCode(coid, cObj))], "the {}".format(cObj)

                                    mapping["dsubject"], mapping["asubject"], mapping["dpsubject"] = definedRef(instance, sId, direct = direct, short = (not direct), simple = simple, noSuffix = direct, blackObjIds = ids + ([coid] if coid != "-" else []), blackRO = rel["rel"])["ref"]

                                    data = {"dobject": {"code": None, "s": True}, "rel": rel["rel"], "tId": coid, "tName": cObj, "subj": False, "pointer": [sId, oId]}
                                    # data = {"dobject": {"code": None}, "rel": rel["rel"], "tId": sId, "tName": sName, "subj": True}
                                    gen(instance, "relVerifyCo", "verifyRel", "verifyRelF", mapping, data, relvk, priority = 3) # , select = 0.65

                            if (sName, rel["rel"], oName) in opsTriples:
                                mapping = copy.deepcopy(baseMapping)
                                mapping["dsubject"], mapping["asubject"], mapping["dpsubject"] = definedRef(instance, sId, direct = True, answer = True, simple = simple)["the"] # , short = True , noSuffix = True
                                mapping["dobject"], mapping["aobject"], mapping["dpobject"] = definedRef(instance, oId, direct = True, answer = True, simple = simple, isSubj = False)["the"] # , short = True noSuffix = True, 
                                # "sId": sId, "sName": sName, 
                                data = getObjCode(sId, s, sName)
                                data.update({"rel": rel["rel"], "tId": oId, "tName": oName, "subj": True, "pointer": [sId, oId]})
                                gen(instance, "relVerifyCop", "verifyRel", "verifyRelF", mapping, data, relr2k) 

                            if rel["rel"] in negative:
                                alts, prefixSize = negative[rel["rel"]]
                                orels = [op for op in alts if countOfRel(sName, op, oName) > 10]
                                orel = choice(orels)
                                # for orel in alts: 
                                if orel is not None:
                                    mapping = copy.deepcopy(baseMapping)

                                    # mapping["dsubject"], mapping["asubject"] = definedRef(instance, sId,)["the"] # , short = True #  direct = True, simple = simple, noSuffix = True
                                    # ref = objRef(oId, oName, orel, q = False) # , q = True
                                    # mapping["dobject"], mapping["aobject"] = ref or definedRef(instance, oId,)["the"] # , short = True , that = True  direct = True, simple = simple, noSuffix = True
                                    
                                    mapping["dsubject"], mapping["asubject"], mapping["dpsubject"] = definedRef(instance, sId, direct = direct, short = (not direct), onlyPrefix = direct, simple = simple, blackObjIds = ids, blackRO = rel["rel"])["the"] # noSuffix = True, 

                                    ref = objRef(oId, oName, rel["rel"], q = False) # , q = True
                                    dRef = definedRef(instance, oId, direct = False, that = direct, ithat = True, blackObjIds = ids, blackRS = rel["rel"], isSubj = False)["the"] # short = (not direct), ,  that = True
                                    if isWeakExistObj(oName) and isSingular(oName) and coin(0.4): # 0.35???? 
                                        dRef = [(anRef(oName, oId), getObjCode(oId, o, oName, clean = True))], anRef(oName, oId), (dRef[2] if dRef is not None else None)
                                    mapping["dobject"], mapping["aobject"], mapping["dpobject"] = ref or dRef

                                    mapping["qcrel"] = orel 
                                    if simple:
                                        mapping["qcrel"] = toBasic(orel)
                                    
                                    mapping["qcrel2"] = " ".join(mapping["qcrel"].split(" ")[prefixSize:])
                                    mapping["qrel2"] = " ".join(mapping["qrel"].split(" ")[prefixSize:])

                                    data = {"dobject": {"code": None}, "rel": orel, "tId": sId, "tName": sName, "subj": True, "pointer": [sId, oId]}
                                    gen(instance, "relVerifyCr", "verifyRel", "verifyRelF", mapping, data, relvk, priority = 3) #  , select = 0.65, priority = 0.3 relr1k                         

                                    mapping["rel1"] = oneWordAns.get(rel["rel"], rel["rel"])
                                    data = {"dobject": {"code": None}, "candidates": [rel["rel"], orel], "tId": sId, "tName": sName, "subj": True, "pointer": [sId, oId]}
                                    gen(instance, "relChooser", "chooseRel", "chooseRel", mapping, data, relcck, select = 0.3) # relr1k
            except:
                print("REDO!!!!!!!!!!!!!!?!?!?!" + imageId)
                redo.append(imageId)

            # print("1", imageId, len(instance["questions"]))

            # print("RRRR")
            # print(imageId)
            dedupQuestions(instance) # instance["questions"] = 

            # print("2", imageId, len(instance["questions"]))

            instance["rQuestions"] = {}
            for key in instance["key2qids"]:
                qs = [instance["questions"][q] for q in instance["key2qids"][key]]
                chosens = sampleUniqueQuestions(qs)
                # print(key)
                for chosen in chosens:
                    # if chosen["type"] in ["verify", "choose", "logical"]: # u'verify': 788630, u'compare': 52333, u'choose': 332612, u'logical': 257803, u'query': 1454187})
                    #     chosen["select"] *= 0.67
                    if chosen["select"] == 1.0 or coin(chosen["select"]):
                        instance["rQuestions"][chosen["id"]] = chosen
                    # print("R", chosen["key"], chosen["question"], chosen["fullAnswer"], chosen["answer"], "->".join(chosen["code"]))

                    # if chosen["group"] in ["exist", "existC"]:
                    #     chosen["select"] = 0.5
                    # if chosen["group"] in subtypeUbPostProb:
                    #     chosen["select"] *= subtypeUbPostProb[chosen["group"]]

            instance["sQuestions"] = {qid: q for qid, q in instance["questions"].items() if q["ansDist"]}
            # print(len(instance["sQuestions"]))
            for qid, question in instance["sQuestions"].items():
                question["question"] = question["question"].replace("type of", "kind of")
                instance["rQuestions"][qid] = question
                # print("S", question["key"], question["question"], question["fullAnswer"], question["answer"], "->".join(question["code"]))

            # print("1", instance["rQuestions"].keys())
            # print("2", instance["questions"].keys())
            # instance["dQuestions"] = removeDups(instance["rQuestions"])
            # instance["sQuestions"] = removeDups(instance["sQuestions"])
            # instance["sQuestions"] = removeDups(instance["sQuestions"])
                    # print("D", question["key"], question["question"], question["fullAnswer"], question["answer"], "->".join(question["code"]))
            # print(len(instance["dQuestions"]))

            for question in instance["questions"].values():
                question["entailedQuestions"] = []
                cpatterns = question["entailed"]
                for cpattern in cpatterns:
                    for ccode in instance["ccode2qids"]:
                        if match(cpattern, ccode):
                            question["entailedQuestions"] += instance["ccode2qids"][ccode]
                question["entailedQuestions"] = list(set(question["entailedQuestions"]))
                if question["id"] in question["entailedQuestions"]:
                    question["entailedQuestions"].remove(question["id"])
                question.pop("entailed")# question["entailed"] = None

            for q in instance["rQuestions"].values():
                typeCounter[q["type"]] += 1
            for q in instance["rQuestions"].values():
                groupCounter[q["group"]] += 1

            if imgIndex % 1000 == 0:
                print(typeCounter)
                for c in sorted(groupCounter.keys()):
                    print(c, groupCounter[c])

            instance["gQuestions"] = {}
            for key in instance["key2qids"]:
                qs = [instance["questions"][q] for q in instance["key2qids"][key]]
                candidates = [q for q in qs if q["id"] not in instance["rQuestions"]]
                chosens = sampleUniqueQuestions(candidates)
                for chosen in chosens:
                    # if chosen["group"] in ["exist", "existC"]:
                    #     chosen["select"] = 0.5
                    # if chosen["group"] in subtypeUbPostProb:
                    #     chosen["select"] *= subtypeUbPostProb[chosen["group"]]
                    # if chosen["type"] in ["verify", "choose", "logical"]: # u'verify': 788630, u'compare': 52333, u'choose': 332612, u'logical': 257803, u'query': 1454187})
                    #     chosen["select"] *= 0.67
                    if chosen["select"] == 1.0 or coin(chosen["select"]):
                        instance["gQuestions"][chosen["id"]] = chosen

            for q in instance["gQuestions"].values():
                typeCounterG[q["type"]] += 1
            for q in instance["gQuestions"].values():
                groupCounterG[q["group"]] += 1

        for imgIndex, imageId in enumerate(vgData): 
            instance = vgData[imageId]    
            for group in ["rQuestions", "sQuestions", "gQuestions"]:
                instance[group] = [question["id"] for question in instance[group].values()]
            
            instance.pop("key2qids")
            instance.pop("ccode2qids")

        with open(dataOutFilename1.format(shardIndex), "w") as f:
            json.dump(vgData, f)

            # for q in instance["sQuestions"].values():
            #     print(q)

            # for q in instance["questions"].values():
            #     print(q)

def id2name(instance, o):
    if o.startswith("id"):
        return instance["objects"][o[2:]]["name"]
    return o

def question2cat(question):
    # return question["cat"]
    cat = re.search(r": (.*) \(", question["code"][0]).group(1)
    return cat

def question2act(question):
    act = re.search(r"filter.*: (.*)", question["code"][1]).group(1)
    return act

def getConditional(instance, question):
    if question["ccode"] is None:
        question["ccode"] = compactCode(question["code"], question["answer"], question["codeGroup"], question["group"])
        # print("none question code", question["question"], question["ccode"])
        if question["ccode"] is None:
            return None # []
    # if question["type"] in ["logical", "compare"]:
    #     return None # []
    # if question["group"] in ["objThisChoose"]: # "activityWho",  "relChooser", 
    #     return None # []
    # if question["codeGroup"] == "common":
    #     return "common" #["common"]
    if question["codeGroup"].startswith("verifyState"):
        t, a = re.search(r"!t ([^!]*)!.*!a:([^!]*)!", question["ccode"]).group(1, 2)
        return "01-{}_{}".format(t, a)
    if question["codeGroup"] in ["queryState", "chooseState"]:
        p = "q" if question["codeGroup"] == "queryState" else "c"
        t = re.search(r"!t ([^!]*)!", question["ccode"]).group(1)
        return "02{}-{}".format(p, t)
    if question["codeGroup"] in ["existT", "existF"]:
        o = re.search(r"!o:([^!]*)!", question["ccode"]).group(1)
        return "03-{}".format(id2name(instance, o))
    if (question["codeGroup"].startswith("existAttr") or question["codeGroup"].startswith("existNot")):
        o, a = re.search(r"!o:([^!]*)!.*!a:([^!]*)!", question["ccode"]).group(1, 2)
        o = id2name(instance, o)
        n = "n#" if ("not#" in question["ccode"]) else ""
        a = "{}{}".format(n, a)
        return "04-{}_{}".format(o, a) # [o, a, "{}_{}".format(o, a)]
    if question["codeGroup"] in ["verifyAttrsT", "verifyAttrsF"]:
        o, a1, a2 = re.search(r"!o:([^!]*)!.*!a:([^!]*)!.*!a:([^!]*)!", question["ccode"]).group(1, 2)
        o = id2name(instance, o)
        a1, a2 = sorted([a1, a2])
        return "05-{}_{}".format(a1, a2) # [o, a, "{}_{}".format(o, a)]        
    if question["codeGroup"] in ["verifyAttrT", "verifyAttrF"]:
        o, a = re.search(r"!o:([^!]*)!.*!a:([^!]*)!", question["ccode"]).group(1, 2)
        o = id2name(instance, o)
        return "06-{}_{}".format(o, a) # [o, a, "{}_{}".format(o, a)]  
    if question["codeGroup"].startswith("all"):
        os,dt = question["ccode"].split("/")
        return "07{}-{}".format(dt.split(":")[0], os[3:-1]) 
    if question["group"] == "objThisChoose":
        o1, o2 = re.search(r": !a:([^!]*)!&!a:([^!]*)!", question["ccode"]).group(1, 2)
        o1, o2 = sorted([o1, o2])
        return "08oc-{}_{}".format(o1, o2) # [o, a, "{}_{}".format(o, a)]
    if question["type"] in ["logical", "compare"]: #  
        o1, o2 = re.search(r"!o:([^!]*)!.*!o:([^!]*)!", question["ccode"]).group(1, 2)
        o1 = id2name(instance, o1)
        o2 = id2name(instance, o2)
        o1, o2 = sorted([o1, o2])
        p = question["codeGroup"] 
        if p[-1] in ["T", "F"]:
            p = p[:-1]
        # "n" if question["codeGroup"] == "common" else "p" # "l" if question["type"] == "logical" else ("n" if question["codeGroup"] == "common" else "p")
        return "09{}-{}_{}".format(p, o1, o2) # [o, a, "{}_{}".format(o, a)]
    if question["codeGroup"] in ["queryAttr", "chooseAttr"]:
        p = "q" if question["codeGroup"] == "queryAttr" else "c"
        o, t = re.search(r"!o:([^!]*)!.*!t ([^!]*)!", question["ccode"]).group(1, 2)
        o = id2name(instance, o)
        return "10{}-{}_{}".format(p, o, t) # [t, "{}_{}".format(t, o)]
    if question["group"] == "activityWho":
        c = question2act(question)
        return c
    if question["group"] in ["category", "categoryThis", "categoryThisChoose"]:
        p = "c" if "Choose" in question["group"] else "q"
        c = question2cat(question)
        return "11{}-{}".format(p, c)
    if question["group"] in ["categoryAttr", "categoryThat", "categoryThatChoose"]:
        p = "c" if "Choose" in question["group"] else "q"
        c = question2cat(question)
        a = re.search(r"!a:([^!]*)!", question["ccode"]).group(1)
        n = "n#" if ("not#" in question["ccode"]) else ""
        a = "{}{}".format(n, a)
        return "12{}-{}_{}".format(p, c, a) # [c, a, "{}_{}".format(c, a)]
    if question["codeGroup"] in ["verifyRelT", "existRelT", "verifyRelF", "existRelF", "chooseRel"]:
        o1, o2 = re.search(r"!o:([^!]*)!.*!o:([^!]*)!", question["ccode"]).group(1, 2)
        return "13-{}_{}".format(id2name(instance, o1), id2name(instance, o2))       
    if question["group"] in ["relS", "relO", "sameRelate", "sameMaterialRelate"]:
        o, r = re.search(r"!o:([^!]*)!.*@([^@]*)@", question["ccode"]).group(1, 2) # .split("/")[0]
        return "14-{}_{}".format(id2name(instance, o), r) # [id2name(instance, o)]
    if question["group"].startswith("categoryRel"):
        # c = re.search(r": (.*),.*,", question["code"][-2]).group(1)
        o, r =  re.search(r"!o:([^!]*)!.*@([^@]*)@", question["ccode"]).group(1, 2) #.split("/")[0]
        return "15-{}_{}".format(id2name(instance, o), r) # [c, id2name(instance, o)]

    print(question)
    raise Exception("missing conditional")
    # print("##########")
    # print(question) 

if args.stats or args.normalize:
    typeCounter = defaultdict(int)
    groupCounter = defaultdict(int)
    answerCounter = defaultdict(int)
    cansCounter = defaultdict(lambda: defaultdict(int))

    for shardIndex in range(shardsNum):
        print("stats1")
        with open(dataOutFilename1.format(shardIndex)) as f:
            vgData = json.load(f)

        for imageId in vgData: 
            instance = vgData[imageId]
            # instance["ccode2qids"] = defaultdict(list)            
            # # print(len(instance["rQuestions"]))
            # for question in instance["questions"].values():
            #     question["ccode"] = compactCodeFix(question["ccode"], question["code"], question["answer"], question["codeGroup"], question["group"])
            #     question["entailed"] = [] if question["ccode"] is None else entailed(question["ccode"], question["codeGroup"])
            #     if question["ccode"] is not None:
            #         instance["ccode2qids"][question["ccode"]].append(question["id"])

            instance["eQuestions"] = []
            for qid in instance["rQuestions"]:
                question = instance["questions"][qid]
                # if (question["type"] not in ["verify", "choose", "logical"]): # or coin(0.85): # 0.67 REMOVED??????
                instance["eQuestions"].append(qid)

            for qid in instance["eQuestions"]:
                question = instance["questions"][qid]
                typeCounter[question["type"]] += 1
                groupCounter[question["group"]] += 1
                answerCounter[question["answer"]] += 1
                ans = question["answer"]
                canss = typeOf(ans, None, retAll = True) or [catn(ans)]
                for cans in canss:
                    if cans is not None:
                        cansCounter[cans][ans] += 1

                # for cond in conds:

        with open(dataOutFilename2.format(args.questionPrefix, shardIndex), "w") as f:
            json.dump(vgData, f)

    # final:b = 1, gamma = 1.05, gup = 0.01
    # first?: b = 3.2, gamma = ?, gup = ?, maxGamma = 1.5
    # def customSmoother(b = 2, gamma = 1.25, gup = 0.03, maxGamma = 1.4)

    printDD(cansCounter, "beforeGlobal")

    gsmoother = [3.2, 1.2, 0.03, 1.35]
    if args.gsmoothPrms != "":
        gsmoother = map(float, args.gsmoothPrms.split())
    smtr = uniformSmoother(args.bigThr) if args.uniform else customSmoother(b = gsmoother[0], gamma = gsmoother[1], gup = gsmoother[2], maxGamma = gsmoother[3]) # b = 3.2, gamma = 1.2, gup = 0.03, maxGamma = 1.35
    oRatios = unbiasOratios(cansCounter, smtr) # 3.2 2.5 1.35
    # oRatios = unbiasOratios(cansCounter, smtr) # 3.2 2.5 1.35

    for shardIndex in range(shardsNum):
        print("stats2")
        with open(dataOutFilename2.format(args.questionPrefix, shardIndex)) as f:
            vgData = json.load(f)

        unbiasCat(vgData, "eQuestions", "bQuestions", oRatios, toprint = True)
        unbiasCat(vgData, "gQuestions", "bgQuestions", oRatios)

        with open(dataOutFilename3.format(args.questionPrefix, shardIndex), "w") as f:
            json.dump(vgData, f)

# if args.newnorm:
    ocondAnswerCounter = defaultdict(lambda: defaultdict(int))
    bcondAnswerCounter = defaultdict(lambda: defaultdict(int))
    ocondAnswerList = defaultdict(lambda: defaultdict(list))
    bcondAnswerList = defaultdict(lambda: defaultdict(list))
    nonList = []
    counters = {"open": ocondAnswerCounter, "boolean": bcondAnswerCounter}
    lists = {"open": ocondAnswerList, "boolean": bcondAnswerList, "non": nonList}

    for shardIndex in range(shardsNum):
        print("stats3")
        with open(dataOutFilename3.format(args.questionPrefix, shardIndex)) as f:
            vgData = json.load(f)

        for imageId in vgData: 
            instance = vgData[imageId]

            for qid in instance["bQuestions"]:
                question = instance["questions"][qid]
                cond = getConditional(instance, question)
                # print(question["question"], question["codeGroup"], question["group"], question["type"], question["code"], question["ccode"], cond)
                if cond is not None:
                    if question["answer"] in ["yes", "no"]:
                        bcondAnswerCounter[cond][question["answer"]] += 1
                        bcondAnswerList[cond][question["answer"]].append((qid, imageId))
                    else:
                        ocondAnswerCounter[cond][question["answer"]] += 1
                        ocondAnswerList[cond][question["answer"]].append((qid, imageId))
                else:
                    # print("BAD: ", question)
                    nonList.append((qid, imageId))
                # for cond in conds:

    # ratios = unbiasRatios(counters, customSmoother()) # 1 #  
    lsmoother = [2, 1.25, 0.03, 1.4]
    if args.lsmoothPrms != "":
        lsmoother = map(float, args.lsmoothPrms.split())

    smtr = uniformSmoother(args.smallThr) if args.uniform else customSmoother(b = lsmoother[0], gamma = lsmoother[1], gup = lsmoother[2], maxGamma = lsmoother[3]) # b = 2, gamma = 1.25, gup = 0.03, maxGamma = 1.4
    ratios = unbiasRatios(counters, smtr) # 1
    # ratios = unbiasRatios(counters, uniformSmoother(args.smallThr)) # 1

    goodIds = unbiasSelect(lists, counters, ratios)
    # ratios2 = unbiasRatios(counters, funcSmoother(sqrtF, 1))
    # ratios3 = unbiasRatios(counters, funcSmoother(lnF, 1))

    # printD(typeCounter, "type")
    # printD(groupCounter, "group")
    # printD(answerCounter, "answer")
    printDD(ocondAnswerCounter, "beforeLocalO")
    printDD(bcondAnswerCounter, "beforeLocalB")    
    printDD(ocondAnswerCounter, "afterLocalO", ratios["open"]) # 1
    printDD(bcondAnswerCounter, "afterLocalB", ratios["boolean"]) # 1
    # with open("biasedCounts.json", "w") as f:
    #     json.dump(ratios, f)
    # with open("unbiasingRatios.json", "w") as f:
    #     json.dump(ratios, f)

if args.normalize: # args.newnorm or args.newnorm or 
    print("normalize")
    # printStats(vgData, "rQuestions")
    # postProb = ratios(groupCounter)
    # postProbG = ratios(groupCounterG)

    pretypeCounter = defaultdict(int)
    outCounter = defaultdict(int) # {"group": defaultdict(int), "cat": defaultdict(dict)}
    # for n in ["u1", "u2", "u3"]: # , "final"
        # outCounters[n] = defaultdict(int) # defaultdict(lambda: defaultdict(int))

    for shardIndex in range(shardsNum):
        print("normalized1")
        with open(dataOutFilename3.format(args.questionPrefix, shardIndex)) as f:
            vgData = json.load(f)

        # for imageId in vgData: 
        #     instance = vgData[imageId]

        #     for question in instance["questions"].values():
        #         question["entailedQuestions"] = []
        #         cpatterns = question["entailed"]
        #         for cpattern in cpatterns:
        #             for ccode in instance["ccode2qids"]:
        #                 if match(cpattern, ccode):
        #                     question["entailedQuestions"] += instance["ccode2qids"][ccode]
        #         question["entailedQuestions"] = list(set(question["entailedQuestions"]))
        #         if question["id"] in question["entailedQuestions"]:
        #             question["entailedQuestions"].remove(question["id"])
        #         question.pop("entailed")# question["entailed"] = None

        #     instance.pop("ccode2qids")

            # newRQuestions = []
            # for qid in instance["rQuestions"]:
            #     question = instance["questions"][qid]
            #     if (question["type"] not in ["verify", "choose", "logical"]) or coin(0.67):
            #         newRQuestions.append(qid)
            # instance["rQuestions"] = newRQuestions    

        select(vgData, "utQuestions", goodIds, outCounter, pretypeCounter) # _1 ["u1"] "rQuestions", t
        unbias(vgData, "bgQuestions","ugtQuestions", ratios) # ratios1 gcUg1 =  , outCounters["u1g"] # _1
        # unbias(vgData, "rQuestions", "u_2Questions", ratios2, outCounters["u2"])
        # unbias(vgData, "rQuestions", "u_3Questions", ratios3, outCounters["u3"])

        with open(dataOutFilename4.format(args.questionPrefix, shardIndex), "w") as f:
            json.dump(vgData, f)

    outProb = toRatios(outCounter)
    # outProb = {} # s s[n]
    # for n in ["u1", "u2", "u3"]: # , "final"
        # outProbs[n] = ratios(outCounters[n])

    subsets1 = [("500k", lambda: (6 if coin(float(1)/3) else 7)), ("100k", lambda: (1 if coin(float(2)/3) else 2))] # (6 if coin(float(1)/3) else 7) (1 if coin(4/7) else 2) 0.5 0.2 ("1m", 10), 

    typeCounterS = defaultdict(int)
    groupCounterS = defaultdict(int)
    ansCounterS = defaultdict(int)
    # typeDict = defaultdict(int)

    for shardIndex in range(shardsNum):
        print("normalized2")
        with open(dataOutFilename4.format(args.questionPrefix, shardIndex)) as f:
            vgData = json.load(f)

        # printDD(outCounter, "out")
        downsampleQuestions(vgData, "utQuestions", "uQuestions", outProb) # , typeDict s["u1"], outCounter = outCounters["final"]
        downsampleQuestions(vgData, "ugtQuestions", "ugQuestions", outProb) # s["u1"]
        # downsampleQuestions(vgData, "u_2Questions", "u2Questions", outProbs["u2"])
        # downsampleQuestions(vgData, "u_3Questions", "u3Questions", outProbs["u2"])

    #     with open(dataOutFilename5.format(shardIndex), "w") as f:
    #         json.dump(vgData, f)
        # print(typeDict)
        typesampleQuestions(vgData, "uQuestions", "samQuestions", pretypeCounter) 
        typesampleQuestions(vgData, "ugQuestions", "samgQuestions", pretypeCounter) 

        # with open(dataOutFilename5.format(shardIndex), "w") as f:
        #     json.dump(vgData, f)
# if args.subsets:
    # for shardIndex in range(shardsNum):
    #     print("subsets")
    #     with open(dataOutFilename5.format(args.questionPrefix, shardIndex)) as f:
    #         vgData = json.load(f)
        for imageId in vgData: 
            instance = vgData[imageId]
            # print("3", imageId, len(instance["questions"]), len(instance["uQuestions"]), len(instance["rQuestions"]))

            # instance["suQuestions"] = subuniqueQuestions(instance, instance["uQuestions"], weak = True) # , args.mturk1 instance, 

            preSubset = "samQuestions" # suQuestions
            for name, nF in subsets1:
                sName = "subset{}".format(name)
                if key2tier[imageId] == "train":
                    instance[sName] = subselectQuestions(instance[preSubset], num = nF()) #, F() instance,  prob = proportion + 0.05
                else:
                    instance[sName] = []
                preSubset = sName

            # instance["mturk1"] = multichoice(instance["uQuestions"], args.mturk1) # suQuestions, isDict = True subuniqueQuestions(instance["uQuestions"].values(), args.mturk1) # instance, 
            # instance["mturk2"] = selectEntailedQuestions(instance, instance["mturk1"], args.mturk2)

            for qid in instance["samQuestions"]:
                question = instance["questions"][qid]
                typeCounterS[question["type"]] += 1
                groupCounterS[question["group"]] += 1
                ansCounterS[question["answer"]] += 1

            # print(instance["mturk1"])
            # print(instance["mturk2"])

        with open(dataOutFilename5.format(args.questionPrefix, shardIndex), "w") as f:
            json.dump(vgData, f)

    print(typeCounterS)
    for c in sorted(groupCounterS.keys()):
        print(c, groupCounterS[c])
    for c in sorted(ansCounterS.keys()):
        print(c, ansCounterS[c])

    print(redo)

# if args.fix:
#     subsets1 = [("500k", lambda: (5 if coin(6/7) else 6)), ("100k", lambda: (14 if coin(5/7) else 15))] # 0.5 0.2 ("1m", 10), 

#     for shardIndex in range(shardsNum):
#         print("fix")
#         with open(dataOutFilename3.format(shardIndex)) as f:
#             vgData = json.load(f)

#         for imageId in vgData: 
#             instance = vgData[imageId]
#             instance["suQuestions"] = subuniqueQuestions(instance, instance["uQuestions"], weak = True) # , args.mturk1 instance, 

#             # print("3", imageId, len(instance["questions"]), len(instance["uQuestions"]), len(instance["rQuestions"]))
#             preSubset = "suQuestions"
#             for name, n in subsets1:
#                 sName = "subset{}".format(name)
#                 instance[sName] = subselectQuestions(instance[preSubset], num = n()) #, instance,  prob = proportion + 0.05
#                 preSubset = sName

#             # print(instance["mturk1"])
#             # print(instance["mturk2"])

#         with open(dataOutFilename4.format(shardIndex), "w") as f:
#             json.dump(vgData, f)    

# urls = {}
# with open("vg14/image_data.json", "r") as f:
#     imgsInfo = json.load(f)
#     for imgInfo in imgsInfo:
#         vgId = str(imgInfo["image_id"])
#         url = imgInfo["url"]
#         urls[vgId] = url

def question2rel(question):
    # return question["rel"][1] won't work for same material TODO!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    if question["ccode"] is None:
        return None
    # nonIds
    ret = re.search(r"!o:id([a-z0-9\-\\\[\]\* ]*)!.*!o:id([a-z0-9\-\\\[\]\* ]*)!", question["ccode"])
    if ret is None and any([x in question["ccode"] for x in nonIds]):
        return None
    objIds = ret.group(1, 2)
    rel, direction = re.search(r"@(.*),(.*)@", question["ccode"]).group(1, 2)
    s, o = (objIds[1], objIds[0]) if direction == "s" else (objIds[0], objIds[1])
    return {"rel": rel, "subj": s, "obj": o}

def toUnique(inList):
    outList = []
    for e in inList:
        se = e.strip()
        if se not in outList:
            outList.append(se)
    return outList


# "verifyState": "scene.verify {type}: {attr}"
# "queryState": "scene.query: {type}"
# "chooseState": "scene.choose {type}: {|candidates}"
# "queryAttr": "oid.query: {type}"
# "verifyAttr": "oid.verify {type}: {attr}"
# "verifyAttrs": "oid.verify {type}: {attr}.verify {type}: {attr}.and"
# "chooseAttr": "oid.choose {type}: {|candidates}"
# "exist": "oid.[filter {t}: not#{a}.]exist"
# "existRel": "oid.@rel,d@ oid.exist"
# "logicOr": "oid1.oid2.[filter {t}: not#{a}.]or"
# "logicAnd": "oid1.oid2.[filter {t}: not#{a}.]and"
# "queryObject": "oid.query: name"
# "chooseObject": "oid.choose name: {|candidates}"
# "queryRel": "oid.@rel,d@ oid.query: name"
# "verifyRel": "oid.verify rel: @rel,d@ oid"
# "chooseRel": "oid.choose rel: @|candidates,d@ oid"
# "chooseObjRel": "oid.@rel,d@ oid.choose name: {|candidates}"
# "allSame": "{cat}.same: {type}"
# "allDiff": "{cat}.different: {type}"
# "compare": "oid.oid.{comparative}"
# "common": "oid.oid.common {type}"
# "same": "oid.oid.same {type}"
# "diff": "oid.oid.different {type}"

def getChoicesNew(instance, question):
    if question["type"] in ["verify", "logical"]:
        return ["yes", "no"], ["yes", "no"]
    
    if any([question["codeGroup"].startswith(c) for c in ["allSame", "allDiff", "same", "diff"]]):
        return ["yes", "no"], ["yes", "no"]
    
    if question["type"] == "common":
        return ["color", "material", "shape"], ["color", "material", "shape"]

    if question["type"] == "choose":
        chooseStep = question["code"][-1]
        if question["codeGroup"] == "chooseRel":
            chooseStep = chooseStep.split(",")[1]
        else:
            chooseStep = chooseStep.split(":")[1]
        candidates = chooseStep.split("|")
        return candidates, candidates

    if question["type"] == "compare":
        candidates = re.search(r"!o:id([a-z0-9\-\\\[\]\* ]*)!.*!o:id([a-z0-9\-\\\[\]\* ]*)!", question["ccode"]).group(1, 2)
        return [instance["objects"][oid]["name"] for oid in candidates], [instance["objects"][oid]["name"] for oid in candidates]

    if question["codeGroup"] == "queryState":
        if question["group"] == "place":
            place = question["answer"]
            return parents2objs["place"], parents2objs["place"] 
        else:
            attr = question["answer"]
            t = typeOf(attr, None)
            return typeGroups[t], typeGroups[t]

    if question["codeGroup"] == "queryAttr":
        obj = instance["objects"][question["pointer"][0]]
        attr = question["answer"]
        if attr in ["left", "right"]:
            return ["left", "right"], ["left", "right"]
        
        aop = toOp(obj, attr)       
        if aop is not None:
            return [attr, aop], [attr, aop]

        t = typeOf(attr, obj)
        if attr not in vocab["a"]:
            choices = list(typeGroups["activity"])
        else:
            choices = typeGroups[t]

        fchoices = [statOf(obj["name"], a, p = False) > 0 for a in choices] # isLikely(a, obj["name"])
        return choices, fchoices

    if question["codeGroup"] in ["queryObject", "queryAttrObject", "queryNotObject"]:
        obj = instance["objects"][question["pointer"][0]]
        cat = question2cat(question)
        sameCat = parents2objs[cat] 
        return sameCat, sameCat

    if question["codeGroup"] == "queryRel":    

        # print(s["name"],r,o["name"])
        obj = instance["objects"][question["pointer"][0]]
        choices = vocab["o"]

        if question["group"].startswith("category"):
            cat = re.search(r": (.*),.*,", question["code"][-2]).group(1)
            sameCat = parents2objs[cat] 
            choices = sameCat

        rel = question2rel(question)
        if rel is None or rel["rel"].startswith("same "):
            if question["ccode"] is not None and any([g in question["ccode"] for g in games]):
                choices = games
            else:
                choices = [x["name"] for x in instance["objects"].values()]
            fchoices = choices
        else:
            s = instance["objects"][rel["subj"]]["name"]
            o = instance["objects"][rel["obj"]]["name"]
            r = rel["rel"]            

            cat = None
            if question["group"] in ["categoryRelS", "categoryRelO"]:
                cat = re.search(r": (.*),", question["code"][-2]).group(1)

            sl, ol = s, o
            if question["group"].endswith("S"):
                sl = None
            else:
                ol = None
            fchoices = [countOfRel(sl or other, r, ol or other) > 0 for other in choices]
        return choices, fchoices

def getChoices(instance, question):
    if question["type"] in ["verify", "logical"]:
        return [], ["yes", "no"]
    
    if any([question["codeGroup"].startswith(c) for c in ["allSame", "allDiff", "same", "diff"]]):
        return [], ["yes", "no"]
    
    if question["type"] == "common":
        return [], ["color", "material", "shape"]

    if question["type"] == "choose":
        chooseStep = question["code"][-1]
        if question["codeGroup"] == "chooseRel":
            chooseStep = chooseStep.split(",")[1]
        else:
            chooseStep = chooseStep.split(":")[1]
        candidates = chooseStep.split("|")
        return [], candidates

    if question["type"] == "compare":
        candidates = re.search(r"!o:id([a-z0-9\-\\\[\]\* ]*)!.*!o:id([a-z0-9\-\\\[\]\* ]*)!", question["ccode"]).group(1, 2)
        return [], [instance["objects"][oid]["name"] for oid in candidates]

    if question["codeGroup"] == "queryState":
        if question["group"] == "place":
            place = question["answer"]
            choices = parents2objs["place"] 
            simObjs = objSims(place, wide = True)
            choices = [o for o in choices if o not in simObjs]
            defaultChoices = objAlts(question["answer"])# alts = objAlts(place)
            choices = [question["answer"]] + choices
            defaultChoices = [question["answer"]] + defaultChoices
            return choices, defaultChoices
        else:
            attr = question["answer"]
            t = typeOf(attr, None)
            simAtts = attrSims(attr)
            choices = [a for a in typeGroups[t] if a not in simAtts]
            if t == "color":
                choices += ["white", "black", "green", "blue", "red", "brown", "gray", "yellow", "orange", "pink", "purple"]
            if t == "material":
                choices += ["rubber", "plastic"]
            defaultChoices = multiSample(candidateAttr(instance, None, attr, likely = False, getAll = True), 10)
            choices = [question["answer"]] + choices
            defaultChoices = [question["answer"]] + defaultChoices           
            return choices, defaultChoices

    if question["codeGroup"] == "queryAttr":
        obj = instance["objects"][question["pointer"][0]]
        attr = question["answer"]
        if attr in ["left", "right"]:
            return [], ["left", "right"]
        
        aop = toOp(obj, attr)       
        if aop is not None:
            return [], [attr, aop]

        t = typeOf(attr, obj)
        if attr not in vocab["a"]:
            choices = list(typeGroups["activity"])
            defaultChoices = list(typeGroups["activity"])
        else:
            simAtts = attrSims(attr)
            choices = [a for a in typeGroups[t] if a not in simAtts]
            defaultChoices = multiSample(candidateAttr(instance, obj, attr, getAll = True), 10)
        choices = [question["answer"]] + choices
        defaultChoices = [question["answer"]] + defaultChoices

        return choices, defaultChoices

    if question["codeGroup"] in ["queryObject", "queryAttrObject", "queryNotObject"]:
        obj = instance["objects"][question["pointer"][0]]
        cat = question2cat(question)
        sameCat = parents2objs[cat] 
        simObjs = objSims(obj["name"], wide = True)
        choices = [o for o in sameCat if o not in simObjs and mod(o) == mod(obj["name"])]
        choices = [question["answer"]] + choices
        return choices, choices

    if question["codeGroup"] == "queryRel":    
        # print(s["name"],r,o["name"])
        obj = instance["objects"][question["pointer"][0]]
        sims = list(objSims(obj["name"], wide = True))
        if obj["name"] in sims:
            sims.remove(obj["name"])
        choices = ["_" + mod(obj["name"])] + sims
        
        if question["group"].startswith("category"):
            cat = re.search(r": (.*),.*,", question["code"][-2]).group(1)
            sameCat = parents2objs[cat] 
            simObjs = objSims(obj["name"], wide = True)
            choices = [o for o in sameCat if o not in simObjs and mod(o) == mod(obj["name"])]
            choices = [question["answer"]] + choices

        rel = question2rel(question)
        if rel is None or rel["rel"].startswith("same "):
            if question["ccode"] is not None and any([g in question["ccode"] for g in games]):
                defaultChoices = games
            else:
                defaultChoices = [x["name"] for x in instance["objects"].values()]
        else:
            s = instance["objects"][rel["subj"]]
            o = instance["objects"][rel["obj"]]
            r = rel["rel"]            

            cat = None
            if question["group"] in ["categoryRelS", "categoryRelO"]:
                cat = re.search(r": (.*),", question["code"][-2]).group(1)

            # printGraph({"0": instance}, "0")
            # print(instance["sr"])
            undefinedAltFunc = undefinedSubjAlt if question["group"].endswith("S") else undefinedObjAlt
            defaultChoices = multiSample(undefinedAltFunc(instance, s["name"], r, o["name"], cat = cat, getAll = True), 10)
        defaultChoices = [question["answer"]] + defaultChoices
        return choices, defaultChoices

    print("????")
    print(question)

def genHit(instances):
    contents = []
    for i in range(0, len(instances), 2):
        id1, instance1 = instances[i]
        id2, instance2 = instances[i+1]
        pages = [(id1, instance1["mturk1"], instance1), (id2, instance2["mturk1"], instance2), 
                 (id1, instance1["mturk2"], instance1), (id2, instance2["mturk2"], instance2)]
        
        for imgId, questionIds, instance in pages:
            content = {}
            content["imgId"] = imgId
            content["img"] = urls[imgId]
            content["answers"] = [instance["questions"][qid]["answer"] for qid in questionIds]
            content["qids"] = questionIds
            content["questions"] = [instance["questions"][qid]["question"] for qid in questionIds]
            choices = [getChoices(instance, instance["questions"][qid]) for qid in questionIds]
            content["choices"] = [toUnique(c[0]) for c in choices]
            content["defaultChoices"] = [toUnique(c[1]) for c in choices]
            contents.append(content)
    return contents

if args.makeMturk:
    out = False
    sets = [(4,2)] + [(10,0) for _ in range(10)]
    hitSize = (2, 4)
    overallNum = sum([(hitSize[0] * s[0] + hitSize[1] * s[1]) for s in sets])

    instances = {}
    fs = list(range(shardsNum))
    random.shuffle(fs)
    for shardIndex in fs:
        if out:
            break
        with open(dataOutFilename3.format(args.questionPrefix, shardIndex)) as f:
            vgData = json.load(f)
        
        vgKeys = [k for k in vgData]
        random.shuffle(vgKeys)
        for imageId in vgKeys: 
            instance = vgData[imageId]
            if len(instance["mturk1"]) < 10 or len(instance["mturk2"]) < 5:
                continue
            instances[imageId] = instance
            if len(instances) == overallNum:
                out = True
                break

    instances = list(instances.items())
    curr = 0
    for setIndex, s in enumerate(sets):
        hits = []
        for _ in range(s[0]):
            hits.append(genHit(instances[curr:curr + hitSize[0]]))
            curr += hitSize[0]

        for _ in range(s[1]):
            hits.append(genHit(instances[curr:curr + hitSize[1]]))
            curr += hitSize[1]

        with open(mturkFilename.format(setIndex), "w") as f:
            json.dump(hits, f)        

if args.models:
    imgIds1 = json.load(open("../gqa/vg_spatial_imgsInfo.json"))
    imgIds2 = json.load(open("../gqa/vg_gt_imgsInfo.json"))
    imgIds3 = json.load(open("../gqa/vg_14_imgsInfo.json"))

    datasets = ["all", "samgQuestions", "samQuestions", "subset500k", "subset100k", "subset50k", "subset10k"] # "subset1m", "u2Questions", "u3Questions", "suQuestions", 
    qsubs = ["samgQuestions", "samQuestions", "subset500k", "subset100k"] # "subset1m", "u2Questions", "u3Questions", "suQuestions", 
    tiers = ["train", "val", "test", "ttest"]

    data = {}    

    for ds in datasets:
        data[ds] = {}
        for tier in tiers:
            data[ds][tier] = {"questions": []}

    for shardIndex in range(shardsNum):
        print("models")
        with open(dataOutFilename5.format(args.questionPrefix, shardIndex)) as f:
            vgData = json.load(f)
         
        for imageId in vgData: 
            if (imageId not in imgIds1) or (imageId not in imgIds2) or (imageId not in imgIds3):
                continue
            instance = vgData[imageId]
            for qid in instance["questions"]:
                question = instance["questions"][qid]
                q = {"question": question["question"],
                     "answer": question["answer"],
                     "fullAnswer": question["fullAnswer"],
                     "questionId": qid,
                     "type": question["type"],
                     "group": question["group"],
                     "imageId": imageId}

                tier = key2tier[imageId]

                data["all"][tier]["questions"].append(q)

                for qsub in qsubs:
                    if q["questionId"] in instance[qsub]:
                        data[qsub][tier]["questions"].append(q)

                if q["questionId"] in instance["subset100k"]:
                    if imageId in subsets2["50k"]: # "subset50k" in instance:
                        data["subset50k"][tier]["questions"].append(q)

                    if imageId in subsets2["10k"]: # "subset10k" in instance: 
                        data["subset10k"][tier]["questions"].append(q)                            

    outFormat = "../gqaFinal/{prefix}aa{ds}_{tier}_questions.json"
    for ds in data:
        for tier in data[ds]:
            with open(outFormat.format(prefix = args.questionPrefix, ds = ds, tier = tier), "w") as f:
                json.dump(data[ds][tier], f)

    # writeIdList(keys, "all.txt")
    # writeIdList(trainKeys, "train.txt")    
if args.graphstats:
    graphStats = {"objs": [], "attrs": [], "allrels": [], "rels": [],
        "objsDict": defaultdict(int), "attrsDict": defaultdict(int),
        "catsDict": defaultdict(int), "relsDict": defaultdict(int)}

    for shardIndex in range(shardsNum):
        print("graphs")
        with open(dataOutFilename5.format(args.questionPrefix, shardIndex)) as f:
            vgData = json.load(f)

        print(len(vgData))

        for i, imageId in enumerate(vgData):
            if (i%100 == 0):
                print(i)
            instance = vgData[imageId]

            graphStats["objs"].append(len(instance["objects"]))
            graphStats["attrs"].append(sum(len(o["attributes"]) for o in instance["objects"].values()))
            graphStats["allrels"].append(sum(len(o["outRels"]) for o in instance["objects"].values()))
            graphStats["rels"].append(sum(len([r for r in o["outRels"].values() if r["rel"] not in ["to the left of", "to the right of"]]) for o in instance["objects"].values()))

            for obj in instance["objects"].values():
                graphStats["objsDict"][obj["name"]] += 1
                for cat in refCats(obj):
                    graphStats["catsDict"][cat] += 1
                for attr in obj["attributes"]:
                    graphStats["attrsDict"][attr] += 1
                for rel in obj["outRels"].values():
                    graphStats["relsDict"][rel["rel"]] += 1

    with open("graphStats.json", "w") as f:
        for t in ["objs", "attrs", "allrels", "rels"]:
            print(t, np.mean(graphStats[t]), np.std(graphStats[t]))
        json.dump(graphStats, f)

if args.histo:
    gbCounter = defaultdict(lambda: defaultdict(int))
    lbCounter = defaultdict(lambda: defaultdict(int))
    gaCounter = defaultdict(lambda: defaultdict(int))
    laCounter = defaultdict(lambda: defaultdict(int))
    for shardIndex in range(shardsNum):
        with open(dataOutFilename5.format(args.questionPrefix, shardIndex)) as f:
            vgData = json.load(f)
        print(shardIndex)
        for imageId in vgData: 
            instance = vgData[imageId]
            samSet = set(instance["samQuestions"])
            for qid in instance["questions"]:
                question = instance["questions"][qid]
                ans = question["answer"]
                cond = getConditional(instance, question) 
                cans = choice(typeOf(ans, None, retAll = True)) or catn(ans) 
                gbCounter[cans][ans] += 1
                lbCounter[cond][ans] += 1 
                if qid in samSet:
                    gaCounter[cans][ans] += 1
                    laCounter[cond][ans] += 1 

    printDD(gbCounter, "gbHist_{}.json".format(args.questionPrefix))    
    printDD(lbCounter, "lbHist_{}.json".format(args.questionPrefix))    
    printDD(gaCounter, "gaHist_{}.json".format(args.questionPrefix))    
    printDD(laCounter, "laHist_{}.json".format(args.questionPrefix))    

if args.entailed:
    for shardIndex in range(shardsNum):
        print("entailed")
        with open(dataOutFilename5.format(shardIndex)) as f:
            vgData = json.load(f)

        for imageId in vgData: 
            instance = vgData[imageId]

            for question in instance["questions"].values():
                question["entailedQuestions"] = []
                cpatterns = question["entailed"]
                for cpattern in cpatterns:
                    for ccode in instance["ccode2qids"]:
                        if match(cpattern, ccode):
                            question["entailedQuestions"] += instance["ccode2qids"][ccode]
                question["entailedQuestions"] = list(set(question["entailedQuestions"]))
                if question["id"] in question["entailedQuestions"]:
                    question["entailedQuestions"].remove(question["id"])
                question.pop("entailed")# question["entailed"] = None

            instance.pop("ccode2qids")

        with open(dataOutFilename7.format(shardIndex), "w") as f: # args.questionPrefix, 
            json.dump(vgData, f)

codes2st = {
    "verifyState": "global",
    "queryState": "global",
    "chooseState": "global",
    "queryAttr": "attr",
    "verifyAttr": "attr",
    "verifyAttrs": "attr", # lambda data:  + [] + ["and": data["attrs"]#["verify: {}".format(",".join(data["candidates"]))] 
    "chooseAttr": "attr",
    "exist": "obj",# query:  (c.replace("select", "exist") for c in data["dobject"]["code"])
    "existRel": "rel",#  query: (c.replace("select", "exist") for c in data["dobject"]["code"])
    "logicOr": "obj", # lambda data: data["dobject"]["code"].replace("select", "exist")
    "logicAnd": "obj", 
    "queryObject": "cat",
    "chooseObject": "cat",
    "queryRel": "rel",
    "verifyRel": "rel",
    "chooseRel": "rel",
    "chooseObjRel": "rel",
    "allSame": "attr",
    "allDiff": "attr",
    "compare": "attr",
    "common": "attr",
    "same": "attr",
    "diff": "attr"
    # "compare": lambda data: data["dobject"]["code"] + [relObjCode("verify", data["tId"], data["tName"], data["rel"], data["subj"])]
}

def getBox(i, j):
    edge = float(1) / 7
    return (edge * i, edge * i, edge * (i + 1), edge * (i + 1))

def toRegion(pointer, instance, scene = False):
    if pointer == "scene":
        return (0, 0, 1, 1) if scene else None
    if pointer is None:
        return None
    if pointer.startswith("id"):
        pointer = pointer[2:]
    obj = instance["objects"][pointer]
    return (obj["x0"], obj["y0"], obj["x1"], obj["y1"])

def centerOf(region):
    return midpoint(xrange(region)), midpoint(yrange(region))

def central(region):
    c = centerOf(region)
    return math.sqrt((c[0] - 0.5)**2 + ((c[1] - 0.5)**2))

def toObjStats(region):
    if region is None:
        return None
    return size(region), central(region)

def getPointer(question, first = False):
    # if question["pointer"] in ["-", "scene"]:
        # return None
    out = [(None if p in ["-", "scene"] else p) for p in question["pointer"]]
    if first:
        out = [p for p in out if p is not None]
        if len(out) > 0:
            return out[0]
        else:
            return "scene"
    else:
        return out
    # return 

def getPointers(ccode):
    return re.findall(r"id[0-9]+", ccode)

def getRegions(ccode, instance):
    pointers = getPointers(ccode)
    regions = []
    for p in pointers:
        r = toRegion(p, instance)
        if r is not None:
            regions.append(r)
    return regions

def groundingScore(attArr, question, instance):
    areas = []
    score = 0
    pointer = getPointer(question)
    areas.append(getRegions(question["ccode"], instance))
    areas.append(toRegion(p, instance) for p in pointer)
    for area in areas:
        for i in range(7):
            for j in range(7):
                if len(area) > 0:
                    score += (0.5 * attArr[i][j] * (avg([intersectionSize(getBox(i, j), subarea) for subarea in area]))) # 0.5?

def mostCommon(lst):
    return max(set(lst), key=lst.count)

def entropy(x):
    return x * math.log(x, 2)

def hist2shared(hist, withCond, entrop = False):
    getnropy = 0
    letnropy = 0
    nn = sum(sum(hist[k][a] for a in hist[k]) for k in hist)
    shared = defaultdict(int)
    n = {}
    for k in hist:
        n[k] = sum(hist[k][a] for a in hist[k])
        for a in hist[k]:
            key = "{}_{}".format(k, a) if withCond else a
            shared[key] += hist[k][a]
            #prob[k][a] = float(hist[k][a]) / n[k]
            letnropy += entropy(float(hist[k][a]) / nn)
        getnropy += entropy(float(n[k]) / nn)
    if entrop:
        print("Global Entropy", str(-getnropy))
        print("Local Entropy", str(-letnropy))
    return shared #, n

def histoMatch(hist, tHist, withCond):
    p = hist2shared(hist, withCond) # , _
    tp = hist2shared(tHist, withCond, entrop = True) # , n
    # sa = 0
    # na = 0
    # for k in tHist:
        # s = 0
    s = 0
    for a in tp: #[k]:
        e = tp[a] # tHist[k][a]
        o = p.get(a, 0) # hist[k].get(a, 0)
        d = o - e
        s += float(d * d) / e
    return s
        #sa += (s * n[k])
        #na += n[k]
    # return float(sa) / na

if args.scores:
    # datasets = ["all", "samgQuestions", "samQuestions", "subset500k", "subset100k", "subset50k", "subset10k"] # "subset1m", "u2Questions", "u3Questions", "suQuestions", 
    # qsubs = ["samgQuestions", "samQuestions", "subset500k", "subset100k"] # "subset1m", "u2Questions", "u3Questions", "suQuestions", 

    inFormat = "../gqaFinal/a1aa{ds}_{tier}_questions.json"#"../gqaFinal/n{ds}_{tier}_questions.json" 
    # with open(inFormat.format(ds = args.ds, tier = "train")) as f:
    #     info1 = json.load(f)
    # with open("gHist_{}.json".format(args.questionPrefix)) as f:
    #     tgHisto = json.load(f)
    # with open("lHist_{}.json".format(args.questionPrefix)) as f:
    #     tlHisto = json.load(f)

    tgHisto = defaultdict(lambda: defaultdict(int))
    tlHisto = defaultdict(lambda: defaultdict(int))

    with open(inFormat.format(ds = args.ds, tier = "val")) as f:
        info2 = json.load(f)
    # with open(inFormat.format(ds = args.ds, tier = "test")) as f:
    #     info3 = json.load(f)
    # with open(inFormat.format(ds = args.ds, tier = "ttest")) as f:
    #     info4 = json.load(f)        
    preds = {}
    for ff in args.scoresFiles:
        with open(ff) as f:
            preds[ff] = json.load(f)

    # allids = set()
    id2tiers = {}
    # for question in info1["questions"]:
    #     id2tiers[question["questionId"]] = "train"
    #     # allids.add(question["questionId"]) 

    for question in info2["questions"]:
        id2tiers[question["questionId"]] = "val"
        # allids.add(question["questionId"]) 

    # for question in info3["questions"]:
    #     id2tiers[question["questionId"]] = "test"
    #     # allids.add(question["questionId"]) 

    # for question in info4["questions"]:
    #     id2tiers[question["questionId"]] = "ttest"
    #     # allids.add(question["questionId"]) 

    file2Scores = {}
    for k in args.scoresFiles:
        file2Scores[k] = {"overall": 0, "overallR": 0, "valid": 0, "plaus": 0,
                          "overalle": 0, "overalleR": 0, "coverage": [], "pos": 0,
                          "type": defaultdict(int), "typeR": defaultdict(int), 
                          "wlen": defaultdict(int), "wlenR": defaultdict(int), 
                          "rlen": defaultdict(int), "rlenR": defaultdict(int), 
                          "os": defaultdict(int), "osR": defaultdict(int), 
                          "od": defaultdict(int), "odR": defaultdict(int), 
                          "st": defaultdict(int), "stR": defaultdict(int), 
                          "gCake": defaultdict(int), "cgCake": defaultdict(int), "csCake": defaultdict(int), 
                          "precision": defaultdict(list), "recall": defaultdict(list),
                          "scores": {e["questionId"]: e["prediction"] for e in preds[k]},
                          "atts": {e["questionId"]: np.array(e["attentions"]["kb"][-1]).reshape((7, 7)) for e in preds[k]} if args.grounding else None
                        }

    for k in ["gb", "lb"]:
        file2Scores[k] = {"overall": 0, "overallR": 0, "valid": 0, "plaus": 0,
                          "overalle": 0, "overalleR": 0, "coverage": [], "pos": 0,
                          "type": defaultdict(int), "typeR": defaultdict(int), 
                          "wlen": defaultdict(int), "wlenR": defaultdict(int), 
                          "rlen": defaultdict(int), "rlenR": defaultdict(int), 
                          "os": defaultdict(int), "osR": defaultdict(int), 
                          "od": defaultdict(int), "odR": defaultdict(int), 
                          "st": defaultdict(int), "stR": defaultdict(int), 
                          "gCake": defaultdict(int), "cgCake": defaultdict(int), "csCake": defaultdict(int), 
                          "precision": defaultdict(list), "recall": defaultdict(list)
                          }

    type1Counter = defaultdict(int)
    type2Counter = defaultdict(int)
    l2ans = defaultdict(list)
    g2ans = defaultdict(list)
    b2c = {"gb": {}, "lb": {}}
    q2c = {"gb": {}, "lb": {}}
    for shardIndex in range(shardsNum):
        print("scores1")

        with open(dataOutFilename5.format(args.questionPrefix, shardIndex)) as f:
            vgData = json.load(f)

        print(len(vgData))
        for i, imageId in enumerate(vgData):
            # if (i%100 == 0):
            #     print(i)
            instance = vgData[imageId]
            for qid in instance["questions"]:
                question = instance["questions"][qid]
                ans = question["answer"]
                cond = getConditional(instance, question)  
                q2c["lb"][qid] = cond
                ans = question["answer"]
                cans = choice(typeOf(ans, None, retAll = True)) or catn(ans)
                q2c["gb"][qid] = cans
                type1Counter[question["type"]] += 1
                type2Counter[codes2st[question["codeSturcture"]]] += 1
                if qid in id2tiers:
                    question = instance["questions"][qid]
                    l2ans[cond].append(question["answer"])
                    g2ans[cans].append(question["answer"])

    for l in l2ans:
        b2c["lb"][l] = mostCommon(l2ans[l])
    
    for l in g2ans:
        b2c["gb"][l] = mostCommon(g2ans[l])

    # with open("outGlobalDist.json", "w") as f:
    #     json.dump(g2ans, f)

    # with open("outLocalDist.json", "w") as f:
    #     json.dump(l2ans, f)

    print(type1Counter)
    print(type2Counter)

    allQuestions = set()
    allSamQuestions = set()

    gHisto = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))
    lHisto = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))

    for shardIndex in range(shardsNum):
        print("scores2")
        with open(dataOutFilename5.format(args.questionPrefix, shardIndex)) as f:
            vgData = json.load(f)

        with open(dataOutFilename7.format(shardIndex)) as f:
            entailments = json.load(f)

        print(len(vgData))

        for i, imageId in enumerate(vgData):
            if (i%100):
                print(i)
            instance = vgData[imageId]

            # graphStats["objs"].append(len(instance["objects"]))
            # graphStats["attrs"].append(sum(len(o["attributes"]) for o in instance["objects"].values()))
            # graphStats["allrels"].append(sum(len(o["outRels"]) for o in instance["objects"].values()))
            # graphStats["rels"].append(sum(len([r for r in o["outRels"].values() if r["rel"] not in ["to the left of", "to the right of"]]) for o in instance["objects"].values()))

            # for obj in instance["objects"].values():
            #     graphStats["objsDict"][obj["name"]] += 1
            #     for cat in refCats(obj):
            #         graphStats["catsDict"][cat] += 1
            #     for attr in obj["attributes"]:
            #         graphStats["attrsDict"][attr] += 1
            #     for rel in obj["outRels"].values():
            #         graphStats["relsDict"][rel["rel"]] += 1

            coverage = defaultdict(lambda: defaultdict(list))
            for qid in instance["questions"]:
                question = instance["questions"][qid]
                ans = question["answer"]

                allQuestions.add(question["question"])
                if qid in instance["samQuestions"]:
                    allSamQuestions.add(question["question"])

                ostats = toObjStats(toRegion(getPointer(question, first = True), instance, scene = True))

                entailedGroup = entailments[imageId]["questions"][qid]["entailedQuestions"]
                if qid in id2tiers: # file2Scores[0]["scores"]
                    for k in args.scoresFiles:
                        if qid in file2Scores[k]["scores"]:
                            predicted = file2Scores[k]["scores"][qid]
                            correct = (predicted == question["answer"])
                            score = float(1 if correct else 0)
                            rlen =  str(len([c for c in question["code"] if not (any([o in c for o in ["exist", "query: name", "choose name"]]))]))
                            
                            file2Scores[k]["overall"] += 1
                            file2Scores[k]["type"][question["type"]] += 1
                            file2Scores[k]["wlen"][str(len(question["question"].split()))] += 1
                            file2Scores[k]["rlen"][rlen] += 1
                            file2Scores[k]["st"][codes2st[question["codeSturcture"]]] += 1
                            file2Scores[k]["gCake"][question["group"]] += 1
                            file2Scores[k]["cgCake"][question["codeGroup"]] += 1
                            file2Scores[k]["csCake"][question["codeSturcture"]] += 1
                            file2Scores[k]["os"][str(ostats[0])] += 1
                            file2Scores[k]["od"][str(ostats[1])] += 1
                            coverage[k][getPointer(question, first = True)].append(score)
                            file2Scores[k]["precision"][predicted].append(score)
                            file2Scores[k]["recall"][ans].append(score)

                            if question["isPos"]:
                                file2Scores[k]["pos"] += 1

                            valid, plaus = getChoicesNew(instance, question)

                            if predicted in valid:
                                file2Scores[k]["valid"] += 1
                            
                            if predicted in plaus:
                                file2Scores[k]["plaus"] += 1
                            
                            if correct:
                                file2Scores[k]["overallR"] += 1
                                file2Scores[k]["typeR"][question["type"]] += 1
                                file2Scores[k]["wlenR"][str(len(question["question"].split()))] += 1
                                file2Scores[k]["rlenR"][rlen] += 1
                                file2Scores[k]["stR"][codes2st[question["codeSturcture"]]] += 1
                                file2Scores[k]["osR"][str(ostats[0])] += 1
                                file2Scores[k]["odR"][str(ostats[1])] += 1                            

                            # strong/weak
                            entailedGroup = [e for e in entailedGroup if e in file2Scores[k]["scores"] and e != qid]
                            if len(entailedGroup) > 0 and correct:
                                file2Scores[k]["overalle"] += 1
                                escores = []
                                for e in entailedGroup:
                                    equestion = instance["questions"][e]
                                    # if e in file2Scores[k]["scores"]:
                                    epredicted = file2Scores[k]["scores"][e]
                                    # else:
                                        # epredicted = ""
                                    score = 1 if (epredicted == equestion["answer"]) else 0
                                    #: escores += 1                                 
                                    escores.append(score)
                                escore = avg(escores)
                                file2Scores[k]["overalleR"] += escore

                            if args.grounding:
                                gscore = groundingScore(file2Scores[k]["atts"][qid], question, instance)
                                if gscore is not None:
                                    file2Scores[k]["grounding"] += 1
                                    file2Scores[k]["groundingR"] += gscore
                            
                            gHisto[k][q2c["gb"][qid]][predicted] += 1
                            lHisto[k][q2c["lb"][qid]][predicted] += 1

                    tgHisto[q2c["gb"][qid]][ans] += 1
                    tlHisto[q2c["lb"][qid]][ans] += 1 

                    for k in ["gb", "lb"]:
                        predicted = b2c[k][q2c[k][qid]]
                        correct = (predicted == question["answer"])
                        score = float(1 if correct else 0)
                        rlen =  str(len([c for c in question["code"] if not (any([o in c for o in ["exist", "query: name", "choose name"]]))]))
                        
                        file2Scores[k]["overall"] += 1
                        file2Scores[k]["type"][question["type"]] += 1
                        file2Scores[k]["wlen"][str(len(question["question"].split()))] += 1
                        file2Scores[k]["rlen"][rlen] += 1
                        file2Scores[k]["st"][codes2st[question["codeSturcture"]]] += 1
                        file2Scores[k]["gCake"][question["group"]] += 1
                        file2Scores[k]["cgCake"][question["codeGroup"]] += 1
                        file2Scores[k]["csCake"][question["codeSturcture"]] += 1                        
                        file2Scores[k]["os"][str(ostats[0])] += 1
                        file2Scores[k]["od"][str(ostats[1])] += 1
                        coverage[k][getPointer(question, first = True)].append(score)
                        file2Scores[k]["precision"][predicted].append(score)
                        file2Scores[k]["recall"][ans].append(score)

                        if question["isPos"]:
                            file2Scores[k]["pos"] += 1

                        valid, plaus = getChoicesNew(instance, question)

                        if predicted in valid:
                            file2Scores[k]["valid"] += 1
                        
                        if predicted in plaus:
                            file2Scores[k]["plaus"] += 1
                        
                        if correct:
                            file2Scores[k]["overallR"] += 1
                            file2Scores[k]["typeR"][question["type"]] += 1
                            file2Scores[k]["wlenR"][str(len(question["question"].split()))] += 1
                            file2Scores[k]["rlenR"][rlen] += 1
                            file2Scores[k]["stR"][codes2st[question["codeSturcture"]]] += 1
                            file2Scores[k]["osR"][str(ostats[0])] += 1
                            file2Scores[k]["odR"][str(ostats[1])] += 1                            
                        
                        # strong/weak
                        entailedGroup = [e for e in entailedGroup if e in q2c[k]]
                        if len(entailedGroup) > 0 and correct:
                            file2Scores[k]["overalle"] += 1
                            escore = float(0.0)
                            for e in entailedGroup:
                                equestion = instance["questions"][e]
                                if q2c[k][e] in b2c[k]: # if e in q2c[k]:
                                    epredicted = b2c[k][q2c[k][e]]
                                else: 
                                    epredicted = ""
                                if (epredicted == equestion["answer"]):
                                    escore += 1                                 
                            escore /= len(entailedGroup)
                            file2Scores[k]["overalleR"] += escore

                            gHisto[k][q2c["gb"][qid]][predicted] += 1
                            lHisto[k][q2c["lb"][qid]][predicted] += 1

            for k in args.scoresFiles:
                if len(coverage[k]) > 0:
                    imgCoverage = avg([avg(coverage[k][oid]) for oid in coverage[k]])
                    file2Scores[k]["coverage"].append(imgCoverage)

    for k in file2Scores:
        file2Scores[k]["gMatch"] = histoMatch(gHisto[k], tgHisto, withCond = False)
        file2Scores[k]["lMatch"] = histoMatch(lHisto[k], tlHisto, withCond = True)
        file2Scores[k]["hMatch"] = file2Scores[k]["gMatch"] * 2/3 + file2Scores[k]["lMatch"] * 1/3
        
        file2Scores[k]["coverage"] = avg(file2Scores[k]["coverage"])
        
        for a in file2Scores[k]["precision"]:
            file2Scores[k]["precision"][a] = avg(file2Scores[k]["precision"][a])
        
        for a in file2Scores[k]["recall"]:
            file2Scores[k]["recall"][a] = avg(file2Scores[k]["recall"][a])

        file2Scores[k].pop("scores", None)

    with open("file2Scores{}.json".format(args.scoresSuffix), "w") as f:
        json.dump(file2Scores, f)

    # print(file2Scores)
    print("uniqueAllNum", len(allQuestions))
    print("uniqueSamNum", len(allSamQuestions))

    # for question in instance["mturk1"].values():
        # print("D2", question["id"], question["key"], question["question"], question["fullAnswer"], question["answer"], "->".join(question["code"]))

    # for question in instance["mturk2"].values():
        # print("E2", question["id"], question["key"], question["question"], question["fullAnswer"], question["answer"], "->".join(question["code"]))

# printStats("suQuestions")

# for i, imageId in enumerate(vgData): 
#     instance = vgData[imageId]    
#     questionGroups = ["rQuestions", "sQuestions", "gQuestions", "uQuestions", "suQuestions", "ugQuestions"] + \
#         ["subset{}".format(n) for n,_ in subsets1] + ["mturk1", "mturk2"] # "questions",  + ["subset{}".format(n) for n in subsets2] 
#     for group in questionGroups:
#         instance[group] = [question["id"] for question in instance[group].values()]
    
# allQuestions = 0
# for i, imageId in enumerate(keys): 
#     instance = vgData[imageId]
#     instance["tier"] = tierOf(i)
#     allQuestions += len(instance["uQuestions"])

# sizes = [10000, 50000, 100000, 500000, 1000000]
# subsets = [(float(1000000) / allQuestions, "1m"), (0.5, "500k"), (0.2, "100k"), (0.5, "50k"), (0.2, "10k")]
# subsets2 = [(0.5, "50k"), (0.2, "10k")]

# gpostProb = ratios(gcounterG)
# print(gpostProb)

# ugcounter = defaultdict(int)
# ugcounterG = defaultdict(int)

# for i, imageId in enumerate(vgData): 
#     instance = vgData[imageId]
#     instance["ugQuestions"] = {}
#     for qid, question in instance["gQuestions"].items():
#         if (question["group"] not in gpostProb) or coin(gpostProb[question["group"]]):
#            instance["ugQuestions"][qid] = question
#            ugcounter[question["type"]] += 1
#            ugcounterG[question["group"]] += 1

# for c in sorted(ugcounterG.keys()):
#     print(c, ugcounterG[c])

# questionSubtypes = [
#     (["diffAnimals"], ["diffAnimalsC"]),
#     (["diffGender"], ["diffGenderC"]),
#     (["exist"], ["existC"]),
#     (["existAnd"], ["existAndC"]),
