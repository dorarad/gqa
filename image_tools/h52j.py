import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
# from visual_genome import api as vg
from PIL import Image as PIL_Image
import json
# import utils
import argparse
import h5py 
import numpy as np
from scipy.misc import imread, imresize
import pickle 
from tqdm import tqdm
import requests
import io
# from models import Image, Object, Attribute, Relationship
# from models import Region, Graph, QA, QAObject, Synset
import http.client
import utils

parser = argparse.ArgumentParser()

parser.add_argument('--name', required=True, type = str)
parser.add_argument('--jsonIn', required=True, type = str)
parser.add_argument('--jsonOut', required=True, type = str)
# parser.add_argument('--tier', required=True, type = str)

parser.add_argument('--vocab', required=True, type = str)
parser.add_argument('--attrVocab', type = str)

parser.add_argument('--thr', default=0.1, type = float)
parser.add_argument('--attrThr', default=0.05, type = float) # TODO: better, top by attribute type / prediction separated for each type

parser.add_argument('--update', action="store_true")
parser.add_argument('--vis', action="store_true")
parser.add_argument('--merge', action="store_true")

parser.add_argument('--interThr', default=0.7, type = float)
parser.add_argument('--sizeThr', default=1.5, type = float)
parser.add_argument('--bigSizeThr', default=2.5, type = float)
parser.add_argument('--margin', default=0.15, type = float)


# parser.add_argument('--count', default=2000, type = int)
# parser.add_argument('--attr', action="store_true")
# parser.add_argument('--topAttrs', default=3, type = int)
args = parser.parse_args()

# def GetImageData(id=61512):
#     data = utils.retrieve_data('/api/v0/images/' + str(id))
#     if 'detail' in data and data['detail'] == 'Not found.':
#         return None
#     image = utils.parse_image_data(data)
#     return image

classesList = ['__background__']  
with open(args.vocab, "r") as f:
    for object in f.readlines():
        classesList.append(object.split(",")[0].lower().strip())

# if args.attr:
attrsList = ['__noAttr__']  
with open(args.attrVocab, "r") as f:
    for object in f.readlines():
        attrsList.append(object.split(",")[0].lower().strip())

with open(args.name + "_imgsInfo.json", "r") as inFile:
   imgsInfo = json.load(inFile)

h5f = h5py.File(args.name + ".h5", "r")

dataFilenameNew = args.jsonIn #+ "_annotationsNew.json"
dataFilenamePred = args.jsonOut #+ "_annotationsPred.json"
   
# with open(dataFilenameNew, "r") as f:
#    data = json.load(f)

def GetImageData(id):
    img = imread("../vg/vgi/{id}.jpg".format(id = id))
    return img
  # data = utils.retrieve_data('/api/v0/images/' + str(id))
  # if 'detail' in data and data['detail'] == 'Not found.':
  #   return None
  # image = utils.parse_image_data(data)
  # return image

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
    return float(r1[1]-r1[0]) / (r2[1] - r2[0])

def midpoint(r):
    return float(r[0] + r[1]) / 2

def leftrange(r1, r2):
    return r1[1] < midpoint(r2)

def rightrange(r1, r2):
    return r1[0] > midpoint(r2)

def overlap(r1, r2):
    i = intersection(r1, r2)
    if i is None:
        return False    
    p1 = percent(i, r1)
    p2 = percent(i, r2)
    p = max(p1,p2)
    return p > args.interThr

def relativeleft(c1, c2):
    return overlap(yrange(c1), yrange(c2)) and leftrange(xrange(c1), xrange(c2))

def relativeright(c1, c2):
    return overlap(yrange(c1), yrange(c2)) and rightrange(xrange(c1), xrange(c2))

def globalleft(c):
    return xrange(c)[1] < 0.4

def globalright(c):
    return xrange(c)[0] > 0.6

def length(r):
    return float(r[1] - r[0])

def size(c):
    return length(xrange(c)) * length(yrange(c))

def bigger(c1, c2):
    return size(c1) > sizeThr * size(c2)

def smaller(c1, c2):
    return bigger(c2, c1)

def main(c1, c2):
    return size(c1) > bigSizeThr * size(c2)

def onMargin(c):
    x = xrange(c)
    y = yrange(c)
    xm = x[1] < args.margin or x[0] > 1 - args.margin
    ym = y[1] < args.margin or y[0] > 1 - args.margin
    return xm or ym

def updateObjDict(objsDict, objs):
    coordsFunc = lambda obj: (obj[1]["rx0"], obj[1]["ry0"], obj[1]["rx1"], obj[1]["ry1"])
    objItems = sorted(objsDict.items(), key = coordsFunc)
    objsCoords = sorted(objs, key = lambda obj: obj[0])
    i,j = 0,0
    while i < len(objItems) and j < len(objsCoords):
        iv = coordsFunc(objItems[i])
        jv = tuple(objsCoords[j][0])
        print(iv)
        print(jv)
        if close(iv,jv):
            objsDict[objItems[i][0]]["predAttributes"] = objsCoords[j][1]
            i += 1
            j += 1
            print("added")
        elif iv < jv:
            i += 1
        else:
            j += 1

