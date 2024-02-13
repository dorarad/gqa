import json
from collections import defaultdict
import en

def rels():
	relsIn = open("cRels.py")
	relsOut = open("cRelsNV.json","w")
	# relsCatsOut = open("cAttrsCats.json","w")

	relsJson = {}
	# relsCatsJson = {}

	for line in relsIn:
		line = line.strip()
		if line == "":
			continue
		line = line.split(",")
		rel = line[0]
		count = line[1]
		if len(line) < 3:
			print(line)
		cat = line[2] 
		simCats = []
		subcat = None
		syms = []
		passive = None
		# stative = False
		cases = ["s","o"]
		where, wherePlaces = False, False
		# spatial = (cat == "spatial")
		of, by, located, catS, catO, noQuestion = False, False, False, False, False, False
		aObjPrefix, noObjPrefix, questionThe = False, False, False
		noThat = False
		freqBased = False
		existQuestionOnly = False
		suffix, suffixLast = False, False
		notobj = False

		for field in line[3:]:
			if field.startswith("E:"):
				syms = field[2:].split(",")
			# elif field.startswith("S"):
			# 	stative = True
			elif field.startswith("W"): # q
				where = True	
			elif field.startswith("w"): # q
				wherePlaces = True	
			elif field.startswith("O"): # q
				of = True	
			elif field.startswith("M"): # q
				by = True				
			elif field.startswith("ss"): # q
				catS = True	
			elif field.startswith("oo"): # q
				catO = True					
			elif field.startswith("Q"): # q
				noQuestion = True
			elif field.startswith("qq"): # q
				existQuestionOnly = True	
				cases = []
			elif field.startswith("F"): # q
				suffix = True
			elif field.startswith("B"): # q
				notobj = True				
			elif field.startswith("ff"): # q
				suffixLast = True														
			elif field.startswith("L"): # q
				located = True	
			elif field.startswith("A"): # done
				aObjPrefix = True	
			elif field.startswith("U"): # done
				noObjPrefix = True	
			elif field.startswith("Y"): # done
				questionThe = True	
			elif field.startswith("T"): # ok.
				noThat = True
			elif field.startswith("C"): # ok.
				freqBased = True																																												
			elif field.startswith("P:"): # ?
				passive = field[2:]
			elif field.startswith("G:"): # ?
				simCats = field[2:].split(".")		
			elif field.startswith("D:"): # ?
				subcat = field[2:]
			elif field.startswith("X:"): # q
				cases = [field[2:]]
		relsJson[rel] = {"cat": cat, "subcat": subcat, "sims": simCats, "syms": syms, 
		                 "count": count, "passive": passive, "cases": cases, "where": where,
		                 "wherePlaces": wherePlaces, "noThat": noThat, "freqBased": freqBased, "notobj": notobj,
		                 "of": of, "by": by, "catS": catS, "catO": catO, "noQuestion": noQuestion, "located": located,
						 "aObjPrefix": aObjPrefix, "noObjPrefix": noObjPrefix, "questionThe": questionThe,
						 "existQuestionOnly": existQuestionOnly, "suffix": suffix, "suffixLast": suffixLast} # "stative": stative, , "spatial": spatial

		# relsCatsJson[cat] = attsCatsJson.get(cat, []) + [att]

	json.dump(relsJson, relsOut)
	# json.dump(attsCatsJson, attsCatsOut)

def attrs():
	attsIn = open("cAttrs.py")
	attsOut = open("cAttrsNV.json","w")
	attsCatsOut = open("cAttrsCatsNV.json","w")

	attsJson = {}
	attsCatsJson = {}

	for line in attsIn:
		line = line.strip()
		if line == "":
			continue
		line = line.split(";")
		att = line[0]
		count = line[1]
		simCats = []
		subcat = None
		cat = ""
		named = False
		sims = []
		syms = []
		adjForm = ""
		isAdj = True
		isPrefix = True
		for field in line[2:]:
			field = field.strip()
			if field == "":
				continue
			if field.startswith("S:"):
				sims = field[2:].split(",")
			elif field.startswith("E:"):
				syms = field[2:].split(",")
			elif field.startswith("A:"):
				adjForm = field[2:]
			elif field.startswith("N"):
				isAdj = False
			elif field.startswith("P"):
				isPrefix = False				
			elif field.startswith("C:"):
				if "," in field[2:]:
					simCats = field[2:].split(",")
				else:
					simCats = [field[2:]]
			elif field.startswith("D:"):
				subcat = field[2:]
			else:
				if field[0].isupper():
					print("!! " + text)				
				if "," in field:
					cat = field.split(",")
				else:
					cat = [field]				
				#named = not cat.isnumeric()				

		if att in attsJson:
			print(att)

		attsJson[att] = {"cat": cat, "subcat": subcat, "simcats": simCats, "sims": sims, 
			"syms": syms, "adjForm": adjForm, "isAdj": isAdj, "isPrefix": isPrefix, "count": count} #"named": named

		for c in cat:
			attsCatsJson[c] = attsCatsJson.get(c, []) + [att]

	json.dump(attsJson, attsOut)
	json.dump(attsCatsJson, attsCatsOut)

def isAn(name):
    prefix = en.noun.article(name).split(" ")[0]
    if prefix not in ["a", "an"]:
    	print(name)
    return (prefix == "an")

