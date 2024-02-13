# liquid
# sport
# flavor
# event
# + mRels, indoors/outdoors # mAttrs # , trivial?
# + positional / left/right side of the image
# + more interesting refs
# + "ref"/"the"

# + rel equivalences (under/above)
# + a/the/direct freq based for all verbs? probablistic?
# + ancestor partical credit, child? brother/sisters partical credit if not choose not cat question 
# "similarity": True, 
# DONE + definedRef in the img sufix 
# DONE attr not trivial remove
# DONE + or/and for attr (are both the apple and the banana red?)
# DONE do you think
# DONE do you see
# TODO go over cats

# bird, tree aircraft bag meal meat sauce label utensil bottle sign road

objCats = {
    "None": ['thing', 'meal', 'drink', 'alive', 'plant', 'building', 'part', 'symbol', 'place', 'env', 'sign', ""],
    'env': ["nature environment", "urban environment", 'vehicle', 'watercraft', 'aircraft'],
    'thing': ['food', "object", 'clothing', "office supplies", 'sauce', 'ingredient', 'textile', 'label'],
    "object": ['furniture', 'appliance', 'device', "toy", 'tableware', 'container', 'bag',
               'cooking utensil', 'footwear', 'accessory', 'instrument', 'weapon'], # 'vehicle'
    'food': ["fruit", "vegetable", "dessert", 'baked good', 'meat', 'fast food'],
    'fruit': [], 'vegetable': [], 'pastry': [], 'fast food': [], 'dessert': [], 'baked good': ["pastry"], 
    'meat': [], 'sauce': [], 'meal': [], 'drink': [], 'ingredient': [], "textile": [],
    'furniture': [], 'appliance': [], 'device': [], "toy": [],
    'tableware': ["utensil"], 'utensil': [], 'cooking utensil': [],
    'alive': ['person', 'animal', 'pokemon'], "pokemon": [],
    'person': [], 'animal': ['bird'], 'plant': ['tree'], 'tree': [], 'bird': [], 'sign': [], 'bag': [], 
    'clothing': [], 'footwear': [], 'accessory': [],
    'vehicle': [], # 'watercraft', 'aircraft'
    'watercraft': [], 'aircraft': [], 'building':[],
    'part': ["body part", "vehicle part"],
    "body part": [], "vehicle part": [],
    'place': ["room", 'road'], 
    "room": [], 'road': [], 'nature environment': [], 'urban environment': [], 'symbol': [],
    "": [], 'label': [], "office supplies": [], "container": ['bottle'], 'bottle': [], 'instrument': [], 'weapon': []
}

catInfo = {
    "thing": {      "countable": True,      "catCountable": True,       "specific": False,      "qspecific": False,     "aspecific": False,       "standalone": True,       "cat": False,       "similarity": False,        "singular": "thing",            "plural": "things"         }, 
    "object": {     "countable": True,      "catCountable": True,       "specific": False,      "qspecific": False,     "aspecific": False,       "standalone": True,       "cat": False,       "similarity": False,        "singular": "object",           "plural": "objects"        },
    "meal": {       "countable": True,      "catCountable": True,       "specific": False,      "qspecific": False,     "aspecific": False,       "standalone": True,       "cat": False,       "similarity": True,         "singular": "meal",             "plural": "meals"          }, 
    "bag": {        "countable": True,      "catCountable": True,       "specific": True,       "qspecific": True,      "aspecific": True,        "standalone": True,       "cat": True,        "similarity": True,         "singular": "bag",              "plural": "bags"           }, 
    "bird": {       "countable": True,      "catCountable": True,       "specific": True,       "qspecific": True,      "aspecific": True,        "standalone": True,       "cat": True,        "similarity": False,        "singular": "bird",             "plural": "birds"          }, # similarity?
    "sign": {       "countable": True,      "catCountable": True,       "specific": True,       "qspecific": True,      "aspecific": True,        "standalone": True,       "cat": True,        "similarity": True,         "singular": "sign",             "plural": "signs"          }, 
    "drink": {      "countable": True,      "catCountable": True,       "specific": True,       "qspecific": True,      "aspecific": True,        "standalone": True,       "cat": True,        "similarity": False,        "singular": "drink",            "plural": "drinks"         }, 
    "building": {   "countable": True,      "catCountable": True,       "specific": True,       "qspecific": False,     "aspecific": False,       "standalone": True,       "cat": False,       "similarity": False,        "singular": "building",         "plural": "buildings"      }, 
    "food": {       "countable": True,      "catCountable": True,       "specific": True,       "qspecific": True,      "aspecific": True,        "standalone": True,       "cat": True,        "similarity": False,        "singular": "food",             "plural": "food"           }, 
    "vehicle": {    "countable": True,      "catCountable": True,       "specific": True,       "qspecific": True,      "aspecific": True,        "standalone": True,       "cat": True,        "similarity": False,        "singular": "vehicle",          "plural": "vehicles"       }, 
    "toy": {        "countable": True,      "catCountable": True,       "specific": True,       "qspecific": True,      "aspecific": True,        "standalone": True,       "cat": False,       "similarity": False,        "singular": "toy",              "plural": "toys"           }, 
    "fruit": {      "countable": True,      "catCountable": True,       "specific": True,       "qspecific": True,      "aspecific": True,        "standalone": True,       "cat": True,        "similarity": False,        "singular": "fruit",            "plural": "fruit"          }, 
    "dessert": {    "countable": True,      "catCountable": True,       "specific": True,       "qspecific": True,      "aspecific": True,        "standalone": True,       "cat": True,        "similarity": False,        "singular": "dessert",          "plural": "desserts"       }, 
    "meat": {       "countable": True,      "catCountable": True,       "specific": True,       "qspecific": True,      "aspecific": True,        "standalone": True,       "cat": True,        "similarity": True,         "singular": "meat",             "plural": "meat"           }, 
    "pastry": {     "countable": True,      "catCountable": True,       "specific": True,       "qspecific": True,      "aspecific": True,        "standalone": True,       "cat": True,        "similarity": False,        "singular": "pastry",           "plural": "pastries"       }, 
    "utensil": {    "countable": True,      "catCountable": True,       "specific": True,       "qspecific": False,     "aspecific": False,       "standalone": True,       "cat": False,       "similarity": False,        "singular": "utensil",          "plural": "utensils"       },
    "person": {     "countable": True,      "catCountable": True,       "specific": True,       "qspecific": False,     "aspecific": False,       "standalone": True,       "cat": False,       "similarity": False,        "singular": "person",           "plural": "people"         }, 
    "animal": {     "countable": True,      "catCountable": True,       "specific": True,       "qspecific": True,      "aspecific": True,        "standalone": True,       "cat": True,        "similarity": False,        "singular": "animal",           "plural": "animals"        },
    "pokemon": {    "countable": True,      "catCountable": True,       "specific": True,       "qspecific": True,      "aspecific": True,        "standalone": True,       "cat": True,        "similarity": False,        "singular": "pokemon",          "plural": "pokemon"        },
    "plant": {      "countable": True,      "catCountable": True,       "specific": False,      "qspecific": False,     "aspecific": False,       "standalone": False,      "cat": False,       "similarity": False,        "singular": "plant",            "plural": "plants"         }, 
    "tree": {       "countable": True,      "catCountable": True,       "specific": True,       "qspecific": False,     "aspecific": False,       "standalone": True,       "cat": False,       "similarity": True,         "singular": "tree",             "plural": "trees"          },
    "aircraft": {   "countable": False,     "catCountable": False,      "specific": False,      "qspecific": True,      "aspecific": True,        "standalone": True,       "cat": False,       "similarity": True,         "singular": "aircraft",         "plural": "aircraft"       },      
    "sauce": {      "countable": True,      "catCountable": True,       "specific": True,       "qspecific": True,      "aspecific": True,        "standalone": False,      "cat": False,       "similarity": True,         "singular": "sauce",            "plural": "sauces"         },
    "label": {      "countable": True,      "catCountable": True,       "specific": False,      "qspecific": False,     "aspecific": False,       "standalone": False,      "cat": False,       "similarity": True,         "singular": "label",            "plural": "labels"         },
    "bottle": {     "countable": True,      "catCountable": True,       "specific": True,       "qspecific": False,     "aspecific": False,       "standalone": True,       "cat": False,       "similarity": True,         "singular": "bottle",           "plural": "bottles"        },
    "weapon": {     "countable": True,      "catCountable": True,       "specific": True,       "qspecific": True,      "aspecific": True,        "standalone": True,       "cat": True,        "similarity": False,        "singular": "weapon",           "plural": "weapons"        },
    "textile": {    "countable": False,     "catCountable": False,      "specific": False,      "qspecific": False,     "aspecific": False,       "standalone": True,       "cat": False,       "similarity": False,        "singular": "textile",          "plural": "textile"        },
    "device": {     "countable": True,      "catCountable": True,       "specific": True,       "qspecific": True,      "aspecific": True,        "standalone": True,       "cat": True,        "similarity": False,        "singular": "device",           "plural": "devices"        },
    "place": {      "countable": False,     "catCountable": True,       "specific": False,      "qspecific": False,     "aspecific": False,       "standalone": False,      "cat": False,       "similarity": False,        "singular": "place",            "plural": "places"         },
    "room": {       "countable": False,     "catCountable": True,       "specific": False,      "qspecific": False,     "aspecific": False,       "standalone": False,      "cat": False,       "similarity": False,        "singular": "room",             "plural": "rooms"          },
    "symbol": {     "countable": True,      "catCountable": True,       "specific": False,      "qspecific": False,     "aspecific": False,       "standalone": False,      "cat": False,       "similarity": False,        "singular": "symbol",           "plural": "symbols"        },
    "part": {       "countable": False,     "catCountable": False,      "specific": False,      "qspecific": False,     "aspecific": False,       "standalone": False,      "cat": False,       "similarity": False,        "singular": "part ",            "plural": "parts"          },
    "footwear": {   "countable": False,     "catCountable": False,      "specific": False,      "qspecific": False,     "aspecific": False,       "standalone": False,      "cat": False,       "similarity": False,        "singular": "footwear",         "plural": "footwear"       }, 
    "road": {       "countable": False,     "catCountable": True,       "specific": False,      "qspecific": False,     "aspecific": False,       "standalone": False,      "cat": False,       "similarity": True,         "singular": "road",             "plural": "roads"          },  
    "tableware": {  "countable": False,     "catCountable": False,      "specific": False,      "qspecific": False,     "aspecific": False,       "standalone": True,       "cat": False,       "similarity": False,        "singular": "tableware",        "plural": "tableware"      }, 
    "accessory": {  "countable": True,      "catCountable": True,       "specific": False,      "qspecific": False,     "aspecific": False,       "standalone": False,      "cat": False,       "similarity": False,        "singular": "accessory",        "plural": "accessories"    },
    "vegetable": {  "countable": True,      "catCountable": True,       "specific": True,       "qspecific": True,      "aspecific": True,        "standalone": True,       "cat": True,        "similarity": False,        "singular": "vegetable",        "plural": "vegetables"     }, 
    "fast food": {  "countable": True,      "catCountable": True,       "specific": False,      "qspecific": True,      "aspecific": True,        "standalone": True,       "cat": True,        "similarity": False,        "singular": "fast food",        "plural": "fast food"      },
    "container": {  "countable": True,      "catCountable": True,       "specific": True,       "qspecific": False,     "aspecific": False,       "standalone": True,       "cat": False,       "similarity": False,        "singular": "container",        "plural": "containers"     },
    "appliance": {  "countable": True,      "catCountable": True,       "specific": True,       "qspecific": True,      "aspecific": True,        "standalone": True,       "cat": True,        "similarity": False,        "singular": "appliance",        "plural": "appliances"     },
    "body part": {  "countable": False,     "catCountable": False,      "specific": False,      "qspecific": False,     "aspecific": False,       "standalone": False,      "cat": False,       "similarity": False,        "singular": "body part",        "plural": "body parts"     },
    "baked good": { "countable": True,      "catCountable": False,      "specific": False,      "qspecific": True,      "aspecific": True,        "standalone": True,       "cat": True,        "similarity": False,        "singular": "baked good",       "plural": "baked good"     },
    "watercraft": { "countable": False,     "catCountable": False,      "specific": False,      "qspecific": True,      "aspecific": True,        "standalone": True,       "cat": False,       "similarity": True,         "singular": "watercraft",       "plural": "watercraft"     }, 
    "ingredient": { "countable": True,      "catCountable": True,       "specific": False,      "qspecific": False,     "aspecific": False,       "standalone": False,      "cat": False,       "similarity": False,        "singular": "ingredient",       "plural": "ingredients"    },
    "instrument": { "countable": True,      "catCountable": True,       "specific": True,       "qspecific": True,      "aspecific": True,        "standalone": True,       "cat": True,        "similarity": False,        "singular": "instrument",       "plural": "instruments"    },   
    "vehicle part": {   "countable": False, "catCountable": False,      "specific": False,      "qspecific": False,     "aspecific": False,       "standalone": False,      "cat": False,       "similarity": False,        "singular": "vehicle part",                     "plural": "vehicle parts"              },
    "clothing": {       "countable": True,  "catCountable": False,      "specific": False,      "qspecific": False,     "aspecific": True,        "standalone": False,      "cat": False,       "similarity": False,        "singular": "piece|item|article of clothing",   "plural": "pieces|items of clothing"   },
    "furniture": {      "countable": True,  "catCountable": False,      "specific": False,      "qspecific": True,      "aspecific": True,        "standalone": True,       "cat": True,        "similarity": False,        "singular": "piece|item of furniture",          "plural": "pieces|items of furniture"  },
    "cooking utensil": {"countable": True,  "catCountable": True,       "specific": True,       "qspecific": True,      "aspecific": True,        "standalone": True,       "cat": True,        "similarity": False,        "singular": "cooking utensil",                  "plural": "cooking utensils"           },
    "office supplies": {"countable": False, "catCountable": False,      "specific": False,      "qspecific": False,     "aspecific": False,       "standalone": True,       "cat": False,       "similarity": False,        "singular": "office supplies",                  "plural": "office supplies"            },
    "nature environment": {"countable": False, "catCountable": False,   "specific": False,      "qspecific": False,     "aspecific": False,       "standalone": False,      "cat": False,       "similarity": False,        "singular": "", "plural": "" },
    "urban environment": {"countable": False,  "catCountable": False,   "specific": False,      "qspecific": False,     "aspecific": False,       "standalone": False,      "cat": False,       "similarity": False,        "singular": "", "plural": "" },
    "None": {           "countable": False, "catCountable": False,      "specific": False,      "qspecific": False,     "aspecific": False,       "standalone": False,      "cat": False,       "similarity": False,        "singular": "", "plural": "" },
    "alive": {          "countable": False, "catCountable": False,      "specific": False,      "qspecific": False,     "aspecific": False,       "standalone": False,      "cat": False,       "similarity": False,        "singular": "", "plural": "" },
    "env": {            "countable": False, "catCountable": False,      "specific": False,      "qspecific": False,     "aspecific": False,       "standalone": False,      "cat": False,       "similarity": False,        "singular": "", "plural": "" },
    "": {               "countable": False, "catCountable": False,      "specific": False,      "qspecific": False,     "aspecific": False,       "standalone": False,      "cat": False,       "similarity": False,        "singular": "", "plural": "" },
}   

catMass = ["food", "dessert", "meat", "fast food", "baked good"]
catNoncountable = {"clothing": (["piece|item|article of clothing", "clothing item", "clothing item"], ["pieces|items|articles of clothing", "clothing items", "clothing items"], False), 
                "furniture": (["piece|item of furniture"], ["pieces|items of furniture"], False),
                "meat": (["meat"], ["meat"], True), "fast food": (["food"], ["food"], True), "baked good": (["food"], ["food"], True),
                "watercraft": (["watercraft"], ["watercraft"], True), "footwear": (["footwear"], ["footwear"], True),
                "aircraft": (["aircraft"], ["aircraft"], True)}
catAnswerReplace = {"the clothing~ is": "the clothing~ item~ is", "the clothing~ are": "the clothing~ items~ are", 
                    "the furniture~ is": "the piece~ of~ furniture~ is", "the furniture~ are": "the pieces~ of~ furniture~ are", 
                    "the baked~ good~ is": "the food~ is", 
                    "piece|item|article~ of~ clothing~": "clothing~ item~",
                    "pieces|items|articles~ of~ clothing~": "clothing~ items~",
                    "piece|item~ of~ furniture~": "piece~ of~ furniture~",
                    "pieces|items~ of~ furniture~": "pieces~ of~ furniture~"
                    } #  "baked good are": "food is", "baked goods are": "food "
toPlural = {"object": "things"}

ansBlacklist = ["person"]

generalCats = ["plant", "thing", "object", "", "None"]
standalone = ["person", "people"]

indoors = ['classroom', 'gym', 'hallway', 'hospital', 'library', 'lobby', 'lounge', 'museum', 'pub', 'restroom', 
'salon', 'theater', 'room', 'attic', 'bathroom', 'bedroom', 'kitchen', 'office', 'pantry', 'dining room', 
'living room']

outdoors = ['beach', 'cemetery', 'city', 'courtyard', 'desert', 'field', 'forest', 'garden', 'hill', 
'hills', 'hillside', 'hilltop', 'intersection', 'lake', 'swamp', 'lawn', 'mountain', 'ocean', 'park', 
'skate park', 'mountain peak', 'plain', 'pond', 'river', 'sea', 'shore', 'street', 'town', 'village', 'meadow']

trivial = ['clothing', 'clothes', 'attire', 'cloths', 'garment', 'outfit', 'pants', 'shirt', 'shirts', 'sock', 
'socks', 't-shirt', 'vest', 'belt', 'earring', 'earrings', 'footwear', 'shoe', 'shoes', 'sneaker', 'sneakers', 'person', 
'people', 'man']

prefixSpec = {
    "playing": {
        "a": ["game", "video game", "instrument"],
        "the": ["guitar", "violin", "keyboard", "string", "piano", "drum", "drums", "trumpet", "saxophone", "accordion"]
    },
    "playing with": {
        "the": ["umbrella", "shoe", "hydrant", "magnet", "shoes", "car", "laptop"],
        "direct": ["snow", "food", "paper", "cotton"]
    },
    "waiting for": {"a": ["food", "wave", "ride", "drink"]},  
    "served on": {"direct": ["bread", "paper"]},
    "serving": {"the": ["ball"]},
    "leaving": {"direct": ["smoke"]},
    "working on": {"a": ["laptop", "computer"]},
    "wrapped in": {"direct": ["plastic", "paper", "foil", "cellophane", "cloth", "bread", "wax paper"]},
    "cooking": {"a": ["pig", "lobster"]},
    "preparing": {
        "a": ["meal", "drink", "sandwich", "hot dog", "cake"],
        "the": ["table"]
    },
    "buying": {"a": ["watermelon", "banana"]},
    "catching": {"a": ["wave", "waves"]},
    "covered with": {"the": ["ball", "carpet", "tablecloth", "glove"]},
    "covered in": {"a": ["towel"]},
    "grazing on": {"direct": ["grass", "hay", "leaves", "wildflowers", "plants"]}, 
    "grabbing": {"the": ["frisbee", "skateboard", "handle", "snowboard", "board"], 
                 "an": ["apple", "slice", "umbrella", "glass", "jar", "donut"],
                 "direct": ["food", "pizza"]
                },
    "contains": {"a": ["liquid", "flower", "plant", "straw", "spoon", "donut", "sandwich", "bag", "towel", "toothbrush", "pie", "candle", "dessert"]},
    "filled with": {"a": ["toast", "meal"]},
    "surrounded by": {"the": ["fence", "ocean", "wall", "field", "frame", "sidewalk", "border"]}
}

natureMats = ["water", "snow", "sand", "rain", "mud", "leaves", "grass", "dirt", "bush", "ice"]
basicMats = ["metal", "wood", "glass", "brick", "concrete", "leather", "porcelain", "plastic"]

basicColors = ["white", "black", "green", "blue", "red", "yellow"]
colorPairs = [("black", "white"), ("green", "white"), ("blue", "white"), ("red", "white"), 
         ("red", "black"), ("yellow", "black"), ("red", "green"), ("red", "blue"), ("yellow", "blue")]
basicMaterials = ["metal", "wood", "glass", "concrete", "plastic"] # plastic?
materialPairs = [("wood", "metal"), ("glass", "metal"), ("concrete", "metal"), ("plastic", "metal"), 
                ("glass", "wood"), ("concrete", "wood"), ("plastic", "wood"), ("concrete", "glass"), 
                ("plastic", "concrete")]
basicShapes = ["round", "square"]

attrRefTypes = ["color", "pose", "activity", "sportActivity", "size", "shape", "age", "height", "length", 
    "weight", "fatness", "realism", "4", "6", "10", "12", "hardness", "16", "17", "depth", "opaqness", 
    "texture", "cleanliness", "21", "thickness", "22", "face expression", "width", "state", "36"]

waters = ["water", "ocean", "river", "lake", "sea"]

withPhrases = [("dessert", "chocolate"), ("cake", "chocolate"), ("water", "ice"), ("building", "brick"), 
    ("window", "glass"), ("cup", "coffee"), ("fence", "wire"), ("sign", "stop"), ("paper", "writing"), ("floor", "tile"), 
    ("wall", "rock"), ("glass", "wine"), ("beach", "sand"), ("glass", "water"), ("chair", "wheel"), ("bowl", "salad"), 
    ("tower", "clock"), ("cone", "ice cream"), ("fixture", "light"), ("sandwich", "cheese"), ("hill", "snow"), 
    ("engine", "car"), ("chair", "arm"), ("pot", "flower"), ("chandelier", "crystal"), ("mountains", "snow"), 
    ("bowl", "orange"), ("signal", "light"), ("post", "lamp"), ("lamp", "light"), ("stand", "fruit"), ("bowl", "soup"), 
    ("glasses", "water"), ("pole", "flag"), ("bowl", "fruit"), ("bowl", "water"), ("bridge", "arch"), ("glass", "beer"), 
    ("pole", "light"), ("basket", "bread"), ("mountain", "snow"), ("bowl", "food"), ("window", "frame"), ("box", "pizza"), 
    ("rack", "towel"), ("tray", "food"), ("plate", "salad"), ("field", "grass"), ("vase", "flower"), ("boat", "sail"), 
    ("plate", "dessert"), ("building", "dome"), ("building", "tower"), ("pizza", "pepperoni"), ("plate", "cake"), 
    ("pan", "pizza"), ("shelf", "book"), ("table", "food"), ("desk", "computer"), ("cup", "water"), ("horse", "carriage"), 
    ("glass", "juice"), ("post", "sign"), ("pizza", "cheese"), ("container", "food"), ("board", "writing"), 
    ("sandwich", "tomato"), ("house", "roof"), ("shaker", "pepper"), ("ground", "stone"), ("plate", "fruit"), 
    ("box", "donuts"), ("sandwich", "meat and cheese"), ("bag", "apple"), ("floor", "tiles"), ("bowl", "liquid"), 
    ("box", "donut"), ("bush", "flower"), ("box", "vegetable"), ("vase", "water"), ("wall", "graffiti"), ("tree", "blossom"), 
    ("hill", "grass"), ("pizza", "tomato"), ("donut", "chocolate"), ("plate", "food"), ("window", "arch"), ("table", "bench"), 
    ("pizza", "onion"), ("cup", "drink"), ("pizza", "sausage"), ("pizza", "mushroom"), ("bowl", "pasta"), ("bowl", "sauce"), 
    ("area", "grass"), ("shirt", "collar"), ("box", "orange"), ("pot", "plant"), ("field", "dirt")]

whatWhereSpec = {
    "playing in": {"what": natureMats},
    "running in": {"what": natureMats},
    "walking in": {"what": natureMats}, 
    "standing in": 
    {"what": ["grass", "water", "snow", "dirt", "vase", "boat", "mud", "fence", "door", "flower vase", 
    "brush", "rain", "basket", "ice", "hole", "container", "garbage", "engine", "bush", "ice", "leaves"]},
    "playing on":
    {"what": ["laptop", "phone", "computer", "wii",  "tablet",  "device", "cell phone"]},
    "scattered on":
    {"where": ["mountain top", "court", "beach", "bathroom", "field", "street", "hill", "path", "road"]},
    "skiing on": 
    {"what": ["snow", "water", "ice", "ground", "skis", "ski", "terrain", "snowboard"]},
    "standing on": 
    {"where": ["sidewalk", "beach", "field", "court", "street", "hill", "road", "slope", "shore", "hillside", 
    "mountain", "balcony", "patio", "walkway", "park", "roadside", "bus", "train"]},
    "walking on":
    {"what": ["grass", "ground", "sand", "platform", "snow", "dirt", "bridge", "rocks", "floor", "concrete", "water", 
    "asphalt", "bricks", "cement", "rock", "tree", "ice", "bed", "boulder", "ramp", "sticks", "curb", "laptop", 
    "roof", "mud", "bathtub", "table", "vegetation"]},
    "sitting in":
    {"where": ["bleachers", "field", "room", "background", "park", "corner", "restaurant", "stadium", "kitchen", 
    "living room", "crowd", "bus", "bathroom", "train", "parking lot", "street", "airplane", "forest", "beach", 
    "ocean", "lake", "plane", "office", "seating area", "garden", "bushes", "trees", "river", "cafe", "woods", 
    "theater", "area", "floor", "building", "hill", "sidewalk", "meadow", "airport", "fountain", "playground", 
    "lobby", "bar", "grass", "snow", "water"]}, 
    "sitting inside":
    {"where": ["bus", "cafe", "bathroom", "classroom", "living room", "building", "room", "shop", "airplane", 
    "hair salon", "train", "kitchen", "office", "restaurant", "restroom"]}, 
    "sitting on": 
    {"where": ["beach", "field", "hill", "court"]},
    "working on": 
    {"where": ["beach", "train", "plane", "field", "building", "airplane", "bus", "roof"]},
    "walking to":
    {"what": ["racetrack", "train", "bus", "plane", "building", "zebra", "door", "bench", "umbrella", "car", "doorway", "truck"]}, # "beach", "store", 
    "going into": {"where": ["building", "ocean", "street", "pasture", "field", "parking lot", "pool", "kitchen", "shore"]},
    "sleeping in": {"where": ["grass", "corner", "building"]}, # "arms", 
    "skating on": {"where": ["road", "street", "sidewalk", "court", "highway"]},
    "eating from": {"where": ["trough", "ground", "field", "table", "tray"]},
    "laying on": {"where": ["yard", "pasture", "walkway", "hillside", "beach", "field", "road", "court", "street", "hill", "shore"]} 
}

notPlaces = ["bleachers", "dock", "hill", "hills", "hillside", "hilltop", "intersection", "mountain", 
    "mountain peak", "mountain side", "bus stop", "shelter", "balcony", "rooftop", "room"] 

# remove [-1] word for Where list: 
whereRemove = ["displayed on", "grazing in", "growing in", "hanging in", "located in", "lying in", "lying inside", 
    "parked at", "parked in", "playing at", "playing in", "playing on", "running in", "running on", "sitting at", 
    "sitting in", "sitting on", "skiing in", "skiing on", "standing at", "standing in", "walking in", "walking on", 
    "eating in", "working in", "sleeping in", "displayed in", "eating at", "grazing on", "in", "at", "on"] # in at on????

