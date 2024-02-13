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

parser = argparse.ArgumentParser()

parser.add_argument('--name', required=True, type = str)
parser.add_argument('--json', required=True, type = str)
parser.add_argument('--tier', required=True, type = str)

parser.add_argument('--vocab', required=True, type = str)
parser.add_argument('--attrVocab', type = str)

parser.add_argument('--thr', default=0.2, type = float)
parser.add_argument('--attrThr', default=0.01, type = float)

parser.add_argument('--update', action="store_true")
parser.add_argument('--vis', action="store_true")

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

dataFilenameNew = args.json + "_annotationsNew.json"
dataFilenamePred = args.json + "_annotationsPred.json"
   
with open(dataFilenamePred, "r") as f:
   data = json.load(f)

for count, imageId in enumerate(imgsInfo):
    idx = imgsInfo[imageId]["idx"]
    objNum = imgsInfo[imageId]["objectsNum"]
    boxes = h5f["features-2"][idx][:objNum]
    scores = h5f["features-3"][idx][:objNum]
    maxScores = np.max(scores, axis = -1)
    maxClasses = np.argmax(scores, axis = -1)
    # if args.attr:
    ascores = h5f["features-4"][idx][:objNum]
        # maxAscores = np.max(ascores, axis = -1)
        # maxAttrs = np.argmax(ascores, axis = -1)
    # image = GetImageData(id=imageId)
    # print ("The url of the image is: %s" % image.url)

    imgWidth = imgsInfo[imageId]["width"]
    imgHeight = imgsInfo[imageId]["height"]
    imgDims = (imgWidth, imgHeight)
    data[imageId]["predObjects"] = {}

    if "name2obj" not in data[imageId]:
        data[imageId]["name2obj"] = hashObjs({}, data[imageId]["objects"])

    if args.update:
        objs = []         
        for objIdx in range(objNum):
            coords = boxes[objIdx].tolist()
            topAttrs, topAScores = getAboveThr(ascores, args.attrThr, attrsList)
            predAttrs = zip(topAttrs, topAScores)
            obj = (coords, predAttrs)
            objs.append(obj)

        updateObjDict(data[imageId]["objects"], objs) 
    
    else:
        for objIdx in range(objNum):
            coords = boxes[objIdx].tolist()
            topNames, topScores = getAboveThr(scores, args.thr, classesList)
            obj = createNewObject(topNames, topScores, coords, imgDims)
            topAttrs, topAScores = getAboveThr(ascores, args.attrThr, attrsList)
            obj["predAttrirbutes"] = zip(topAttrs, topAScores)
            objId = "p{}".format(objIdx)
            data[imageId]["predObjects"][objId] = obj 
            
        data[imageId]["name2obj"] = hashObjs(data[imageId]["name2obj"], data[imageId]["predObjects"])

    if args.vis:
        fig, ax = plt.subplots()
        fig.set_size_inches(18.5, 10.5)
        # response = requests.get(image.url)
        # img = PIL_Image.open(io.BytesIO(response.content))
        idp = ("00000000000" + str(imageId))[-12:]
        img = imread("coco/{tier}/COCO_{tier}2014_{idp}.jpg".format(tier = args.tier, idp = idp))

        i = 0
        # if len(objs) == 0: 
        plt.imshow(img)
        # ax = plt.gca()
        for i in range(objNum):
            # if i >= len(objs):
            #     break
            # obj = objs[i]
            # if "relations" not in obj or len(obj["relations"]) == 0:
            #     continue        
            #print(obj)
            ax.add_patch(Rectangle((boxes[i][0], boxes[i][1]),
                                   boxes[i][2] - boxes[i][0],
                                   boxes[i][3] - boxes[i][1],
                                   fill=False,
                                   edgecolor='red',
                                   linewidth=1))
            text = classesList[maxClasses[i]] + ("({})".format(int(maxScores[i]*100)))
            # if args.attr:
            topK = ascores[i].argsort()[::-1]
            topScores = [str(int(x*100)) for x in ascores[i][topK].tolist()]
            text += "\n"
            text += " ".join([attrsList[k] for k in topK.tolist()]) + ("({})".format(" ".join(topScores)))
            ax.text(boxes[i][0], boxes[i][1], text, style='italic', bbox={'facecolor':'white', 'alpha':0.5}) # , 'pad':10
            # i += 1
        # fig = plt.gcf()
        plt.tick_params(labelbottom='off', labelleft='off')
        #plt.show()
        plt.savefig("r"+count+"_"+imageId+".jpg", dpi = 720) # +"_"+str(j) # _rel
        plt.close(fig)
    
    # count += 1
    # if count > args.count:
    #     break