def getAboveThr(scores, thr, namelist):
    scores[0] = 0.0
    topK = scores.argsort()[::-1]
    topScores = scores[topK]
    # print(topScores[0])
    aboveThr = np.argwhere(topScores >= thr)
    # print(aboveThr)
    if aboveThr.size == 0:
        return [], []
    k = np.amax(aboveThr)
    # print(k)
    topK = topK[:k].tolist()
    topScores = topScores[:k].tolist()
    topNames = [namelist[k] for k in topK]
    # print(topNames)
    # print(topScores)
    return topNames, topScores

def createNewObject(names, scores, coords, imgDims):
    rx0 = coords[0]
    ry0 = coords[1]
    rw = coords[2] - coords[0]
    rh = coords[3] - coords[1]
    rx1 = coords[2]
    ry1 = coords[3]
    x0 = float(rx0) / imgDims[0]
    y0 = float(ry0) / imgDims[1]
    w = float(rw) / imgDims[0]
    h = float(rh) / imgDims[1]
    x1 = x0 + w
    y1 = y0 + h
    xc = float(x1 + x0) / 2
    yc = float(y1 + y0) / 2
    size = w * h
    preds = list(zip(names, scores))
    newObj = {
        "x0": x0,
        "y0": y0,
        "w": w,
        "h": h,
        "size": size,
        "x1": x1,
        "y1": y1,
        "xc": xc,
        "yc": yc,
        "rx0": rx0,
        "ry0": ry0,
        "rw": rw,
        "rh": rh,
        "rx1": rx1,
        "ry1": ry1,
        "preds": preds
    }
    # print(preds)
    return newObj

def addPred(hashTable, objId, name, score):
    if name not in hashTable:
        hashTable[name] = []       
    hashTable[name].append((objId, score))

def hashObjs(hashTable, objDict):
    for objId in objDict:
        obj = objDict[objId]
        if "name" in obj:
            addPred(hashTable, objId, obj["name"], 1.0)
        if "preds" in obj:
            for pred in enumerate(obj["preds"]):
                addPred(hashTable, objId, pred[0], pred[1])
    return hashTable

def vis(imageId):   
    img = GetImageData(id=imageId)
    # print ("The url of the image is: %s" % image.url)

    fig, ax = plt.subplots()
    fig.set_size_inches(18.5, 10.5)

    # fig = plt.gcf()
    # fig.set_size_inches(18.5, 10.5)
    # response = requests.get(image.url)
    objs = list(data[imageId]["objects"].values())
    # img = PIL_Image.open(io.BytesIO(response.content))

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
            text += " " + "{}-{}".format(rel["rel"], rel["obj"])

        ax.text(obj["rx0"], obj["ry0"], text, style='italic', bbox={'facecolor':'white', 'alpha':0.5}) # , 'pad':10
        #text = obj["name"] + ("({})".format(",".join([x["rel"]+"-"+x["subjN"]+"-"+x["objN"] for x in obj["relations"]])) if "relations" in obj and len(obj["relations"]) > 0 else "")
        #ax.text(obj["x"], obj["y"], text, style='italic', bbox={'facecolor':'white', 'alpha':0.7, 'pad':10})
        # i += 1
    # fig = plt.gcf()
    plt.tick_params(labelbottom='off', labelleft='off')
    #plt.show()
    plt.savefig("photos/"+imageId+"Data.jpg", dpi = 720) # +"_"+str(j)
    plt.close(fig)

    # fig, ax = plt.subplots()
    # fig.set_size_inches(18.5, 10.5)
    # plt.imshow(img)

    # # fig = plt.gcf()
    # # fig.set_size_inches(18.5, 10.5)
    # # response = requests.get(image.url)
    # objs = list(data[imageId]["predObjects"].values())
    # # img = PIL_Image.open(io.BytesIO(response.content))
    # plt.imshow(img)
    # # ax = plt.gca()
    # print(len(objs))
    # for obj in objs:
    #     # if "relations" not in obj or len(obj["relations"]) == 0:
    #     #     continue        
    #     # print(obj)
    #     ax.add_patch(Rectangle((obj["rx0"], obj["ry0"]),
    #                            obj["rw"],
    #                            obj["rh"],
    #                            fill=False,
    #                            edgecolor='red',
    #                            linewidth=3))
    #     print(obj["preds"])
    #     print(obj["predAttributes"])
    #     text = " ".join([o[0] for o in obj["preds"]])
    #     text += "\n"
    #     text += " ".join([str(o[1])[:5] for o in obj["preds"]])
    #     # text += "\n"        
    #     # text += " ".join([o[0] for o in obj["predAttributes"]])
    #     # text += "\n"        
    #     # text += " ".join([str(o[1])[:5] for o in obj["predAttributes"]])
    #     ax.text(obj["rx0"], obj["ry0"], text, style='italic', bbox={'facecolor':'white', 'alpha':0.5}) # , 'pad':10
    #     #text = obj["name"] + ("({})".format(",".join([x["rel"]+"-"+x["subjN"]+"-"+x["objN"] for x in obj["relations"]])) if "relations" in obj and len(obj["relations"]) > 0 else "")
    #     #ax.text(obj["x"], obj["y"], text, style='italic', bbox={'facecolor':'white', 'alpha':0.7, 'pad':10})
    #     # i += 1
    # # fig = plt.gcf()
    # plt.tick_params(labelbottom='off', labelleft='off')
    # #plt.show()
    # plt.savefig("photos/"+imageId+"Preds.jpg", dpi = 720) # +"_"+str(j)
    # plt.close(fig) 

