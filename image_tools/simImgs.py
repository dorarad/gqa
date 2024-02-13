import json
import h5py
import argparse
import numpy as np
import math
import multiprocessing

parser = argparse.ArgumentParser()
parser.add_argument('--sample', default=2000, type=int)
parser.add_argument('--l2', action = "store_true")
parser.add_argument('--median', action = "store_true")
parser.add_argument('--dataname', type=str)
parser.add_argument('--outname', type=str)
parser.add_argument('--thr', default=0.2, type=float)
parser.add_argument('--num', default=2000, type=int)
parser.add_argument('--verbose', action = "store_true")
parser.add_argument('--tnum', default=20, type=int)
parser.add_argument('--vocab', required=True, type = str)

# python simImgs.py --l2 --dataname --verbose --vocab

args = parser.parse_args()

from numpy import dot
from numpy.linalg import norm

def simFunc(a,b): 
    if args.l2:
      return norm(a-b)
    else:
      na = norm(a)
      nb = norm(b) 
      if na == 0 or nb == 0:
          return 0 
      return dot(a, b)/(na*nb)

def simListFunc(alist,b): 
    if args.median:
      distances = [simFunc(a,b) for a in alist]      
    else:
      distances = [simFunc(a,b)**2 for a in alist]
    return sum(distances)

def processList(kList, output):
  for k in kList:
    # print(i)
    certainImgs = [imgId for imgId in key2img[k] if key2img[k][imgId] == 1.0]
    idxs = [imgInfo[imgId]["idx"] for imgId in certainImgs if imgId in imgInfo][:args.sample] 
    kFeats = [features[idx] for idx in idxs]
    if len(kFeats) > 0:
      candidates = np.array([imgId for imgId in imgInfo if imgId not in key2img[k] or (imgId in key2img[k] and key2img[k][imgId] < args.thr)])
      #lengths = [(imgId, simListFunc(kFeats,features[imgInfo[imgC]])) for imgC in candidates]
      lengths = np.array([simListFunc(kFeats,features[imgInfo[imgC]["idx"]]) for imgC in candidates])

      topk = np.argpartition(lengths, min(args.num,len(lengths)))[:args.num]
      topc = candidates[topk]
      topl = lengths[topk]
      top = [(topc[j],str(topl[j])) for j in range(len(topk))]
      output[k] = top
      if args.verbose:
        print(k)
        print([t[0] for t in top])

output_h5_file = args.dataname + ".h5"
output_ids_file = args.dataname + "_imgsInfo.json"

# objList = [x.strip() for x in list(open("objList.txt"))]
imgInfo = json.load(open(output_ids_file))
key2img = json.load(open("key2img.json"))

features = h5py.File(output_h5_file, "r")["features"]

classesList = ['__background__']  
with open(args.vocab, "r") as f:
    for object in f.readlines():
        classesList.append(object.split(",")[0].lower().strip())

# for o in obj2img:
#   obj2img[o] = obj2img[o]

output = {}

kList = [k for k in key2img if k in classesList]

tsize = math.ceil(len(kList) / args.tnum)
points = [tsize * n for n in range(args.tnum)] + [len(kList)]
kLists = [kList[points[n]:points[n+1]] for n in range(args.tnum)]
ps = []
outDicts = []
output = {}

for n in range(args.tnum):
  outDict = {}
  outDicts.append(outDict)

  p = multiprocessing.Process(target=processList, args=(kLists[n],outDict))
  ps.append(p)
  
  p.start()

for n in range(args.tnum):
  ps[n].join()
  outn = outDicts[n]
  for k in outn:
    output[k] = outn[k]

with open("{}.json".format(outname),"w") as f:
  json.dump(output, f)