extraPlaces = ["sky", "grass", "snow", "mud", "dirt", "water", "sand", "mirror", "ground", "floor"]

blacklistObjs = ["cloud", "sock"]
tooCommon = ["car", "cars", "cloud", "clouds"]

opsTriples = [
    ("window", "above", "clock"),
    ("fence", "behind", "bench"),
    ("window", "below", "clock"),
    ("bike", "behind", "man"),
    ("cabinet", "below", "sink"),
    ("sign", "above", "window"),
    ("clock", "above", "window"),
    ("bench", "behind", "fence"),
    ("clock", "below", "window"),
    ("man", "behind", "bike"),
    ("sink", "below", "cabinet"),
    ("window", "above", "sign")
]

directions = ["down", "up", "left", "right", "away", "forward", "ahead", "out", "outside", "behind", "back", "upward", "straight", 
              "downward", "sideways", "at camera", "in mirror", "downwards", "upwards", "backwards"]
facingDirections = ["left", "right", "the same direction", "the camera", "away", "front", "back"]


mRelActivity = ["holding up", "shaking", "taking", "making", "brushing"]
mRelWhere = {"pointing": "pointing to", "looking": "looking at", "facing": "facing"}
mRelWhereDir = {"pointing": directions, "looking": directions, "facing": facingDirections}
mRelWhat = ["looking for", "playing"] # music, games
games = ["frisbee", "tennis", "baseball", "soccer"]

subtypes = {
    "ball": ["tennis", "soccer"],
    "player": ["tennis", "soccer", "baseball"],
    "game": ["tennis", "soccer", "baseball"],
    "cake": ["chocolate", "vanilla", "cheese"],
    "ice cream": ["chocolate", "vanilla", "strawberry"],
    "syrup": ["chocolate", "vanilla", "strawberry"],
    "sauce": ["chocolate", "vanilla", "strawberry"],
    "cupcake": ["chocolate", "vanilla", "strawberry"],
    "milkshake": ["chocolate", "vanilla", "strawberry"],
    "donut": ["chocolate", "vanilla"],
    "frosting": ["chocolate", "vanilla", "strawberry"],
    "icing": ["chocolate", "vanilla", "strawberry"],
    "cookie": ["chocolate", "vanilla"],
    "mug": ["coffee", "beer"],
    "bottle": ["water", "wine"],
    "glass": ["water", "wine"]
}

nonIds = ["frisbee", "tennis", "baseball", "wii", "music", "soccer", "video games", 
    "games", "football", "volleyball", "basketball", "badminton", "cricket", "food", 
    "waves", "fish", "luggage", "shoe", "wave", "seat"]

flavors = ["chocolate", "vanilla", "cheese", "strawberry"]
tabletop = ["table", "counter", "countertop", "desk"]
weathers = ["clear", "sunny", "cloudless", "cloudy", "foggy", "overcast", "partly cloudy", "stormy", "rainy"]

multiObj = [("man", "wearing"), ("woman", "wearing"), ("person", "wearing"), ("boy", "wearing"), ("girl", "wearing"), 
    ("pizza", "with"), ("player", "wearing"), ("snow", "covering"), ("snow", "on"), ("guy", "wearing"), 
    ("child", "wearing"), ("fence", "in front of"), ("lady", "wearing"), ("people", "on"), ("man", "in front of"), 
    ("man", "with"), ("skier", "wearing"), ("batter", "wearing"), ("people", "wearing"),("leaves", "on"), 
    ("sandwich", "with"), ("hot dog", "with"), ("grass", "on"), ("catcher", "wearing"), ("giraffe", "in front of"), 
    ("woman", "with"), ("tree", "in front of"), ("grass", "covering"), ("woman", "in front of"), ("bus", "in front of"), 
    ("fence", "surrounding"), ("people", "in"), ("bench", "in front of"), ("elephant", "in front of"), 
    ("skateboarder", "wearing"), ("umpire", "wearing"), ("train", "in front of"), ("snowboarder", "wearing"), 
    ("tiles", "covering")] # wearing

multiSubj = [("on", "table"), ("in", "sky"), ("on", "plate"), ("on", "wall"), ("in", "water"), ("on", "bed"), 
    ("on", "pizza"), ("on", "ground"), ("on", "desk"), ("on", "floor"), ("on", "counter"), ("on top of", "table"), 
    ("on", "grass"), ("on", "shelf"), ("in front of", "building"), ("in", "grass"), ("on", "boat"), ("in", "snow"), 
    ("on top of", "plate"), ("on", "hill"), ("on", "tray"), ("on", "sand"), ("in front of", "trees"), ("below", "sky"), 
    ("on", "dish"), ("in front of", "tree"), ("on", "mountain"), ("on", "snow"), ("on the side of", "building"), 
    ("in front of", "fence"), ("in front of", "wall"), ("on top of", "bed"), ("at", "table"), ("on top of", "pizza"), 
    ("covered by", "snow"), ("on", "stove"), ("on top of", "counter"), ("on top of", "desk"), ("on", "pavement"), 
    ("in", "bag"), ("in", "boat"), ("on", "paper"), ("crossing", "street"), ("on", "bookshelf"), ("on", "countertop")]

multiRel = ["to the left of", "to the right of", "behind", "above", "below", "on the side of", "near"]
onWhitelist = ["desk", "counter", "countertop", "carpet"]
toys = ["mickey mouse", "snoopy", "monster", "figure", "robot", "pikachu"]

# opsList = [
#     (["covering"], ["covered by"]),
#     (["behind", "in back of"], ["in front of"]),
#     (["above"], ["under", "below", "beneath", "underneath"]),
#     (["to the left of"], ["to the right of"]),
#     (["near", "next to"], ["near", "next to"]),
#     (["surrounding"], ["surrounded by"]),
#     (["supporting"], ["supported by"]),
#     (["decorating"], ["decorated with"])
# ] # cast by,

opsList = [
    (["covering"], ["covered by"]),
    (["behind", "in the back of"], ["in front of"]),
    (["above"], ["below", "under", "beneath", "underneath"]),
    (["to the left of"], ["to the right of"]),
    (["near", "next to"], ["near", "next to"]),
    (["surrounding"], ["surrounded by"]),
    (["following"], ["followed by"]),
    (["pulling"], ["pulled by"]),
    (["pushing"], ["pushed by"]),
    # (["surrounding"], ["surrounded by"]),
    # (["supporting"], ["supported by"]),
    (["decorating"], ["decorated with"])
    # (["shorter than"], ["taller than", "longer than"])
    # (["smaller than"], ["larger than", "bigger than"])    
] # cast by,

def opsList2Dict(l):
    d = {}
    for x, y in l:
        for xx in x:
            d[xx] = y[0]
        for yy in y:
            d[yy] = x[0]
    return d 

ops = opsList2Dict(opsList) 

negativeList = [
    (["behind", "in the back of"], ["in front of"], 0),
    (["above"], ["under", "below", "beneath", "underneath"], 0),
    (["to the left of"], ["to the right of"], 0),
    (["on top of"], ["on the bottom of"], 0),
    (["inside"], ["outside"], 0),
    (["on the back of"], ["on the front of"], 0),
    (["standing in front of"], ["standing behind"], 1),
    (["sitting in front of"], ["sitting behind"], 1),
    (["parked in front of"], ["parked behind"], 1),
    (["entering"], ["exiting"], 0)
    # (["shorter than"], ["taller than", "longer than"], 1)
    # (["smaller than"], ["larger than", "bigger than"], 1)
]

oneWordAns = {
    "in the back of": "back",
    "in front of": "front",
    "to the left of": "left",
    "to the right of": "right",
    "on top of": "top",
    "on the bottom of": "bottom",
    "on the front of": "front",
    "standing in front of": "front",
    "standing behind": "behind",
    "sitting in front of": "front", 
    "sitting behind": "behind",
    "parked in front of": "front",
    "parked behind": "behind"
}

def negList2Dict(l):
    d = {}
    for x, y, p in l:
        for xx in x:
            d[xx] = (y, p)
        for yy in y:
            d[yy] = (x, p) 
    return d 

# ops = opsList2Dict(opsList)  
negative = negList2Dict(negativeList)

oppositeComp = {
    "healthier": "less healthy",
    "less healthy": "healthier",
    "younger": "older",
    "older": "younger",
    "taller": "shorter",
    "longer": "shorter",
    "larger": "smaller",
    "bigger": "smaller",
    "smaller": "larger",
    "higher": "lower",
    "lower": "higher"
}

toCaps = {"tv": "TV", "tvs": "TVs", "cd": "CD", "cds": "CDs", "dvds": "DVDs", "suv": "SUV", "eiffel": "Eiffel", 
    "christmas": "Christmas", "elmo": "Elmo", "mickey": "Mickey", "asian": "Asian", "styrofoam": "Styrofoam", 
    "caucasian": "Caucasian", "adidas": "Adidas", "nike": "Nike", "wii": "Wii", "american": "American", 
    "chinese": "Chinese", "french": "French", "santa": "Santa", "parmesan": "Parmesan", "mexican": "Mexican", 
    "nutella": "Nutella", "coke": "Coke", "coca": "Coca", "cola": "Cola", "xbox": "Xbox", "dvd": "DVD", 
    "lego": "Lego", "oreo": "Oreo", "pikachu": "Pikachu", "pokemon": "Pokemon"} #  mouse
withoutThe = ["Pikachu", "Elmo", "Mickey~ mouse"]

attrOps ={"large": "small",
    "young": "old",
    "tall": "short",
    "long": "short",
    "new": "old",
    "sparse": "dense",
    "dense": "sparse",
    "fresh": "rotten",
    "rotten": "fresh",
    "adidas": "nike",
    "nike": "adidas",
    "happy": "sad",
    "sad": "happy",
    "vertical": "horizontal",
    "horizontal": "vertical",
    "narrow": "wide",
    "wide": "narrow",
    "short sleeved": "long sleeved",
    "long sleeved": "short sleeved",
    "modern": "antique",
    "antique": "modern",
    "male": "female",
    "female": "male",
    "paved": "unpaved",
    "unpaved": "paved",
    "ripe": "unripe",
    "unripe": "ripe",
    "peeled": "unpeeled",
    "unpeeled": "peeled",
    "lit": "unlit",
    "unlit": "lit",
    "up": "down",
    "down": "up",
    "on": "off",
    "off": "on",
    "beautiful": "ugly",
    "ugly": "beautiful",
    "immature": "mature",
    "mature": "immature",
    "healthy": "unhealthy",
    "unhealthy": "healthy",
    "uncomfortable": "comfortable",
    "comfortable": "uncomfortable",
    "regular": "irregular",
    "irregular": "regular",
    "open": "closed",
    "closed": "open",
    "empty": "full",
    "full": "empty",
    "wet": "dry",
    "dry": "wet",
    "light colored": "dark colored",
    "dark colored": "light colored",
    "shallow": "deep",
    "deep": "shallow",
    "dirty": "clean",
    "clean": "dirty",
    "thick": "thin",
    "fat": "thin",
    # "blond": "brunette",
    # "brunette": "blond",
    "opaque": "clear"
}

attrOpsList = ["large", "young", "tall", "long", "new", "sparse", "dense", "fresh", "rotten", 
    "adidas", "nike", "happy", "sad", "vertical", "horizontal", "narrow", "wide", "short sleeved", 
    "long sleeved", "modern", "antique", "male", "female", "paved", "unpaved", "ripe", "unripe", 
    "peeled", "unpeeled", "lit", "unlit", "up", "down", "on", "off", "beautiful", "ugly", "immature", 
    "mature", "healthy", "unhealthy", "uncomfortable", "comfortable", "regular", "irregular", "open", 
    "closed", "empty", "full", "wet", "dry", "light colored", "dark colored", "shallow", "deep", 
    "dirty", "clean", "thick", "fat", "opaque", "old", "short", "thin",
    "left", "right", "bottom", "top", "indoors", "outdoors"] # "blond", "brunette", 

attrMultiOps = {
    "old": {"age": "young", "4": "new"},
    "short": {"height": "tall", "length": "long"},
    "thin": {"fatness": "fat", "thickness": "thick"}
}

toDelAttrs = [
    ("large", "water"),
    ("large", "sky"),
    ("large", "grass"),
    ("open", "grass"),
    ("open", "water")
]

exceptAttrs = [
    ("large", "wall"),
    ("open", "sky"),
    ("open", "field"),
    ("full", "tree"),
    ("fresh", "snow"),
    ("open", "wings")
]

attrWhich = ['flavor', 'color', 'shape', 'texture', 'race', 'company', 'pattern', 'gender'] # , "orientation"

anFixes = {
    " an crocodile": " a crocodile",
    " a engine": " an engine",
    " an plane": " a plane",
    " an rubber": " a rubber",
    " an power~ outlet": " a power~ outlet",
    " a oar": " an oar",
    " a extinguisher":  " an extinguisher"
}

gInfo = {
    "verifyState":      { "type": "verify"  },
    "verifyStateT":     {                    "out": ["queryState"] },
    "verifyStateF":     {                    "out": ["chooseState"] },
    "queryState":       { "type": "query",   "out": ["verifyStateT", "verifyStateF", "chooseState"] },
    "chooseState":      { "type": "choose" }, # "out": ["verifyStateT", "verifyStateF", "queryState"]
    "queryAttr":        { "type": "query",   "out": ["verifyAttrT", "verifyAttrF", "chooseAttr"] }, # , "existT", "existOrT", "existNotOrT", "existAttrOrT", "existAttrT"
    "verifyAttr":       { "type": "verify"  },
    "verifyAttrT":      {                    "out": ["queryAttr"] }, # , "existT", "existOrT", "existNotOrT", "existAttrOrT", "existAttrT", 
    "verifyAttrF":      {                    "out": ["chooseAttr", "verifyAttrsF", "verifyAttrAndF"] },
    "verifyAttrs":      { "type": "logical" },
    "verifyAttrsT":     {                    "out": ["verifyAttrT"] }, #  "existT", "existOrT", "existNotOrT", "existAttrOrT", "existAttrT", 
    "verifyAttrsF":     {                   },
    "chooseAttr":       { "type": "choose"}, # "out": ["verifyAttrT", "verifyAttrF", "chooseAttr", "existT", "verifyAttrsF"] "existOrT", "existNotOrT", "existAttrOrT", "existAttrT", 
    "exist":            { "type": "verify"  },
    "existT":           {                    "out": ["existOrT"] },
    "existF":           {                    "out": ["existAndF", "existRelF", "existNotF"] }, # existAttrF
    "existAttrT":       {                    "out": ["existNotT", "existAttrOrT"] },
    "existAttrF":       {                   }, # "verifyAttrF", "chooseAttr"
    "existNotT":        {                    "out": ["existT"] },
    "existNotF":        {                    "out": ["existAttrF"] },
    "existRel":         { "type": "verify"  },
    "existRelT":        { "type": "verify",  "out": ["existT", "queryRel"] },
    "existRelF":        { "type": "verify"  },
    "logicOr":          { "type": "logical" },
    "logicAnd":         { "type": "logical" },
    "existOrT":         {                   },
    "existOrF":         {                    "out": ["existF"] },
    "existAttrOrT":     {                    "out": ["existNotOrT"] },
    "existAttrOrF":     {                    "out": ["existAttrF"] },
    "existNotOrT":      {                    "out": ["existOrT"] },
    "existNotOrF":      {                    "out": ["existNotF", "existAttrOrF"] },
    "existAndT":        {                    "out": ["existT"] },
    "existAndF":        {                   },
    "verifyAttrAndT":   {                    "out": ["verifyAttrT"] },
    "verifyAttrAndF":   {                   },
    "queryObject":      { "type": "query",   "out": ["existT"] }, # "chooseObject", 
    "queryAttrObject":  { "type": "query",   "out": ["existAttrT"] }, # "queryObject", "chooseObject", queryAttr and verifyAttr?????????? 
    "queryNotObject":   { "type": "query",   "out": ["existNotT"] }, # "queryObject", 
    "chooseObject":     { "type": "choose" },
    "chooseAttrObject": { "type": "choose",  "out": ["chooseNotObject"] },
    "chooseNotObject":  { "type": "choose",  "out": ["chooseAttrObject"] },
    "queryRel":         { "type": "query",   "out": ["verifyRelT", "existRelT", "compare", "sameT", "chooseRel"] }, # verifyRelT ?????? similar to exist
    "verifyRel":        { "type": "verify",  "out": ["queryRel"]}, # queryRelT
    "verifyRelT":       {                    "out": ["verifyRelTO", "verifyRelFN"] },
    "verifyRelF":       {                   },
    "chooseRel":        { "type": "choose",  "out": ["verifyRelT"] },
    "chooseObjRel":     { "type": "choose",  "out": ["verifyRelT"] },
    "allSame":          { "type": "compare" },
    "allSameT":         {                    "out": ["allDiffF"] },
    "allSameF":         {                    "out": ["allDiffT"] },
    "allDiff":          { "type": "compare" },
    "allDiffT":         {                    "out": ["allSameF"]},
    "allDiffF":         {                    "out": ["allSameT"] },    
    "compare":          { "type": "compare", "out": ["verifyRelT", "compareT"] }, # , "verifyRelF" "verifyRelTO", 
    "common":           { "type": "compare", "out": ["sameT"] },
    "same":             { "type": "compare" },
    "sameT":            {                    "out": ["diffF"] },
    "sameF":            {                    "out": ["diffT"] },
    "diff":             { "type": "compare" },
    "diffT":            {                    "out": ["sameF"] },
    "diffF":            {                    "out": ["sameT"] },
} # count, more compare
# "chooseAttr" -> "queryT" for opsAtrs + left/right
questionSubtypes = [
    (["diffAnimals"], ["diffAnimalsC"]),
    (["diffGender"], ["diffGenderC"]),
    (["exist"], ["existC"]),
    (["existAnd"], ["existAndC"]),
    (["existAttr"], ["existAttrC"]),
    (["existAttrNot"], ["existAttrNotC"]),
    (["existAttrOr"], ["existAttrOrC"]),
    (["existMaterial"], ["existMaterialC"]),
    (["existMaterialNot"], ["existMaterialNotC"]),
    (["existOr"], ["existOrC"]),
    (["existRelS"], ["existRelSC", "existRelSRC"]),
    (["existThatOr"], ["existThatOrC"]),
    (["locationVerify"], ["locationVerifyC"]),
    (["materialVerify"], ["materialVerifyC"]),
    (["placeVerify"], ["placeVerifyC"]),
    (["positionVerify"], ["positionVerifyC"]),
    (["relVerify"], ["relVerifyCo", "relVerifyCop", "relVerifyCs", "relVerifyCr"]),
    (["sameAnimals"], ["sameAnimalsC"]),
    (["sameGender"], ["sameGenderC"]),
    (["twoDifferent"], ["twoDifferentC"]),
    (["twoSame"], ["twoSameC"]),
    (["verifyAttr"], ["verifyAttrC"]),
    (["verifyAttrAnd"], ["verifyAttrAndC"]),
    (["verifyAttrThis"], ["verifyAttrCThis"]),
    (["verifyAttrs"], ["verifyAttrsC"]),
    (["verifyMaterialAnd"], ["verifyMaterialAndC"]),
    (["weatherVerify"], ["weatherVerifyC"]),
    (["typeVerify"], ["typeVerifyC"]),
    (["companyVerify"], ["companyVerifyC"])
]

subtypeOf = {}
for tlist, flist in questionSubtypes:
    t = tlist[0]
    for f in flist:
        subtypeOf[f] = t
    subtypeOf[t] = t

subtypeUbPreProb = {
    "diffAnimals": 0.5, # 0.8,
    "diffGender": 0.5, # 0.25,
    "exist": 0.5, # 0.56,
    "existAnd": 0.75,
    "existAttr": 0.5, # 0.32,
    "existAttrNot": 0.5, # 0.3,
    "existAttrOr": 0.25,
    "existMaterial": 0.5, # 0.55,
    "existMaterialNot": 0.5, # 0.58,
    "existOr": 0.29,
    "existRelS": 0.5, # 0.48,
    "existThatOr": 0.18,
    "locationVerify": 0.5,
    "materialVerify": 0.5, # 0.35,
    "placeVerify": 0.5,
    "positionVerify": 0.5,
    "relVerify": 0.5, #0.25, #36,
    "sameAnimals": 0.5, #0.27,
    "sameGender": 0.5, #0.77,
    "twoDifferent": 0.5, #0.22,
    "twoSame": 0.5, #0.78,
    "verifyAttr": 0.5, # 0.44,
    "verifyAttrAnd": 0.87,
    "verifyAttrThis": 0.5, #0.3,
    "verifyAttrs": 0.5,
    "verifyMaterialAnd": 0.82,
    "weatherVerify": 0.5,
    "typeVerify": 0.5,
    "companyVerify": 0.5
}

# subtypeUbPostProb = {
# }

# "small": "large" # person
ofTypes = ['weight', 'depth', 'pattern'] # , 'orientation'
directTypes = ['flavor', 'color', 'size', 'shape', 'height', 'width', 'gender', 'length', 'texture']

shortTemplates = {
    "weather": (("How is the weather?", "It is {weather}.", "{weather}"), None),
    "place": (("Which {placeroom} is it?", "It is {aPlace}.", "{place}"), None),
    "directOfD": (("What {type} {is} {dobject}?", "{dobject} {is} {attribute}.", "{attribute}"), "o"), # direct
    "directOfO": (("What is the {type} of {dobject}?", "{dobject} {is} {attribute}.", "{attribute}"), "o"), # direct
    "material": (("What {is} {dobject} made of?", "{dobject} {is} made of {attribute}.", "{attribute}"), "o"),
    "activity": (("What {qis} {dpobject} doing?", "{dobject} {is} {attribute}.", "{attribute}"), "o"),
    "company": (("Which company {is} {dobject} from?", "{dobject} {is} from {attribute}.", "{attribute}"), "o"),
    "category": (("What {kategory} {kis} {kit}?", "The {othis} {ois} {a} {object}.", "{object}"), None),
    "categoryThat": (("What {kategory} {kis} {prop}?", "The {kategory} {kis} {a} {object}.", "{object}"), None),
    "relS": (("{what} {sis} {srel} {dobject}?", "{dsubject} {is} {rel} {dobject}.", "{subject}"), "o"),
    "relO": (("{suffix} {what} {qis} {dsubject} {qrel} {of}?", "{dsubject} {is} {rel} {dobject}.", "{object}"), "su"),
    "categoryRelO": (("{suffix} what {kategory} {qis} {dsubject} {qrel} {of}?", "{dsubject} {is} {rel} {dobject}.", "{object}"), "su"),
    "categoryRelS": (("What {kategory} {kis} {krel} {dobject}?", "The {category} {cis} {a} {subject}.", "{subject}"), "o")
}