def objs():
	objsIn = open("finishedObjs.py")
	objsOut = open("cObjsNV.json","w")
	objsCatsOut = open("cObjsCatsNV.json","w")
	objsOutTxt = open("cObjsSortedNV.py","w")
	# objsOutSTxt = open("cObjsSuperSortedNew.py","w")

	objsJson = {}
	objsCatsJson = {"main": {}, "extra": {}}

	healthy = []
	unhealthy = []
	indoors = []
	outdoors = []
	trivial = []
	singulars = []
	plurals = []
	masses = []
		
	cats = defaultdict(lambda: defaultdict(list))

	for line in objsIn:
		line = line.strip()
		if line == "":
			continue
		# line = line.split(";")
		# if len(line) > 1:
		# 	if line[2].startswith("X"):
		# 		main = False
		# line = line[0]
		text = line
		line = line.split(",")
		obj = line[0]
		count = line[1]
		main = 0
		side = False
		cat = ""
		syms = []
		sims = []
		c = ""
		noCat = False
		personO = False
		the = False
		general = False
		tooGeneral = False
		who = False
		exception = False
		alts = []
		altscat = ""
		indicators = []
		catIndicator = ""
		placeA = False

		inBlacklist = False
		onBlacklist = False

		for field in line[2:]:
			field = field.strip()
			if field == "":
				continue
			if field.startswith("X"):
				main = 1
			elif field.startswith("x"):
				main = 2
			elif field.startswith("V"):
				exception = True								
			elif field.startswith("E:"):
				syms = field[2:].split(".")		
			elif field.startswith("K:"): # ANS dist
				sims = field[2:].split(".")
			elif field.startswith("a:"):
				alts = field[2:].split(".")
			elif field.startswith("b:"):
				altscat = field[2:]
			elif field.startswith("B:"):
				indicators = field[2:].split(".")
			elif field.startswith("J:"):
				catIndicator = field[2:]						
			elif field.startswith("H"): # ok.
				healthy.append(obj)				
			elif field.startswith("U"): # ok.
				unhealthy.append(obj)
			elif field == "i": # done
				indoors.append(obj)				
			elif field == "o": # done
				outdoors.append(obj)				
			elif field.startswith("T"): # ?
				trivial.append(obj)		
			elif field.startswith("S"):
				c = "singular"
				singulars.append(obj)
			elif field.startswith("P"):
				c = "plural"
				plurals.append(obj)				
			elif field.startswith("M"):
				c = "mass"
				masses.append(obj)	
			elif field.startswith("C"): # ok
				c = "singular"
				the = True
			elif field.startswith("F"): # ?
				inBlacklist = True
			elif field.startswith("Z"): # ?
				onBlacklist = True									
			elif field.startswith("A"): # ok
				general = True	
			elif field.startswith("G"): # ok
				tooGeneral = True											
			elif field.startswith("N"): # ok
				noCat = True
			elif field.startswith("W"):	
				who = True					
			elif field.startswith("O"): # ok
				personO = True
			elif field.startswith("pp"): # ok
				placeA = True																								
			else:
				if field[0].isupper():
					print("!! " + text)
				cat = field

		an = False
		if c == "singular":
			an = isAn(obj)
			# print(("an" if an else "a") + " " + obj)

				# if "," in field:
				# 	cat = field.split(",")
				# else:
		# cat = line[-1] if line[-1] != "X" and not line[-1].isnumeric() else ""		
		# if len(line) > 2:
		# 	main = (line[2] != "X")
		# cat = line[-1] if line[-1] != "X" and not line[-1].isnumeric() else ""

		objsJson[obj] = {"count": count, "main": main, "cat": cat, "syms": syms, "sims": sims, "who": who, 
			"exception": exception, "text": text, "mod": c, "noCat": noCat, "personO": personO, "the": the, 
			"general": general, "tooGeneral": tooGeneral, "an": an, "alts": alts, "altscat": altscat, 
			"indicators": indicators, "catIndicator": catIndicator, "placeA": placeA,
			"inBlacklist": inBlacklist, "onBlacklist": onBlacklist} #, "health": health

		objsCatsJson["main" if main else "extra"][cat] = objsCatsJson["main" if main == 0 else "extra"].get(cat, []) + [obj] 
		key = obj.split(" ")[-1]
		cats[cat][key].append(obj)

	# for cat in cats:
	# 	sortedKeys = sorted(cats[cat].keys())
	# 	for key in sortedKeys:
	# 		sortedObjs = sorted(cats[cat][key])
	# 		for obj in sortedObjs:
	# 			objsOutSTxt.write(objsJson[obj]["text"])

	# 			# objsOutSTxt.write("\t\t")

	# 			sing = en.noun.singular(obj)
	# 			plu = en.noun.plural(sing)
	# 			# objsOutSTxt.write(", ".join([sing, plu]))

	# 			# objsOutSTxt.write("\t")

	# 			isSingular = sing == obj
	# 			isMass = (plu == obj) and isSingular
	# 			c = "M" if isMass else ("S" if isSingular else "P") 

	# 			objsOutSTxt.write(", " + c)

	# 			objsOutSTxt.write("\n")
	# 	objsOutSTxt.write("\n")				
	print(healthy)
	print(unhealthy)
	print(indoors)
	print(outdoors)	
	print(trivial)

	# print(singulars)
	# print(plurals)
	# print(masses)

	json.dump(objsJson, objsOut)
	json.dump(objsCatsJson, objsCatsOut)

	for cat in objsCatsJson["main"]:
		for obj in objsCatsJson["main"][cat]:
			objsOutTxt.write("{},{} {}\n".format(obj,objsJson[obj]["count"],cat))
		objsOutTxt.write("\n")

	for cat in objsCatsJson["extra"]:
		for obj in objsCatsJson["extra"][cat]:
			objsOutTxt.write("{},{},X {}\n".format(obj,objsJson[obj]["count"],cat))
		objsOutTxt.write("\n")

attrs() # TODO change count to int
objs()
rels()