def addItem2set(d, k, v):
    if k not in d:
        d[k] = set()
    d[k].add(v)

def addItem2dict(d, k, vk, vv):
    if k not in d:
        d[k] = {}
    d[k][vk] = vv

def createKey2img():
    key2img = {}
    obj2key = {}
    for i, imageId in enumerate(data):
        instance = data[imageId]
        if i % 1000 == 0:
            print (i)
        for obj in instance["objects"].values():
            key = en.noun.singular(obj["name"])
            addItem2set(obj2key, key, obj["name"])
            addItem2dict(key2img, key, imageId, 1.0)
        if "predObjects" in instance:
            for obj in instance["predObjects"].values():
                for pred in obj["preds"]:
                    name, score = pred
                    key = en.noun.singular(name)
                    addItem2set(obj2key, key, name)
                    addItem2dict(key2img, key, imageId, score)                

    for k in obj2key:
        obj2key[k] = list(obj2key[k])

    return key2img, obj2key

# for i, imageId in enumerate(imgsInfo):
#     if args.merge:
#         if i % 100 == 0:
#             print(i)
#         idx = imgsInfo[imageId]["idx"]
#         objNum = imgsInfo[imageId]["objectsNum"]
#         boxes = h5f["features-2"][idx][:objNum]
#         scores = h5f["features-3"][idx][:objNum]
#         # maxScores = np.max(scores, axis = -1)
#         # maxClasses = np.argmax(scores, axis = -1)
#         # if args.attr:
#         ascores = h5f["features-4"][idx][:objNum]
#             # maxAscores = np.max(ascores, axis = -1)
#             # maxAttrs = np.argmax(ascores, axis = -1)
#         # image = GetImageData(id=imageId)
#         # print ("The url of the image is: %s" % image.url)

#         imgWidth = imgsInfo[imageId]["width"]
#         imgHeight = imgsInfo[imageId]["height"]
#         imgDims = (imgWidth, imgHeight)
#         data[imageId]["predObjects"] = {}

#         if "name2obj" not in data[imageId]:
#             data[imageId]["name2obj"] = hashObjs({}, data[imageId]["objects"])

#         if args.update:
#             objs = []         
#             for objIdx in range(objNum):
#                 coords = boxes[objIdx].tolist()
#                 topAttrs, topAScores = getAboveThr(ascores[objIdx], args.attrThr, attrsList)
#                 predAttrs = list(zip(topAttrs, topAScores))
#                 obj = (coords, predAttrs)
#                 objs.append(obj)

#             updateObjDict(data[imageId]["objects"], objs) 
#         else:
#             for objIdx in range(objNum):
#                 coords = boxes[objIdx].tolist()
#                 topNames, topScores = getAboveThr(scores[objIdx], args.thr, classesList)
#                 if len(topScores) == 0:
#                     continue
#                 # print(topNames, topScores)
#                 obj = createNewObject(topNames, topScores, coords, imgDims)
#                 topAttrs, topAScores = getAboveThr(ascores[objIdx], args.attrThr, attrsList)
#                 # print(topAttrs, topAScores)
#                 obj["predAttributes"] = list(zip(topAttrs, topAScores))
#                 objId = "p{}".format(objIdx)
#                 data[imageId]["predObjects"][objId] = obj 
                
#             data[imageId]["name2obj"] = hashObjs(data[imageId]["name2obj"], data[imageId]["predObjects"])

#     if args.vis:
#         vis(imageId)

# with open(dataFilenamePred, "w") as f:
#     json.dump(data, f)
with open(dataFilenamePred, "r") as f:
    data = json.load(f)

key2img, obj2key = createKey2img()

with open("key2img.json", "w") as f:
    json.dump(key2img, f)
    
with open("obj2key.json", "w") as f:
    json.dump(obj2key, f)

    # count += 1
    # if count > args.count:
    #     break   