templates = {
    "verifyAttr": {"list": [ # done
            ("{is} {dpobject} {attribute}?", "Yes, {dobject} {is} {attribute}.", "yes", 1, "short"),
            ("Do you think {dpobject} {is} {attribute}?", "Yes, {dobject} {is} {attribute}.", "yes", 0.08),
            ("{does} {dpobject} {look} {attribute}?", "Yes, {dobject} {is} {attribute}.", "yes", 0.25),
            ("{does} {dpobject} have {attribute} {type}?", "Yes, {dobject} {is} {attribute}.", "yes", 0.12, "have"),
            ("Is the {type} of {dobject} {attribute}?", "Yes, {dobject} {is} {attribute}.", "yes", 0.1, "typed", "short"),    # the {type} of 
            # ("{is} {this} {a} {attribute} {sobject}?", "Yes, {dobject} {is} {attribute}.", "yes", 0.3)    
            # is X white in color? small in size? of white color? of small size?
        ],
        "extra": {
            "have": ["color", "size", "shape", "length", "weight", "tone", "texture", "pattern"], # "width" , "orientation"
            "typed": ["color", "size", "shape", "tone", "texture", "pattern"] # , "orientation"
        }
    },
    # are the X and the Y both Z? are either X or Y Z?
    "verifyAttrC": {"list": [ # done
            ("{is} {dpobject} {cAttribute}?", "No, {dobject} {is} {attribute}.", "no", 1),
            ("Do you think {dpobject} {is} {cAttribute}?", "No, {dobject} {is} {attribute}.", "no", 0.08),
            ("{does} {dpobject} {look} {cAttribute}?", "No, {dobject} {is} {attribute}.", "no", 0.25),
            ("{does} {dpobject} have {cAttribute} {type}?", "No, {dobject} {is} {attribute}.", "no", 0.12, "have"),
            ("Is the {type} of {dobject} {cAttribute}?", "No, {dobject} {is} {attribute}.", "no", 0.1, "typed"), # the {type} of     
            # ("{is} {this} {a} {cAttribute} {sobject}?", "No, {dobject} {is} {attribute}.", "no", 0.3)        
            # is X white in color? small in size? of white color? of small size?
        ],
        "extra": {
            "have": ["color", "size", "shape", "length", "weight", "tone", "texture", "pattern"], # "width" , "orientation"
            "typed": ["color", "size", "shape", "tone", "texture", "pattern"] # , "orientation"
        }
    },
    "verifyAttrAnd": {"list": [ # done
            ("Are both {dobject} and {cdobject} {attribute}?", "Yes, both {dobject} and {cdobject} are {attribute}.", "yes", 1),
            ("Do both {dobject} and {cdobject} {look} {attribute}?", "Yes, both {dobject} and {cdobject} are {attribute}.", "yes", 0.3),
            ("Do both {dobject} and {cdobject} have {attribute} {type}?", "Yes, both {dobject} and {cdobject} are {attribute}.", "yes", 0.4, "have"),
            ("Are {dobject} and {cdobject} both {attribute}?", "Yes, both {dobject} and {cdobject} are {attribute}.", "yes", 1),
            ("Do {dobject} and {cdobject} both {look} {attribute}?", "Yes, both {dobject} and {cdobject} are {attribute}.", "yes", 0.3),
            ("Do {dobject} and {cdobject} both have {attribute} {type}?", "Yes, both {dobject} and {cdobject} are {attribute}.", "yes", 0.4, "have"),
            # ("{is} {this} {a} {attribute} {sobject}?", "Yes, {dobject} {is} {attribute}.", "yes", 0.3)    
            # is X white in color? small in size? of white color? of small size?
        ],
        "extra": {
            "have": ["color", "size", "shape", "length", "weight", "tone", "texture", "pattern"], # "width" , "orientation"
            "typed": ["color", "size", "shape", "tone", "texture", "pattern"] # , "orientation"
        }
    },
    # are the X and the Y both Z? are either X or Y Z?
    "verifyAttrAndC": {"list": [ # done
            ("Are both {dobject} and {cdobject} {cAttribute}?", "No, {dobject} {is} {attribute}.", "no", 1), # "No, {dobject} {is} {attribute} but {cdobject} {is} not."
            ("Do both {dobject} and {cdobject} {look} {cAttribute}?", "No, {dobject} {is} {attribute}.", "no", 0.3),
            ("Do both {dobject} and {cdobject} have {cAttribute} {type}?", "No, {dobject} {is} {attribute}.", "no", 0.4, "have"),
            ("Are {dobject} and {cdobject} both {cAttribute}?", "No, {dobject} {is} {attribute}.", "no", 1), # "No, {dobject} {is} {attribute} but {cdobject} {is} not."
            ("Do {dobject} and {cdobject} both {look} {cAttribute}?", "No, {dobject} {is} {attribute}.", "no", 0.3),
            ("Do {dobject} and {cdobject} both have {cAttribute} {type}?", "No, {dobject} {is} {attribute}.", "no", 0.4, "have"),
            # ("{is} {this} {a} {cAttribute} {sobject}?", "No, {dobject} {is} {attribute}.", "no", 0.3)        
            # is X white in color? small in size? of white color? of small size?
        ],
        "extra": {
            "have": ["color", "size", "shape", "length", "weight", "tone", "texture", "pattern"], # "width" , "orientation"
            "typed": ["color", "size", "shape", "tone", "texture", "pattern"] # , "orientation"
        }
    },
    "verifyMaterialAnd": {"list": [ # done
            ("Are both {dobject} and {cdobject} made [out]=0.03 of {attribute}?", "Yes, both {dobject} and {cdobject} are made of {attribute}.", "yes", 1),
            # ("{is} {this} {a} {attribute} {sobject}?", "Yes, {dobject} {is} {attribute}.", "yes", 0.3)    
            # is X white in color? small in size? of white color? of small size?
        ],
        "extra": {
            "have": ["color", "size", "shape", "length", "weight", "tone", "texture", "pattern"], # "width" , "orientation"
            "typed": ["color", "size", "shape", "tone", "texture", "pattern"] # , "orientation"
        }
    },
    # are the X and the Y both Z? are either X or Y Z?
    "verifyMaterialAndC": {"list": [ # done 
            ("Are both {dobject} and {cdobject} made [out]=0.03 of {cAttribute}?", "No, {dobject} {is} made of {attribute}.", "no", 1), # No, {dobject} {is} made of {attribute} but {cdobject} {is} not.
            # ("{is} {this} {a} {cAttribute} {sobject}?", "No, {dobject} {is} {attribute}.", "no", 0.3)        
            # is X white in color? small in size? of white color? of small size?
        ],
        "extra": {
            "have": ["color", "size", "shape", "length", "weight", "tone", "texture", "pattern"], # "width" , "orientation"
            "typed": ["color", "size", "shape", "tone", "texture", "pattern"] # , "orientation"
        }
    }, 
    "verifyAttrThis": {"list": [ # done
            ("{is} {this} {a} {attribute} {object}?", "Yes, {this} {is} {a} {attribute} {object}.", "yes", 1)
            # ("Do you think {this} {is} {a} {attribute} {sobject}?", "Yes, {this} {is} {attribute} {object}.", "yes", 0.1)
        ]
    },
    "verifyAttrCThis": {"list": [ # done
            ("{is} {this} {ca} {cAttribute} {object}?", "No, {this} {is} {a} {attribute} {object}.", "no", 1)
            # ("Do you think {this} {is} {a} {cAttribute} {sobject}?", "No, {this} {is} {attribute} {object}.", "no", 1)
        ]
    },
    # 2 colors
    "verifyAttrs": {"list": [ # done
            ("{is} {dpobject} [both]=0.2 {attribute} and {attribute2}?", "Yes, {dobject} {is} {attribute} and {attribute2}.", "yes", 1),
            #("{does} {dobject} look {attribute1} and {attribute2}?", "Yes, {dobject} {is} {attribute1} and {attribute2}.", "yes", 0.2),
            ("{does} {dpobject} {look} {attribute} and {attribute2}?", "Yes, {dobject} {is} {attribute} and {attribute2}.", "yes", 0.5)
            ("{does} {dpobject} have {attribute} {type} and {attribute2} {type2}?", "Yes, {dobject} {is} {attribute} and {attribute2}.", "yes", 0.3, "have")
            # ("{is} {dobject} [both]=0.2 {attribute2} and {attribute}?", "Yes, {dobject} {is} {attribute2} and {attribute}.", "yes", 1),
            # ("{does} {dobject} have {attribute2} {type2} and {attribute} {type}?", "Yes, {dobject} {is} {attribute2} and {attribute}.", "yes", 0.2, "have")
        ],
        "extra": {
            "have": ["color", "size", "shape", "length", "weight", "tone", "texture", "pattern"] # "width" , "orientation"
        }
    },
    # but not? we cant be sure..
    "verifyAttrsC": {"list": [ # done
            ("{is} {dpobject} [both]=0.2 {attribute} and {cAttribute2}?", "No, {dobject} {is} {attribute} but {attribute2}.", "no", 1),
            ("{is} {dpobject} [both]=0.2 {cAttribute2} and {attribute}?", "No, {dobject} {is} {attribute} but {attribute2}.", "no", 1),
            #("{does} {dobject} look {attribute1} and {cAttribute2}?", "No, {dobject} {is} {attribute1} but {attribute2}.", "no", 0.2),
            #("{does} {dobject} look {cAttribute1} and {attribute2}?", "No, {dobject} {is} {attribute2} but {attribute1}.", "no", 0.2),
            ("{does} {dpobject} {look} {attribute} and {cAttribute2}?", "No, {dobject} {is} {attribute} but {attribute2}.", "no", 0.5),
            ("{does} {dpobject} {look} {cAttribute2} and {attribute}?", "No, {dobject} {is} {attribute} but {attribute2}.", "no", 0.5)
            ("{does} {dpobject} have {attribute} {type} and {cAttribute2} {type2}?", "No, {dobject} {is} {attribute} but {attribute2}.", "no", 0.3, "have"),
            ("{does} {dpobject} have {cAttribute2} {type} and {attribute} {type2}?", "No, {dobject} {is} {attribute} but {attribute2}.", "no", 0.3, "have")
        ],
        "extra": {
            "have": ["color", "size", "shape", "length", "weight", "tone", "texture", "pattern"] # "width" , "orientation"
        }
    },
    "chooseAttr": {"list": [ # done
            ("{is} {dobject} {attribute} or [maybe]=0.02 [{is}_{ref}]=0.02 {cAttribute}?", "{dobject} {is} {attribute}.", "{attribute}", 1),
            ("{does} {dobject} {look} {attribute} or [maybe]=0.02 {cAttribute}?", "{dobject} {is} {attribute}.", "{attribute}", 0.3),
            ("Do you think {dobject} {is} {attribute} or {cAttribute}?", "{dobject} {is} {attribute}.", "{attribute}", 0.05),
            ("How {does} {dobject} {look} [like]=0.3 , {attribute} or [maybe]=0.02 {cAttribute}?", "{dobject} {is} {attribute}.", "{attribute}", 0.08),
            ("What|Which {type} {is} {dobject} , {attribute} or {cAttribute}?", "{dobject} {is} {attribute}.", "{attribute}", 0.3, "typed"),
            ("{is} {dobject} {cAttribute} or [maybe]=0.02 [{is}_{ref}]=0.02 {attribute}?", "{dobject} {is} {attribute}.", "{attribute}", 1),
            ("{does} {dobject} {look} {cAttribute} or [maybe]=0.02 {attribute}?", "{dobject} {is} {attribute}.", "{attribute}", 0.16),
            ("How {does} {dobject} {look} [like]=0.3 , {cAttribute} or [maybe]=0.02 {attribute}?", "{dobject} {is} {attribute}.", "{attribute}", 0.08),
            ("What|Which {type} {is} {dobject} , {attribute} or {cAttribute}?", "{dobject} {is} {attribute}.", "{attribute}", 0.3, "typed"),
        ],
        "extra": {
            "typed": ["color", "size", "shape", "tone", "texture", "pattern"] # , "orientation"
        }
    },
    "directOf": {"list": [ # done
            ("What {type} [do_you_think]=0.03 {is} {dobject}?", "{dobject} {is} {attribute}.", "{attribute}", 1, "direct"),
            ("What {type} do you think {dobject} {is}?", "{dobject} {is} {attribute}.", "{attribute}", 0.05, "direct"),
            ("What {type} {does} {dobject} have?", "{dobject} {has} {attribute} {type}.", "{attribute}", 0.1, "have"),
            ("What {type} do you think {dobject} {has}?", "{dobject} {has} {attribute} {type}.", "{attribute}", 0.01, "have"),
            ("What [do_you_think]=0.03 is the {type} of {dobject}?", "{dobject} {is} {attribute}.", "{attribute}", 1, "of"),
            ("Of what {type} [do_you_think]=0.03 {is} {dobject}?", "{dobject} {is} {attribute}.", "{attribute}", 0.05, "of"),
            ("{dobject} {is} [of] what {type}?", "{dobject} {is} {attribute}.", "{attribute}", 0.05, "of"),
            ("{dobject} {has} what {type}?", "{dobject} {is} {attribute}.", "{attribute}", 0.05, "have")
            #("What is the {1dobject}'s {type}?", "{dobject} {is} {attribute}.", "{attribute}",  0.5, "apos")    
        ],
        "extra": {"of": ['flavor', 'color', 'size', 'shape', 'height', 'length', 'weight', 'depth', 'texture', 'race', # 'tone',  'company', 
            'pattern', 'width', 'gender'], # 'state' , 'orientation'
            "direct": ['flavor', 'color', 'size', 'shape', 'height', 'width', 'gender', 'length', 'texture'], # 'pattern',  'state', 'company', 'race', 
            "have": ["flavor", "color", "size", "shape", "length", "weight", "tone", "texture", "pattern"], # "width" , "orientation"
            "synonyms": {"race": ["ethnicity", "ethnic group"]} #, "state": ["condition"]
        }
        #"apos": []} # 'thickness'
    },
    "directWhich": {"list": [ # done
            ("Which {type} [do_you_think]=0.03 {is} {dobject}?", "{dobject} {is} {attribute}.", "{attribute}", 1, "direct"),
            ("Which {type} do you think {dobject} {is}?", "{dobject} {is} {attribute}.", "{attribute}", 0.05, "direct"),
            ("Which {type} {does} {dobject} have?", "{dobject} {has} {attribute} {type}.", "{attribute}", 0.1, "have"),
            ("Which {type} do you think {dobject} {has}?", "{dobject} {has} {attribute} {type}.", "{attribute}", 0.01, "have"),
            # ("Which is the {type} of {dobject}?", "{dobject} {is} {attribute}.", "{attribute}", 1, "of"),
            ("Of which {type} {is} {dobject}?", "{dobject} {is} {attribute}.", "{attribute}", 0.05, "of"),
            ("{dobject} {is} [of] which {type}?", "{dobject} {is} {attribute}.", "{attribute}", 0.05, "of"),
            ("{dobject} {has} which {type}?", "{dobject} {is} {attribute}.", "{attribute}", 0.05, "have")
            #("What is the {1dobject}'s {type}?", "{dobject} {is} {attribute}.", "{attribute}",  0.5, "apos")    
        ],
        "extra": {"of": ['flavor', 'color', 'shape', 'texture', 'race', 'company', 'pattern', 'gender'], # 'state'
            "direct": ['flavor', 'color', 'shape', 'race', 'gender', 'pattern', 'texture'], # 'state', 'company', 
            "have": ["flavor", "color", "shape", "texture", "pattern"], # "width" , "orientation"    
            "synonyms": {"race": ["ethnicity", "ethnic group"]} #, "state": ["condition"]
        }
        # 'size', 'tone', 'size', "size", "length", "weight", "tone", 
        #"apos": []} # 'thickness'
    },
    "how": {"list": [ # done
            ("How {adjType} [do_you_think]=0.03 {is} {dpobject}?", "{dobject} {is} {attribute}.", "{attribute}", 1)
        ],
        "extra": {"aDict": {'size': "large|big", "age": "old", "height": "tall", "length": "long", "weight": "heavy", 
            "depth": "deep", "thickness": "thick", "width": "wide", "cleanliness": "clean", 
            "fatness": "fat", "realism": "real", "hardness": "hard"} # "tone": "dark"
        }
    },
    "material": {"list": [ # done # check what to do with multiple materials
            ("What material [do_you_think]=0.03 {is} {dobject}?", "{dobject} {is} made of {attribute}.", "{attribute}", 0.2),
            ("What [do_you_think]=0.03 is the material of {dobject}?", "{dobject} {is} made of {attribute}.", "{attribute}", 0.2),
            # ("What|Which kind of {mobject} is it?", "The {mobject} {is} {attribute}.", "{attribute}", 0.1),
            ("What [material]=0.05 {is} {dobject} made [out]=0.03 of?", "{dobject} {is} made of {attribute}.", "{attribute}", 1.3),
            ("What [material]=0.05 do you think {dobject} {is} made [out]=0.03 of?", "{dobject} {is} made of {attribute}.", "{attribute}", 0.05),
            ("What [material]=0.2 makes up {dobject}?", "{dobject} {is} made of {attribute}.", "{attribute}",  0.15),
            ("What [material]=0.2 was|is used to make {dobject}?", "{dobject} {is} made of {attribute}.", "{attribute}", 0.15),
            ("What|Which [kind|type_of] material {is} {dobject} made [out]=0.03 of?", "{dobject} {is} made of {attribute}.", "{attribute}", 0.7),
            ("What|Which [kind|type_of] material makes up {dobject}?", "{dobject} {is} made of {attribute}.", "{attribute}",  0.12),
            ("What|Which [kind|type_of] material was|is used to make {dobject}?", "{dobject} {is} made of {attribute}.", "{attribute}", 0.12),    
            ("Of what material {dobject}?", "{dobject} {is} made of {attribute}.", "{attribute}", 0.03),
            ("{dobject} is made [out]=0.03 of what material?", "{dobject} {is} made of {attribute}.", "{attribute}", 0.03)
        ],
        # "extra": {"what/which": 0.85} # what which
    },
    "materialVerify": {"list": [ # done # wood and glass. multiple
            ("{is} {dobject} made [out]=0.03 of {attribute}?", "Yes, {dobject} {is} made of {attribute}.", "yes", 1),
            ("Was|is {attribute} used to make {dobject}?", "Yes, {dobject} {is} made of {attribute}.", "yes", 0.1)
        ]
    },
    "materialVerifyC": {"list": [ # done
            ("{is} {dobject} made [out]=0.03 of {cAttribute}?", "No, {dobject} {is} made of {attribute}.", "no", 1),
            ("Was|is {cAttribute} used to make {dobject}?", "No, {dobject} {is} made of {attribute}.", "no", 0.1)
        ]
    },
    "materialChoose": {"list": [ # done
            ("{is} {dobject} made [out]=0.03 of {attribute} or [maybe]=0.02 {cAttribute}?", "{dobject} {is} made of {attribute}.", "{attribute}", 1),
            ("What [do_you_think]=0.03 was|is used to make {dobject} , {attribute} or [maybe]=0.02 {cAttribute}?", "{dobject} {is} made of {attribute}.", "{attribute}", 0.1),
            ("What material [do_you_think]=0.03 {is} {dobject} , {attribute} or [maybe]=0.02 {cAttribute}?", "{dobject} {is} made of {attribute}.", "{attribute}", 0.3),
            ("What [do_you_think]=0.03 {is} {dobject} made [out]=0.03 of, {attribute} or [maybe]=0.02 {cAttribute}?", "{dobject} {is} made of {attribute}.", "{attribute}", 0.3),
            ("What makes up {dobject} , {attribute} or [maybe]=0.02 {cAttribute}?", "{dobject} {is} made of {attribute}.", "{attribute}",  0.3),
            ("Which material {is} {dobject} made [out]=0.03 of, {attribute} or [maybe]=0.02 {cAttribute}?", "{dobject} {is} made of {attribute}.", "{attribute}", 0.3),
            ("Which material makes up {dobject} , {attribute} or [maybe]=0.02 {cAttribute}?", "{dobject} {is} made of {attribute}.", "{attribute}",  0.3),
            ("Which material [do_you_think]=0.03 was|is used to make {dobject} , {attribute} or [maybe]=0.02 {cAttribute}?", "{dobject} {is} made of {attribute}.", "{attribute}", 0.3),
            ("{is} {dobject} made [out]=0.03 of {cAttribute} or [maybe]=0.02 {attribute}?", "{dobject} {is} made of {attribute}.", "{attribute}", 1),
            ("What was|is used to make {dobject} , {cAttribute} or [maybe]=0.02 {attribute}?", "{dobject} {is} made of {attribute}.", "{attribute}", 0.1)
        ]
    },
    # same activity questions?
    "activity": {"list": [ # done
            ("What [do_you_think]=0.03 {qis} {dpobject} doing?", "{dobject} {is} {attribute}.", "{attribute}", 1)
        ]
    },
    "activityChoose": {"list": [ # done
            ("What [do_you_think]=0.03 {is} {dpobject} doing, {attribute} or [maybe]=0.02 {cAttribute}?", "{dobject} {is} {attribute}.", "{attribute}", 1),
            ("What [do_you_think]=0.03 {is} {dpobject} doing, {cAttribute} or [maybe]=0.02 {attribute}?", "{dobject} {is} {attribute}.", "{attribute}", 1)
        ]
    },
    "company": {"list": [ # done
            ("What|which|which company [do_you_think]=0.03 {is} {dobject} from?", "{dobject} {is} from {attribute}.", "{attribute}", 1),
            ("What|which|which company made {dobject}?", "{attribute} made {attribute}.", "{attribute}", 1),
            ("What [do_you_think]=0.03 is the company that made {dobject}?", "The company that made {dobject} is {attribute}.", "{attribute}", 0.2),
            # ("What [do_you_think]=0.03 is the name of {dobject} company?", "The company name is {attribute}.", "{attribute}", 0.4),
            ("{how} is the company the made {dobject} called?", "The company is {attribute}.", "{attribute}", 0.4)
        ]
    },
    "companyVerify": {"list": [ # done
            ("Did {attribute} make {dobject}?", "Yes, {dobject} {was} made by {attribute}.", "yes", 1),
            ("{was} {dobject} made by {attribute}?", "Yes, {dobject} {was} made by {attribute}.", "yes", 1),
        ]
    },
    "companyVerifyC": {"list": [ # done
            ("Did {cAttribute} make {dobject}?", "No, {dobject} {was} made by {attribute}.", "no", 1),
            ("{was} {dobject} made by {cAttribute}?", "No, {dobject} {was} made by {attribute}.", "no", 1),
        ]
    },
    "companyChoose": {"list": [ # done
            ("What|which|which company [do_you_think]=0.03 made {dobject} , {attribute} or [maybe]=0.02 {cAttribute}?", "{dobject} {was} made {attribute}.", "{attribute}", 1),
            ("{was} {dobject} made by {attribute} or [maybe]=0.02 {cAttribute}?", "{dobject} {was} made {attribute}.", "{attribute}", 1),
            ("What|which|which company [do_you_think]=0.03 made {dobject} , {cAttribute} or [maybe]=0.02 {attribute}?", "{dobject} {was} made {attribute}.", "{attribute}", 1),
            ("{was} {dobject} made by {cAttribute} or [maybe]=0.02 {attribute}?", "{dobject} {was} made {attribute}.", "{attribute}", 1),
        ]
    },
    "state": {"list": [ # state object list
            ("How {is} {dobject} [today/{inImg}] ?", "{dobject} {is} {attribute}.", "{attribute}", 1)
            #("What {is} {1dobject}'s condition|state?", "{1dobject} {is} {attribute}.", "{attribute}", 0.3),
        ]
    },
    "stateChoose": {"list": [
            ("How {is} {dobject} [today/{inImg}] , {attribute} or [maybe]=0.02 {cAttribute}?", "{dobject} {is} {attribute}.", "{attribute}", 1)
            ("How {is} {dobject} [today/{inImg}] , {cAttribute} or [maybe]=0.02 {cAttribute}?", "{dobject} {is} {attribute}.", "{attribute}", 1)
            #("What {is} {1dobject}'s condition|state?", "{1dobject} {is} {attribute}.", "{attribute}", 0.3),
        ]
    },

    # "expression": {"list": [ # should?????
    #         ("What is the {edobject}'s facial|face expression?", "{dobject} {is} {attribute}.", "{attribute}", 1),
    #         ("What is the expression on the {edobject}'s face{plural}?", "{edobject}'s expression is {attribute}.", "{attribute}", 0.3),
    #         ("What [kind_of] expression does the {dobject} have [on {refhis} face{plural}]=0.3?", "{edobject}'s expression is {attribute}.", "{attribute}", 0.3)
    #         #("What emotion {is} the {dobject} displaying?", "{1dobject}'s expression is {attribute}.", "{attribute}", 0.3)
    #     ],
    #     "extra" = [
    #         "oList": ["alive"]
    #     ]
    # },
    "place": {"list": [ # Where add todo # done
            ("What kind|type of {placeroom} is it|this|shown|pictured?", "It is {aPlace}.", "{place}", 0.3, "notroom"),
            ("What kind|type of {placeroom} do you think is shown|pictured?", "It is {aPlace}.", "{place}", 0.01, "notroom"),
            ("What kind|type of {placeroom} do you think it is?", "It is {aPlace}.", "{place}", 0.01, "notroom"),
            ("Which room of the house is it|this|shown|pictured?", "It is {aPlace}.", "{place}", 0.3, "room"),            
            ("What|Which {placeroom} is it|this|shown|pictured?", "It is {aPlace}.", "{place}", 1),
            ("What|Which {placeroom} could this be?", "It is {aPlace}.", "{place}", 0.3),
            ("What {placeroom} was the picture|image|photo taken at?", "It was taken at {dPlace}.", "{place}", 0.3),
            ("Where [do_you_think]=0.03 was the picture|image|photo taken?", "It was taken at {dPlace}.", "{place}", 0.3),   
            ("Where is it?", "This is at {dPlace}.", "{place}", 0.5),
            ("Where is this?", "This is at {dPlace}.", "{place}", 0.1),
            ("Which venue [do_you_think]=0.03 is this?", "This is {aPlace}.", "{place}", 0.05),     
            ("What [do_you_think]=0.03 is the picture|image|photo showing?", "It is showing {aPlace}.", "{place}", 0.3),
            ("What {placeroom} does this represent?", "It represents {dPlace}.", "{place}", 0.1),
            ("What|Which {placeroom} is this|the picture|image|photo at|in?", "It is at {dPlace}.", "{place}", 0.3)
        ]
    },
    "placeVerify": {"list": [ # done
            ("Is it {adPlace}?", "Yes, it is {adPlace}.", "yes", 1.5),
            ("Is this {adPlace}?", "Yes, it is {adPlace}.", "yes", 0.5),
            # ("Is this place {place}?", "Yes, it is a {place}.", "yes", 0.5),
            ("Could the|this {placeroom} be {adPlace}?", "Yes, it is {adPlace}.", "yes", 0.5),
            ("Was this|the picture|image|photo taken at|in {adPlace}?", "Yes, it was taken in {adPlace}.", "yes", 0.5),
            ("Is this|the picture|image|photo showing {adPlace}?", "Yes, it is showing {adPlace}.", "yes", 0.5),
            ("Is this a picture|image|photo of {adPlace}?", "Yes, it is showing {adPlace}.", "yes", 0.5)
        ]
    },
    "placeVerifyC": {"list": [ # done
            ("Is it {cadPlace}?", "No, it is {adPlace}.", "no", 1.5),
            ("Is this {cadPlace}?", "No, it is {adPlace}.", "no", 0.5),
            # ("Is this place {place}?", "Yes, it is a {place}.", "yes", 0.5),
            ("Could the|this {placeroom} be {cadPlace}?", "No, it is {adPlace}.", "no", 0.5),
            ("Was this|the picture|image|photo taken at|in {cadPlace}?", "No, the picture was taken in {adPlace}.", "no", 0.5),
            ("Is this|the picture|image|photo showing {cadPlace}?", "No, the picture is showing {adPlace}.", "no", 0.5),
            ("Is this a picture|image|photo of {cadPlace}?", "No, the picture is showing {adPlace}.", "no", 0.5)
        ]
    },    
    "placeChoose": {"list": [ # done
            ("Is it {adPlace} or [maybe]=0.02 {cadPlace}?", "It is {adPlace}.", "{place}", 0.5),
            ("Is this {adPlace} or [maybe]=0.02 {cadPlace}?", "It is {adPlace}.", "{place}", 0.5),
            ("Is this {placeroom} {adPlace} or [maybe]=0.02 {cadPlace}?", "It is {adPlace}.", "{place}", 0.5),
            # ("Could the|this {placeroom} be {adPlace} or [maybe]=0.5 {cadPlace}?", "It is {adPlace}.", "{place}", 0.5),
            ("Was this|the picture|image|photo taken at|in {adPlace} or [maybe]=0.02 at|in {cadPlace}?", "It was taken at {adPlace}.", "{place}", 0.5),
            ("Is this|the picture|image|photo showing {adPlace} or [maybe]=0.02 {cadPlace}?", "It is showing {adPlace}.", "{place}", 0.5),
            ("Is this a picture|image|photo of {adPlace} or [maybe]=0.02 {cadPlace}?", "It is showing {adPlace}.", "{place}", 0.5),
            ("What kind|type of {placeroom} is it,|this,|shown,|pictured, {adPlace} or [maybe]=0.02 {cadPlace}?", "It is {adPlace}.", "{place}", 0.3),
            ("Which {placeroom} is it,|this,|shown,|pictured, {adPlace} or [maybe]=0.02 {cadPlace}?", "It is {adPlace}.", "{place}", 0.3),
            ("What|Which {placeroom} is it,|this,|shown,|pictured, {adPlace} or [maybe]=0.02 {cadPlace}?", "It is {adPlace}.", "{place}", 0.3),
            ("What|Which {placeroom} could this be, {adPlace} or [maybe]=0.02 {cadPlace}?", "It is {adPlace}.", "{place}", 0.3),
            ("What {placeroom} [do_you_think]=0.03 was the picture|image|photo taken at, {adPlace} or [maybe]=0.02 {cadPlace}?", "It was taken at {adPlace}.", "{place}", 0.3),
            ("Where [do_you_think]=0.03 was the picture|image|photo taken, {adPlace} or [maybe]=0.02 {cadPlace}?", "It was taken at {adPlace}.", "{place}", 0.3),   
            ("Where is it, {adPlace} or [maybe]=0.02 {cadPlace}?", "It is {adPlace}.", "{place}", 0.3),
            ("Is it {cadPlace} or [maybe]=0.02 {adPlace}?", "It is {adPlace}.", "{place}", 0.5),
            ("Is this {cadPlace} or [maybe]=0.02 {adPlace}?", "It is {adPlace}.", "{place}", 0.5),
            ("Is this {placeroom} {cadPlace} or [maybe]=0.02 {adPlace}?", "It is {adPlace}.", "{place}", 0.5),
            ("Could the|this {placeroom} be {cadPlace} or [maybe]=0.5 {adPlace}?", "It is {adPlace}.", "{place}", 0.5),
            ("Was this|the picture|image|photo taken at|in {cadPlace} or [maybe]=0.02 at|in {adPlace}?", "It was taken at {adPlace}.", "{place}", 0.5),
            ("Is this|the picture|image|photo showing {cadPlace} or [maybe]=0.02 {adPlace}?", "It is showing {adPlace}.", "{place}", 0.5),
            ("Is this a picture|image|photo of {cadPlace} or [maybe]=0.02 {adPlace}?", "It is showing {adPlace}.", "{place}", 0.5),
            ("What kind|type of {placeroom} is it,|this,|shown,|pictured, {cadPlace} or [maybe]=0.02 {adPlace}?", "It is {adPlace}.", "{place}", 0.3),
            ("What|Which {placeroom} is it,|this,|shown,|pictured, {cadPlace} or [maybe]=0.02 {adPlace}?", "It is {adPlace}.", "{place}", 0.3),
            ("What|Which {placeroom} could this be, {cadPlace} or [maybe]=0.02 {adPlace}?", "It is {adPlace}.", "{place}", 0.3),
            ("What {placeroom} [do_you_think]=0.03 was the picture|image|photo taken at, {cadPlace} or [maybe]=0.02 {adPlace}?", "It was taken at {adPlace}.", "{place}", 0.3),
            ("Where [do_you_think]=0.03 was the picture|image|photo taken, {cadPlace} or [maybe]=0.02 {adPlace}?", "It was taken at {adPlace}.", "{place}", 0.3)   
            ("Where is it, {cadPlace} or [maybe]=0.02 {adPlace}?", "It is {adPlace}.", "{place}", 0.3),
        ]
    },
    # "where": {"list": [
    #         ("Where {is} [the|{this}] {dobject} [at]=0.1?", "{dobject} {is} {in} {dplace}.",  "{dplace}", 1)
    #         ("Where could|might [the|{this}] {dobject} be [at]=0.1?", "{dobject} {is} {in} {dplace}.",  "{dplace}", 0.3)
    #         # ("Where {is} [the|{this}] {dobject} [located]=0.2?", "{dobject} {is} {sptaialRel} {dplace}.", "{dplace}", 1, spatialObj)
    #         # ("Where {is} [the|{this}] {dobject} {sptaialRelVerb}?", "{dobject} {is} {sptaialRel} {dplace}.", "{dplace}", 1, spatialObj)
    #     ]
    # },
    "weather": {"list": [  # done
            ("What weather conditions appear [today/{inImg}]?", "It is {weather}.", "{weather}", 1),
            ("What weather conditions are shown [today/{inImg}]?", "It is {weather}.", "{weather}", 0.3),
            ("What is the weather like [today/{inImg}]?", "It is {weather}.", "{weather}", 3),
            ("How is the weather [today/{inImg}]?", "It is {weather}.", "{weather}", 5),
            ("What are the weather conditions [today/{inImg}]?", "It is {weather}.", "{weather}", 1),
            ("What type of weather do you see [today/{inImg}]?", "It is {weather}.", "{weather}", 1),
            ("What type of weather is in the background?", "It is {weather}.", "{weather}", 0.3),
            ("What type of weather is [today/{inImg}]?", "It is {weather}.", "{weather}", 1),
            ("How is the weather on this day?", "It is {weather}.", "{weather}", 1)
        ]
    },
    "weatherVerify": {"list": [ # ["sunny", "cloudy", "foggy", "stormy", "rainy"] -> snowing  # done
            ("Is it {weather} [today/{inImg}]=0.2?", "Yes, it is {weather}.", "yes", 1),
            ("Is the weather {weather} [today/{inImg}]=0.2?", "Yes, it is {weather}.", "yes", 1),
            ("Does the weather appear to be {weather} [today/{inImg}]=0.2?", "Yes, it is {weather}.", "yes", 0.2)
        ]
    },
    "weatherVerifyC": {"list": [ # done
            ("Is it {cWeather} [today/{inImg}]=0.2?", "No, it is {weather}.", "no", 1),
            ("Is the weather {cWeather} [today/{inImg}]=0.2?", "No, it is {weather}.", "no", 1),
            ("Does the weather appear to be {cWeather} [today/{inImg}]=0.2?", "No, it is {weather}.", "no", 0.2)    
        ]
    },
    "weatherChoose": {"list": [ # done
            ("Is it {weather} or {cWeather} [today/{inImg}]=0.2?", "It is {weather}.", "{weather}", 1),
            ("Is the weather {weather} or {cWeather} [today/{inImg}]=0.2?", "It is {weather}.", "{weather}", 1),
            ("What is the weather like [today/{inImg}] , {weather} or [maybe]=0.02 {cWeather}?", "It is {weather}.", "{weather}", 1),
            ("How is the weather [today/{inImg}] , {weather} or [maybe]=0.02 {cWeather}?", "It is {weather}.", "{weather}", 1),
            ("Is it {cWeather} or {weather} [today/{inImg}]=0.2?", "It is {weather}.", "{weather}", 1),
            ("Is the weather {cWeather} or {weather} [today/{inImg}]=0.2?", "It is {weather}.", "{weather}", 1),
            ("What is the weather like [today/{inImg}] , {cWeather} or [maybe]=0.02 {weather}?", "It is {weather}.", "{weather}", 1),
            ("How is the weather [today/{inImg}] , {cWeather} or [maybe]=0.02 {weather}?", "It is {weather}.", "{weather}", 1)
        ]
    },
    "locationVerify": {"list": [ # done ["sunny", "cloudy", "foggy", "stormy", "rainy"] -> snowing  # done
            ("Is it {location}?", "Yes, it is {location}.", "yes", 1), # [{inImg}]=0.3
            # ("Is the|this picture {location}?", "Yes, it is {location}.", "yes", 0.5),
            ("Is it an {location} scene?", "Yes, it is {location}.", "yes", 1) # |picture
        ]
    },
    "locationVerifyC": {"list": [ # done
            ("Is it {cLocation}?", "No, it is {location}.", "no", 1), #  [{inImg}]=0.3
            # ("Is the picture {cLocation}?", "No, it is {location}.", "no", 0.5),
            ("Is it an {cLocation} scene?", "No, it is {location}.", "no", 1) # |picture
        ]
    },
    "locationChoose": {"list": [ # done
            ("Is it indoors or outdoors?", "It is {location}.", "{location}", 1),
            # ("Is the picture|image indoors or outdoors?", "It is {location}.", "{location}", 0.5),
            ("Is it an indoors or outdoors scene|picture?", "It is {location}.", "{location}", 1),
            ("Is it outdoors or indoors?", "It is {location}.", "{location}", 0.5),
            # ("Is the picture|image outdoors or indoors?", "It is {location}.", "{location}", 0.25),
            ("Is it an outdoors or indoors scene|picture?", "It is {location}.", "{location}", 0.5)            
        ]
    },
    "typeVerify": {"list": [ # done # ["sunny", "cloudy", "foggy", "stormy", "rainy"] -> snowing  # done
            ("{is} {this}|{ref} a {attribute} {object}?", "Yes, {this} {is} a {attribute} {object}.", "yes", 1),
        ]
    },
    "typeVerifyC": {"list": [ # done 
            ("{is} {this}|{ref} a {cAttribute} {object}?", "No, {this} {is} a {attribute} {object}.", "no", 1),

        ]
    },
    "typeChoose": {"list": [ # done 
            ("{is} {this}|{ref} a {attribute} or {cAttribute} {object}?", "{this} {is} a {attribute} {object}.", "{attribute}", 1),
            ("{is} {this}|{ref} a {cAttribute} or {attribute} {object}?", "{this} {is} a {attribute} {object}.", "{attribute}", 1),
        ]
    },
    "activityWho": {"list": [ # done # done
            ("Who [{inImg}]=0.1 {sis} {qattribute}?", "{dobject} {is} {attribute}.", "{object}", 1)
        ]
    },
    "positionVerify": {"list": [ # done # wood and glass. multiple
            ("{is} {dobject} {position} [{side}] [of_the_image|photo|picture]={prob}?", "Yes, {dobject} {is} {position} of the image.", "yes", 1)
        ]
    },    
    "positionVerifyC": {"list": [ # done # wood and glass. multiple
            ("{is} {dobject} {cPosition} [{side}] [of_the_image|photo|picture]={prob}?", "No, {dobject} {is} {position} of the image.", "no", 1)
        ]
    },
    "positionChoose": {"list": [ # done # wood and glass. multiple
            ("{is} {dobject} {position} or {cPosition} [{side}/{side}_of_the_image|photo|picture/of_the_image|photo|picture]={prob}?", "{dobject} {is} {position} of the image.", "{pos}", 1),
            ("{is} {dobject} {cPosition} or {position} [{side}/{side}_of_the_image|photo|picture/of_the_image|photo|picture]={prob}?", "{dobject} {is} {position} of the image.", "{pos}", 1),
            ("{is} {dobject} {position} {side} or {cPosition} [of_the_image|photo|picture/of_the_image|photo|picture]={prob}?", "{dobject} {is} {position} of the image.", "{pos}", 1),
            ("{is} {dobject} {cPosition} {side} or {position} [of_the_image|photo|picture/of_the_image|photo|picture]={prob}?", "{dobject} {is} {position} of the image.", "{pos}", 1),
            ("On which {side} [of_the_image|photo|picture]={prob} {is} {dobject} , the left or the right?", "{dobject} {is} {position} of the image.", "{pos}", 1),
            ("On which {side} [of_the_image|photo|picture]={prob} {is} {dobject} , the right or the left?", "{dobject} {is} {position} of the image.", "{pos}", 1),
            ("Which {side} [of_the_image|photo|picture]={prob} {is} {dobject} on, the left or the right?", "{dobject} {is} {position} of the image.", "{pos}", 0.2),
            ("Which {side} [of_the_image|photo|picture]={prob} {is} {dobject} on, the right or the left?", "{dobject} {is} {position} of the image.", "{pos}", 0.2),
            ("Where {inImg} {is} {dobject} , {position} or {cPosition} [{side}]=0.1?", "{dobject} {is} {position} of the image.", "{pos}", 0.125),
            ("Where {inImg} {is} {dobject} , {cPosition} or {position} [{side}]=0.1?", "{dobject} {is} {position} of the image.", "{pos}", 0.125),
            ("Where {inImg} {is} {dobject} , {position} [{side}]=0.1 or {cPosition}?", "{dobject} {is} {position} of the image.", "{pos}", 0.125),
            ("Where {inImg} {is} {dobject} , {cPosition} [{side}]=0.1 or {position}?", "{dobject} {is} {position} of the image.", "{pos}", 0.125),
            ("Where {is} {dobject} , {position} or {cPosition} [{side}]=0.3 [of_the_image|photo|picture]=1.0?", "{dobject} {is} {position} of the image.", "{pos}", 0.075),
            ("Where {is} {dobject} , {cPosition} or {position} [{side}]=0.3 [of_the_image|photo|picture]=1.0?", "{dobject} {is} {position} of the image.", "{pos}", 0.075)
        ]
    },
    "positionQuery": {"list": [ # done # wood and glass. multiple
            ("On which {side} [of_the_image|photo|picture]={prob} {is} {dobject}?", "{dobject} {is} {position} of the image.", "{pos}", 1),
            ("Which {side} [of_the_image|photo|picture]={prob} {is} {dobject} on?", "{dobject} {is} {position} of the image.", "{pos}", 0.25)
        ]
    },                
    # relO, activity

    # There is a <obj>...; ___ (what type) is it, what is its <type>?

    ## TODO: consistent groups between them!
    # for each question -> entailed questions 
    # 3 clauses?  
    "exist": {"list": [ # done # good candidates: if o -> similar images, if a o -> o with opposite a
                  # o that is not A -> when there is o a 
                  # For Answer: max plural if there is 
            # ("Is there any {object}?", "Yes, there {is} {object}.", "yes", 1),
            ("Are there any {pObject} [{inImg}]=0.25?", "Yes, there {is} {a} {object}.", "yes", 1, "plural"),
            ("Is there {any} {sObject} [{inImg}]=0.9?", "Yes, there {is} {a} {object}.", "yes", 1, "singular"), # TODO! [{inImg}]=0.2? .format(inImg),
            ("Are there {pObject} [{inImg}]=0.9?", "Yes, there {is} {a} {object}.", "yes", 1, "plural"), # TODO! [{inImg}]=0.8 .format(inImg),
            ("Do you see any {pObject} [there/{inImg}]=0.25?", "Yes, there {is} {a} {object}.", "yes", 0.25, "plural"),
            ("Do you see {any} {sObject} [there/{inImg}]=0.6?", "Yes, there {is} {a} {object}.", "yes", 0.25, "singular"), # TODO! [{inImg}]=0.2? .format(inImg),
            ("Do you see {pObject} [there/{inImg}]=0.9?", "Yes, there {is} {a} {object}.", "yes", 0.25, "plural"), # TODO! [{inImg}]=0.8 .format(inImg)
            ("Is any {sObject} visible|observable [there/{inImg}]=0.75?", "Yes, there {is} {a} {object}.", "yes", 0.03, "singular"), # TODO! [{inImg}]=0.2? .format(inImg),
            ("Are any {pObject} visible|observable [there/{inImg}]=0.25?", "Yes, there {is} {a} {object}.", "yes", 0.03, "plural"),
        ]
    },
    "existC": {"list": [ # done # good candidates: if o -> similar images, if a o -> o with opposite a
                  # o that is not A -> when there is o a
            # ("Is there any {cObject}?", "No, there is no {object}.", "no", 1),
            ("Are there any {pObject} [{inImg}]=0.25?", "No, there are no {pObject}.", "no", 1, "plural"),
            ("Is there {any} {sObject} [{inImg}]=0.9?", "No, there {isp} no {psObject}.", "no", 1, "singular"), # TODO!  [{inImg}]=0.2? .format(inImg),
            ("Are there {pObject} [{inImg}]=0.9?", "No, there are no {pObject}.", "no", 1, "plural"), # TODO!  [{inImg}]=0.8 .format(inImg),
            ("Do you see any {pObject} [there/{inImg}]=0.25?", "No, there are no {pObject}.", "no", 0.25, "plural"),
            ("Do you see {any} {sObject} [there/{inImg}]=0.6?", "No, there {isp} no {psObject}.", "no", 0.25, "singular"), # TODO!  [{inImg}]=0.2? .format(inImg),
            ("Do you see {pObject} [there/{inImg}]=0.9?", "No, there are no {pObject}.", "no", 0.25, "plural"), # TODO!  [{inImg}]=0.8 .format(inImg)
            ("Is any {sObject} visible|observable [there/{inImg}]=0.75?", "No, there {isp} no {psObject}.", "no", 0.03, "singular"), # TODO!  [{inImg}]=0.2? .format(inImg),
            ("Are any {pObject} visible|observable [there/{inImg}]=0.25?", "No, there are no {pObject}.", "no", 0.03, "plural"),
        ]
    },
    "existAttr": {"list": [ # done # good candidates: if o -> similar images, if a o -> o with opposite a
                  # o that is not A -> when there is o a
            # ("Is there any {object}?", "Yes, there {is} {a} {attribute} {object} but {ref} {is} not {attribute}.", "yes", 1),
            ("Are there any {attribute} {pObject} [{inImg}]=0.25?", "Yes, there {is} {a} {attribute} {object}.", "yes", 1, "plural"),
            ("Is there {anya} {attribute} {sObject} [{inImg}]=0.9?", "Yes, there {is} {a} {attribute} {object}.", "yes", 1, "singular"),
            ("Are there {attribute} {pObject} [{inImg}]=0.9?", "Yes, there {is} {a} {attribute} {object}.", "yes", 1, "plural"),
            ("Are there any {pObject} [{inImg}] that are {attribute}?", "Yes, there {is} {a} {attribute} {object}.", "yes", 0.13, "plural"),
            ("Is there {any} {sObject} [{inImg}]=0.7 that is {attribute}?", "Yes, there {is} {a} {attribute} {object}.", "yes", 0.11, "singular"),
            ("Are there {pObject} [{inImg}]=0.9 that are {attribute}?", "Yes, there {is} {a} {attribute} {object}.", "yes", 0.11, "plural"),
            ("Are there any {pObject} that are {attribute} {inImg}?", "Yes, there {is} {a} {attribute} {object}.", "yes", 0.13, "plural"),
            ("Is there {any} {sObject} that is {attribute} {inImg}?", "Yes, there {is} {a} {attribute} {object}.", "yes", 0.16, "singular"),
            ("Are there {pObject} that are {attribute} {inImg}?", "Yes, there {is} {a} {attribute} {object}.", "yes", 0.16, "plural"),
            ("Do you see any {attribute} {pObject} [there/{inImg}]=0.1?", "Yes, there {is} {a} {attribute} {object}.", "yes", 0.25, "plural"),
            ("Do you see {anya} {attribute} {sObject} [there/{inImg}]=0.3?", "Yes, there {is} {a} {attribute} {object}.", "yes", 0.25, "singular"),
            ("Do you see {attribute} {pObject} [there/{inImg}]=0.3?", "Yes, there {is} {a} {attribute} {object}.", "yes", 0.25, "plural"),
            ("Do you see any {pObject} [there/{inImg}]=0.1 that are {attribute}?", "Yes, there {is} {a} {attribute} {object}.", "yes", 0.12, "plural"),
            ("Do you see {any} {sObject} [there/{inImg}]=0.2 that is {attribute}?", "Yes, there {is} {a} {attribute} {object}.", "yes", 0.11, "singular"),
            ("Do you see {pObject} [there/{inImg}]=0.3 that are {attribute}?", "Yes, there {is} {a} {attribute} {object}.", "yes", 0.11, "plural")

            # ("Are there any {pObject} [{inImg}] that are {attribute}?", "Yes, there {is} {a} {attribute} {object}.", "yes", 0.1, "plural"),
            # ("Is there {any} {sObject} [{inImg}]=0.7 that is {attribute}?", "Yes, there {is} {a} {attribute} {object}.", "yes", 0.03, "singular"),
            # ("Are there {pObject} [{inImg}]=0.9 that are {attribute}?", "Yes, there {is} {a} {attribute} {object}.", "yes", 0.03, "plural"),
            # ("Do you see any {pObject} [there/{inImg}]=0.1 that are {attribute}?", "Yes, there {is} {a} {attribute} {object}.", "yes", 0.05, "plural"),
            # ("Do you see {any} {sObject} [there/{inImg}]=0.2 that is {attribute}?", "Yes, there {is} {a} {attribute} {object}.", "yes", 0.03, "singular"),
            # ("Do you see {pObject} [there/{inImg}]=0.3 that are {attribute}?", "Yes, there {is} {a} {attribute} {object}.", "yes", 0.03, "plural")
        ]
    },
    "existAttrC": {"list": [ # done # good candidates: if o -> similar images, if a o -> o with opposite a
                  # o that is not A -> when there is o a
            # ("Is there any {object}?", "Yes, there {is} {object} but {ref} {is} not {attribute}.", "yes", 1),
            ("Are there any {cAttribute} {pObject} [{inImg}]=0.25?", "No, there {is} {a} {object} but {ref} {is} {attribute}.", "no", 1, "plural"),
            ("Is there {anya} {cAttribute} {sObject} [{inImg}]=0.9?", "No, there {is} {a} {object} but {ref} {is} {attribute}.", "no", 1, "singular"),
            ("Are there {cAttribute} {pObject} [{inImg}]=0.9?", "No, there {is} {a} {object} but {ref} {is} {attribute}.", "no", 1, "plural"),
            ("Are there any {pObject} [{inImg}] that are {cAttribute}?", "No, there {is} {a} {object} but {ref} {is} {attribute}.", "no", 0.1, "plural"),
            ("Is there {any} {sObject} [{inImg}]=0.7 that is {cAttribute}?", "No, there {is} {a} {object} but {ref} {is} {attribute}.", "no", 0.13, "singular"),
            ("Are there {pObject} [{inImg}]=0.9 that are {cAttribute}?", "No, there {is} {a} {object} but {ref} {is} {attribute}.", "no", 0.13, "plural"),
            ("Are there any {pObject} that are {cAttribute} {inImg}?", "No, there {is} {a} {object} but {ref} {is} {attribute}.", "no", 0.13, "plural"),
            ("Is there {any} {sObject} that is {cAttribute} {inImg}?", "No, there {is} {a} {object} but {ref} {is} {attribute}.", "no", 0.16, "singular"),
            ("Are there {pObject} that are {cAttribute} {inImg}?", "No, there {is} {a} {object} but {ref} {is} {attribute}.", "no", 0.16, "plural"),
            ("Do you see any {cAttribute} {pObject} [there/{inImg}]=0.1?", "No, there {is} {a} {object} but {ref} {is} {attribute}.", "no", 0.25, "plural"),
            ("Do you see {anya} {cAttribute} {sObject} [there/{inImg}]=0.3?", "No, there {is} {a} {object} but {ref} {is} {attribute}.", "no", 0.25, "singular"),
            ("Do you see {cAttribute} {pObject} [there/{inImg}]=0.3?", "No, there {is} {a} {object} but {ref} {is} {attribute}.", "no", 0.25, "plural"),
            ("Do you see any {pObject} [there/{inImg}]=0.1 that are {cAttribute}?", "No, there {is} {a} {object} but {ref} {is} {attribute}.", "no", 0.12, "plural"),
            ("Do you see {any} {sObject} [there/{inImg}]=0.2 that is {cAttribute}?", "No, there {is} {a} {object} but {ref} {is} {attribute}.", "no", 0.11, "singular"),
            ("Do you see {pObject} [there/{inImg}]=0.3 that are {cAttribute}?", "No, there {is} {a} {object} but {ref} {is} {attribute}.", "no", 0.11, "plural")
        ]
    },
    "existThat": {"list": [ # done # good candidates: if o -> similar images, if a o -> o with opposite a
                  # o that is not A -> when there is o a
            # ("Is there any {object}?", "Yes, there {is} {a} {attribute} {object} but {ref} {is} not {attribute}.", "yes", 1),
            ("Are there [any] {pObject} [{inImg}] that are {attribute}?", "Yes, there {is} {a} {object} that {is} {attribute}.", "yes", 1, "plural"),
            ("Is there {any} {sObject} [{inImg}] that is {attribute}?", "Yes, there {is} {a} {object} that {is} {attribute}.", "yes", 1, "singular"),
            ("Do you see [any] {pObject} [there/{inImg}] that are {attribute}?", "Yes, there {is} {a} {object} that {is} {attribute}.", "yes", 0.25, "plural"),
            ("Do you see {any} {sObject} [there/{inImg}] that is {attribute}?", "Yes, there {is} {a} {object} that {is} {attribute}.", "yes", 0.25, "singular")
        ]
    },
    "existThatC": {"list": [ # done # good candidates: if o -> similar images, if a o -> o with opposite a
                  # o that is not A -> when there is o a
            # ("Is there any {object}?", "Yes, there {is} {object} but {ref} {is} not {attribute}.", "yes", 1),
            ("Are there [any] {pObject} [{inImg}] that are {cAttribute}?", "No, there {is} {a} {object} but {ref} {is} {attribute}.", "no", 0.1, "plural"),
            ("Is there {any} {sObject} [{inImg}] that is {cAttribute}?", "No, there {is} {a} {object} but {ref} {is} {attribute}.", "no", 1, "singular"),
            ("Do you see [any] {pObject} [there/{inImg}] that are {cAttribute}?", "No, there {is} {a} {object} but {ref} {is} {attribute}.", "no", 0.25, "plural"),
            ("Do you see {any} {sObject} [there/{inImg}] that is {cAttribute}?", "No, there {is} {a} {object} but {ref} {is} {attribute}.", "no", 0.25, "singular")
        ]
    }, 
    "existAttrNot": {"list": [ # done # good candidates: if o -> similar images, if a o -> o with opposite a
                  # o that is not A -> when there is o a
            # ("Is there any {object}?", "Yes, there {is} {a} {attribute} {object} but {ref} {is} not {attribute}.", "yes", 1),
            ("Are there [any] {pObject} [{inImg}] that are not {cAttribute}?", "Yes, there {is} {a} {attribute} {object}.", "yes", 1, "plural"),
            ("Is there {any} {sObject} [{inImg}] that is not {cAttribute}?", "Yes, there {is} {a} {attribute} {object}.", "yes", 1, "singular"),
            ("Do you see [any] {pObject} [there/{inImg}] that are not {cAttribute}?", "Yes, there {is} {a} {attribute} {object}.", "yes", 0.25, "plural"),
            ("Do you see {any} {sObject} [there/{inImg}] that is not {cAttribute}?", "Yes, there {is} {a} {attribute} {object}.", "yes", 0.25, "singular")
        ]
    },
    # "existAttrNotP": {"list": [ # done # good candidates: if o -> similar images, if a o -> o with opposite a
    #               # o that is not A -> when there is o a
    #         # ("Is there any {object}?", "Yes, there {is} {a} {attribute} {object} but {ref} {is} not {attribute}.", "yes", 1)
    #         ("Are there [any] {pObject} [{inImg}] that are not {cAttribute}?", "Yes, there {is} {a} {object} that {is} {attribute}.", "yes", 1, "plural")
    #         ("Is there {any} {sObject} [{inImg}] that is not {cAttribute}?", "Yes, there {is} {a} {object} that {is} {attribute}.", "yes", 1, "singular")
    #         ("Do you see [any] {pObject} [there/{inImg}] that are not {cAttribute}?", "Yes, there {is} {a} {object} that {is} {attribute}.", "yes", 0.25, "plural")
    #         ("Do you see {any} {sObject} [there/{inImg}] that is not {cAttribute}?", "Yes, there {is} {a} {object} that {is} {attribute}.", "yes", 0.25, "singular")
    #     ]
    # },
    "existAttrNotC": {"list": [ # done # good candidates: if o -> similar images, if a o -> o with opposite a
                  # o that is not A -> when there is o a
            # ("Is there any {object}?", "Yes, there {is} {object} but {ref} {is} not {attribute}.", "yes", 1),
            ("Are there [any] {pObject} [{inImg}] that are not {attribute}?", "No, there {is} {a} {object} but {ref} {is} {attribute}.", "no", 0.1, "plural"),
            ("Is there {any} {sObject} [{inImg}] that is not {attribute}?", "No, there {is} {a} {object} but {ref} {is} {attribute}.", "no", 1, "singular"),
            ("Do you see [any] {pObject} [there/{inImg}] that are not {attribute}?", "No, there {is} {a} {object} but {ref} {is} {attribute}.", "no", 0.25, "plural"),
            ("Do you see {any} {sObject} [there/{inImg}] that is not {attribute}?", "No, there {is} {a} {object} but {ref} {is} {attribute}.", "no", 0.25, "singular")
        ]
    }, 
    "existThatNot": {"list": [ # done # good candidates: if o -> similar images, if a o -> o with opposite a
                  # o that is not A -> when there is o a
            # ("Is there any {object}?", "Yes, there {is} {a} {attribute} {object} but {ref} {is} not {attribute}.", "yes", 1),
            ("Are there [any] {pObject} [{inImg}] that are not {cAttribute}?", "Yes, there {is} {a} {object} that {is} {attribute}.", "yes", 1, "plural"),
            ("Is there {any} {sObject} [{inImg}] that is not {cAttribute}?", "Yes, there {is} {a} {object} that {is} {attribute}.", "yes", 1, "singular"),
            ("Do you see [any] {pObject} [there/{inImg}] that are not {cAttribute}?", "Yes, there {is} {a} {object} that {is} {attribute} .", "yes", 0.25, "plural"),
            ("Do you see {any} {sObject} [there/{inImg}] that is not {cAttribute}?", "Yes, there {is} {a} {object} that {is} {attribute} .", "yes", 0.25, "singular")
        ]
    },
    "existThatNotC": {"list": [ # done # good candidates: if o -> similar images, if a o -> o with opposite a
                  # o that is not A -> when there is o a
            # ("Is there any {object}?", "Yes, there {is} {object} but {ref} {is} not {attribute}.", "yes", 1),
            ("Are there [any] {pObject} [{inImg}] that are not {attribute}?", "No, there {is} {a} {object} but {ref} {is} {attribute}.", "no", 0.1, "plural"),
            ("Is there {any} {sObject} [{inImg}] that is not {attribute}?", "No, there {is} {a} {object} but {ref} {is} {attribute}.", "no", 1, "singular"),
            ("Do you see [any] {pObject} [there/{inImg}] that are not {attribute}?", "No, there {is} {a} {object} but {ref} {is} {attribute}.", "no", 0.25, "plural"),
            ("Do you see {any} {sObject} [there/{inImg}] that is not {attribute}?", "No, there {is} {a} {object} but {ref} {is} {attribute}.", "no", 0.25, "singular")
        ]
    },     
    # "existProp": {"list": [ # done # good candidates: if o -> similar images, if a o -> o with opposite a
    #               # o that is not A -> when there is o a
    #         # ("Is there any {object}?", "Yes, there {is} {a} {attribute} {object} but {ref} {is} not {attribute}.", "yes", 1)
    #         ("Are there any {pObject} [{inImg}] that are {attribute}?", "Yes, there {is} {a} {object} that {is} {attribute}.", "yes", 1, "plural")
    #         ("Is there {any} {sObject} [{inImg}] that is {attribute}?", "Yes, there {is} {a} {object} that {is} {attribute}.", "yes", 1)
    #         ("Are there {pObject} [{inImg}] that are {attribute}?", "Yes, there {is} {a} {object} that {is} {attribute}.", "yes", 1, "plural")
    #     ]
    # },
    # "existPropC": {"list": [ # done # good candidates: if o -> similar images, if a o -> o with opposite a
    #               # o that is not A -> when there is o a
    #         # ("Is there any {object}?", "Yes, there {is} {object} but {ref} {is} not {attribute}.", "yes", 1)
    #         ("Are there any {pObject} [{inImg}] that are {cAttribute}?", "No, there {is} {a} {object} but {ref} {is} {attribute}.", "no", 0.1, "plural")
    #         ("Is there {any} {sObject} [{inImg}] that is {cAttribute}?", "No, there {is} {a} {object} but {ref} {is} {attribute}.", "no", 1)
    #         ("Are there {pObject} [{inImg}] that are {cAttribute}?", "No, there {is} {a} {object} but {ref} {is} {attribute}.", "no", 1, "plural")
    #     ]
    # },    
    # "existPropNot": {"list": [ # done # good candidates: if o -> similar images, if a o -> o with opposite a
    #               # o that is not A -> when there is o a
    #         # ("Is there any {object}?", "Yes, there {is} {a} {attribute} {object} but {ref} {is} not {attribute}.", "yes", 1)
    #         ("Are there any {pObject} [{inImg}] that are not {cAttribute}?", "Yes, there {is} {a} {object} {is} {attribute}.", "yes", 1, "plural")
    #         ("Is there {any} {sObject} [{inImg}] that is not {cAttribute}?", "Yes, there {is} {a} {object} {is} {attribute}.", "yes", 1)
    #         ("Are there {pObject} [{inImg}] that are not {cAttribute}?", "Yes, there {is} {a} {object} {is} {attribute}.", "yes", 1, "plural")
    #     ]
    # },
    # "existPropNotC": {"list": [ # done # good candidates: if o -> similar images, if a o -> o with opposite a
    #               # o that is not A -> when there is o a
    #         # ("Is there any {object}?", "Yes, there {is} {object} but {ref} {is} not {attribute}.", "yes", 1)
    #         ("Are there any {pObject} [{inImg}] that are not {attribute}?", "No, there {is} {a} {object} but {ref} {is} {attribute}.", "no", 0.1, "plural")
    #         ("Is there {any} {sObject} [{inImg}] that is not {attribute}?", "No, there {is} {a} {object} but {ref} {is} {attribute}.", "no", 1)
    #         ("Are there {pObject} [{inImg}] that are not {attribute}?", "No, there {is} {a} {object} but {ref} {is} {attribute}.", "no", 1, "plural")
    #     ]
    # },    
    "existMaterial": {"list": [ # done # good candidates: if o -> similar images, if a o -> o with opposite a
                  # o that is not A -> when there is o a
            # ("Is there any {object}?", "Yes, there {is} {a} {attribute} {object} but {ref} {is} not {attribute}.", "yes", 1),
            ("Are there [any] {pObject} [{inImg}]=0.1 [that_are]=0.75 made [out]=0.03 of {attribute}?", "Yes, there {is} {a} {object} that {is} made of {attribute}.", "yes", 1, "plural"),
            ("Is there {any} {sObject} [{inImg}]=0.1 [that_is]=0.75 made [out]=0.03 of {attribute}?", "Yes, there {is} {a} {object} that {is} made of {attribute}.", "yes", 1, "singular"),
            ("Do you see [any] {pObject} [there/{inImg}]=0.1 [that_are]=0.75 made [out]=0.03 of {attribute}?", "Yes, there {is} {a} {object} that {is} made of {attribute}.", "yes", 0.25, "plural"),
            ("Do you see {any} {sObject} [there/{inImg}]=0.1 [that_is]=0.75 made [out]=0.03 of {attribute}?", "Yes, there {is} {a} {object} that {is} made of {attribute}.", "yes", 0.25, "singular")
            # ("Are there any {pObject} [{inImg}]=0.25 that are {attribute}?", "Yes, there {is} {a} {attribute} {object}.", "yes", 0.3, "plural")
        ]
    },
    "existMaterialC": {"list": [ # done # good candidates: if o -> similar images, if a o -> o with opposite a
                  # o that is not A -> when there is o a
            # ("Is there any {object}?", "Yes, there {is} {a} {attribute} {object} but {ref} {is} not {attribute}.", "yes", 1),
            ("Are there [any] {pObject} [{inImg}]=0.1 [that_are]=0.75 made [out]=0.03 of {cAttribute}?", "No, there {is} {a} {object} but {ref} {is} made of {attribute}.", "no", 1, "plural"),
            ("Is there {any} {sObject} [{inImg}]=0.1 [that_is]=0.75 made [out]=0.03 of {cAttribute}?", "No, there {is} {a} {object} but {ref} {is} made of {attribute}.", "no", 1, "singular"),
            ("Do you see [any] {pObject} [there/{inImg}]=0.1 [that_are]=0.75 made [out]=0.03 of {cAttribute}?", "No, there {is} {a} {object} but {ref} {is} made of {attribute}.", "no", 0.25, "plural"),
            ("Do you see {any} {sObject} [there/{inImg}]=0.1 [that_is]=0.75 made [out]=0.03 of {cAttribute}?", "No, there {is} {a} {object} but {ref} {is} made of {attribute}.", "no", 0.25, "singular")
            # ("Are there any {pObject} [{inImg}]=0.25 that are {attribute}?", "Yes, there {is} {a} {attribute} {object}.", "yes", 0.3, "plural")
        ]
    },  
    "existMaterialNot": {"list": [ # done # good candidates: if o -> similar images, if a o -> o with opposite a
                  # o that is not A -> when there is o a
            # ("Is there any {object}?", "Yes, there {is} {a} {attribute} {object} but {ref} {is} not {attribute}.", "yes", 1),
            ("Are there [any] {pObject} [{inImg}]=0.1 that are not made [out]=0.03 of {cAttribute}?", "Yes, there {is} {a} {object} that {is} made of {attribute}.", "yes", 1, "plural"),
            ("Is there {any} {sObject} [{inImg}]=0.1 that is not made [out]=0.03 of {cAttribute}?", "Yes, there {is} {a} {object} that {is} made of {attribute}.", "yes", 1, "singular"),
            ("Do you see [any] {pObject} [there/{inImg}]=0.1 that are not made [out]=0.03 of {cAttribute}?", "Yes, there {is} {a} {object} that {is} made of {attribute}.", "yes", 0.25, "plural"),
            ("Do you see {any} {sObject} [there/{inImg}]=0.1 that is not made [out]=0.03 of {cAttribute}?", "Yes, there {is} {a} {object} that {is} made of {attribute}.", "yes", 0.25, "singular")
            # ("Are there any {pObject} [{inImg}]=0.25 that are {attribute}?", "Yes, there {is} {a} {attribute} {object}.", "yes", 0.3, "plural")
        ]
    },
    "existMaterialNotC": {"list": [ # done # good candidates: if o -> similar images, if a o -> o with opposite a
                  # o that is not A -> when there is o a
            # ("Is there any {object}?", "Yes, there {is} {a} {attribute} {object} but {ref} {is} not {attribute}.", "yes", 1),
            ("Are there [any] {pObject} [{inImg}]=0.1 that are not made [out]=0.03 of {attribute}?", "No, there {is} {a} {object} but {ref} {is} made of {attribute}.", "no", 1, "plural"),
            ("Is there {any} {sObject} [{inImg}]=0.1 that is not made [out]=0.03 of {attribute}?", "No, there {is} {a} {object} but {ref} {is} made of {attribute}.", "no", 1, "singular"),
            ("Do you see [any] {pObject} [there/{inImg}]=0.1 that are not made [out]=0.03 of {attribute}?", "No, there {is} {a} {object} but {ref} {is} made of {attribute}.", "no", 0.25, "plural"),
            ("Do you see {any} {sObject} [there/{inImg}]=0.1 that is not made [out]=0.03 of {attribute}?", "No, there {is} {a} {object} but {ref} {is} made of {attribute}.", "no", 0.25, "singular")
            # ("Are there any {pObject} [{inImg}]=0.25 that are {attribute}?", "Yes, there {is} {a} {attribute} {object}.", "yes", 0.3, "plural")
        ]
    },        
    # "existOr": {"list": [ # for or / and more simpler phrases (c that is not o or c2 that is a2)
    #     # modifier = e.g. on the table, that...
    #         ("Is there any {object1} or {object2} {thatModifier}?", "Yes, there both {object1} and {object2} {thatModifier}.", "yes", 1)
    #         ("Are there any {objects1} or {objects2} {thatModifier}?", "Yes, there are both {objects1} and {objects2} {thatModifier}.", "yes", 1)
    #         ("Is there [either] {object1} or {object2} {thatModifier}?", "Yes, there are both {object1} and {objects2} {thatModifier}.", "yes", 1)
    #         ("Are there [either] {objects1} or {object2} {thatModifier}?", "Yes, there are both {object1} and {objects2} {thatModifier}.", "yes", 1)
    #     ]
    # },
    "existOr": {"list": [ # done # for or / and more simpler phrases (c that is not o or c2 that is a2)
            # ("Is there any {object} or {cObject} [{inImg}]=0.25?", "Yes, there is {object} {thatModifier}.", "yes", 1),
            ("Are there [either/any/either_any]=1.0 {pObject} or {cpObject} [{inImg}]?", "Yes, there {is} {a} {object}.", "yes", 1, "plural"),
            ("Is there {eAny} {sObject} or {cAny2} {csObject} [{inImg}]=0.9?", "Yes, there {is} {a} {object}.", "yes", 1, "singular"),
            ("Are there [either/any/either_any]=1.0 {cpObject} or {pObject} [{inImg}]?", "Yes, there {is} {a} {object}.", "yes", 1, "plural"),
            ("Is there {ecAny} {csObject} or {any2} {sObject} [{inImg}]=0.9?", "Yes, there {is} {a} {object}.", "yes", 1, "singular"),
            ("Do you see [either/any/either_any]=1.0 {pObject} or {cpObject} [there/{inImg}]?", "Yes, there {is} {a} {object}.", "yes", 0.25, "plural"),
            ("Do you see {eAny} {sObject} or {cAny2} {csObject} [there/{inImg}]=0.7?", "Yes, there {is} {a} {object}.", "yes", 0.25, "singular"),
            ("Do you see [either/any/either_any]=1.0 {cpObject} or {pObject} [there/{inImg}]?", "Yes, there {is} {a} {object}.", "yes", 0.25, "plural"),
            ("Do you see {ecAny} {csObject} or {any2} {sObject} [there/{inImg}]=0.7?", "Yes, there {is} {a} {object}.", "yes", 0.25, "singular")
        ]
    },
    "existOrC": {"list": [ # done # for or / and more simpler phrases (c that is not o or c2 that is a2)
            # ("Is there any {object} or {cObject} [{inImg}]=0.25?", "Yes, there is {object} {thatModifier}.", "yes", 1),
            ("Are there [either/any/either_any]=1.0 {pObject} or {cpObject} [{inImg}]?", "No, there are no {pObject} or {cpObject}.", "no", 1, "plural"),
            ("Is there {eAny} {sObject} or {cAny2} {csObject} [{inImg}]=0.9?", "No, there are no {psObject} or {cpsObject}.", "no", 1, "singular"), # {isp}
            ("Do you see [either/any/either_any]=1.0 {cpObject} or {pObject} [there/{inImg}]?", "No, there are no {pObject} or {cpObject}.", "no", 0.15, "plural"),
            ("Do you see {ecAny} {csObject} or {any2} {sObject} [there/{inImg}]=0.7?", "No, there are no {psObject} or {cpsObject}.", "no", 0.15, "singular") # {isp}
        ]
    },    
    # "existOrC2": {"list": [ # for or / and more simpler phrases (c that is not o or c2 that is a2)
    #         ("Is there any {cObject} or {object} {thatModifier}?", "Yes, there is {object} {thatModifier}.", "yes", 1)
    #         ("Are there any {cObjects} or {objects} {thatModifier}?", "Yes, there are {objects} {thatModifier}.", "yes", 1)
    #         ("Is there [either] {cObject} or {object} {thatModifier}?", "Yes, there is {object} {thatModifier}.", "yes", 1)
    #         ("Are there [either] {cObjects} or {objects} {thatModifier}?", "Yes, there are {objects} {thatModifier}.", "yes", 1)    
    #     ]
    # }, 
    "existAnd": {"list": [ # done 
            ("Are there both {pObject} and {cpObject} [{inImg}]=0.95?", "Yes, there are both {pObject} and {cpObject}.", "yes", 1, "plural"), # TODO!  [{inImg}]=0.8 .format(inImg),
            ("Are there both {cpObject} and {pObject} [{inImg}]=0.95?", "Yes, there are both {pObject} and {cpObject}.", "yes", 1, "plural"), # TODO!  [{inImg}]=0.8 .format(inImg),
            ("Do you see both {pObject} and {cpObject} [there/{inImg}]=0.25?", "Yes, there are both {pObject} and {cpObject}.", "yes", 0.15, "plural"), # TODO!  [{inImg}]=0.8 .format(inImg),
            ("Do you see both {cpObject} and {pObject} [there/{inImg}]=0.25?", "Yes, there are both {pObject} and {cpObject}.", "yes", 0.15, "plural"), # TODO!  [{inImg}]=0.8 .format(inImg),
            ("Are there both {a} {sObject} and {ca} {csObject} [{inImg}]=0.95?", "Yes, there are both {a} {sObject} and {ca} {csObject}.", "yes", 1, "singular"), # TODO!  [{inImg}]=0.8 .format(inImg),
            ("Are there both {ca} {csObject} and {a} {sObject} [{inImg}]=0.95?", "Yes, there are both {a} {sObject} and {ca} {csObject}.", "yes", 1, "singular"), # TODO!  [{inImg}]=0.8 .format(inImg),
            ("Do you see both {a} {sObject} and {ca} {csObject} [there/{inImg}]=0.25?", "Yes, there are both {a} {sObject} and {ca} {csObject}.", "yes", 0.15, "singular"), # TODO!  [{inImg}]=0.8 .format(inImg),
            ("Do you see both {ca} {csObject} and {a} {sObject} [there/{inImg}]=0.25?", "Yes, there are both {a} {sObject} and {ca} {csObject}.", "yes", 0.15, "singular") # TODO!  [{inImg}]=0.8 .format(inImg)
        ]
    },
    "existAndC": {"list": [ # done # short modifiers? spatial modifiers
            ("Are there both {pObject} and {cpObject} [{inImg}]=0.95?", "No, there {is} {a} {object} but no {cpsObject}.", "no", 1, "plural"), # TODO!  [{inImg}]=0.8 .format(inImg), # not
            ("Are there both {cpObject} and {pObject} [{inImg}]=0.95?", "No, there {is} {a} {object} but no {cpsObject}.", "no", 1, "plural"), # TODO!  [{inImg}]=0.8 .format(inImg),
            ("Do you see both {pObject} and {cpObject} [there/{inImg}]=0.25?", "No, there {is} {a} {object} but no {cpsObject}.", "no", 0.15, "plural"), # TODO!  [{inImg}]=0.8 .format(inImg),
            ("Do you see both {cpObject} and {pObject} [there/{inImg}]=0.25?", "No, there {is} {a} {object} but no {cpsObject}.", "no", 0.15, "plural"), # TODO!  [{inImg}]=0.8 .format(inImg),
            ("Are there both {a} {sObject} and {ca} {csObject} [{inImg}]=0.95?", "No, there {is} {a} {object} but no {cpsObject}.", "no", 1, "singular"), # TODO!  [{inImg}]=0.8 .format(inImg), # not {ca}
            ("Are there both {ca} {csObject} and {a} {sObject} [{inImg}]=0.95?", "No, there {is} {a} {object} but no {cpsObject}.", "no", 1, "singular"), # TODO!  [{inImg}]=0.8 .format(inImg),
            ("Do you see both {a} {sObject} and {ca} {csObject} [there/{inImg}]=0.25?", "No, there {is} {a} {object} but no {cpsObject}.", "no", 0.15, "singular"), # TODO!  [{inImg}]=0.8 .format(inImg),
            ("Do you see both {ca} {csObject} and {a} {sObject} [there/{inImg}]=0.25?", "No, there {is} {a} {object} but no {cpsObject}.", "no", 0.15, "singular") # TODO!  [{inImg}]=0.8 .format(inImg)
            # ("Are there [both] {cObject} and {cObject} {thatModifier}?", "No, there is no {object} and no {object} {thatModifier}.", "no", 1) # TODO!  [{inImg}]=0.8 .format(inImg)
            # ("Are there [both] {cObjects} and {cObjects} {thatModifier}?", "No, there are no {objects} or {objects} {thatModifier}.", "no", 1) # TODO!  [{inImg}]=0.8 .format(inImg)
        ]
    }, 
    "existAttrOr": {"list": [ # done # obj exist. # for or / and more simpler phrases (c that is not o or c2 that is a2)
            # ("Is there any {object} or {cObject} [{inImg}]=0.25?", "Yes, there is {object} {thatModifier}.", "yes", 1),
            ("Are there [either] [any] {attribute} {pObject} or {cpObject} [{inImg}]=0.1?", "Yes, there {is} {a} {attribute} {object}.", "yes", 1, "plural"),
            ("Is there [either] {any} {sObject} or {cAny2} {csObject} that is {attribute}?", "Yes, there {is} {a} {attribute} {object}.", "yes", 1, "singular"),
            ("Are there [either] [any] {attribute} {cpObject} or {pObject} [{inImg}]=0.1?", "Yes, there {is} {a} {attribute} {object}.", "yes", 1, "plural"),
            ("Is there [either] {cAny} {csObject} or {any2} {sObject} that is {attribute}?", "Yes, there {is} {a} {attribute} {object}.", "yes", 1, "singular"),
            ("Do you see [either] [any] {attribute} {pObject} or {cpObject} [there/{inImg}]=0.1?", "Yes, there {is} {a} {attribute} {object}.", "yes", 0.25, "plural"),
            ("Do you see [either] {any} {sObject} or {cAny2} {csObject} that are {attribute}?", "Yes, there {is} {a} {attribute} {object}.", "yes", 0.25, "singular"),
            ("Do you see [either] [any] {attribute} {cpObject} or {pObject} [there/{inImg}]=0.1?", "Yes, there {is} {a} {attribute} {object}.", "yes", 0.25, "plural"),
            ("Do you see [either] {cAny} {csObject} or {any2} {sObject} that are {attribute}?", "Yes, there {is} {a} {attribute} {object}.", "yes", 0.25, "singular")
        ]
    },
    "existAttrOrC": {"list": [ # done # obj unique, cObj not exist # for or / and more simpler phrases (c that is not o or c2 that is a2)
            # ("Is there any {object} or {cObject} [{inImg}]=0.25?", "Yes, there is {object} {thatModifier}.", "yes", 1),
            ("Are there [either] [any] {cAttribute} {pObject} or {cpObject} [{inImg}]=0.1?", "No, there {is} {a} {object} but {ref} {is} {attribute}.", "no", 1, "plural"), # No, there are no {cAttribute} {pObject} or {pObject}
            ("Is there [either] {any} {sObject} or {cAny2} {csObject} that is {cAttribute}?", "No, there {is} {a} {object} but {ref} {is} {attribute}.", "no", 1, "singular"),
            ("Are there [either] [any] {cAttribute} {cpObject} or {pObject} [{inImg}]=0.1?", "No, there {is} {a} {object} but {ref} {is} {attribute}.", "no", 1, "plural"),
            ("Is there [either] {cAny} {csObject} or {any2} {sObject} that is {cAttribute}?", "No, there {is} {a} {object} but {ref} {is} {attribute}.", "no", 1, "singular"),
            ("Do you see [either] [any] {cAttribute} {pObject} or {cpObject} [there/{inImg}]=0.1?", "No, there {is} {a} {object} but {ref} {is} {attribute}.", "no", 0.15, "plural"),
            ("Do you see [either] {any} {sObject} or {cAny2} {csObject} that are {cAttribute}?", "No, there {is} {a} {object} but {ref} {is} {attribute}.", "no", 0.15, "singular"),
            ("Do you see [either] [any] {cAttribute} {cpObject} or {pObject} [there/{inImg}]=0.1?", "No, there {is} {a} {object} but {ref} {is} {attribute}.", "no", 0.15, "plural"),
            ("Do you see [either] {cAny} {csObject} or {any2} {sObject} that are {cAttribute}?", "No, there {is} {a} {object} but {ref} {is} {attribute}.", "no", 0.15, "singular")
        ]
    }, 
    # "existAndAttr": {"list": [ 
    #         ("Are there both {attribute} {pObject} and {cpObject} [{inImg}]=0.85?", "Yes, there are both {attribute} {pObject} and {cpObject}.", "yes", 1, "plural") # TODO!  [{inImg}]=0.8 .format(inImg)
    #         ("Are there both {attribute} {cpObject} and {pObject} [{inImg}]=0.85?", "Yes, there are both {attribute} {pObject} and {cpObject}.", "yes", 1, "plural") # TODO!  [{inImg}]=0.8 .format(inImg)
    #         ("Do you see both {attribute} {pObject} and {cpObject} [there/{inImg}]=0.75?", "Yes, there are both {attribute} {pObject} and {cpObject}.", "yes", 0.15, "plural") # TODO!  [{inImg}]=0.8 .format(inImg)
    #         ("Do you see both {attribute} {cpObject} and {pObject} [there/{inImg}]=0.75?", "Yes, there are both {attribute} {pObject} and {cpObject}.", "yes", 0.15, "plural") # TODO!  [{inImg}]=0.8 .format(inImg)
    #         ("Are there both {a} {sObject} and {ca} {csObject} that are {attribute}?", "Yes, there are both {aa} {attribute} {sObject} and {caa} {attribute} {csObject}.", "yes", 1, "singular") # TODO!  [{inImg}]=0.8 .format(inImg)
    #         ("Are there both {ca} {csObject} and {a} {sObject} that are {attribute}?", "Yes, there are both {aa} {attribute} {sObject} and {caa} {attribute} {csObject}.", "yes", 1, "singular") # TODO!  [{inImg}]=0.8 .format(inImg)
    #         ("Do you see both {a} {sObject} and {ca} {csObject} that are {attribute}?", "Yes, there are both {aa} {attribute} {sObject} and {caa} {attribute} {csObject}.", "yes", 0.15, "singular") # TODO!  [{inImg}]=0.8 .format(inImg)
    #         ("Do you see both {ca} {csObject} and {a} {sObject} that are {attribute}?", "Yes, there are both {aa} {attribute} {sObject} and {caa} {attribute} {csObject}.", "yes", 0.15, "singular") # TODO!  [{inImg}]=0.8 .format(inImg)
    #     ]
    # },
    # "existAndAttrC": {"list": [ # short modifiers? spatial modifiers
    #         ("Are there both {cAttribute} {pObject} and {cpObject} [{inImg}]=0.85?", "No, the {object} {is} not {cAttribute}.", "no", 1, "plural") # TODO!  [{inImg}]=0.8 .format(inImg)
    #         ("Are there both {cAttribute} {cpObject} and {pObject} [{inImg}]=0.85?", "No, the {object} {is} not {cAttribute}.", "no", 1, "plural") # TODO!  [{inImg}]=0.8 .format(inImg)
    #         ("Do you see both {cAttribute} {pObject} and {cpObject} [there/{inImg}]=0.75?", "No, the {object} {is} not {cAttribute}.", "no", 0.15, "plural") # TODO!  [{inImg}]=0.8 .format(inImg)
    #         ("Do you see both {cAttribute} {cpObject} and {pObject} [there/{inImg}]=0.75?", "No, the {object} {is} not {cAttribute}.", "no", 0.15, "plural") # TODO!  [{inImg}]=0.8 .format(inImg)
    #         ("Are there both {a} {sObject} and {ca} {csObject} that are {cAttribute}?", "No, the {object} {is} not {cAttribute}.", "no", 1, "singular") # TODO!  [{inImg}]=0.8 .format(inImg)
    #         ("Are there both {ca} {csObject} and {a} {sObject} that are {cAttribute}?", "No, the {object} {is} not {cAttribute}.", "no", 1, "singular") # TODO!  [{inImg}]=0.8 .format(inImg)
    #         ("Do you see both {a} {sObject} and {ca} {csObject} that are {cAttribute}?", "No, the {object} {is} not {cAttribute}.", "no", 0.15, "singular") # TODO!  [{inImg}]=0.8 .format(inImg)
    #         ("Do you see both {ca} {csObject} and {a} {sObject} that are {cAttribute}?", "No, the {object} {is} not {cAttribute}.", "no", 0.15, "singular") # TODO!  [{inImg}]=0.8 .format(inImg)
    #         # ("Are there [both] {cObject} and {cObject} {thatModifier}?", "No, there is no {object} and no {object} {thatModifier}.", "no", 1) # TODO!  [{inImg}]=0.8 .format(inImg)
    #         # ("Are there [both] {cObjects} and {cObjects} {thatModifier}?", "No, there are no {objects} or {objects} {thatModifier}.", "no", 1) # TODO!  [{inImg}]=0.8 .format(inImg)
    #     ]
    # }, 
    "existThatOr": {"list": [ # done # obj exist. # for or / and more simpler phrases (c that is not o or c2 that is a2)
            # ("Is there any {object} or {cObject} [{inImg}]=0.25?", "Yes, there is {object} {thatModifier}.", "yes", 1),
            ("Are there [either] [any] {pObject} or {cpObject} that are {cprop}?", "Yes, the {object} {is} {prop}.", "yes", 1, "plural"),
            ("Is there [either] {any} {sObject} or {cAny2} {csObject} that is {cprop}?", "Yes, the {object} {is} {prop}.", "yes", 0.3, "singular"),
            ("Are there [either] [any] {cpObject} or {pObject} that are {cprop}?", "Yes, the {object} {is} {prop}.", "yes", 1, "plural"),
            ("Is there [either] {cAny} {csObject} or {any2} {sObject} that is {cprop}?", "Yes, the {object} {is} {prop}.", "yes", 0.3, "singular"),
            ("Do you see [either] [any] {pObject} or {cpObject} that are {cprop}?", "Yes, the {object} {is} {prop}.", "yes", 0.25, "plural"),
            ("Do you see [either] {any} {sObject} or {cAny2} {csObject} that are {cprop}?", "Yes, the {object} {is} {prop}.", "yes", 0.08, "singular"),
            ("Do you see [either] [any] {cpObject} or {pObject} that are {cprop}?", "Yes, the {object} {is} {prop}.", "yes", 0.25, "plural"),
            ("Do you see [either] {cAny} {csObject} or {any2} {sObject} that are {cprop}?", "Yes, the {object} {is} {prop}.", "yes", 0.08, "singular")
        ]
    },
    "existThatOrC": {"list": [ # done # obj unique, cObj not exist # for or / and more simpler phrases (c that is not o or c2 that is a2)
            # ("Is there any {object} or {cObject} [{inImg}]=0.25?", "Yes, there is {object} {thatModifier}.", "yes", 1),
            ("Are there [either] [any] {pObject} or {cpObject} that are {cprop}?", "No, there {is} {a} {object} but {ref} {is} {prop}.", "no", 1, "plural"),
            ("Is there [either] {any} {sObject} or {cAny2} {csObject} that is {cprop}?", "No, there {is} {a} {object} but {ref} {is} {prop}.", "no", 0.3, "singular"),
            ("Do you see [either] [any] {cpObject} or {pObject} that are {cprop}?", "No, there {is} {a} {object} but {ref} {is} {prop}.", "no", 0.15, "plural"),
            ("Do you see [either] {cAny} {csObject} or {any2} {sObject} that are {cprop}?", "No, there {is} {a} {object} but {ref} {is} {prop}.", "no", 0.05, "singular")
        ]
    }, 
    # "existAndThat": {"list": [ # ??????????? 
    #         ("Are there both {pObject} and {cpObject} {that}?", "Yes, both {pObject} and {cpObject}.", "yes", 1, "plural") # TODO!  [{inImg}]=0.8 .format(inImg)
    #         ("Are there both {cpObject} and {pObject} {that}?", "Yes, both {pObject} and {cpObject}.", "yes", 1, "plural") # TODO!  [{inImg}]=0.8 .format(inImg)
    #         ("Do you see both {pObject} and {cpObject} {that}?", "Yes, both {pObject} and {cpObject}.", "yes", 0.15, "plural") # TODO!  [{inImg}]=0.8 .format(inImg)
    #         ("Do you see both {cpObject} and {pObject} {that}?", "Yes, both {pObject} and {cpObject}.", "yes", 0.15, "plural") # TODO!  [{inImg}]=0.8 .format(inImg)
    #         ("Are there both {a} {sObject} and {ca} {csObject} {that}?", "Yes, both {a} {sObject} and {ca} {csObject}.", "yes", 1, "singular") # TODO!  [{inImg}]=0.8 .format(inImg)
    #         ("Are there both {ca} {csObject} and {a} {sObject} {that}?", "Yes, both {a} {sObject} and {ca} {csObject}.", "yes", 1, "singular") # TODO!  [{inImg}]=0.8 .format(inImg)
    #         ("Do you see [there] both {a} {sObject} and {ca} {csObject} {that}?", "Yes, there are both {a} {sObject} and {ca} {csObject}.", "yes", 0.15, "singular") # TODO!  [{inImg}]=0.8 .format(inImg)
    #         ("Do you see [there] both {ca} {csObject} and {a} {sObject} {that}?", "Yes, there are both {a} {sObject} and {ca} {csObject}.", "yes", 0.15, "singular") # TODO!  [{inImg}]=0.8 .format(inImg)
    #     ]
    # },
    # "existAndC": {"list": [ # ???????? # done # short modifiers? spatial modifiers
    #         ("Are there both {pObject} and {cpObject} [{inImg}]=0.95?", "No, there are {pObject} but not {cpObject}.", "no", 1, "plural") # TODO!  [{inImg}]=0.8 .format(inImg)
    #         ("Are there both {cpObject} and {pObject} [{inImg}]=0.95?", "No, there are {pObject} but not {cpObject}.", "no", 1, "plural") # TODO!  [{inImg}]=0.8 .format(inImg)
    #         ("Do you see both {pObject} and {cpObject} [there/{inImg}]=0.25?", "No, there are {pObject} but not {cpObject}.", "no", 0.15, "plural") # TODO!  [{inImg}]=0.8 .format(inImg)
    #         ("Do you see both {cpObject} and {pObject} [there/{inImg}]=0.25?", "No, there are {pObject} but not {cpObject}.", "no", 0.15, "plural") # TODO!  [{inImg}]=0.8 .format(inImg)
    #         ("Are there both {a} {sObject} and {ca} {csObject} [{inImg}]=0.95?", "No, there is {a} {sObject} but not {ca} {csObject}.", "no", 1, "singular") # TODO!  [{inImg}]=0.8 .format(inImg)
    #         ("Are there both {ca} {csObject} and {a} {sObject} [{inImg}]=0.95?", "No, there is {a} {sObject} but not {ca} {csObject}.", "no", 1, "singular") # TODO!  [{inImg}]=0.8 .format(inImg)
    #         ("Do you see both {a} {sObject} and {ca} {csObject} [there/{inImg}]=0.25?", "No, there is {a} {sObject} but not {ca} {csObject}.", "no", 0.15, "singular") # TODO!  [{inImg}]=0.8 .format(inImg)
    #         ("Do you see both {ca} {csObject} and {a} {sObject} [there/{inImg}]=0.25?", "No, there is {a} {sObject} but not {ca} {csObject}.", "no", 0.15, "singular") # TODO!  [{inImg}]=0.8 .format(inImg)
    #         # ("Are there [both] {cObject} and {cObject} {thatModifier}?", "No, there is no {object} and no {object} {thatModifier}.", "no", 1) # TODO!  [{inImg}]=0.8 .format(inImg)
    #         # ("Are there [both] {cObjects} and {cObjects} {thatModifier}?", "No, there are no {objects} or {objects} {thatModifier}.", "no", 1) # TODO!  [{inImg}]=0.8 .format(inImg)
    #     ]
    # },         
    # are either the X or the Y modifier? size threshold?
    "category": {"list": [ # done # {what}?????
            ("What|What|Which {kategory} {kis} shown|presented [{inImg}]=0.8?", "The {kategory} {kis} {a} {object}.", "{object}", 1),
            ("What|What|Which {kategory} {kis} pictured?", "The {kategory} {kis} {a} {object}.", "{object}", 0.25),
            ("What|What|Which {kategory} {kis} {inImg}?", "The {kategory} {kis} {a} {object}.",  "{object}", 0.8),
            ("What|What|Which {kategory} can be seen [{inImg}]=0.7?", "The {kategory} {kis} {a} {object}.",  "{object}", 0.05),
            ("What|What|Which {kategory} do you see [{inImg}]=0.2?", "The {kategory} {kis} {a} {object}.",  "{object}", 0.1),
            ("What|Which kind|type {is} the {category}?", "The {category} {is} {a} {object}.", "{object}", 0.1, "countable"),
            ("What [do_you_think]=0.03 {is} the {category} [that_{is}]=0.1 {inImg}?", "The {category} {is} {a} {object}.", "{object}", 0.4, "countable"),
            ("What [do_you_think]=0.03 {is} the {category} that {is} shown|presented [{inImg}]?", "The {category} {is} {a} {object}.", "{object}", 0.15, "countable"),
            ("What [do_you_think]=0.03 {is} the {category} that {is} pictured?", "The {category} {is} {a} {object}.", "{object}", 0.05, "countable"),
            ("What [do_you_think]=0.03 is the name of the {category} [that_{is}_shown]=0.85 {inImg}?", "The {category} {is} {a} {object}.", "{object}", 0.08, "countable"),
            ("What [do_you_think]=0.03 is the name of the {category}?", "The {category} {is} {a} {object}.", "{object}", 0.2, "countable"),
            ("{how} [do_you_think]=0.03 {is} the {category} [that_{is}_shown]=0.3 {inImg} called?", "The {category} {is} {a} {object}.", "{object}", 0.3, "countable"),
            ("{how} [do_you_think]=0.03 {is} the {category} called?", "The {category} {is} {a} {object}.", "{object}", 0.6, "countable")
            # ("Which kind|type of {category} {is} shown|pictured|presented|{inImg}?", "The {category} {is} {object}.",  "{object}", 0.2),        
            # ("What|Which kind|type of {category} {is} there|shown {inImg}?", "The {category} {is} {object}.",  "{object}", 0.1),
            # ("Which {category} {is} shown|pictured|presented|{inImg}?", "The {category} {is} {object}.",  "{object}", 0.2, "countable"),
            # ("What|Which {category} {is} shown|pictured|presented|{inImg}?", "The {category} {is} {object}.", "{object}", 1, "countable"),
            # ("What {category} {is} there|shown {inImg}?", "The {category} {is} {object}.",  "{object}", 0.1, "countable"),
            # ("What {category} can be seen [{inImg}]=0.3?", "The {category} {is} {object}.",  "{object}", 0.05, "countable"),
        ]
    },
    "categoryThis": {"list": [ # done # TODO: !!!! category if object equals category ignore (what type of) 
            ("What|What|Which {kategory} {kis} {this}?", "{othis} {ois} {a} {object}.", "{object}", 1),
            ("What|Which kind|type [do_you_think]=0.03 {is} {this} {category}?", "{othis} {ois} {a} {object}.", "{object}", 0.2, "countable"),
            ("What [do_you_think]=0.03 is the name of {this} {category}?", "{othis} {ois} {a} {object}.", "{object}", 0.3, "countable"),
            ("{how} [do_you_think]=0.03 {is} {this} {category} called?", "{othis} {ois} {a} {object}.", "{object}", 1, "countable"),
            # ("Which kind|type of {category} {is} {this}?", "{this} {is} {object}.", "{object}", 1)
            # ("What {category} {is} {this}?", "{this} {is} {object}.", "{object}", 1, "countable"),
            # ("Which {category} {is} {this}?", "{this} {is} {object}.", "{object}", 1, "countable")            
        ]
    },    
    # "categoryMultiple": {"list": [
    #         ("What|Which kind|type of {category} [{inImg}] {is} {modifier}?", "The {category} {is} {object}.", "{object}", 1),
    #         ("What|Which {category} [{inImg}] {is} {modifier}?", "The {category} {is} {object}.", "{object}", 1, "countable"),
    #     ]
    # },
    # "identifyAttr": {"list": [ # not...?????????
    #         ("What [{inImg}] {is} {attribute}?", "The {object} {is} {attribute}.", "{object}", 1),
    #     ]
    # },    
    # made of X, red?     
    # modifier can be subcategory, modifier can be not, is being held, is being held by.., is y holding
    # left of a or the?
    "categoryAttr": {"list": [ # done
            ("What|What|Which {kategory} [{inImg}]=0.1 {kis} {attribute}?", "The {kategory} {kis} {a} {object}.", "{object}", 1),
            ("{how} [do_you_think]=0.03 {is} the {attribute} {category} [{inImg}]=0.03 called?", "The {category} {is} {a} {object}.", "{object}", 1, "countable"),
            ("{how} [do_you_think]=0.03 {is} the {category} that {is} {attribute} called?", "The {category} {is} {a} {object}.", "{object}", 0.15, "countable"),
            ("{how} [do_you_think]=0.03 the {attribute} {category} [{inImg}]=0.03 {is} called?", "The {category} {is} {a} {object}.", "{object}", 0.05, "countable"),    
            ("{how} [do_you_think]=0.03 the {category} that {is} {attribute} {is} called?", "The {category} {is} {a} {object}.", "{object}", 0.05, "countable"),
            ("What [do_you_think]=0.03 is the name of the {attribute} {category} [{inImg}]=0.03?", "The {category} {is} {a} {object}.", "{object}", 0.3, "countable"),    
            ("What [do_you_think]=0.03 is the name of the {category} {is} {attribute}?", "The {category} {is} {a} {object}.", "{object}", 0.08, "countable"),
            ("What [do_you_think]=0.03 {is} the {attribute} {category} [{inImg}]=0.3?", "The {category} {is} {a} {object}.", "{object}", 0.8, "countable"),
            ("What [do_you_think]=0.03 {is} the {category} that {is} {attribute}?", "The {category} {is} {a} {object}.", "{object}", 0.05, "countable")
            # ("Which kind|type of {category} {is} {modifier}?", "{dobject} {is} {modifier}.", "{object}", 1)
            # ("Which {category} {is} {modifier}?", "{dobject} {is} {modifier}.", "{object}", 1, "countable")            
            # ("What|Which {category} {is} {modifier}?", "{dobject} {is} {modifier}.", "{object}", 1)
        ]
    },
    # NOT attr ????
    "categoryThat": {"list": [ # done
            ("What|What|Which {kategory} [{inImg}]=0.1 {kis} {prop}?", "The {kategory} {kis} {a} {object}.", "{object}", 1),
            ("{how} [do_you_think]=0.03 {is} the {category} that {is} {prop} called?", "The {category} {is} {a} {object}.", "{object}", 0.15, "countable"),
            ("{how} [do_you_think]=0.03 the {category} that {is} {prop} {is} called?", "The {category} {is} {a} {object}.", "{object}", 0.05, "countable"),
            ("What [do_you_think]=0.03 is the name of the {category} that {is} {prop}?", "The {category} {is} {a} {object}.", "{object}", 0.08, "countable"), # {this} {is} {a} {object}
            ("What [do_you_think]=0.03 {is} the {category} that {is} {prop}?", "The {category} {is} {a} {object}.", "{object}", 0.15, "countable")    
            # ("Which kind|type of {category} {is} {modifier}?", "{dobject} {is} {modifier}.", "{object}", 1)
            # ("Which {category} {is} {modifier}?", "{dobject} {is} {modifier}.", "{object}", 1, "countable")            
            # ("What|Which {category} {is} {modifier}?", "{dobject} {is} {modifier}.", "{object}", 1)
        ]
    },
    "categoryThatChoose": {"list": [ # done # + attr and that
            ("What|Which {kategory} {kis} {prop} , {dobject} or {cdobject}?", "{dobject} {is} {prop}.", "{object}", 1),
            ("What|Which {kategory} {kis} {prop} , {cdobject} or {dobject}?", "{dobject} {is} {prop}.", "{object}", 1)
            # ("How {is} the {attribute} {category} called?", "The {category} {is} {a} {object}.", "{object}", 1)
            # ("How {is} the {category} that {is} {attribute} called?", "The {category} {is} {a} {object}.", "{object}", 0.2)
            # ("Which kind|type of {category} {is} {modifier} , {dobject} or {cdobject}?", "{dobject} {is} {modifier}.", "{object}", 0.3)
            # ("Which kind|type of {category} {is} {modifier} , {cdobject} or {dobject}?", "{dobject} {is} {modifier}.", "{object}", 0.3)
            # ("Which {category} {is} {modifier} , {dobject} or {cdobject}?", "{dobject} {is} {modifier}.", "{object}", 0.2, "countable")
            # ("Which {category} {is} {modifier} , {cdobject} or {dobject}?", "{dobject} {is} {modifier}.", "{object}", 0.2, "countable")
            # ("What|Which {category} {is} {modifier} , {dobject} or {cdobject}?", "{dobject} {is} {modifier}.", "{object}", 1, "countable")
            # ("What|Which {category} {is} {modifier} , {cdobject} or {dobject}?", "{dobject} {is} {modifier}.", "{object}", 1, "countable")
        ]
    },
    "categoryThisChoose": {"list": [ # done
            ("What|Which {kategory} [do_you_think]=0.03 {kis} {this} , {a} {object} or {ca} {cObject}?", "{othis} {ois} {a} {object}.", "{object}", 1),
            ("What|Which {kategory} [do_you_think]=0.03 {kis} {this} , {ca} {cObject} or {a} {object}?", "{othis} {ois} {a} {object}.", "{object}", 1)
        ]
    },
    "objThisChoose": {"list": [ # done
            ("{is} {this} {a} {object} or {ca} {cObject}?", "{this} {is} {a} {object}.", "{object}", 1),
            ("{is} {this} {ca} {cObject} or {a} {object}?", "{this} {is} {a} {object}.", "{object}", 1),
            ("{what} [do_you_think]=0.03 {is} {this} , {a} {object} or {ca} {cObject}?", "{this} {is} {a} {object}.", "{object}", 0.15),
            ("{what} [do_you_think]=0.03 {is} {this} , {ca} {cObject} or {a} {object}?", "{this} {is} {a} {object}.", "{object}", 0.15)
        ]
    },
    # daobject
    "categoryRelO": {"list": [ # done
            ("{suffix} what {kategory} [do_you_think]=0.03 {qis} {dpsubject} {qrel} {of}?", "{dsubject} {is} {rel} {dobject}.", "{object}", 1),
            ("{how} [do_you_think]=0.03 {cis} the {category} that {dpsubject} {is} {rel} {of} called?", "The {category} {cis} {a} {object}.", "{object}", 0.3, "countable"),
            ("What [do_you_think]=0.03 is the name of the {category} that {dpsubject} {is} {rel} {of}?", "The {category} {cis} {a} {object}.", "{object}", 0.1, "countable"),
            ("What [do_you_think]=0.03 {cis} the {category} that {dpsubject} {is} {rel} {of}?", "The {category} {cis} {a} {object}.", "{object}", 1, "countable")
            # ("Which {kindof} {category} {is} {dobject2} {rel}?", "{dobject2} {is} {rel} {dobject}.", "{object}", 0.2)
            # ("What {category} {is} {dobject2} {rel}?", "{dobject2} {is} {rel} {dobject}.", "{object}", 1, "countable")
            # ("Which {category} {is} {dobject2} {rel}?", "{dobject2} {is} {rel} {dobject}.", "{object}", 0.2, "countable")            
        ]
    },
    # daobject
    "categoryRelOChoose": {"list": [ # done # ????????? "answer"
            ("{suffix} what {kategory} {qis} {dpsubject} {qrel} {of} , {dobject} or {cdobject}?", "{dsubject} {is} {rel} {dobject}.", "{object}", 1),
            ("{suffix} what {kategory} {qis} {dpsubject} {qrel} {of} , {cdobject} or {dobject}?", "{dsubject} {is} {rel} {dobject}.", "{object}", 1)
            ("{suffix} what {qis} {dpsubject} {qrel} {of} , {dobject} or {cdobject}?", "{dsubject} {is} {rel} {dobject}.", "{object}", 1),
            ("{suffix} what {qis} {dpsubject} {qrel} {of} , {cdobject} or {dobject}?", "{dsubject} {is} {rel} {dobject}.", "{object}", 1)
            # ("What|Which {category} {is} {dobject2} {rel} , {dobject} or {cdobject}?", "{dobject2} {is} {rel} {dobject}.", "{object}", 1, "countable")
            # ("What|Which {category} {is} {dobject2} {rel} , {cdobject} or {dobject}?", "{dobject2} {is} {rel} {dobject}.", "{object}", 1, "countable")
            # ("Which kind|type of {category} {is} {dobject2} {rel} , {dobject} or {cdobject}?", "{dobject2} {is} {rel} {dobject}.", "{object}", 0.2)
            # ("Which kind|type of {category} {is} {dobject2} {rel} , {cdobject} or {dobject}?", "{dobject2} {is} {rel} {dobject}.", "{object}", 0.2)
        ]
    },
    # daobject
    "categoryRelS": {"list": [ # done
            ("What {kategory} [do_you_think]=0.03 {kis} {krel} {dpobject}?", "The {category} {cis} {a} {subject}.", "{subject}", 1),
            ("{how} [do_you_think]=0.03 {cis} the {category} {that} {is} {crel} {dpobject} called?", "The {category} {cis} {a} {subject}.", "{subject}", 0.3, "countable"),
            ("What [do_you_think]=0.03 is the name of the {category} {that} {is} {crel} {dpobject}?", "The {category} {cis} {a} {subject}.", "{subject}", 0.1, "countable"),
            ("What [do_you_think]=0.03 {cis} the {category} {that} {is} {crel} {dpobject}?", "The {category} {cis} {a} {subject}.", "{subject}", 1, "countable")
            # ("What {category} {is} {rel} {dobject2}?", "{dobject} {is} {rel} {dobject}.", "{object2}", 1, "countable")
            # ("Which {category} {is} {rel} {dobject2}?", "{dobject} {is} {rel} {dobject}.", "{object2}", 0.2, "countable")            
            # ("Which {kindof} {category} {is} {rel} {dobject2}?", "{dobject} {is} {rel} {dobject2}.", "{object}", 0.2)
        ]
    },
    # daobject
    "categoryRelSChoose": {"list": [ # done # ??????? "answer"
            ("What {kategory} {kis} {krel} {dpobject} , {dsubject} or {cdsubject}?", "{dsubject} {ois} {rel} {dobject}.", "{subject}", 1),
            ("What {kategory} {kis} {krel} {dpobject} , {cdsubject} or {dsubject}?", "{dsubject} {ois} {rel} {dobject}.", "{subject}", 1)
            ("What {kis} {krel} {dpobject} , {dsubject} or {cdsubject}?", "{dsubject} {ois} {rel} {dobject}.", "{subject}", 1),
            ("What {kis} {krel} {dpobject} , {cdsubject} or {dsubject}?", "{dsubject} {ois} {rel} {dobject}.", "{subject}", 1)
            # ("What|Which {category} {is} {rel} {dobject2} , {dobject} or {cdobject}?", "{dobject} {is} {rel} {dobject2}.", "{object}", 1, "countable")
            # ("What|Which {category} {is} {rel} {dobject2} , {cdobject} or {dobject}?", "{dobject} {is} {rel} {dobject2}.", "{object}", 1, "countable")
            # ("Which kind|type of {category} {is} {dobject2} {rel} , {dobject} or {cdobject}?", "{dobject2} {is} {rel} {dobject}.", "{object}", 0.2)
            # ("Which kind|type of {category} {is} {dobject2} {rel} , {cdobject} or {dobject}?", "{dobject2} {is} {rel} {dobject}.", "{object}", 0.2)
        ]
    },
    # relSchoose TODO???????
    # relOchoose TODO???????
    # spatial rel is a sub case of rel 
    "relS": {"list": [ # done
            ("{what} [do_you_think]=0.03 {sis} {srel} {dpobject}?", "{dsubject} {is} {rel} {dobject}.", "{subject}", 1)
        ]
    },
    # daobject
    "relO": {"list": [ # done 
            ("{suffix} {what} [do_you_think]=0.03 {qis} {dpsubject} {qrel} {of}?", "{dsubject} {is} {rel} {dobject}.", "{object}", 1),
            ("{dpsubject} {is} {relq} {what}?", "{dsubject} {is} {rel} {dobject}.", "{object}", 0.05) # , "where"
        ]
    },
    # "where": {"list": [ # done 
    #         ("Where [do_you_think]=0.03 {is} {dpsubject}?", "{dsubject} {is} {rel} {dobject}.", "{object}", 1),
    #         # ("Where could|might [the|{this}] {dobject} be [at]=0.1?", "{dobject} {is} {in} {dplace}.",  "{dplace}", 0.3)
    #     ]
    # },
    # daobject
    "relVerify": {"list": [ # done
            ("{qis} {dpsubject} {qrel} {dpobject}?", "Yes, {dsubject} {is} {rel} {dobject}.", "yes", 1)
            # ("{is} {dobject} {rel} {object2}?", "Yes, {dobject} {is} {rel} {object2}.", "yes", 1)
        ]
    },
    # daobject
    "relVerifyCo": {"list": [ # done 
            ("{qis} {dpsubject} {qrel} {cdobject}?", "No, {dsubject} {is} {rel} {dobject}.", "no", 1)
            # ("{is} {dobject} {rel} {cobject2}?", "No, {dobject} {is} {rel} {object2}.", "no", 1)
        ]
    },
    # daobject    
    "relVerifyCs": {"list": [ # done 
            ("{qis} {cdsubject} {qrel} {dpobject}?", "No, {dsubject} {is} {rel} {dobject}.", "no", 1)
            # ("{is} {cdobject} {rel} {object2}?", "No, {dobject} {is} {rel} {object2}.", "no", 1)
        ]
    },
    "relVerifyCop": {"list": [ # done 
            ("{qis} {dobject} {qrel} {dsubject}?", "No, {dsubject} {is} {rel} {dobject}.", "no", 1)
            # ("{is} {dobject2} {rel} {object}?", "No, {dobject} {is} {rel} {object2}.", "no", 1)
        ]
    },
    # daobject        
    "relVerifyCr": {"list": [ # done 
            ("{qis} {dpsubject} {qcrel} {dpobject}?", "No, {dsubject} {is} {rel} {dobject}.", "no", 1)
            # ("{is} {dsubject} {crel} {object2}?", "No, {dobject} {is} {rel} {object2}.", "no", 1)
        ]
    },
    # daobject            
    "relChooser": {"list": [ # done
            ("{qis} {dpsubject} {qrel} or {qcrel2} {dpobject}?", "{dsubject} {is} {rel} {dobject}.", "{rel1}", 1),
            ("{qis} {dpsubject} {qcrel} or {qrel2} {dpobject}?", "{dsubject} {is} {rel} {dobject}.", "{rel1}", 1)
            # ("{is} {dsubject} {rel} or {crel} {suffix} {object}?", "{dsubject} {is} {rel} {suffix} {object2}.", "{rel}", 1)
        ]
    # shared suffix: left/right of
    },
    "dir": {"list": [ # done 
            ("Which direction [do_you_think]=0.03 {qis} {dpsubject} {qrel}?", "{dsubject} {is} {rel} {dobject}.", "{object}", 1),
            ("Where [do_you_think]=0.03 {qis} {dpsubject} {qrel}?", "{dsubject} {is} {rel} {dobject}.", "{object}", 1),
        ]
    },
    # "where": {"list": [ # done 
    #         ("Where [do_you_think]=0.03 {is} {dpsubject}?", "{dsubject} {is} {rel} {dobject}.", "{object}", 1),
    #         # ("Where could|might [the|{this}] {dobject} be [at]=0.1?", "{dobject} {is} {in} {dplace}.",  "{dplace}", 0.3)
    #     ]
    # },
    # daobject   
    # "objThisVerify": {"list": [ # ?????
    #         ("{is} {this} {sobject}?", "Yes, {this} {is} {object}.", "yes", 1)
    #     ]
    # },
    # "objThisVerifyC": {"list": [ # ?????
    #         ("{is} {this} {csObject}?", "No, {this} {is} {object}.", "no", 1)
    #     ]
    # },
    # "objThisChooseC": {"list": [
    #         ("{is} {this} {csObject} or {sobject}?", "{this} {is} {object}.", "{object}", 1)
    #     ]
    # },
    "existRelS": {"list": [ # done # good candidates: if o -> similar images, if a o -> o with opposite a
                  # o that is not A -> when there is o a
            ("Are there [any] {pSubject} {rel} {dpobject}?", "Yes, there {is} {a} {subject} {rel} {dobject}.", "yes", 1, "plural"),
            ("Is there {any} {sSubject} {rel} {dpobject}?", "Yes, there {is} {a} {subject} {rel} {dobject}.", "yes", 1, "singular"),
            ("Do you see [any] {pSubject} {rel} {dpobject}?", "Yes, there {is} {a} {subject} {rel} {dobject}.", "yes", 0.25, "plural"),
            ("Do you see {any} {sSubject} {rel} {dpobject}?", "Yes, there {is} {a} {subject} {rel} {dobject}.", "yes", 0.25, "singular")
            # ("Is there {sObject} {that} {is} {object2}?", "Yes, there {is} {a} {object} but {itsnot}.", "yes", 1)
            # ("Are there {pObjects} {thatModifier}?", "Yes, there {is} {a} {object} but {itsnot}.", "yes", 1)
        ]
    },
    "existRelSC": {"list": [ # done # good candidates: if o -> similar images, if a o -> o with opposite a
                  # o that is not A -> when there is o a
            ("Are there [any] {cpSubject} {rel} {dpobject}?", "No, there {is} {a} {subject} {rel} {dobject}.", "no", 1, "plural"), # ????? change answer?
            ("Is there {any} {csSubject} {rel} {dpobject}?", "No, there {is} {a} {subject} {rel} {dobject}.", "no", 1, "singular"),
            ("Do you see [any] {cpSubject} {rel} {dpobject}?", "No, there {is} {a} {subject} {rel} {dobject}.", "no", 0.25, "plural"),
            ("Do you see {any} {csSubject} {rel} {dpobject}?", "No, there {is} {a} {subject} {rel} {dobject}.", "no", 0.25, "singular")
            # ("Is there any {object} {thatModifier}?", "No, there {is} {a} {object} but {itsnot}.", "no", 1) # No, there {is} {a} {object} but {itsnot}.
            # ("Are there any {objects} {thatModifier}?", "No, there {is} {a} {object} but {itsnot}.", "no", 1)
            # ("Is there {object} {thatModifier}?", "No, there {is} {a} {object} but {itsnot}.", "no", 1)
            # ("Are there {objects} {thatModifier}?", "No, there {is} {a} {object} but {itsnot}.", "no", 1)
        ]
    },
    "existRelSRC": {"list": [ # done 
            ("Are there [any] {pSubject} {nrel} {dpobject}?", "No, the {subject} {is} {rel} {dobject}.", "no", 1, "plural"),
            ("Is there {any} {sSubject} {nrel} {dpobject}?", "No, the {subject} {is} {rel} {dobject}.", "no", 1, "singular"),
            ("Do you see [any] {pSubject} {nrel} {dpobject}?", "No, the {subject} {is} {rel} {dobject}.", "no", 0.25, "plural"),
            ("Do you see {any} {sSubject} {nrel} {dpobject}?", "No, the {subject} {is} {rel} {dobject}.", "no", 0.25, "singular")
            # ("{is} {dsubject} {crel} {object2}?", "No, {dobject} {is} {rel} {object2}.", "no", 1)
        ]
    },       
    # existRelO {of}
    # existRelOC {of}
    # (is there [any] food on the pizza) 
    # existOrRel TODO? sounds like choose
    # existAndRel TODO? in relation to the same object or different? depends on the context
    # not
    #subcategory = []
    # questions with different?
    # "animalsAllType": {"list": [  
    #         ("Are [all] the|these animals [{inImg}]=0.1 [from] the same species|breed?", "Yes, all the animals are {objects}.", "yes", 2, "all"),
    #         ("Are the|these animals [{inImg}]=0.1 all [from] the same species|breed?", "Yes, all the animals are {objects}.", "yes", 1, "all"),
    #         ("Are [both] the|these animals [{inImg}]=0.1 [from] the same species|breed?", "Yes, all the animals are {objects}.", "yes", 2, "both"),
    #         ("Are the|these two animals [{inImg}]=0.1 [from] the same species|breed?", "Yes, all the animals are {objects}.", "yes", 1, "both")
    #     ]
    # },
    "allSameType": {"list": [
            ("Are [all] the|these {categories} [inImg]=0.1 the same type|kind?", "Yes, all the {categories} are {objects}.", "yes", 2, "all"),
            ("Are the|these {categories} [inImg]=0.1 all the same type|kind?", "Yes, all the {categories} are {objects}.", "yes", 1, "all"),
            ("Are [both] the|these {categories} [inImg]=0.1 the same type|kind?", "Yes, both the {categories} are {objects}.", "yes", 2, "both"),
            ("Are the|these two {categories} [inImg]=0.1 the same type|kind?", "Yes, both the {categories} are {objects}.", "yes", 1, "both"),
            ("Do [all] the|these {categories} [inImg]=0.1 have the same type|kind?", "Yes, all the {categories} are {objects}.", "yes", 1, "all"),
            ("Do the|these {categories} [inImg]=0.1 all have the same type|kind?", "Yes, all the {categories} are {objects}.", "yes", 0.5, "all"),
            ("Do [both] the|these {categories} [inImg]=0.1 have the same type|kind?", "Yes, both the {categories} are {objects}.", "yes", 0.5, "both"),
            ("Do the|these two {categories} [inImg]=0.1 have the same type|kind?", "Yes, both the {categories} are {objects}.", "yes", 0.5, "both")
        ],
        "extra": {"both": {"num": 2}}
    },
    "sameAnimals": {"list": [  # done
            ("Are [all] the|these animals [of] the same type|species?", "Yes, all the animals are {pObject}.", "yes", 2, ">2"),
            ("Are the|these animals all [of] the same type|species?", "Yes, all the animals are {pObject}.", "yes", 1, ">2"),
            ("Are [both] the|these animals [of] the same type|species?", "Yes, all the animals are {pObject}.", "yes", 2, "2"),
            ("Are the|these two animals [of] the same type|species?", "Yes, all the animals are {pObject}.", "yes", 1, "2"),
            ("Are [all] the animals {inImg} [of] the same type|species?", "Yes, all the animals are {pObject}.", "yes", 0.2, ">2"),
            ("Are the animals {inImg} all [of] the same type|species?", "Yes, all the animals are {pObject}.", "yes", 0.1, ">2"),
            ("Are [both] the animals {inImg} [of] the same type|species?", "Yes, all the animals are {pObject}.", "yes", 0.2, "2"),
            ("Are the two animals {inImg} [of] the same type|species?", "Yes, all the animals are {pObject}.", "yes", 0.1, "2"),
            ("Do [all] the|these animals have the same type|species?", "Yes, all the animals are {pObject}.", "yes", 2, ">2"),
            ("Do the|these animals all have the same type|species?", "Yes, all the animals are {pObject}.", "yes", 1, ">2"),
            ("Do [both] the|these animals have the same type|species?", "Yes, all the animals are {pObject}.", "yes", 2, "2"),
            ("Do the|these two animals have the same type|species?", "Yes, all the animals are {pObject}.", "yes", 1, "2"),
            ("Do [all] the animals {inImg} have the same type|species?", "Yes, all the animals are {pObject}.", "yes", 0.2, ">2"),
            ("Do the animals {inImg} all have the same type|species?", "Yes, all the animals are {pObject}.", "yes", 0.1, ">2"),
            ("Do [both] the animals {inImg} have the same type|species?", "Yes, all the animals are {pObject}.", "yes", 0.2, "2"),
            ("Do the two animals {inImg} have the same type|species?", "Yes, all the animals are {pObject}.", "yes", 0.1, "2"),
            ("Are [all] the|these animals {pObject}?", "Yes, all the animals are {pObject}.", "yes", 1.2, ">2"),
            ("Are [both] the|these animals {pObject}?", "Yes, all the animals are {pObject}.", "yes", 1.2, "2"),
        ]
    },
    "sameAnimalsC": {"list": [ # done
            ("Are [all] the|these animals [of] the same type|species?", "No, there are both {pObject} and {pObject2}.", "no", 2, ">2"),
            ("Are the|these animals all [of] the same type|species?", "No, there are both {pObject} and {pObject2}.", "no", 1, ">2"),
            ("Are [both] the|these animals [of] the same type|species?", "No, they are {pObject} and {pObject2}.", "no", 2, "2"),
            ("Are the|these two animals [of] the same type|species?", "No, they are {pObject} and {pObject2}.", "no", 1, "2"),
            ("Are [all] the animals {inImg} [of] the same type|species?", "No, they are {pObject} and {pObject2}.", "no", 0.2, ">2"),
            ("Are the animals {inImg} all [of] the same type|species?", "No, they are {pObject} and {pObject2}.", "no", 0.1, ">2"),
            ("Are [both] the animals {inImg} [of] the same type|species?", "No, they are {pObject} and {pObject2}.", "no", 0.2, "2"),
            ("Are the two animals {inImg} [of] the same type|species?", "No, they are {pObject} and {pObject2}.", "no", 0.1, "2"),
            ("Do [all] the|these animals have the same type|species?", "No, there are both {pObject} and {pObject2}.", "no", 2, ">2"),
            ("Do the|these animals all have the same type|species?", "No, there are both {pObject} and {pObject2}.", "no", 1, ">2"),
            ("Do [both] the|these animals have the same type|species?", "No, they are {pObject} and {pObject2}.", "no", 2, "2"),
            ("Do the|these two animals have the same type|species?", "No, they are {pObject} and {pObject2}.", "no", 1, "2"),
            ("Do [all] the animals {inImg} have the same type|species?", "No, they are {pObject} and {pObject2}.", "no", 0.2, ">2"),
            ("Do the animals {inImg} all have the same type|species?", "No, they are {pObject} and {pObject2}.", "no", 0.1, ">2"),
            ("Do [both] the animals {inImg} have the same type|species?", "No, they are {pObject} and {pObject2}.", "no", 0.2, "2"),
            ("Do the two animals {inImg} have the same type|species?", "No, they are {pObject} and {pObject2}.", "no", 0.1, "2"),
            ("Are [all] the|these animals {pObject}?", "No, there are both {pObject} and {pObject2}.", "no", 0.6, ">2"),
            ("Are [both] the|these animals {pObject}?", "No, they are {pObject} and {pObject2}.", "no", 0.6, "2"),
            ("Are [all] the|these animals {pObject2}?", "No, there are both {pObject} and {pObject2}.", "no", 0.6, ">2"),
            ("Are [both] the|these animals {pObject2}?", "No, they are {pObject} and {pObject2}.", "no", 0.6, "2"),
        ]
    }, 
    "diffAnimals": {"list": [  # done
            ("Are the|these animals of different types|species?", "Yes, they are {pObject} and {pObject2}.", "yes", 1),
            ("Are the animals {inImg} of different types|species?", "Yes, they are {pObject} and {pObject2}.", "yes", 0.1),
            ("Do the|these animals have different types|species?", "Yes, they are {pObject} and {pObject2}.", "yes", 1),
            ("Do the animals {inImg} have different types|species?", "Yes, they are {pObject} and {pObject2}.", "yes", 0.1),
            # ("Are the|these two animals of different types|species?", "Yes, they are {pObject} and {pObject2}.", "yes", 1, "2"),
            # ("Are the two animals {inImg} of different types|species?", "Yes, they are {pObject} and {pObject2}.", "yes", 0.1, "2"),
            # ("Do the|these two animals have different types|species?", "Yes, they are {pObject} and {pObject2}.", "yes", 1, "2"),
            # ("Do the two animals {inImg} have different types|species?", "Yes, they are {pObject} and {pObject2}.", "yes", 0.1, "2")
        ]
    },
    "diffAnimalsC": {"list": [  # done
            ("Are the|these animals of different types|species?", "No, all the animals are {pObject}.", "no", 1),
            ("Are the animals {inImg} of different types|species?", "No, all the animals are {pObject}.", "no", 0.1),
            ("Do the|these animals have different types|species?", "No, all the animals are {pObject}.", "no", 1),
            ("Do the animals {inImg} have different types|species?", "No, all the animals are {pObject}.", "no", 0.1),
            # ("Are the|these two animals of different types|species?", "No, all the animals are {pObject}.", "no", 1, "2"),
            # ("Are the two animals {inImg} of different types|species?", "No, all the animals are {pObject}.", "no", 0.1, "2"),
            # ("Do the|these two animals have different types|species?", "No, all the animals are {pObject}.", "no", 1, "2"),
            # ("Do the two animals {inImg} have different types|species?", "No, all the animals are {pObject}.", "no", 0.1, "2")
        ]
    },
    "sameGender": {"list": [  # done
            ("Are [all] the|these people [of] the same gender?", "Yes, all the people are {gender}.", "yes", 2, ">2"),
            ("Are the|these people all [of] the same gender?", "Yes, all the people are {gender}.", "yes", 1, ">2"),
            ("Are [both] the|these people [of] the same gender?", "Yes, all the people are {gender}.", "yes", 2, "2"),
            ("Are the|these two people [of] the same gender?", "Yes, all the people are {gender}.", "yes", 1, "2"),
            ("Are [all] the people {inImg} [of] the same gender?", "Yes, all the people are {gender}.", "yes", 0.2, ">2"),
            ("Are the people {inImg} all [of] the same gender?", "Yes, all the people are {gender}.", "yes", 0.1, ">2"),
            ("Are [both] the people {inImg} [of] the same gender?", "Yes, all the people are {gender}.", "yes", 0.2, "2"),
            ("Are the two people {inImg} [of] the same gender?", "Yes, all the people are {gender}.", "yes", 0.1, "2"),
            ("Do [all] the|these people have the same gender?", "Yes, all the people are {gender}.", "yes", 2, ">2"),
            ("Do the|these people all have the same gender?", "Yes, all the people are {gender}.", "yes", 1, ">2"),
            ("Do [both] the|these people have the same gender?", "Yes, all the people are {gender}.", "yes", 2, "2"),
            ("Do the|these two people have the same gender?", "Yes, all the people are {gender}.", "yes", 1, "2"),
            ("Do [all] the people {inImg} have the same gender?", "Yes, all the people are {gender}.", "yes", 0.2, ">2"),
            ("Do the people {inImg} all have the same gender?", "Yes, all the people are {gender}.", "yes", 0.1, ">2"),
            ("Do [both] the people {inImg} have the same gender?", "Yes, all the people are {gender}.", "yes", 0.2, "2"),
            ("Do the two people {inImg} have the same gender?", "Yes, all the people are {gender}.", "yes", 0.1, "2"),
            ("Are [all] the|these people {gender}?", "Yes, all the people are {gender}.", "yes", 1.2, ">2"),
            ("Are [both] the|these people {gender}?", "Yes, all the people are {gender}.", "yes", 1.2, "2"),

        ]
    },
    "sameGenderC": {"list": [  # done
            ("Are [all] the|these people [of] the same gender?", "No, they are both male and female.", "no", 2, ">2"),
            ("Are the|these people all [of] the same gender?", "No, they are both male and female.", "no", 1, ">2"),
            ("Are [both] the|these people [of] the same gender?", "No, they are both male and female.", "no", 2, "2"),
            ("Are the|these two people [of] the same gender?", "No, they are both male and female.", "no", 1, "2"),
            ("Are [all] the people {inImg} [of] the same gender?", "No, they are both male and female.", "no", 0.2, ">2"),
            ("Are the people {inImg} all [of] the same gender?", "No, they are both male and female.", "no", 0.1, ">2"),
            ("Are [both] the people {inImg} [of] the same gender?", "No, they are both male and female.", "no", 0.2, "2"),
            ("Are the two people {inImg} [of] the same gender?", "No, they are both male and female.", "no", 0.1, "2"),
            ("Do [all] the|these people have the same gender?", "No, they are both male and female.", "no", 2, ">2"),
            ("Do the|these people all have the same gender?", "No, they are both male and female.", "no", 1, ">2"),
            ("Do [both] the|these people have the same gender?", "No, they are both male and female.", "no", 2, "2"),
            ("Do the|these two people have the same gender?", "No, they are both male and female.", "no", 1, "2"),
            ("Do [all] the people {inImg} have the same gender?", "No, they are both male and female.", "no", 0.2, ">2"),
            ("Do the people {inImg} all have the same gender?", "No, they are both male and female.", "no", 0.1, ">2"),
            ("Do [both] the people {inImg} have the same gender?", "No, they are both male and female.", "no", 0.2, "2"),
            ("Do the two people {inImg} have the same gender?", "No, they are both male and female.", "no", 0.1, "2"),
            ("Are [all] the|these people male?", "No, they are both male and female.", "no", 0.6, ">2"),
            ("Are [both] the|these people male?", "No, they are both male and female.", "no", 0.6, "2"),
            ("Are [all] the|these people female?", "No, they are both male and female.", "no", 0.6, ">2"),
            ("Are [both] the|these people female?", "No, they are both male and female.", "no", 0.6, "2"),
        ]
    },
    "diffGender": {"list": [  # done
            ("Are the|these people [of] different genders?", "No, they are both male and female.", "no", 1),
            ("Are the people {inImg} [of] different genders?", "No, they are both male and female.", "no", 0.1),
            ("Do the|these people have different genders?", "No, they are both male and female.", "no", 1),
            ("Do the people {inImg} have different genders?", "No, they are both male and female.", "no", 0.1),
            # ("Are the|these two people [of] different genders?", "No, they are both male and female.", "no", 1, "2"),
            # ("Are the two people {inImg} [of] different genders?", "No, they are both male and female.", "no", 0.1, "2"),
            # ("Do the|these two people have different genders?", "No, they are both male and female.", "no", 1, "2"),
            # ("Do the two people {inImg} have different genders?", "No, they are both male and female.", "no", 0.1, "2"),

        ]
    }, 
    "diffGenderC": {"list": [  # done
            ("Are the|these people [of] different genders?", "No, all the people are {gender}.", "no", 1),
            ("Are the people {inImg} [of] different genders?", "No, all the people are {gender}.", "no", 0.1),
            ("Do the|these people have different genders?", "No, all the people are {gender}.", "no", 1),
            ("Do the people {inImg} have different genders?", "No, all the people are {gender}.", "no", 0.1),
            # ("Are the|these two people [of] different genders?", "No, all the people are {pObject}.", "no", 1, "2"),
            # ("Are the two people {inImg} [of] different genders?", "No, all the people are {pObject}.", "no", 0.1, "2"),
            # ("Do the|these two people have different genders?", "No, all the people are {pObject}.", "no", 1, "2"),
            # ("Do the two people {inImg} have different genders?", "No, all the people are {pObject}.", "no", 0.1, "2"),
        ]
    },        
    # "allSameTypeC": {"list": [ # shouldo????
    #         ("Are [all] the|these {categories} [inImg]=0.1 the same type|kind?", "No, there are both {objects} and {objects2}.", "no", 2, all),
    #         ("Are the|these {categories} [inImg]=0.1 all the same type|kind?", "No, there are both {objects} and {objects2}.", "no", 1, all),
    #         ("Are [both] the|these {categories} [inImg]=0.1 the same type|kind?", "No, they are {object} and {object2}.", "no", 2, both),
    #         ("Are the|these two {categories} [inImg]=0.1 the same type|kind?", "No, they are {object} and {object2}.", "no", 1, both),
    #         ("Do [all] the|these {categories} [inImg]=0.1 have the same type|kind?", "No, there are both {objects} and {objects2}.", "no", 1, all),
    #         ("Do the|these {categories} [inImg]=0.1 all have the same type|kind?", "No, there are both {objects} and {objects2}.", "no", 0.5, all),
    #         ("Do [both] the|these {categories} [inImg]=0.1 have the same type|kind?", "No, they are {object} and {object2}.", "no", 0.5, both),
    #         ("Do the|these two {categories} [inImg]=0.1 have the same type|kind?", "No, they are {object} and {object2}.", "no", 0.5, both)
    #     ],
    #     "extra": {"both": {"num": 2}}
    #     # different types?
    # },
    # "allSame": {"list": [ # same or similar? # shouldo????
    #         ("Are [all] the|these {categories} [inImg]=0.1 the same {type}?", "Yes, all the {categories} are {attribute}.", "yes", 2, all),
    #         ("Are the|these {categories} [inImg]=0.1 all the same {type}?", "Yes, all the {categories} are {attribute}.", "yes", 1, all),
    #         ("Are [both] the|these {categories} [inImg]=0.1 the same {type}?", "Yes, both the {categories} are {attribute}.", "yes", 2, both),
    #         ("Are the|these two {categories} [inImg]=0.1 the same {type}?", "Yes, both the {categories} are {attribute}.", "yes", 1, both),
    #         ("Do [all] the|these {categories} [inImg]=0.1 have the same {type}?", "Yes, all the {categories} are {attribute}.", "yes", 1, all),
    #         ("Do the|these {categories} [inImg]=0.1 all have the same {type}?", "Yes, all the {categories} are {attribute}.", "yes", 0.5, all),
    #         ("Do [both] the|these {categories} [inImg]=0.1 have the same {type}?", "Yes, both the {categories} are {attribute}.", "yes", 0.5, both),
    #         ("Do the|these two {categories} [inImg]=0.1 have the same {type}?", "Yes, both the {categories} are {attribute}.", "yes", 0.5, both),
    #         ("Is the {type} of all the {categories} [inImg]=0.1 the same?", "Yes, all the {categories} are {attribute}.", "yes", 1, all),
    #     ],
    #     "extra": {
    #         "types": {["color", "shape", "gender", "race", "material"]},
    #         "both": {"num": 2}
    #     }
    # },
    # "allSameC": {"list": [ # shouldo????
    #         ("Are [all] the|these {categories} [inImg]=0.1 the same {type}?", "No, there are both {attribute} and {attribute2} {categories}.", "no", 2, all),
    #         ("Are the|these {categories} [inImg]=0.1 all the same {type}?", "No, there are both {attribute} and {attribute2} {categories}.", "no", 1, all),
    #         ("Are [both] the|these {categories} [inImg]=0.1 the same {type}?", "No, the {categories} are {attribute} and {attribute2}.", "no", 2, both),
    #         ("Are the|these two {categories} [inImg]=0.1 the same {type}?", "No, the {categories} are {attribute} and {attribute2}.", "no", 1, both),
    #         ("Do [all] the|these {categories} [inImg]=0.1 have the same {type}?", "No, there are both {attribute} and {attribute2} {categories}.", "no", 1, all, have),
    #         ("Do the|these {categories} [inImg]=0.1 all have the same {type}?", "No, there are both {attribute} and {attribute2} {categories}.", "no", 0.5, all, have),
    #         ("Do [both] the|these {categories} [inImg]=0.1 have the same {type}?", "No, the {categories} are {attribute} and {attribute2}.", "no", 0.5, both, have),
    #         ("Do the|these two {categories} [inImg]=0.1 have the same {type}?", "No, the {categories} are {attribute} and {attribute2}.", "no", 0.5, both, have),
    #         ("Is the {type} of all the {categories} [inImg]=0.1 the same?", "No, there are both {attribute} and {attribute2} {categories}.", "no", 1, all),
    #     ],
    #     "extra": {
    #         "types": ["color", "shape", "gender", "race", "material"],
    #         "haveTypes": ["color", "shape", "gender", "race"],
    #         "synonyms": {"race": ["ethnicity", "ethnic group"]},
    #         "both": {"num": 2}
    #     }
    # },
    # treat multiple objects of the same category as group object?
    # "allAttr": {"list": [ # shouldo????? # same or similar?  
    #         ("Are [all] the|these {categories} [inImg]=0.1 {attribute}?", "Yes, all the {categories} are {attribute}.", "yes", 2, all),
    #         ("Are [both] the|these {categories} [inImg]=0.1 {attribute}?", "Yes, both the {categories} are {attribute}.", "yes", 2, both),
    #         ("Do [all] the|these {categories} [inImg]=0.1 have {attribute} {type}?", "Yes, all the {categories} are {attribute}.", "yes", 1, all),
    #         ("Do [both] the|these {categories} [inImg]=0.1 have {attribute} {type}?", "Yes, both the {categories} are {attribute}.", "yes", 1, both),
    #         ("Is the {type} of all the {categories} [inImg]=0.1 {attribute}?", "Yes, all the {categories} are {attribute}.", "yes", 1, all)
    #     ]
    # },
    # "allAttrC": {"list": [ # shouldo????? 
    #         ("Are [all] the|these {categories} [inImg]=0.1 {attribute}?", "No, there are both {attribute} and {attribute2} {categories}.", "no", 2, all),
    #         ("Are [both] the|these {categories} [inImg]=0.1 {attribute}?", "No, the {categories} are {attribute} and {attribute2}.", "no", 2, both),
    #         ("Do [all] the|these {categories} [inImg]=0.1 have {attribute} {type}?", "No, there are both {attribute} and {attribute2} {categories}.", "no", 1, all),
    #         ("Do [both] the|these {categories} [inImg]=0.1 have {attribute} {type}?", "No, the {categories} are {attribute} and {attribute2}.", "no", 1, both),
    #         ("Is the {type} of all the {categories} [inImg]=0.1 {attribute}?", "No, there are both {attribute} and {attribute2} {categories}.", "no", 1, all)
    #     ]
    # },
    # "allAttrC2": {"list": [ # shouldo????? 
    #         ("Are [all] the|these {categories} [inImg]=0.1 {cAttribute}?", "No, the {categories} are {attribute}.", "no", 2, all),
    #         ("Are [both] the|these {categories} [inImg]=0.1 {cAttribute}?", "No, the {categories} are {attribute}.", "no", 2, both),
    #         ("Do [all] the|these {categories} [inImg]=0.1 have {cAttribute} {type}?", "No, the {categories} are {attribute}.", "no", 1, all),
    #         ("Do [both] the|these {categories} [inImg]=0.1 have {cAttribute} {type}?", "No, the {categories} are {attribute}.", "no", 1, both),
    #         ("Is the {type} of all the {categories} [inImg]=0.1 {cAttribute}?", "No, the {categories} are {attribute}.", "no", 1, all)
    #     ]
    # },
    "twoSame": {"list": [ # done 
            ("Are [both] {dsubject} and {dobject} the same {type}?", "Yes, both {dsubject} and {dobject} are {attribute}.", "yes", 2),
            ("Do {dsubject} and {dobject} have the same {type}?", "Yes, both {dsubject} and {dobject} are {attribute}.", "yes", 2),
            ("{is} {dsubject} the same {type} as {dobject}?", "Yes, both {dsubject} and {dobject} are {attribute}.", "yes", 1),
            ("{does} {dsubject} have the same {type} as {dobject}?", "Yes, both {dsubject} and {dobject} are {attribute}.", "yes", 1),
            ("Is the {type} of {dsubject} the same as [that_of/the_{type}_of]=0.35 {dobject}?", "Yes, both {dsubject} and {dobject} are {attribute}.", "yes", 1)
        ]
        # "extra": {
        #     "types": ["color", "shape", "gender", "race", "material"],
        #     "synonyms": {"race": ["ethnicity", "ethnic group"]
        # }
    },
    "twoSameC": {"list": [ # done # short dobject
            ("Are [both] {dsubject} and {dobject} the same {type}?", "No, {dsubject} {is} {attribute} and {dobject} {is} {attribute2}.", "no", 2),
            ("Do {dsubject} and {dobject} have the same {type}?", "No, {dsubject} {is} {attribute} and {dobject} {is} {attribute2}.", "no", 2),
            ("{is} {dsubject} the same {type} as {dobject}?", "No, {dsubject} {is} {attribute} and {dobject} {is} {attribute2}.", "no", 1),
            ("{does} {dsubject} have the same {type} as {dobject}?", "No, {dsubject} {is} {attribute} and {dobject} {is} {attribute2}.", "no", 1),
            ("Is the {type} of {dsubject} the same as [that_of/the_{type}_of]=0.35 {dobject}?", "No, {dsubject} {is} {attribute} and {dobject} {is} {attribute2}.", "no", 1),
            ("Are [both] {dobject} and {dsubject} the same {type}?", "No, {dsubject} {is} {attribute} and {dobject} {is} {attribute2}.", "no", 2),
            ("Do {dobject} and {dsubject} have the same {type}?", "No, {dsubject} {is} {attribute} and {dobject} {is} {attribute2}.", "no", 2),
            ("{is} {dobject} the same {type} as {dsubject}?", "No, {dsubject} {is} {attribute} and {dobject} {is} {attribute2}.", "no", 1),
            ("{does} {dobject} have the same {type} as {dsubject}?", "No, {dsubject} {is} {attribute} and {dobject} {is} {attribute2}.", "no", 1),
            ("Is the {type} of {dobject} the same as [that_of/the_{type}_of]=0.35 {dsubject}?", "No, {dsubject} {is} {attribute} and {dobject} {is} {attribute2}.", "no", 1)
        ]
        # "extra": {        
        #     "types": ["color", "shape", "gender", "race", "material"],
        #     "synonyms": {"race": ["ethnicity", "ethnic group"]
        # }
    },
    "twoSameMaterial": {"list": [ # done 
            ("Are [both] {dsubject} and {dobject} the same {type}?", "Yes, both {dsubject} and {dobject} are made of {attribute}.", "yes", 2),
            ("Do {dsubject} and {dobject} have the same {type}?", "Yes, both {dsubject} and {dobject} are made of {attribute}.", "yes", 2),
            ("{is} {dsubject} the same {type} as {dobject}?", "Yes, both {dsubject} and {dobject} are made of {attribute}.", "yes", 1),
            ("{does} {dsubject} have the same {type} as {dobject}?", "Yes, both {dsubject} and {dobject} are made of {attribute}.", "yes", 1),
            ("Is the {type} of {dsubject} the same as [that_of/the_{type}_of]=0.35 {dobject}?", "Yes, both {dsubject} and {dobject} are made of {attribute}.", "yes", 1)
        ]
        # "extra": {
        #     "types": ["color", "shape", "gender", "race", "material"],
        #     "synonyms": {"race": ["ethnicity", "ethnic group"]
        # }
    },    
    # "allDifferentC": {"list": [
    #         ("Do the|these {categories} [inImg]=0.1 have different {type}s?", "No, all the {categories} are {attribute}.", "no", 1, all),
    #         ("Do the|these two {categories} [inImg]=0.1 have different {type}s?", "No, both the {categories} are {attribute}.", "no", 0.5, both)
    #     ]
    #     "extra": {
    #         "types": ["color", "shape", "gender", "race", "material"],
    #         "both": {"num": 2}
    #     }
    # },
    # "allDifferent": {"list": [
    #         ("Do the|these {categories} [inImg]=0.1 have different {type}s?", "Yes, there are both {attribute} and {attribute2} {categories}.", "yes", 1, all),
    #         ("Do the|these two {categories} [inImg]=0.1 have different {type}s?", "Yes, they are {attribute} and {attribute2} {categories}.", "yes", 0.5, both)
    #     ]
    #     "extra": {
    #         "types": ["color", "shape", "gender", "race", "material"],
    #         "synonyms": {"race": ["ethnicity", "ethnic group"],
    #         "both": {"num": 2}
    #     }
    # },
    "twoDifferentC": {"list": [ # done 
            ("Do {dsubject} and {dobject} have different {type}s?", "No, both {dsubject} and {dobject} are {attribute}.", "no", 1),
            ("{is} {dsubject} different in {type} than {dobject}?", "No, both {dsubject} and {dobject} are {attribute}.", "no", 1),
            ("{does} {dsubject} have different {type} than {dobject}?", "No, both {dsubject} and {dobject} are {attribute}.", "no", 1),
            ("Is the {type} of {dsubject} different than [that_of/the_{type}_of]=0.35 {dobject}?", "No, both {dsubject} and {dobject} are {attribute}.", "no", 1)  
        ]
        # "extra": {
        #     "types": ["color", "shape", "gender", "race", "material"],
        #     "synonyms": {"race": ["ethnicity", "ethnic group"]
        # }
    },
    "twoDifferent": {"list": [ # done  # short dobject
            ("Do {dsubject} and {dobject} have different {type}s?", "Yes, {dsubject} {is} {attribute} and {dobject} {is} {attribute2}.", "yes", 1),
            ("{is} {dsubject} different in {type} than {dobject}?", "Yes, {dsubject} {is} {attribute} and {dobject} {is} {attribute2}.", "yes", 1), # both {dsubject} and {dobject} are {attribute}
            ("{does} {dsubject} have different {type} than {dobject}?", "Yes, {dsubject} {is} {attribute} and {dobject} {is} {attribute2}.", "yes", 1),
            ("Is the {type} of {dsubject} different than [that_of/the_{type}_of]=0.35 {dobject}?", "Yes, {dsubject} {is} {attribute} and {dobject} {is} {attribute2}.", "yes", 1),       
            ("Do {dobject} and {dsubject} have different {type}s?", "Yes, {dobject} {is} {attribute} and {dsubject} {is} {attribute2}.", "yes", 1),
            ("{is} {dobject} different in {type} than {dsubject}?", "Yes, {dsubject} {is} {attribute} and {dobject} {is} {attribute2}.", "yes", 1),
            ("{does} {dobject} have different {type} than {dsubject}?", "Yes, {dsubject} {is} {attribute} and {dobject} {is} {attribute2}.", "yes", 1),
            ("Is the {type} of {dobject} different than [that_of/the_{type}_of]=0.35 {dsubject}?", "Yes, {dsubject} {is} {attribute} and {dobject} {is} {attribute2}.", "yes", 1)        
        ]
        # "extra": {
        #     "types": ["color", "shape", "gender", "race", "material"],
        #     "synonyms": {"race": ["ethnicity", "ethnic group"]}
        # }
    },
    # "allSameMaterial": {"list": [ # shouldo???? # same or similar?
    #         ("Are [all] the|these {categories} [inImg]=0.1 made [out]=0.03 of the same material?", "Yes, all the {categories} are made of {attribute}.", "yes", 2, all),
    #         ("Are the|these {categories} [inImg]=0.1 all made [out]=0.03 of the same material?", "Yes, all the {categories} are made of {attribute}.", "yes", 1, all),
    #         ("Are [both] the|these {categories} [inImg]=0.1 made [out]=0.03 of the same material?", "Yes, both the {categories} are made of {attribute}.", "yes", 2, both),
    #         ("Are the|these two {categories} [inImg]=0.1 made [out]=0.03 of the same material?", "Yes, both the {categories} are made of {attribute}.", "yes", 1, both),
    #     ]
    # },
    # "allSameMaterialC": {"list": [ # shouldo???? 
    #         ("Are [all] the|these {categories} [inImg]=0.1 made [out]=0.03 of the same material?", "No, there are both {attribute} and {attribute2} {categories}.", "no", 2, all),
    #         ("Are the|these {categories} [inImg]=0.1 all made [out]=0.03 of the same material?", "No, there are both {attribute} and {attribute2} {categories}.", "no", 1, all),
    #         ("Are [both] the|these {categories} [inImg]=0.1 made [out]=0.03 of the same material?", "No, they are {attribute} and {attribute2} {categories}.", "no", 2, both),
    #         ("Are the|these two {categories} [inImg]=0.1 made [out]=0.03 of the same material?", "No, they are {attribute} and {attribute2} {categories}.", "no", 1, both),
    #     ]
    # },
    # "allSameMaterialC": {"list": [
    #         ("Are [all] the|these {categories} [inImg]=0.1 made [out]=0.03 of the same material?", "No, the {categories} are made of {attribute}.", "no", 2, all),
    #         ("Are the|these {categories} [inImg]=0.1 all made [out]=0.03 of the same material?", "No, the {categories} are made of {attribute}.", "no", 1, all),
    #         ("Are [both] the|these {categories} [inImg]=0.1 made [out]=0.03 of the same material?", "No, the {categories} are made of {attribute}.", "no", 2, both),
    #         ("Are the|these two {categories} [inImg]=0.1 made [out]=0.03 of the same material?", "No, the {categories} are made of {attribute}.", "no", 1, both),
    #     ]
    # },
    # "allSameMaterial": {"list": [ # same or similar?
    #         ("Are [all] the|these {categories} [inImg]=0.1 made [out]=0.03 of {attribute}?", "Yes, all the {categories} are made of {attribute}.", "yes", 2, all),
    #         ("Are the|these {categories} [inImg]=0.1 all made [out]=0.03 of {attribute}?", "Yes, all the {categories} are made of {attribute}.", "yes", 1, all),
    #         ("Are [both] the|these {categories} [inImg]=0.1 made [out]=0.03 of {attribute}?", "Yes, both the {categories} are made of {attribute}.", "yes", 2, both),
    #         ("Are the|these two {categories} [inImg]=0.1 made [out]=0.03 of {attribute}?", "Yes, both the {categories} are made of {attribute}.", "yes", 1, both),
    #     ]
    # },
    # "allSameMaterialC": {"list": [
    #         ("Are [all] the|these {categories} [inImg]=0.1 made [out]=0.03 of {attribute}?", "No, there are both {attribute} and {attribute2} {categories}.", "no", 2, all),
    #         ("Are the|these {categories} [inImg]=0.1 all made [out]=0.03 of {attribute}?", "No, there are both {attribute} and {attribute2} {categories}.", "no", 1, all),
    #         ("Are [both] the|these {categories} [inImg]=0.1 made [out]=0.03 of {attribute}?", "No, they are {attribute} and {attribute2} {categories}.", "no", 2, both),
    #         ("Are the|these two {categories} [inImg]=0.1 made [out]=0.03 of {attribute}?", "No, they are {attribute} and {attribute2} {categories}.", "no", 1, both),
    #     ]
    # },
    "twoSameMaterial": {"list": [ # done 
            ("Are [both] {dsubject} and {dobject} made [out]=0.03 of the same material?", "Yes, both {dsubject} and {dobject} are made of {attribute}.", "yes", 1),
            ("{is} {dsubject} made [out]=0.03 of the same material as {dobject}?", "Yes, both {dsubject} and {dobject} are made of {attribute}.", "yes", 1),
            ("Do {dsubject} and {dobject} have the same material?", "Yes, both {dsubject} and {dobject} are made of {attribute}.", "yes", 0.05),
            ("{is} {dsubject} the same material as {dobject}?", "Yes, both {dsubject} and {dobject} are made of {attribute}.", "yes", 0.05),
            ("{does} {dsubject} have the same material as {dobject}?", "Yes, both {dsubject} and {dobject} are made of {attribute}.", "yes", 0.05),
            ("{is} the material of {dsubject} the same as {dobject}?", "Yes, both {dsubject} and {dobject} are made of {attribute}.", "yes", 0.05)
        ]
    },
    "twoSameMaterialC": {"list": [ # done  # short dobject
            ("Are [both] {dsubject} and {dobject} made [out]=0.03 of the same material?", "No, {dsubject} {is} made of {attribute} and {dobject} {is} made of {attribute2}.", "no", 1),
            ("{is} {dsubject} made [out]=0.03 of the same material as {dobject}?", "No, {dsubject} {is} made of {attribute} and {dobject} {is} made of {attribute2}.", "no", 1),
            ("Do {dsubject} and {dobject} have the same material?", "No, {dsubject} {is} made of {attribute} and {dobject} {is} made of {attribute2}.", "no", 0.05),
            ("{is} {dsubject} the same material as {dobject}?", "No, {dsubject} {is} made of {attribute} and {dobject} {is} made of {attribute2}.", "no", 0.05),
            ("{does} {dsubject} have the same material as {dobject}?", "No, {dsubject} {is} made of {attribute} and {dobject} {is} made of {attribute2}.", "no", 0.05),
            ("{is} the material of {dsubject} the same as {dobject}?", "No, {dsubject} {is} made of {attribute} and {dobject} {is} made of {attribute2}.", "no", 0.05)
        ]
    },
    # "allDifferentMaterialC": {"list": [
    #         ("Are the|these {categories} [inImg]=0.1 made [out]=0.03 of different materials?", "No, all the {categories} are  made of {attribute}.", "no", 1, all),
    #         ("Are the|these two {categories} [inImg]=0.1 made [out]=0.03 of different materials?", "No, both the {categories} are  made of {attribute}.", "no", 0.5, both)
    #     ]
    #     "extra": {"both": {"num": 2}}
    # },
    # "allDifferentMaterial": {"list": [
    #         ("Are the|these {categories} [inImg]=0.1 made [out]=0.03 of different materials?", "Yes, there are both {attribute} and {attribute2} {categories}.", "yes", 1, all),
    #         ("Are the|these two {categories} [inImg]=0.1 made [out]=0.03 of different materials?", "Yes, they are {attribute} and {attribute2} {categories}.", "yes", 0.5, both)
    #     ]
    #     "extra": {"both": {"num": 2}}
    # },
    "twoDifferentMaterialC": {"list": [  
            ("Are {dobject} and {dobject2} made [out]=0.03 of different materials?", "No, both {dobject} and {dobject2} are {attribute}.", "no", 1)
        ]
    },
    "twoDifferentMaterial": {"list": [ # short dobject
            ("Are {dobject} and {dobject2} made [out]=0.03 of different materials?", "Yes, {dobject} {is} {attribute} and {dobject2} {is} {attribute2}.", "yes", 1)
        ]
    },
    # "allCommon": {"list": [ # shouldo?????
    #         ("What is common to [all] the {categories} [inImg]=0.1?", "Yes, all the {categories} are {attribute}.", "yes", 1, all),
    #         ("What is common to [both] the|these {categories} [inImg]=0.1 the same {type}?", "Yes, both the {categories} are {attribute}.", "yes", 1, both),
    #         ("What is common to the|these two {categories} [inImg]=0.1 the same {type}?", "Yes, both the {categories} are {attribute}.", "yes", 0.5, both),
    #         ("What do [all] the|these {categories} [inImg]=0.1 have in common?", "Yes, all the {categories} are {attribute}.", "yes", 3, all),
    #         ("What do the {categories} [inImg]=0.1 all have in common?", "Yes, all the {categories} are {attribute}.", "yes", 1.5, all),
    #         ("What do both the|these {categories} [inImg]=0.1 have in common?", "Yes, both the {categories} are {attribute}.", "yes", 3, both)
    #         ("What do the|these two {categories} [inImg]=0.1 have in common?", "Yes, both the {categories} are {attribute}.", "yes", 1.5, both)
    #     ]
    #     "extra": {
    #         "types": ["color", "shape", "gender", "race", "material"],
    #         "synonyms": {"race": ["ethnicity", "ethnic group"],
    #         "both": {"num": 2}
    #     }
    # },
    "twoCommon": {"list": [  # done # type or attribute as 1-word answer 
            ("What is common to {dsubject} and {dobject}?", "The {type} , both {dsubject} and {dobject} are {attribute}.", "{type}", 1),
            ("What do [both] {dsubject} and {dobject} have in common?", "The {type} , both {dsubject} and {dobject} are {attribute}.", "{type}", 3)
        ],
    },
    "twoCommonMaterial": {"list": [  # done # type or attribute as 1-word answer 
            ("What is common to {dsubject} and {dobject}?", "The {type} , both {dsubject} and {dobject} are made of {attribute}.", "{type}", 1),
            ("What do [both] {dsubject} and {dobject} have in common?", "The {type} , both {dsubject} and {dobject} are made of {attribute}.", "{type}", 3)
        ],
    },    
    # "comparative": {"list": [  # done
    #         ("Is {dobject} {comparative} {than} {dobject2}?", "Yes, {dobject} {is} {comparative} {than} {dobject2}.", "yes", 1)
    #     ]
    # },
    # "comparativeC": {"list": [  # done
    #         ("Is {dobject} {cComparative} {than} {dobject2}?", "No, {dobject} {is} {comparative} {than} {dobject2}.", "no", 1)
    #     ]
    # },
    "comparativeChoose": {"list": [ # WHO? # done
            ("{which} {is} {comparative} , {dsubject} or {dobject}?", "{dsubject} {is} {comparative} than {dobject}.", "{subject}", 1),
            ("{which} {is} {comparative} , {dobject} or {dsubject}?", "{dsubject} {is} {comparative} than {dobject}.", "{subject}", 1),
            ("{which} seem{s} to be {comparative} , {dsubject} or {dobject}?", "{dsubject} {is} {comparative} than {dobject}.", "{subject}", 0.15),
            ("{which} seem{s} to be {comparative} , {dobject} or {dsubject}?", "{dsubject} {is} {comparative} than {dobject}.", "{subject}", 0.15)
        ]
    },
    # here instead of there?
    # are there more X than Y?
    "count": {"list": [ # short objects (without rel),
            ("How many {dobjects} [are_there]=0.96?", "There {are} {count} {dobject}.", "{count}", 1), #0 -> no,
            ("What number of {dobjects} [are_there]=0.96?", "There {are} {count} {dobject}.", "{count}", 0.1),
            ("How many {dobjects} are [there]=0.1? {inImg}", "There {are} {count} {dobject}.", "{count}", 0.3), #0 -> no,
            ("What number of {dobjects} are [there]=0.1 {inImg}?", "There {are} {count} {dobject}.", "{count}", 0.03),
            ("How many {dobjects} are visible|observable|shown|presented [{inImg}]=0.2", "There {are} {count} {dobject}.", "{count}", 0.05), #0 -> no,
            ("What number of {dobjects} are visible|observable|shown|presented [{inImg}]=0.2?", "There {are} {count} {dobject}.", "{count}", 0.01),    
            ("How many {dobjects} can|do you see [there]=0.2?", "There {are} {count} {dobject}.", "{count}", 0.1), #0 -> no,
            ("What number of {dobjects} can|do you see [there]=0.2?", "There {are} {count} {dobject}.", "{count}", 0.05)    
        ]
    },
    "countVerify": {"list": [
            ("Are there {count} {dobjects} there?", "Yes, there {are} {count} {dobject}.", "yes", 1)
        ]
    },
    "countVerifyC": {"list": [
            ("Are there {cCount} {dobjects} there?", "No, there {are} {count} {dobject}.", "no", 1)
        ]
    },
    # add: how many X is Y rel?
    "countModifier": {"list": [
            ("How many {dobjects} [there]=0.2 [are]=0.98 {modifier}?", "There {are} {count} {dobject} {modifier}.", "{count}", 1), #0 -> no,
            ("What number of {dobjects} [there]=0.2 [are]=0.98 {modifier}?", "There {are} {count} {dobject} {modifier}.", "{count}", 0.1),
            ("How many {dobjects} {inImg} [are]=0.98 {modifier}?", "There {are} {count} {dobject} {modifier}.", "{count}", 0.1), #0 -> no,
            ("What number of {dobjects} {inImg} [are]=0.98 {modifier}?", "There {are} {count} {dobject} {modifier}.", "{count}", 0.01)
        ]
    },
    "countVerifyModifier": {"list": [
            ("Are there {count} {dobjects} {modifier}?", "Yes, there {are} {count} {dobject}.", "yes", 1)
        ]
    },
    "countVerifyCModifier": {"list": [
            ("Are there {cCount} {dobjects} {modifier}?", "No, there {are} {count} {dobject}.", "no", 1)
        ]
    },
    # "moreless": {"list": [ # shuoldo??????
    #         ("Are there more {dobjects} than {dobjects2}?", "Yes, there are {count} {dobjects} and {count2} {dobjects2}.", "yes", 1, more),
    #         ("Is the number of {dobjects} greater than {dobjects2}?", "Yes, there are {count} {dobjects} and {count2} {dobjects2}.", "yes", 0.3, more),
    #         ("Are there less {dobjects} than {dobjects2}?", "Yes, there are {count} {dobjects} and {count2} {dobjects2}.", "yes", 1, less),
    #         ("Are there fewer {dobjects} than {dobjects2}?", "Yes, there are {count} {dobjects} and {count2} {dobjects2}.", "yes", 0.5, less),
    #         ("Is the number of {dobjects} smaller than {dobjects2}?", "Yes, there are {count} {dobjects} and {count2} {dobjects2}.", "yes", 0.3, less),
    #         ("Is the number of {dobjects} lower|less than {dobjects2}?", "Yes, there are {count} {dobjects} and {count2} {dobjects2}.", "yes", 0.03, less),
    #         ("Are there the same number of {dobjects} and {dobjects2}?", "Yes, there are {count} {dobjects} and {count2} {dobjects2}.", "yes", 0.2, equal),
    #         ("Are there an equal number of {dobjects} and {dobjects2}?", "Yes, there are {count} {dobjects} and {count2} {dobjects2}.", "yes", 0.2, equal),
    #         ("Is the number of {dobjects} equal to the number of {dobjects2}?", "Yes, there are {count} {dobjects} and {count2} {dobjects2}.", "yes", 1, equal),
    #         ("Is the number of {dobjects} the same as the number of {dobjects2}?", "Yes, there are {count} {dobjects} and {count2} {dobjects2}.", "yes", 1, equal)
    #     ]
    # },
    # "morelessC": {"list": [ # shuoldo??????
    #         ("Are there more {dobjects} than {dobjects2}?", "No, there are {count} {dobjects} and {count2} {dobjects2}.", "no", 1, more),
    #         ("Is the number of {dobjects} greater than {dobjects2}?", "No, there are {count} {dobjects} and {count2} {dobjects2}.", "no", 0.3, more),
    #         ("Are there less {dobjects} than {dobjects2}?", "No, there are {count} {dobjects} and {count2} {dobjects2}.", "no", 1, less),
    #         ("Are there fewer {dobjects} than {dobjects2}?", "No, there are {count} {dobjects} and {count2} {dobjects2}.", "no", 0.5, less),
    #         ("Is the number of {dobjects} smaller than {dobjects2}?", "No, there are {count} {dobjects} and {count2} {dobjects2}.", "no", 0.3, less),
    #         ("Is the number of {dobjects} lower|less than {dobjects2}?", "No, there are {count} {dobjects} and {count2} {dobjects2}.", "no", 0.03, less),
    #         ("Are there the same number of {dobjects} and {dobjects2}?", "No, there are {count} {dobjects} and {count2} {dobjects2}.", "no", 0.2, equal),
    #         ("Are there an equal number of {dobjects} and {dobjects2}?", "No, there are {count} {dobjects} and {count2} {dobjects2}.", "no", 0.2, equal),
    #         ("Is the number of {dobjects} equal to the number of {dobjects2}?", "No, there are {count} {dobjects} and {count2} {dobjects2}.", "no", 1, equal),
    #         ("Is the number of {dobjects} the same as the number of {dobjects2}?", "No, there are {count} {dobjects} and {count2} {dobjects2}.", "no", 1, equal)
    #     ]
    # },
    # "morelessChoose": {"list": [ # shuoldo??????
    #         ("Are there more {dobjects} or {dobjects2}?", "There are more {dobjects} than {dobjects2}.", "{dobjects}", 1, more),
    #         ("Are there more {dobjects2} or {dobjects}?", "There are more {dobjects} than {dobjects2}.", "{dobjects}", 1, more),
    #         ("Are there less {dobjects} or {dobjects2}?", "There are less {dobjects} than {dobjects2}.", "{dobjects}", 1, less),
    #         ("Are there less {dobjects2} or {dobjects}?", "There are less {dobjects} than {dobjects2}.", "{dobjects}", 1, less)
    #     ]
    # },
    # # bottom / top?
    # "leftOrRight": {"list": [  # shuoldo?????? #dobject short
    #         ("Which {dobject} is {attribute} , the left or the right?", "The left {dobject} is {attribute}.", "left", 1, left),
    #         ("Which {dobject} is {attribute} , the right or the left?", "The left {dobject} is {attribute}.", "left", 1, left),
    #         ("Which {dobject} is {attribute} , the left or the right?", "The right {dobject} is {attribute}.", "right", 1, right),
    #         ("Which {dobject} is {attribute} , the right or the left?", "The right {dobject} is {attribute}.", "right", 1, right)
    #     ]
    # },
    "sameRelate": {"list": [ # done
            ("What {kategory} {kis} the same {type} as {dobject}?", "{dsubject} {is} the same {type} as {dobject}.", "{subject}", 1),
            ("What {kategory} {khas} the same {type} as {dobject}?", "{dsubject} {is} the same {type} as {dobject}.", "{subject}", 1),
            ("What is the name of the {category} that {is} the same {type} as {dobject}?", "The {category} {cis} {a} {subject}.", "{subject}", 0.15, "countable"),
            ("What is the name of the {category} that {chas} the same {type} as {dobject}?", "The {category} {cis} {a} {subject}.", "{subject}", 0.15, "countable"),
            ("{how} {cis} the {category} that {cis} the same {type} as {dobject} called?", "The {category} {cis} {a} {subject}.", "{subject}", 0.3, "countable"),
            ("{how} {cis} the {category} that {chas} the same {type} as {dobject} called?", "The {category} {cis} {a} {subject}.", "{subject}", 0.3, "countable")
        ]
    },
    "sameMaterialRelate": {"list": [ # done
            ("What {kategory} {kis} made [out]=0.03 of the same {type} as {dobject}?", "{dsubject} {is} made of the same {type} as {dobject}.", "{subject}", 1),
            ("What is the name of the {category} that {cis} made [out]=0.03 of the same {type} as {dobject}?", "The {category} {cis} {a} {subject}.", "{subject}", 0.15, "countable"),
            ("{how} {cis} the {category} that {cis} made [out]=0.03 of same {type} as {dobject} called?", "The {category} {cis} {a} {subject}.", "{subject}", 0.3, "countable")
        ]
    }
}