def updateObjDict(objsDict, objs):
    coordsFunc = lambda obj: (obj[1]["x0"], obj[1]["y0"], obj[1]["x1"], obj[1]["y1"])
    objItems = sorted(objsDict.items(), key = coordsFunc)
    objsCoords = sorted(objs, key = lambda obj: obj[0])
    i,j = 0,0
    while i < len(objItems) and j < len(objsCrds):
        iv = coordsFunc(objItems[i])
        jv = objsCrds[j][0]
        if iv == jv:
            objsDict[objItems[i]]["predAttrirbutes"] = objsCoords[j][1]
            i += 1
            j += 1
        elif iv < jv:
            i += 1
        else:
            j += 1

def getAboveThr(scores, thr, namelist):
    scores[0] = 0.0
    topK = scores.argsort()[::-1]
    topScores = scores[topK]
    k = np.amax(np.argwhere(sortedScores >= thr))
    topK = topK[:k].tolist()
    topScores = topScores[:k].tolist()
    topNames = [namelist[k] for k in topK.tolist()]
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
    preds = zip(names, scores)
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

def addPred(hashTable, objId, name, score):
    if  not in hashTable:
        hashTable[name] = []       
    hashTable[name].append((objId, score))

def hashObjs(hashTable, objDict):
    for objId in objDict:
        obj = objDict[objId]
        if "name" in obj:
            addPred(hashTable, objId, obj["name"], 1.0)
        if "preds" in obj:
            for pred in enumerate("preds"):
                addPred(hashTable, objId, pred[0], pred[1])
    return hashTable

with open(dataFilenamePred, "w") as f:
   json.dump(data, f)

# count = 0

