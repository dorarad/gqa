import json

with open("bbox_labels_600_hierarchy.json") as f:
	cats = json.load(f)

names = {}
with open("class-descriptions.csv") as f:
	for line in f:
		line = line.split(",")
		names[line[0]] = line[1].strip().lower()

# print(names)

hrcy = {}
def rec(cat, d):
	cd = {}
	d[names.get(cat["LabelName"],cat["LabelName"])] = cd
	if "Subcategory" in cat:
		for c in cat["Subcategory"]:
			rec(c, cd)

rec(cats, hrcy)

with open("hrcy.json", "w") as f:
	json.dump(hrcy, f) 


with open("vg14/metadata_objsNew.json", "r") as f:
	objectNames = json.load(f) 

objectNames = {o[0]: o[1] for o in objectNames}

ol = open("ol.txt", "w")
fol =  open("fol.txt", "w")

def recPrint(d, prefix):
	cd = {}
	for key in d:
		ol.write(key + "\t\t" + prefix + "\n")
		# if key in objectNames:
		fol.write(key +"," + str(objectNames.get(key,0)) + "\t\t" + prefix + "\n")
		recPrint(d[key], key + "\t\t" + prefix)

recPrint(hrcy, "")

def printCat(d):
	for key in d:
		if d[key] != {}:
			print(key)
			printCat(d[key])

printCat(hrcy)


# with open("hrcy.json") as f:
# 	hrcy = json.load(f)