# Translates the txt ontology to json ontology.
# See below for specific annotations of objects, attributes and relations.

import json
from collections import defaultdict
import en


def objs():
	objsIn = open("objects.txt")
	objsOut = open("objects.json","w")
	objsCatsOut = open("object_categories.json","w")
	objsOutTxt = open("objects_sorted_output.txt","w")
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
				# Objects to avoid asking direct questions about, since they are not distinctive enough (e.g. dirt)
				# We have 3 degree of avoidance, X, x, and V, based on the types of questions we want to avoid with these objects.
				main = 1
			elif field.startswith("x"):
				# Objects to avoid asking direct questions about, since they are not distinctive enough (e.g. dirt)
				# We have 3 degree of avoidance, X, x, and V, based on the types of questions we want to avoid with these objects.
				main = 2
			elif field.startswith("V"):
				# Objects to avoid asking direct questions about, since they are not distinctive enough (e.g. dirt)
				# We have 3 degree of avoidance, X, x, and V, based on the types of questions we want to avoid with these objects.
				exception = True								
			elif field.startswith("E:"):
				# Synonyms: alternative ways to refer to the attribute (e.g. small and little)
				syms = field[2:].split(".")		
			elif field.startswith("K:"): # ANS dist
				# Similarity group for the object. Indicates objects we don't want to distinguish with
				# e.g., we don't want to have questions that will ask about a lake image, "Is it a sea? no"
				# since that might be too visually similar.
				sims = field[2:].split(".")
			elif field.startswith("a:"):
				# Similarity group for the object. Indicates objects we don't want to distinguish with
				# e.g., we don't want to have questions that will ask about a beach image, "Is it a desert? no"
				# since that might be too visually similar.
				alts = field[2:].split(".")
			elif field.startswith("b:"):
				# Indicates a sub-category, e.g. livestock animals
				altscat = field[2:]
			elif field.startswith("B:"):
				# Indicates a related object, that tends to co-occour, e.g. motorcycle for biker
				# The question engine takes that into account when creating questions to avoid trivial ones.
				indicators = field[2:].split(".")
			elif field.startswith("J:"):
				# Indicates a related category, that tends to co-occour e.g. toy for baby 
				catIndicator = field[2:]						
			elif field.startswith("H"):
				# Does the object refer to healthy food item? e.g. apple
				healthy.append(obj)				
			elif field.startswith("U"):
				# Does the object refer to unhealthy food item? e.g. candy
				unhealthy.append(obj)
			elif field == "i":
				# Does the object refer to indoors place
				indoors.append(obj)				
			elif field == "o":
				# Does the object refer to outdoors place 
				outdoors.append(obj)				
			elif field.startswith("T"):
				# Is the object too similiar to its category?
				# e.g. shoe is a type of footwear, but isn't realy a specific one, so we shouldn't have
				# a question: "what footwear appears in the image? shoe". But for a specific shoe type 
				# like sandal, this question is alright.
				trivial.append(obj)		
			elif field.startswith("S"):
				# Is the object singular? e.g. bear
				c = "singular"
				singulars.append(obj)
			elif field.startswith("P"):
				# Is the object plural? e.g. bears
				c = "plural"
				plurals.append(obj)				
			elif field.startswith("M"):
				# Is the object a mass object? e.g. grass
				c = "mass"
				masses.append(obj)	
			elif field.startswith("C"):
				# Should the object be treated like a proper noun? e.g. the sky 
				c = "singular"
				the = True
			elif field.startswith("F"):
				# Is the object not allowed to be with the relation "in"?
				# e.g. in the fence
				inBlacklist = True
			elif field.startswith("Z"):
				# Is the object not allowed to be with the relation "on"?
				# e.g. in the fence
				onBlacklist = True									
			elif field.startswith("A"):
				# Does the object refer to a category (e.g. appliance)?
				general = True	
			elif field.startswith("G"):
				# This annotation isn't used anymore. Everything that is annotated by A, is also annotated by G.
				tooGeneral = True											
			elif field.startswith("N"):
				# 
				noCat = True
			elif field.startswith("W"):
				# Could the object be an answer to who? (singular or plural, e.g. family)
				who = True					
			elif field.startswith("O"):
				# Is the object a singular person
				personO = True
			elif field.startswith("pp"):
				# Is the object a place, e.g. auditorium
				placeA = True																								
			else:
				# Captures the object category
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