# for imageId in [468993, 252940, 75888, 469134, 536947, 207178, 469338, 338304, 469398, 427762, 427762, 207323, 469529, 207400, 469618, 207507, 338591, 469671, 76468, 207548, 469824, 473919, 469896, 207797, 338949, 338949, 338986, 207967, 339058, 208050, 208054, 208169, 470366, 208494, 208524, 208623, 470773, 339738, 470909, 208861, 471043, 208991, 209018, 209048, 78035, 471342, 423935, 13031, 209290, 209419, 471578, 253386, 340701, 231568, 78748, 253433, 209901, 472109, 210002, 253455, 362682, 472164, 210050, 341196, 79084, 210273, 79446, 210520, 79721, 472960, 210920, 473109, 79920, 209930, 341006, 473196, 473219, 80013, 211108, 211120, 80104, 211186, 342367, 211386, 473632, 473720, 473821, 342817, 342933, 211891, 343031, 81079, 474398, 212346, 212346, 81287, 81303, 474571, 343506, 474609, 474786, 474862, 474862, 474868, 474906, 474906, 101013, 343954, 81860, 212945, 344025, 344094, 475208, 344271, 82138, 213224, 82157, 82157, 79229, 475398, 475407, 101088, 344415, 82293, 213432, 122954, 122962, 213525, 57433, 213586, 82518, 82668, 213765, 213773, 344928, 476029, 82826, 82921, 476172, 214224, 214224, 83161, 214255, 345507, 214503, 214527, 83531, 345711, 369404, 476843, 214703, 83639, 214753, 476936, 345884, 477042, 345993, 35826, 346140, 346140, 84130, 477435, 84235, 215353, 215394, 346517, 84431, 346577, 215524, 215554, 215608, 84540, 215633, 477791, 101491, 346821, 346904, 346954, 538423, 215897, 84929, 478155, 85005, 85005, 216133, 216161, 85298, 85328, 85340, 85353, 347666, 216618, 478766, 478798, 347772, 85632, 347836, 216852, 216861, 479011, 85956, 217156, 86250, 479477, 210988, 479586, 479597, 479617, 86442, 276552, 276552, 348594, 138179, 217554, 369503, 58137, 348854, 86951, 218234, 544104, 349480, 87356, 218637, 218678, 480842, 349837, 87740, 349888, 349926, 350002, 429710, 87912, 87920, 88040, 88092, 88102, 386066, 386066, 219261, 219315, 481550, 350623, 219589, 211370, 351017, 351053, 351057, 351081, 212462, 89071, 89078, 482305, 89174, 89174, 89210, 482562, 351504, 351590, 351590, 89503, 482720, 482730, 80470, 298924, 482848, 220716, 89781, 89814, 221000, 352127, 352184, 221155, 124243, 483389, 483476, 483476, 352495, 90374, 352549, 352684, 90560, 352789, 352794, 221846, 352949, 484066, 484075, 221932, 15157, 222317, 222317, 91263, 222340, 222340, 91318, 222424, 353551, 484627, 353577, 222548, 353624, 484722, 238911, 484842, 484842, 353817, 91715, 91715, 91844, 485071, 223033, 354126, 223241, 223243, 223335, 92377, 354527, 223554, 485709, 485731, 92534, 354744, 354814, 223874, 486034, 486172, 355272, 224238, 486438, 321385, 486632, 93434, 224594, 93534, 190372, 93670, 224777, 224916, 356094, 93964, 225075, 225238, 94194, 356351, 487428, 487498, 225378, 487630, 225532, 168662, 487702, 487774, 225700, 356863, 356937, 357096, 226111, 387216, 357254, 95132, 168781, 488673, 226579, 226631, 95595, 357748, 357819, 95677, 488915, 357860, 357888, 226848, 6748, 489019, 226883, 226959, 227187, 16025, 358302, 358302, 358342, 96354, 436218, 227460, 227468, 358572, 96492, 358652, 489764, 358795, 227801, 96755, 358901, 227893, 227901, 490081, 97036, 359219, 490322, 359268, 490529, 97379, 46889, 359569, 97465, 490683, 490701, 228771, 97800, 260765, 97865, 229014, 97974, 300323, 409572, 360350, 322211, 98493, 491755, 492075, 361029, 492102, 229981, 230056, 361147, 99067, 562645, 230175, 492609, 169505, 230669, 492817, 230739, 361819, 492905, 492914, 361992, 361993, 475396, 230964, 362090, 99984, 100001, 100006, 448511, 231140, 100111, 493334, 362289, 362483, 38574, 169648, 100438, 362640, 494077, 494085, 494141, 232088, 257136, 257136, 363181, 232315, 363403, 101270, 363432, 363460, 494608, 232563, 101588, 494869, 232905, 363981, 232950, 101985, 364190, 364205, 495291, 410231, 495349, 102367, 233553, 364665, 102644, 233790, 235575, 102741, 233825, 505344, 496081, 102872, 82688, 365133, 496402, 234349, 257529, 234526, 103490, 365642, 365642, 365642, 365652, 234592, 234684, 496854, 103851, 497158, 104002, 235130, 366295, 17365, 235491, 497660, 235778, 366873, 104829, 367074, 236023, 104980, 105052, 105052, 501055, 367313, 105220, 105234, 498489, 367452, 367528, 454478, 498666, 236535, 498747, 498747, 498856, 236717, 105647, 105668, 105670, 105751, 236837, 105872, 499104, 410880, 148737, 237230, 237263, 499591, 499618, 214349, 367275, 368671, 106661, 237745, 237759, 237797, 368884, 237860, 237869, 500019, 106901, 369122, 238071, 238147, 107105, 369309, 107167, 107183, 500435, 500446, 369379, 500514, 238449, 345580, 500765, 238700, 238708, 369817, 542260, 107939, 370090, 370170, 239235, 160726, 501439, 501523, 501538, 370475, 370711, 236604, 502141, 240028, 502229, 240185, 371395, 324051, 371503, 147675, 371650, 371652, 502848, 109916, 503144, 503148, 109942, 503196, 241149, 241209, 241269, 372466, 138975, 138975, 241453, 110460, 241559, 503707, 372654, 241602, 95336, 110562, 503790, 372756, 110617, 372817, 372861, 241844, 241867, 504074, 241986, 373060, 242095, 111109, 373255, 373266, 504378, 242363, 111448, 504726, 373713, 504811, 504891, 111683, 504900, 373848, 111811, 111819, 374083, 243031, 374115, 106046, 243090, 243091, 243104, 112110, 243218, 505371, 505447, 112298, 505528, 324554, 579859, 243482, 374564, 505650, 171678, 112739, 112798, 243946, 243955, 112988, 113019, 244099, 244111, 375198, 113113, 237316, 113282, 506515, 244455, 113473, 113493, 244571, 113828, 245026, 245153, 376233, 245232, 245274, 368559, 245295, 376372, 376456, 507557, 245448, 245462, 245462, 114398, 379158, 139113, 114586, 565233, 114684, 114726, 376891, 508101, 114972, 115088, 508312, 246197, 508370, 246252, 346880, 565341, 565341, 508538, 508541, 246436, 508672, 150320, 508713, 412471, 246613, 377723, 246717, 508977, 368821, 377946, 246878, 368836, 509131, 378096, 378147, 378169, 281512, 509531, 412604, 116370, 247576, 509786, 116574, 378948, 247918, 379014, 200296, 379055, 247984, 116936, 379085, 248129, 379332, 379378, 117308, 248488, 117425, 379584, 117527, 379837, 128849, 248847, 511066, 303653, 303667, 118073, 118124, 511379, 511546, 118447, 249534, 118465, 249608, 380754, 511892, 511895, 249838, 369323, 118788, 118802, 118867, 381031, 381037, 512112, 249969, 118911, 512151, 250066, 381246, 250227, 250240, 512421, 381430, 250368, 381519, 381599, 381610, 250655, 119630, 250703, 250758, 119710, 119752, 512974, 512985, 381991, 513066, 250954, 347664, 513129, 382122, 120061, 382207, 251181, 382256, 382307, 382307, 382333, 575755, 382411, 120282, 382670, 513778, 251801, 383066, 120935, 383137, 252135, 383229, 121162, 514417, 514437, 252342, 514508, 391588, 391588, 383607, 121497, 479008, 383703, 383842, 514984, 121849, 384015, 304305, 366316, 122172, 384482, 384486, 515585, 515670, 515777, 384723, 42288, 515876, 515895, 384827, 253767, 516143, 516342, 516503, 123469, 217205, 516865, 254732, 254745, 254789, 254807, 254814, 123810, 254919, 386119, 386164, 255096, 386204, 124135, 386332, 517454, 195470, 517465, 124297, 517612, 255483, 386592, 517832, 545093, 387082, 124975, 125072, 256195, 387355, 387369, 518605, 256518, 125539, 387725, 256668, 387773, 125755, 256838, 387916, 125782, 519027, 388130, 125997, 125997, 519271, 388299, 424196, 388395, 388395, 126257, 388422, 126340, 519569, 130291, 283217, 519744, 195851, 126540, 519758, 126606, 126606, 558510, 126833, 126914, 126983, 126995, 520289, 127092, 389256, 127120, 567329, 479953, 520427, 389400, 127313, 258509, 127477, 389649, 127510, 127517, 258702, 127775, 389986, 327149, 127987, 390184, 340332, 128058, 521282, 128110, 521359, 259342, 259513, 521669, 521689, 259576, 390671, 567565, 259690, 522007, 21498, 391139, 260094, 480268, 129113, 260221, 391365, 522489, 391463, 327413, 391837, 391857, 522941, 129735, 391889, 391940, 260910, 523123, 261026, 261050, 523195, 480416, 523360, 205102, 153624, 523403, 392392, 392476, 392481, 523565, 130432, 130619, 261732, 130712, 130732, 392915, 392915, 393054, 261999, 262016, 130948, 524245, 524245]:
#     idx = imgsInfo[imageId]["idx"]
#     objNum = imgsInfo[imageId]["objectsNum"]
#     boxes = h5f["features-2"][idx][:objNum]
#     scores = h5f["features-3"][idx][:objNum]
#     maxScores = np.max(scores, axis = -1)
#     maxClasses = np.argmax(scores, axis = -1)
#     if args.attr:
#         ascores = h5f["features-4"][idx][:objNum]
#         # maxAscores = np.max(ascores, axis = -1)
#         # maxAttrs = np.argmax(ascores, axis = -1)
#     # image = GetImageData(id=imageId)
#     # print ("The url of the image is: %s" % image.url)

#     fig, ax = plt.subplots()
#     fig.set_size_inches(18.5, 10.5)
#     # response = requests.get(image.url)
#     # img = PIL_Image.open(io.BytesIO(response.content))
#     idp = ("00000000000" + str(imageId))[-12:]
#     img = imread("coco/{tier}/COCO_{tier}2014_{idp}.jpg".format(tier = args.tier, idp = idp))

#     i = 0
#     # if len(objs) == 0: 
#     plt.imshow(img)
#     # ax = plt.gca()
#     for i in range(objNum):
#         # if i >= len(objs):
#         #     break
#         # obj = objs[i]
#         # if "relations" not in obj or len(obj["relations"]) == 0:
#         #     continue        
#         #print(obj)
#         ax.add_patch(Rectangle((boxes[i][0], boxes[i][1]),
#                                boxes[i][2] - boxes[i][0],
#                                boxes[i][3] - boxes[i][1],
#                                fill=False,
#                                edgecolor='red',
#                                linewidth=1))
#         text = classes[maxClasses[i]] + ("({})".format(int(maxScores[i]*100)))
#         if args.attr:
#             topK = ascores[i].argsort()[-args.topAttrs:][::-1]
#             topScores = [str(int(x*100)) for x in ascores[i][topK].tolist()]
#             text += "\n"
#             text += " ".join([attrs[k] for k in topK.tolist()]) + ("({})".format(" ".join(topScores)))
#         ax.text(boxes[i][0], boxes[i][1], text, style='italic', bbox={'facecolor':'white', 'alpha':0.5}) # , 'pad':10
#         # i += 1
#     # fig = plt.gcf()
#     plt.tick_params(labelbottom='off', labelleft='off')
#     #plt.show()
#     plt.savefig("w"+count+"_"+imageId+".jpg", dpi = 720) # +"_"+str(j) # _rel
#     plt.close(fig)
    
#     count += 1
#     if count > args.count:
#         break 