def attrs():
	attsIn = open("attributes.txt")
	attsOut = open("attributes.json","w")
	attsCatsOut = open("attribute_categories.json","w")

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
				# Similarity group. Attributes that are too similar to ask about distinguishing between them.
				# For instance, if the object is white, we don't want to have a question: "Is it grey? No", since grey might be too similar.
				# But it is ok to ask "Is it red? No", since red and white colors are too distant.
				sims = field[2:].split(",")
			elif field.startswith("E:"):
				# Synonyms: alternative ways to refer to the attribute (e.g. small and little)
				syms = field[2:].split(",")
			elif field.startswith("N"):
				# Is the attribute an adjective? If N, then it is not
				# (e.g. glass attribute isn't an adjective, while ceramic is an adjective)
				isAdj = False
			elif field.startswith("A:"):
				# Adjective Form: adjective form for the attribute, if it's not an adjective but has an adjective form.
				# (e.g. metallic for metal, wooden for wood)
				adjForm = field[2:]
			elif field.startswith("P"):
				# Is the attribute could be treated like a verb? (e.g. standing)
				isPrefix = False
			elif field.startswith("C:"):
				# A sub-category for the attribute. e.g. "metal" for steel and iron, cooked for fried and toasted. 
				if "," in field[2:]:
					simCats = field[2:].split(",")
				else:
					simCats = [field[2:]]
			elif field.startswith("D:"):
				# This annotation isn't used anymore.
				subcat = field[2:]
			else:
				# Capture all the category names for the attribute.
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


def rels():
	relsIn = open("relations.txt")
	relsOut = open("relations.json","w")
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
				# Synonyms for the relation. E.g. bigger for larger
				syms = field[2:].split(",")
			# elif field.startswith("S"):
			# 	stative = True
			elif field.startswith("W"): # q
				# relations that refer to location, and thus can be used with "where"
				# questions, e.g. for the relation "eating at" -> "where is he eating?
				where = True	
			elif field.startswith("w"):
				# relations that refer to location, and can be used to indicate location, e.g. on, in 
				wherePlaces = True	
			elif field.startswith("O"): # q
				# relations that refer to location, and thus can be used with "of" questions
				of = True	
			elif field.startswith("M"):
				# relations that refer to location, and thus can be used with "by" questions
				by = True				
			elif field.startswith("ss"): # q
				# relations that go with a singular object 
				catS = True	
			elif field.startswith("oo"): # q
				# relations that go with a plural object 
				catO = True					
			elif field.startswith("Q"): # q
				# relations to skip question generation for
				noQuestion = True
			elif field.startswith("qq"): # q
				# relations to use only in exist questions
				existQuestionOnly = True	
				cases = []
			elif field.startswith("F"): # q
				# relations that could be used at the end of a sentence
				# e.g. what is he standing on? (on appears at the end) 
				suffix = True
			elif field.startswith("B"): # q
				# Relations that don't refer to an object
				notobj = True				
			elif field.startswith("ff"): # q
				# relations that could be used at the end of a sentence
				# and have a verb. "painted on" 
				suffixLast = True														
			elif field.startswith("L"):
				# Spatial relations
				located = True	
			elif field.startswith("A"):
				# Relations after which we can put a countable object (a/an)
				# e.g. served on a plate.
				aObjPrefix = True	
			elif field.startswith("U"):
				# Relations after which we can put a mass object
				# e.g. contains water
				noObjPrefix = True	
			elif field.startswith("Y"):
				# Relations after which we can put a proper object (the)
				# e.g. eating the food
				questionThe = True	
			elif field.startswith("T"):
				# relations that we shouldn't translate in a "that" phrase
				# e.g. for "of": The clock "of" the girl shouldn't be translated to
				# The clock "that is of" the girl, but for relations like "standing behind"
				# it's ok to say: the person "that is standing" behind that girl.
				noThat = True
			elif field.startswith("C"):
				freqBased = True																																												
			elif field.startswith("P:"):
				# annotation of the passive voice for the relation
				# e.g. pulled for pulling
				passive = field[2:]
			elif field.startswith("G:"):
				# sub-category of the relation, e.g. relations that refer to location 
				simCats = field[2:].split(".")		
			elif field.startswith("D:"):
				# antonyms of the relation. e.g. above for under.
				subcat = field[2:]
			elif field.startswith("X:"):
				# relations to avoid in particular questions
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

def isAn(name):
    prefix = en.noun.article(name).split(" ")[0]
    if prefix not in ["a", "an"]:
    	print(name)
    return (prefix == "an")

objs()
attrs()
rels()
