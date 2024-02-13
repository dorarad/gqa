from collections import defaultdict
import argparse
import json
import pickle 
from tqdm import tqdm
#import matplotlib.pyplot as plt
#from matplotlib.patches import Rectangle
# from visual_genome import api as vg
#from PIL import Image as PIL_Image
import requests
import io
import copy
# from models import Image, Object, Attribute, Relationship
# from models import Region, Graph, QA, QAObject, Synset
import json
import en
# import utils
from nltk.corpus import wordnet as wn
# import en
# from progress.bar import Bar
# from nltk.corpus import wordnet_ic
# brown_ic = wordnet_ic.ic('ic-brown.dat')
import pprint
pp = pprint.PrettyPrinter(indent=2)
import os
from nltk.stem import WordNetLemmatizer
#metadata_annotationsNew.json
import utils 
wnl = WordNetLemmatizer()

def filterOn(s, o):
    # numbers, chair, branch, trunk wall
    background = ["background", "ground", "terrain", "land", "cloud", "clouds", "mountains", "rock", "rocks", "boulders", "sky", "rain", "snow flakes", "sea foam", "fire", "stone", "stones", "wave", "waves", "bubble", "bubbles", "steam", "smoke", "leaf", "petal", 
        "petals", "branch", "branches", "tree branch", "tree branches", "twig", "twigs", "stick", "sticks", "log", "logs", "stump", "cliff", "island", "waterfall", "moon", "sun", "air", "ceiling", "roof", "floor", "deck", "wall", "walls", "wallpaper", "step", 
        "steps", "staircase", "stairs", "window", "windows", "door", "doors", "garage door", "tile", "floor tile", "pillars", "bridge", "elevator", "chimney", "smoke stack", "paint", "platform", "hook"]
    blacklistSubjects = ["ski", "pole", "sign post", "fence post", "seed", "post", "handle", "heel", "pocket", "pockets", "frame", "drawers", "drawer", "belt", "balcony", "crust", "floor", "window", "windows", "tile", "leaf", "door", "doors", "hair", "skin", "fur", "wool", "feathers"]
    blacklistObjects = ["bookcase", "glasses", "strap", "air", "land", "ground", "step", "oven door", "soup", "mirror", "pen", "background", "wave", "waves", "number", "numbers", "word", "words", "weeds", "weed", "skis", "plant", "plants", "sandwiches", "characters", 
        "character", "painting", "drawing", "ring", "fire", "collar", "money", "phones", "phone", "display", "photo", "tile", "wheels", "wheel"] # mirror?
    sblackcat = ["body part", "part", "vehicle part", "place", "road", "building", "room"]
    clothing = ["clothing", "footwear", "accessory"]
    oblackcat = ["building", "vehicle", "aircraft", "clothing", "device", "part", "accessory", "label", "symbol", "meal", "drink", "weapon", "person", "body part", "room"]
    hats = ["chef hat", "cowboy hat", "hat", "hats", "cap", "crown", "bandage", "helmet", "sugar", "watch", "wristwatch", "bracelet"] 
    waterWhitelist = ["surfboard", "ice", "snow"]
    waterWhitelistCat = ["animal", "watercraft"]
    curtains = ["curtain", "curtains", "drape", "drapes", "blind", "blinds", "shower curtain"] 
    containers = ["bottle", "bottles", "cup", "container", "containers", "food container", "egg carton", "milk carton", "jar", "jars", "cookie jar", "box", 
    "storage box", "juice box", "cereal box", "bread box", "lunch box", "pizza box", "pizza boxes", "boxes", 
    "canister", "canisters", "package", "packages", "basket", "baskets", "bowl", "bowls"]
    onWindow = ["curtain", "blinds", "curtains", "sign", "drapes", "number", "words", "lock", "drape"]
    food = ["food", "fruit", "vegetable", "dessert", 'baked good', 'meat', 'fast food', 'sauce', 'ingredient']
    foodExtra = ["icing", "frosting", "glaze", "powder"]
    extraParts = ["door frame", "doorway", "window frame", "touchpad", "horse hoof", "strap", "straps", "hair", "skin", "fur", "wool", "feathers", "seat belt", "cockpit"]
    chairs = ["office chair", "chairs", "couch", "couches", "sofa", "bench", "chair"]
    vehicleWhitelistCats = ["person", "animal"]
    bags = ["bag", "bags", "pouch", "purse", "wallet", "handbag", "backpack", "backpacks", "briefcase", "luggage", 
    "suitcase", "suitcases", "luggage cart", "shopping bag", "sack", "trash bag"]
    vehicleWhitelist = ["ladder", "surfboard", "ladder", "antenna", "flag", "basket", "helmet", "chain"] 
    buildingWhitelist = ["clock", "sign", "flag", "cross", "statue", "dome", "pole", "number", "flags", "flag", 
    "antenna", "statue", "cross", "satellite dish", "bell", "snow", "flag", "clocks", "bell", "sculpture", "antenna", 
    "bird", "birds", "snow"]
    person = ["man", "person", "woman", "girl", "people", "guy", "lady"]

    blacklist = [("train", "windshield"), ("containers", "spices"), ("cap", "oil"), ("cup", "flour"),
        ("socks", "shoe"), ("scissors", "balloon"), ("keyboard", "piano"), ("airplane", "wing"), 
        ("gloves", "bat"), ("tree", "trunk"), ("tree", "trunks"), ("trees", "trunk"), ("trees", "trunks"), 
        ("faucet", "sink"), ("bear", "branch"), ("elephant", "branch"), ("duck", "branch"), ("soda", "post"), 
        ("toilet", "wall"), ("sink", "wall"), ("refrigerator", "wall"), ("cabinets", "wall"), ("cabinet", "wall"), 
        ("box", "herbs"), ("drawers", "nightstand"), ("drink", "food"), ("plate", "food"), ("food", "oven"), 
        ("chicken", "oven"), ("fish", "oven"), ("bread", "microwave"), ("seat", "toilet"),
        ("pears", "microwave"), ("glass", "door"), ("glass", "building"), ("glass", "train"), ("glass", "bus"), 
        ("glass", "wall"), ("glass", "oven"), ("glass", "car"), ("glass", "cabinet door"),  ("glass", "motorcycle"), 
        ("glass", "pole"), ("glass", "shower"), ("glass", "parking meter"),  ("glass", "helmet"), ("glass", "shop"), 
        ("glass", "clock"), ("glass", "computer"), ("glass", "ceiling"), ("glass", "tower"), ("glass", "cockpit"), 
        ("glass", "roof"), ("glass", "island"), ("glass", "label"), ("glass", "screen"), ("glass", "windshield"), 
        ("glass", "monitor"), ("glass", "bridge"), ("glass", "balcony"), ("glass", "television"), ("glass", "street"), 
        ("glass", "menu"), ("train", "boat"), ("plant", "pot"), ("pole", "canopy"), ("cabinet", "door"), ("lid", "toilet"), 
        ("bowl", "toilet"), ("hat", "face"), ("helmet", "face"), ("people", "seat"), ("grass", "park"), ("post", "pole"), 
        ("toilet", "floor"), ("man", "statue"), ("person", "statue"), ("woman", "statue"), 
        ("elephant", "water"), ("horse", "water"), ("dog", "water"), ("bear", "water"), 
        ("faucet", "wall"), ("man", "wall"), ("fence", "wall"), ("fireplace", "wall"), ("toaster", "wall"), 
        ("person", "wall"), ("sheep", "wall"), ("oven", "wall"), ("tree", "wall"), ("woman", "wall"), ("vase", "wall"), 
        ("microwave", "wall"), ("chair", "wall"), ("container", "wall"), ("shower", "wall"), ("book", "wall"), 
        ("cow", "wall"), ("boy", "wall"), ("people", "wall"), ("deer", "wall"), ("grass", "floor"), ("urinal", "floor"),
        ("leaves", "grass"), ("leaves", "branches"), ("leaves", "bush"), ("leaves", "leaves"), 
        ("leaves", "tree branch"), ("leaves", "flower"), ("leaves", "flowers"), ("leaves", "vine"), 
        ("leaves", "tree branches"), ("leaves", "hillside"), ("tree leaves", "tree"), ("leaves", "crust"),
        ("sandwich", "bread"), ("bread", "sandwich"), ("dirt", "grass"), ("grass", "dirt"), ("plate", "field"), 
        ("home plate", "field")]

    whitelist = [("whipped cream", "milkshake"), ("whipped cream", "drink"), ("strawberry", "smoothie"),
        ("snow", "ground"), ("grass", "groun"), ("leaves", "ground"), ("ball", "ground"), ("bag", "ground"), 
        ("backpack", "ground"), ("kite", "ground"), ("bottle", "ground"), ("box", "ground"), ("suitcase", "ground"), 
        ("bucket", "ground"), ("cup", "groun"), ("frisbee", "ground"), ("luggage", "ground"), ("carpet", "ground"), 
        ("bat", "ground"), ("fruit", "ground"), ("snowboard", "ground"), ("helmet", "ground"), ("shoes", "ground"), 
        ("banana", "ground"), ("rug", "ground"), ("pot", "ground"), ("snow", "car"), ("dog", "bike"), ("towel", "oven door"), 
        ("towels", "oven door"),  ("cross", "necklace"), ("beads", "necklace"), ("bead", "necklace"), ("heart", "necklace"), 
        ("cat", "laptop"), ("cat", "computer"), ("cat", "keyboard"), ("animal", "computer"), ("book", "computer"), 
        ("pen", "keyboard"), ("kitten", "laptop"), ("antenna", "television"), ("antenna", "cell phone"),  
        ("flowers", "laptop"), ("basket", "bike"), ("helmet", "motorcycle"), ("cat", "car"), ("man", "train"), 
        ("person", "bus"), ("man", "bus"), ("helmet", "bike"), ("bag", "bike"), ("bag", "motorcycle"), 
        ("people", "train"), ("driver", "bus"), ("passenger", "bus"), ("ladder", "truck"), ("flag", "truck"), 
        ("surfboard", "car"), ("ladder", "train"), ("flag", "bus"), ("bell", "train"), ("cat", "jeep"), ("bike", "bus"), 
        ("passenger", "train"), ("toy", "car"), ("bags", "truck"), ("passengers", "bus"), ("flag", "airplane"), 
        ("star", "airplane"), ("man", "airplane"), ("people", "airplane"), ("person", "airplane"), 
        ("mickey mouse", "airplane"), ("passenger", "airplane"), ("pilot", "airplane"), ("girl", "airplane"), 
        ("antennas", "airplane"), ("woman", "airplane"), ("antenna", "airplane"), ("flags", "airplane"), 
        ("flag", "aircraft"), ("antenna", "aircraft"), ("man", "bike"), ("man", "motorcycle"), ("person", "bike"), 
        ("woman", "bike"), ("basket", "bike"), ("helmet", "motorcycle"), ("woman", "motorcycle"), ("cat", "car"), 
        ("man", "train"), ("person", "bus"), ("man", "bus"), ("man", "scooter"), ("people", "bus"), ("bag", "bike"), 
        ("bag", "motorcycle"), ("people", "train"), ("driver", "bus"), ("passenger", "bus"), ("dog", "motorcycle"), 
        ("ladder", "truck"), ("person", "train"), ("flag", "train"), ("flag", "motorcycle"), ("chain", "bike"), 
        ("box", "train"), ("flag", "truck"), ("guy", "bike"), ("person", "scooter"), ("boy", "bike"), ("dog", "bike"), 
        ("surfboard", "car"), ("ladder", "train"), ("flag", "bus"), ("bike", "bus"), ("passenger", "train"), 
        ("woman", "bus"), ("birds", "car"), ("snow", "car"), ("toy", "car"), ("bags", "truck"), ("luggage", "truck"), 
        ("sack", "wagon"), ("antenna", "car"), ("dog", "truck"), ("box", "motorcycle"), ("ladder", "car"), 
        ("antenna", "motorcycle"), ("bananas", "bike"), ("bike", "train"), ("man", "car"), ("container", "train"), 
        ("flower", "truck"), ("bike", "car"), ("surfboard", "vehicle"), ("kitten", "bus"), ("box", "bike"), 
        ("surfboard", "truck"), ("backpack", "bike"), ("dog", "bus"), ("luggage", "motorcycle"), ("sack", "scooter"), 
        ("cows", "truck"), ("grass", "ground"), ("glove", "hand"), ("ring", "finger"), ("flowers", "grass"),
        ("tag", "ear"), ("airplane", "ground"), ("bird", "ground"), ("chimney", "roof"), ("building", "hill")]

    if isPlural(o) and not isPlural(s) and o not in ["rocks", "steps", "stairs", "papers", "books"] and s not in ["snow","grass"] and not (s == "train" and o == "train tracks") and not (catn(o) in food and (catn(s) in food or s in foodExtra)):
        return True
    for (s, o) in whitelist:
        return False    
    if (catn(s) in vehicleWhitelistCats or s in bags or s in vehicleWhitelist) and catn(o) == "vehicle":
        return False 
    if s in buildingWhitelist and catn(o) == "building":
        return False
    if s in hats and catn(o) == "body part":
        return False        
    for (s, o) in blacklist:
        return True         
    # if s in person and o in chairs:
    #   return True
    if catn(s) == "flower" and o == "vase":
        return True
    if s in extraParts:
        return True
    if s not in onWindow and o in ["window", "windows"]:
        return True
    if o in containers and s != "lid":
        return True     
    if (s in background or s in blacklistSubjects or catn(s) in sblackcat) and s not in ["bracelet"]:
        return True
    if (o in blacklistObjects or catn(o) in oblackcat) and o not in ["handle"]:
        return True
    if catn(o) in oblackcat: # and catn(s) in clothing:
        return True
    if o == "water" and s not in waterWhitelist and catn(s) not in waterWhitelistCat:
        return True
    if s in curtains and o not in ["window", "door"]:
        return True
    if (catn(s) in ["person", "animal"] or s in ["bear", "teddy bear"]) and catn(o) in ["clothing", "footwear"]:
        return True
    # if isPlural(o) and not isPlural(s) and (catn(o) in food and (catn(s) in food or s in foodExtra)):
    #   return False
    # if catn(s) in ["animal"] and catn(o) in ["clothing", "footwear"]:
    #   return False    
    return False

# window / mirror 
# natural env: stick, leaf pillars bubble log ( also for on)
# TODO on the head, hand,... earring / ear/nose in the mouth?
# as expression: in the sauce, cheese, rain foil sun, wall in the
# toOn: curtain,in,window, road, pizza
def filterIn(s, o):
    whitelist = [("foot", "sand"),  
        ("hair", "sink"), ("card", "pocket"), ("cards", "pocket"), ("cards", "car"), 
        ("receipt", "box"), ("card", "wallet"), ("tire", "water"), ("tire", "suitcase"),
        ("paper", "printer"), ("vegetable", "pizza"), ("tomato", "pizza"), ("cheese", "hot dog"), ("sauce", "pizza"), 
        ("pepperoni", "pizza"), ("egg", "pizza"), ("peppers", "pizza"), ("basil", "pizza"), ("ham", "pizza"), 
        ("onion", "hot dog"), ("ketchup", "hot dog"), ("candle", "pizza"), ("mushroom", "pizza"), ("meat", "pizza"),
        ("tag", "ear"), ("baby", "blanket"), ("pig", "blanket"), ("cat", "blanket"), ("knife", "apple"), 
        ("drawer", "desk"), ("drawers", "desk"), ("drawer", "table"), ("drawers", "table"), ("bird", "clouds"), 
        ("airplane", "clouds"), ("kite", "clouds"), ("stick", "bread"), ("sticks", "vase"), ("stick", "pot"), 
        ("stick", "sandwich"), ("stick", "buns"), ("stick", "cake"), ("leaves", "background"), ("leaves", "pond"), 
        ("leaves", "basket"), ("leaves", "living room"), ("leaves", "container"), ("leaves", "window"), 
        ("leaves", "bag"), ("leaves", "jar"), ("clock", "tower"), ("flower", "bouquet"), ("house", "mountains") ] # ("hand", "pocket"),  ("hand", "snow"), ("hands", "pockets"), 
        # ("feet", "sand"), ("feet", "water"), 

    blacklist = [("pot", "flower"), ("faucet", "sink"), ("toilet", "room"), ("furniture", "glass"),
        ("curtains", "window"), ("blind", "window"), ("blinds", "window"), ("sign", "snow"), ("umbrella", "sand"), 
        ("sign", "grass"), ("bag", "can"),("curtain", "window"), ("air conditioner", "window"), ("leaves", "tree"), 
        ("water", "toilet"), ("sign", "window"), ("water", "ocean"), ("cloud", "clouds"), ("sheep", "sheep"), 
        ("airplane", "airplanes"), ("bag", "bags"), ("banana", "bananas"), ("knife", "knives"), ("glass", "glass"), 
        ("fruit", "fruit"), ("building", "buildings"), ("orange", "oranges"), ("car", "cars"), ("person", "people"), 
        ("chicken", "chickens"), ("boat", "boats"), ("mountain", "mountains"), ("elephant", "elephants"), 
        ("cabinet", "cabinets"), ("bread", "bread"), ("luggage", "luggage"), ("cup", "cups"), ("sand", "sand"), 
        ("peanut butter"), ("peanut butter"), ("hot dogs", "croissant"), ("zucchini", "meat"), ("pepper", "meat"), 
        ("bun", "sausage"), ("pepperoni", "pepperoni"), ("utensil", "meat"), ("orange", "meat"), ("hamburger", "meat"),
        ("background", "sky"), ("box", "sky"), ("bridge", "sky"), ("number", "sky"), ("propeller", "sky"), 
        ("seeds", "sky"), ("steam", "sky"), ("smoke", "sky"), ("crane", "sky"), ("leaf", "sky"), ("sign", "sky"), 
        ("cross", "sky"), ("wing", "sky"), ("mountains", "sky"), ("cables", "sky"), ("mountain", "sky"), 
        ("clock", "sky"), ("stick", "mud"), ("cap", "river"), ("sign", "shop"), ("bubbles", "ocean"), 
        ("bubble", "ocean"), ("bubbles", "sink"), ("bubbles", "river"), ("bubbles", "bathroom"), ("bubble", "pan"), 
        ("land", "ocean"), ("woman", "ladle"), ("lid", "pan"), ("price tag", "pan"), ("cake", "pans"), 
        ("pie", "pans"), ("pot", "pans"), ("basket", "pot"), ("bottle", "pot"), ("bowl", "pot"), ("brush", "pot"), 
        ("container", "pot"), ("mixer", "pot"), ("plates", "pot"), ("tool", "pot"), ("nut", "brownies"), 
        ("vanilla", "ice cream"), ("fruit", "cake"), ("glass", "dessert"), ("dip", "cake"), ("camera", "cake"), 
        ("candle", "cakes"), ("cookies", "cupcake"), ("cake", "cupcake"), ("cat", "cake"), ("dog", "cake"), 
        ("people", "cake"), ("cake slice", "cake"), ("woman", "cake"), ("cookies", "cupcakes"), ("beer", "drink"), 
        ("beer", "beverage"), ("liquid", "drink"), ("cream", "drink"), ("cappuccino", "coffee"), ("glass", "wine"), 
        ("wine", "drink"), ("cup", "coffee"), ("napkin", "coffee"), ("motorcycle", "bed"), ("wall", "bed"), 
        ("wall", "entertainment center"), ("cap", "bottle"), ("cup", "bottle"), ("milk", "cereal"), 
        ("candle", "chocolate"), ("mound", "food"), ("hot dog", "food"), ("drape", "window"), ("glass", "window"), 
        ("drapes", "window"), ("blind", "window"), ("blinds", "window"), ("curtain", "window"), 
        ("curtains", "window"), ("man", "cooker"), ("bowl", "stove"), ("clouds", "mountains"), 
        ("clock", "alarm clock"), ("man", "backpacks"), ("boy", "suitcase"), ("girl", "suitcase"), 
        ("workers", "bucket"), ("woman", "suitcase"), ("land", "water"), ("sail", "water"), 
        ("sign", "water"), ("deck", "water"), ("lighthouse", "water"), ("pillars", "water"), 
        ("beach", "water"), ("platform", "water"), ("stairs", "water"), ("stick", "water"), ("log", "water"), 
        ("trunk", "water"), ("post", "water"), ("bone", "water"), ("ocean", "water"), ("island", "water"), 
        ("mountain", "water"), ("waterfall", "water"), ("mud", "water"), ("stump", "water"), ("forest", "water"), 
        ("sticks", "water"), ("pole", "water"), ("ice", "water"), ("sidewalk", "street"),
        ("grass", "water"), ("weeds", "field"), ("grass", "forest"), ("plants", "water"), ("grass", "pond"), 
        ("plants", "forest"), ("plants", "yard"), ("grass", "backyard"), ("bush", "backyard"), ("grass", "basket"), 
        ("grass", "garden"), ("weeds", "snow"), ("bushes", "yard"), ("bush", "forest"), ("hay", "field"),
        ("pond", "field"), ("bleachers", "stadium"), ("pond", "park"), ("pond", "zoo"), ("house", "field"), 
        ("barn", "field"), ("clock tower", "park"), ("building", "forest"), ("container", "glass"), 
        ("trunks", "background"), ("coat", "snow"), ("clothes", "sand"), ("wetsuit", "ocean"), 
        ("blinds", "windows"), ("pizza", "background"), ("food", "shop"), ("food", "restaurant"), 
        ("sign", "background"), ("glass", "cabinet"), ("crane", "background"), ("bridge", "water"), 
        ("countertop", "kitchen"), ("stump", "sand"), ("outlet", "kitchen"), ("countertop", "bathroom"), 
        ("bowl", "bathroom"), ("crane", "water"), ("umbrella", "crowd"), ("vines", "field"), ("plants", "field"), 
        ("plant", "field"), ("weed", "field"), ("weeds", "forest"), ("plant", "forest"), ("bushes", "forest"), 
        ("weed", "garden"), ("weeds", "garden"), ("plant", "garden"), ("bush", "garden"), ("plants", "garden"), 
        ("plants", "lake"), ("grass", "lawn"), ("weeds", "mud"), ("grass", "mud"), ("grass", "ocean"), 
        ("weeds", "ocean"), ("flowers", "paper"), ("bush", "park"), ("grass", "park"), ("bushes", "park"), 
        ("bush", "parking lot"), ("plant", "plain"), ("grass", "plain"), ("bush", "pond"), ("plant", "pond"), 
        ("grass", "river"), ("plant", "river"), ("weeds", "river"), ("bush", "river"), ("grass", "sky"), 
        ("plants", "snow"), ("plant", "snow"), ("weeds", "steps"), ("bushes", "train"), ("bushes", "water"), 
        ("weed", "water"), ("bush", "water"), ("grass", "weeds"), ("flowers", "weeds"), ("weeds", "yard"), 
        ("plant", "zoo"), ("ski", "snow"), ("seat", "bleachers"), ("seat", "car"), ("leaf", "water"),  
        ("seat", "bathroom"), ("seat", "boat"), ("seat", "bus"), ("seat", "auditorium"), ("bubble", "water"), 
        ("log", "field"), ("fence", "yard"), ("ski", "water"), ("snow", "sky"), ("stick", "bathroom"), 
        ("seat", "vehicle"), ("leaves", "forest"), ("leaves", "field"), ("stick", "sand"), ("leaves", "pot"), 
        ("leaf", "bowl"), ("leaf", "pot"), ("leaf", "glass"), ("leaf", "pond"), ("leaves", "yard"), 
        ("lid", "bathroom"), ("sticks", "snow"), ("frosting", "cake"), ("leaf", "salad"), ("bubble", "coffee"), 
        ("seed", "field"), ("tree branch", "background"), ("leaf", "soup"), ("seed", "food"), 
        ("leaves", "park"), ("leaves", "snow"), ("leaves", "salad"), ("leaf", "park"), ("sticks", "field"), 
        ("leaves", "bowl"), ("grass", "water"), ("weeds", "field"), ("grass", "forest"), ("plants", "water"), 
        ("grass", "pond"), ("plants", "forest"), ("plants", "yard"), ("grass", "backyard"), ("bush", "backyard"), 
        ("grass", "basket"), ("grass", "garden"), ("weeds", "snow"), ("bushes", "yard"), ("bush", "forest"), 
        ("hay", "field"), ("flag", "sky"), ("tree", "sky"), ("tree", "water"), ("trees", "sky"), ("trees", "water"), 
        ("fence", "field"), ("leaf", "vase"), ("fence", "grass"), ("leaves", "water"), ("seat", "stadium"), 
        ("leaves", "vase"), ("fence", "park"), ("leaf", "snow"), ("stick", "snow"), ("seat", "bleachers"),
        ("seat", "stadium"), ("person", "boats"), ("microwave", "cabinets"), ("fruit", "baskets"), 
        ("toothbrush", "cups"), ("fruit", "boxes"), ("pepper", "mashed potatoes"), ("hot dog", "buns"), 
        ("spoon", "pots"), ("plant", "pots"), ("refrigerator", "cabinets"), ("sink", "cabinets"), 
        ("sheep", "cages"), ("potato", "pots"), ("tomato", "sandwiches"), ("oven", "cabinets"), 
        ("silverware", "plates"), ("trees", "houses"), ("lid", "dish"), ("lid", "cupboard"), 
        ("lid", "bag"), ("tree branch", "water"), ("tree branches", "sky"), ("bubbles", "bathtub"),
        ("seaweed", "sand"), ("stick", "weeds"), ("log", "weeds"), ("man", "glass"), 
        ("cat", "glass"), ("kitten", "glass"), ("tree", "glass"), ("clock", "glass"), ("trees", "glass"), 
        ("glass", "bathroom"), ("snow", "grass"), ("sign", "field"), ("stick", "field"), ("mirror", "car"), 
        ("mirror", "vehicle"), ("mirror", "park"), ("mirror", "window"), ("mirror", "train"), ("mirror", "minivan"),
        ("chair", "stadium"), ("lamb", "hay")]

    blacklistS = ["seat", "leaves", "leaf", "log", "pillars", "stick", "sticks", "bush", "bubble", "fence post", "post", "mound", "screen", "background", 
        "ceiling", "pole", "wall", "garage door", "shower door", "cabinet doors", "cabinet door", "door", "doors", 
        "doorway", "doorways", "tiles", "air", "sky", "floor", "wave", "waves"]
    blacklistO = ["windows", "hill", "table", "mountain side", "wallpaper", "terrain", "wave", "waves", "rain", "mountains", "land", "town", "shore", 
        "mountain", "hills", "hillside", "hilltop", "entrance", "dock", "display", "city", "room", "flower", "flowers", "bush", "motorcycle", "bike", "candy", 
        "cheese", "chips", "chocolate", "cream cheese", "cream", "dip", "egg", "eggs", 
        "mozzarella", "parmesan cheese", "carpet" ,"ceiling" ,"roof" ,"staircase" ,"stairs" ,"walls", "cutting board", 
        "picnic table", "furniture", "armchair", "desk", "shelf", "shelves", "buildings", "house", "apartment", 
        "utensil", "wig", "door", "doors", "fence", "glasses", "tower", "tree", "trees", "wall", "floor", 
        "building", "herd", "ground", "cap", "post", "fence post", "sign post"] 
    blacklistScat = ["place", "nature environment", "urban environment", "meal", "road", "vehicle part", "part", "room", "label", "body part"]
    blacklistOcat = ["road", "office supplies", "animal", "person", "sauce", "textile", "fast food", "device", 
    "meal", "part", "footwear", "vehicle part", "label", "ingredient", "accessory", "clothing", "body part", "utensil"]
    chairs = ["office chair", "chairs", "couch", "couches", "sofa", "bench", "chair"]
    waterWhitelsit = ["mug", "glass", "vase", "bowl", "bottle", "cup", "jar", "fountain", "sink", "bathtub", "bucket", "container", 
        "glasses", "bottles", "flower pot", "basket", "aquarium"] 
    natural = ["sand", "rock", "rocks", "boulders", "water", "mud", "ice", "stone", "stones", "leaf", "leaves", 
        "tree leaves", "petal", "petals", "branch", "branches", "tree branch", "tree branches", "twig", 
        "twigs", "stick", "sticks", "log", "logs", "stump"]
    naturalR = ["branch", "branches", "twig", "twigs", "stone", "stones", "rock", "rocks", "tile", "hair", "skin", "fur", "wool", "feathers"]
    extraParts = ["door frame", "doorway", "window frame", "touchpad", "horse hoof", "strap", "straps", "hair", "skin", "fur", "wool", "feathers", "seat belt", "cockpit"]
    inclusiveObjs = ["stroller", "pot", "planter", "mirror", "backpack", "bag", "basket", "baskets", "bird cage", "bowl", "briefcase", "bucket", "can", 
        "candle holder", "cart", "crate", "crates", "dish drainer", "dispenser", "dumpster", "flower pot", "grinder", 
        "knife block", "napkin dispenser", "package", "pouch", "salt shaker", "suitcase", "tissue box", "towel dispenser", 
        "tray", "utensil holder", "vase", "vending machine", "wallet", "waste basket", "wheelchair"] 
    airWhitelist = ["phone", "pigeon", "aircraft", "dog", "guy", "airplane", "jet", "man", "apple", "snowboards", 
    "frisbee", "snowboard", "snowboarder", "bike", "birds", "skateboarder", "kite", "skier", "kites", "boy", "ball", 
    "horse", "people", "surfer", "woman", "helicopter", "shoe", "skis", "person", "balloon", "motorcycle", "player", 
    "bird", "baseball", "airplanes", "skateboard"]
    noneWhitelist = ["net", "pen", "air", "aquarium", "audience", "bathtub", "cockpit", "cooler", "crowd", "doorway", "fireplace", "fountain", 
        "glass", "pitcher", "pocket", "pockets", "shower", "sink"]
    thingWhitelist = ["cages", "cage", "ice", "nest", "painting", "napkin", "paper", "sand", "snow", "tent", "water"]

    for (s, o) in whitelist:
        return False
    for (s, o) in blacklist:
        return True
    if s in blacklistS or catn(s) in blacklistScat:
        return True
    if o in blacklistO or catn(o) in blacklistOcat:
        return True
    # if o in ["mirror", "window"]:
    #   return False
    if s in ["window", "windows"]: # and o not in ["bathroom", "kitchen", "bedroom", "living room"]:
        return True
    if o in chairs:
        return True
    if s == "water" and o not in waterWhitelsit:
        return True
    if (catn(s) in ["plant", "tree"] or s in natural) and o in ["grass", "bushes"]:
        return True
    if s in naturalR or o in naturalR:
        return True
    if catn(o) == "symbol" and o not in ["drawing", "drawings"]:
        return True
    if catn(s) == "symbol" and s not in ["drawing", "drawings"]:
        return True     
    if catn(o) == "plant" and o not in ["grass", "bushes", "hay", "weeds"]:
        return True     
    if catn(o) in ["vegetable", "fruit"] and s not in ["seed", "seeds"]:
        return True 
    if catn(o) == "aircraft" and catn(s) != "person":
        return True
    if s in extraParts:
        return True
    if catn(o) == "object" and o not in inclusiveObjs:
        return True
    if catn(o) == "" and o not in noneWhitelist:
        return True 
    if catn(o) == "thing" and o not in thingWhitelist:
        return True             
    if o == "air" and s not in airWhitelist:
        return True
    if catn(s) == "building" and o != "background":
        return True
    return False

def filterInside(s, o):
    whitelist = [  
        ("frisbee", "mouth"), ("hand", "glove"), ("toothbrush", "mouth"),
        ("hair", "sink"), ("card", "pocket"), ("cards", "pocket"), ("cards", "car"), 
        ("receipt", "box"), ("card", "wallet"), ("tire", "water"), ("tire", "suitcase"),
        ("paper", "printer"),  ("cheese", "hot dog"), 
        ("onion", "hot dog"), ("ketchup", "hot dog"),  
        ("baby", "blanket"), ("pig", "blanket"), ("cat", "blanket"), ("knife", "apple"), 
        ("drawer", "desk"), ("drawers", "desk"), ("drawer", "table"), ("drawers", "table"), ("bird", "clouds"), 
        ("airplane", "clouds"), ("kite", "clouds"), ("stick", "bread"), ("sticks", "vase"), ("stick", "pot"), 
        ("stick", "sandwich"), ("stick", "buns"), ("stick", "cake"), ("leaves", "background"), ("leaves", "pond"), 
        ("leaves", "basket"), ("leaves", "living room"), ("leaves", "container"), 
        ("leaves", "bag"), ("leaves", "jar"), ("flower", "bouquet") ] # ("hand", "pocket"),  ("hand", "snow"), ("hands", "pockets"), 
        # ("feet", "sand"), ("feet", "water"), 

    blacklist = [("pot", "flower"), ("faucet", "sink"), ("toilet", "room"), ("furniture", "glass"),
        ("curtains", "window"), ("blind", "window"), ("blinds", "window"), ("sign", "snow"), ("umbrella", "sand"), 
        ("sign", "grass"), ("bag", "can"),("curtain", "window"), ("air conditioner", "window"), ("leaves", "tree"), 
        ("water", "toilet"), ("sign", "window"), ("water", "ocean"), ("cloud", "clouds"), ("sheep", "sheep"), 
        ("airplane", "airplanes"), ("bag", "bags"), ("banana", "bananas"), ("knife", "knives"), ("glass", "glass"), 
        ("fruit", "fruit"), ("building", "buildings"), ("orange", "oranges"), ("car", "cars"), ("person", "people"), 
        ("chicken", "chickens"), ("boat", "boats"), ("mountain", "mountains"), ("elephant", "elephants"), 
        ("cabinet", "cabinets"), ("bread", "bread"), ("luggage", "luggage"), ("cup", "cups"), ("sand", "sand"), 
        ("peanut butter"), ("peanut butter"), ("hot dogs", "croissant"), ("zucchini", "meat"), ("pepper", "meat"), 
        ("bun", "sausage"), ("pepperoni", "pepperoni"), ("utensil", "meat"), ("orange", "meat"), ("hamburger", "meat"),
        ("background", "sky"), ("box", "sky"), ("bridge", "sky"), ("number", "sky"), ("propeller", "sky"), 
        ("seeds", "sky"), ("steam", "sky"), ("smoke", "sky"), ("crane", "sky"), ("leaf", "sky"), ("sign", "sky"), 
        ("cross", "sky"), ("wing", "sky"), ("mountains", "sky"), ("cables", "sky"), ("mountain", "sky"), 
        ("clock", "sky"), ("stick", "mud"), ("cap", "river"), ("sign", "shop"), ("bubbles", "ocean"), 
        ("bubble", "ocean"), ("bubbles", "sink"), ("bubbles", "river"), ("bubbles", "bathroom"), ("bubble", "pan"), 
        ("land", "ocean"), ("woman", "ladle"), ("lid", "pan"), ("price tag", "pan"), ("cake", "pans"), 
        ("pie", "pans"), ("pot", "pans"), ("basket", "pot"), ("bottle", "pot"), ("bowl", "pot"), ("brush", "pot"), 
        ("container", "pot"), ("mixer", "pot"), ("plates", "pot"), ("tool", "pot"), ("nut", "brownies"), 
        ("vanilla", "ice cream"), ("fruit", "cake"), ("glass", "dessert"), ("dip", "cake"), ("camera", "cake"), 
        ("candle", "cakes"), ("cookies", "cupcake"), ("cake", "cupcake"), ("cat", "cake"), ("dog", "cake"), 
        ("people", "cake"), ("cake slice", "cake"), ("woman", "cake"), ("cookies", "cupcakes"), ("beer", "drink"), 
        ("beer", "beverage"), ("liquid", "drink"), ("cream", "drink"), ("cappuccino", "coffee"), ("glass", "wine"), 
        ("wine", "drink"), ("cup", "coffee"), ("napkin", "coffee"), ("motorcycle", "bed"), ("wall", "bed"), 
        ("wall", "entertainment center"), ("cap", "bottle"), ("cup", "bottle"), ("milk", "cereal"), 
        ("candle", "chocolate"), ("mound", "food"), ("hot dog", "food"), ("drape", "window"), ("glass", "window"), 
        ("drapes", "window"), ("blind", "window"), ("blinds", "window"), ("curtain", "window"), 
        ("curtains", "window"), ("man", "cooker"), ("bowl", "stove"), ("clouds", "mountains"), 
        ("clock", "alarm clock"), ("man", "backpacks"), ("boy", "suitcase"), ("girl", "suitcase"), 
        ("workers", "bucket"), ("woman", "suitcase"), ("land", "water"), ("sail", "water"), 
        ("sign", "water"), ("deck", "water"), ("lighthouse", "water"), ("pillars", "water"), 
        ("beach", "water"), ("platform", "water"), ("stairs", "water"), ("stick", "water"), ("log", "water"), 
        ("trunk", "water"), ("post", "water"), ("bone", "water"), ("ocean", "water"), ("island", "water"), 
        ("mountain", "water"), ("waterfall", "water"), ("mud", "water"), ("stump", "water"), ("forest", "water"), 
        ("sticks", "water"), ("pole", "water"), ("ice", "water"), ("sidewalk", "street"),
        ("grass", "water"), ("weeds", "field"), ("grass", "forest"), ("plants", "water"), ("grass", "pond"), 
        ("plants", "forest"), ("plants", "yard"), ("grass", "backyard"), ("bush", "backyard"), ("grass", "basket"), 
        ("grass", "garden"), ("weeds", "snow"), ("bushes", "yard"), ("bush", "forest"), ("hay", "field"),
        ("pond", "field"), ("bleachers", "stadium"), ("pond", "park"), ("pond", "zoo"), ("house", "field"), 
        ("barn", "field"), ("clock tower", "park"), ("building", "forest"), ("container", "glass"), 
        ("trunks", "background"), ("coat", "snow"), ("clothes", "sand"), ("wetsuit", "ocean"), 
        ("blinds", "windows"), ("pizza", "background"), ("food", "shop"), ("food", "restaurant"), 
        ("sign", "background"), ("glass", "cabinet"), ("crane", "background"), ("bridge", "water"), 
        ("countertop", "kitchen"), ("stump", "sand"), ("outlet", "kitchen"), ("countertop", "bathroom"), 
        ("bowl", "bathroom"), ("crane", "water"), ("umbrella", "crowd"), ("vines", "field"), ("plants", "field"), 
        ("plant", "field"), ("weed", "field"), ("weeds", "forest"), ("plant", "forest"), ("bushes", "forest"), 
        ("weed", "garden"), ("weeds", "garden"), ("plant", "garden"), ("bush", "garden"), ("plants", "garden"), 
        ("plants", "lake"), ("grass", "lawn"), ("weeds", "mud"), ("grass", "mud"), ("grass", "ocean"), 
        ("weeds", "ocean"), ("flowers", "paper"), ("bush", "park"), ("grass", "park"), ("bushes", "park"), 
        ("bush", "parking lot"), ("plant", "plain"), ("grass", "plain"), ("bush", "pond"), ("plant", "pond"), 
        ("grass", "river"), ("plant", "river"), ("weeds", "river"), ("bush", "river"), ("grass", "sky"), 
        ("plants", "snow"), ("plant", "snow"), ("weeds", "steps"), ("bushes", "train"), ("bushes", "water"), 
        ("weed", "water"), ("bush", "water"), ("grass", "weeds"), ("flowers", "weeds"), ("weeds", "yard"), 
        ("plant", "zoo"), ("ski", "snow"), ("seat", "bleachers"), ("leaf", "water"),  
        ("seat", "bathroom"), ("seat", "boat"),  ("seat", "auditorium"), ("bubble", "water"), 
        ("log", "field"), ("fence", "yard"), ("ski", "water"), ("snow", "sky"), ("stick", "bathroom"), 
        ("leaves", "forest"), ("leaves", "field"), ("stick", "sand"), ("leaves", "pot"), 
        ("leaf", "bowl"), ("leaf", "pot"), ("leaf", "glass"), ("leaf", "pond"), ("leaves", "yard"), 
        ("lid", "bathroom"), ("sticks", "snow"), ("frosting", "cake"), ("leaf", "salad"), ("bubble", "coffee"), 
        ("seed", "field"), ("tree branch", "background"), ("leaf", "soup"), ("seed", "food"), 
        ("leaves", "park"), ("leaves", "snow"), ("leaves", "salad"), ("leaf", "park"), ("sticks", "field"), 
        ("leaves", "bowl"), ("grass", "water"), ("weeds", "field"), ("grass", "forest"), ("plants", "water"), 
        ("grass", "pond"), ("plants", "forest"), ("plants", "yard"), ("grass", "backyard"), ("bush", "backyard"), 
        ("grass", "basket"), ("grass", "garden"), ("weeds", "snow"), ("bushes", "yard"), ("bush", "forest"), 
        ("hay", "field"), ("flag", "sky"), ("tree", "sky"), ("tree", "water"), ("trees", "sky"), ("trees", "water"), 
        ("fence", "field"), ("leaf", "vase"), ("fence", "grass"), ("leaves", "water"), ("seat", "stadium"), 
        ("leaves", "vase"), ("fence", "park"), ("leaf", "snow"), ("stick", "snow"), ("seat", "bleachers"),
        ("seat", "stadium"), ("person", "boats"), ("microwave", "cabinets"), ("fruit", "baskets"), 
        ("toothbrush", "cups"), ("fruit", "boxes"), ("pepper", "mashed potatoes"), ("hot dog", "buns"), 
        ("spoon", "pots"), ("plant", "pots"), ("refrigerator", "cabinets"), ("sink", "cabinets"), 
        ("sheep", "cages"), ("potato", "pots"), ("tomato", "sandwiches"), ("oven", "cabinets"), 
        ("silverware", "plates"), ("trees", "houses"), ("lid", "dish"), ("lid", "cupboard"), 
        ("lid", "bag"), ("tree branch", "water"), ("tree branches", "sky"), ("bubbles", "bathtub"),
        ("seaweed", "sand"), ("stick", "weeds"), ("log", "weeds"), ("man", "glass"),  
        ("cat", "glass"), ("kitten", "glass"), ("tree", "glass"), ("clock", "glass"), ("trees", "glass"), 
        ("glass", "bathroom"), ("snow", "grass"), ("sign", "field"), ("stick", "field"), ("mirror", "car"), 
        ("mirror", "vehicle"), ("mirror", "park"), ("mirror", "window"), ("mirror", "train"), ("mirror", "minivan"),
        ("chair", "stadium"), ("lamb", "hay")]

    blacklistS = ["sky", "leaves", "leaf", "log", "pillars", "stick", "sticks", "bush", "bubble", "fence post", "post", "mound", "screen", 
        "background", "ceiling", "pole", "wall", "garage door", "shower door", "cabinet doors", "cabinet door", "door", "doors", 
        "doorway", "doorways", "tiles", "air", "sky", "floor", "wave", "waves"]
    blacklistO = ["mirror", "window", "crowd", "cake", "tray", "sky", "beach", "cemetery", "city", "coast", "desert", "field", "garden", "dock", "harbor", 
        "marina", "hill", "hills", "hillside", "hilltop", "lawn", "shore line", "parking lot", "mountain", "mountain peak", "plain", "shore", "mountain side", 
        "stage", "street", "town", "village", "rooftop", "meadow", 
        "windows", "hill", "table", "mountain side", "wallpaper", "terrain", "wave", "waves", "rain", "mountains", "land", "town", "shore", "mountain", 
        "hills", "hillside", "hilltop", "entrance", "dock", "display", "city", "room", "flower", "flowers", "bush", "motorcycle", "bike", "candy", 
        "cheese", "chips", "chocolate", "cream cheese", "cream", "dip", "egg", "eggs", 
        "mozzarella", "parmesan cheese", "carpet" ,"ceiling" ,"roof" ,"staircase" ,"stairs" ,"walls", "cutting board", 
        "picnic table", "furniture", "armchair", "desk", "shelf", "shelves", "buildings",  "apartment", 
        "utensil", "wig", "door", "doors", "glasses", "tower", "tree", "trees", "wall", "floor", 
        "herd", "ground", "cap", "post", "fence post", "sign post"] 
    blacklistScat = ["place", "nature environment", "urban environment", "meal", "road", "vehicle part", "part", "room", "label", "body part"]
    blacklistOcat = ["road", "office supplies", "animal", "person", "sauce", "textile", "fast food", "device", 
    "meal", "part", "footwear", "vehicle part", "label", "ingredient", "accessory", "clothing", "body part", "utensil"]
    chairs = ["office chair", "chairs", "couch", "couches", "sofa", "bench", "chair"]
    waterWhitelsit = ["mug", "glass", "vase", "bowl", "bottle", "cup", "jar", "fountain", "sink", "bathtub", "bucket", "container", 
        "glasses", "bottles", "flower pot", "basket", "aquarium"] 
    natural = ["sand", "rock", "rocks", "boulders", "water", "mud", "ice", "stone", "stones", "leaf", "leaves", 
        "tree leaves", "petal", "petals", "branch", "branches", "tree branch", "tree branches", "twig", 
        "twigs", "stick", "sticks", "log", "logs", "stump"]
    naturalR = ["branch", "branches", "twig", "twigs", "stone", "stones", "rock", "rocks", "tile", "hair", "skin", "fur", "wool", "feathers"]
    extraParts = ["door frame", "doorway", "window frame", "touchpad", "horse hoof", "strap", "straps", "hair", "skin", "fur", "wool", "feathers", "seat belt", "cockpit"]
    inclusiveObjs = ["lamp", "stroller", "pot", "planter", "mirror", "backpack", "bag", "basket", "baskets", "bird cage", "bowl", "briefcase", "bucket", "can", 
        "candle holder", "cart", "crate", "crates", "dish drainer", "dispenser", "dumpster", "flower pot", "grinder", 
        "knife block", "napkin dispenser", "package", "pouch", "salt shaker", "suitcase", "tissue box", "towel dispenser", 
        "tray", "utensil holder", "vase", "vending machine", "wallet", "waste basket", "wheelchair"] 
    # airWhitelist = ["phone", "pigeon", "aircraft", "dog", "guy", "airplane", "jet", "man", "apple", "snowboards", 
    # "frisbee", "snowboard", "snowboarder", "bike", "birds", "skateboarder", "kite", "skier", "kites", "boy", "ball", 
    # "horse", "people", "surfer", "woman", "helicopter", "shoe", "skis", "person", "balloon", "motorcycle", "player", 
    # "bird", "baseball", "airplanes", "skateboard"]
    noneWhitelist = ["net", "pen", "aquarium", "audience", "bathtub", "cockpit", "cooler", "crowd", "doorway", "fireplace", "fountain", 
        "glass", "pitcher", "pocket", "pockets", "shower", "sink"]
    thingWhitelist = ["fence", "cages", "cage", "ice", "nest", "painting", "napkin", "paper", "sand", "snow", "tent", "water"]

    for (s, o) in whitelist:
        return False
    for (s, o) in blacklist:
        return True
    if s in blacklistS or catn(s) in blacklistScat:
        return True
    if o in blacklistO or catn(o) in blacklistOcat and o not in ["shoe"]:
        return True
    # if o in ["mirror", "window"]:
    #   return False
    if s in ["window", "windows"]: # and o not in ["bathroom", "kitchen", "bedroom", "living room"]:
        return True
    if o in chairs:
        return True
    if s == "water" and o not in waterWhitelsit:
        return True
    if (catn(s) in ["plant", "tree"] or s in natural) and o in ["grass", "bushes"]:
        return True
    if s in naturalR or o in naturalR:
        return True
    if catn(o) == "symbol" and o not in ["drawing", "drawings"]:
        return True
    if catn(s) == "symbol" and s not in ["drawing", "drawings"]:
        return True     
    if catn(o) == "plant" and o not in ["grass", "bushes", "hay", "weeds"]:
        return True     
    if catn(o) in ["vegetable", "fruit"] and s not in ["seed", "seeds"]:
        return True 
    if catn(o) == "aircraft" and catn(s) != "person":
        return True
    if s in extraParts:
        return True
    if catn(o) == "object" and o not in inclusiveObjs:
        return True
    if catn(o) == "" and o not in noneWhitelist:
        return True 
    if catn(o) == "thing" and o not in thingWhitelist:
        return True             
    # if o == "air" and s not in airWhitelist:
    #     return True
    if catn(s) == "building" and o != "background":
        return True
    return False

def filterWith(s, o):
    whitelist = [("man", "beard"), ("man", "hat"), ("man", "glasses"), ("plate", "food"), ("vase", "flowers"), 
    ("man", "backpack"), ("woman", "umbrella"), ("donut", "sprinkles"), ("glass", "wine"), ("woman", "bag"), 
    ("man", "jacket"), ("man", "racket"), ("man", "camera"), ("man", "surfboard"), ("bottle", "label"), 
    ("man", "sunglasses"), ("man", "bag"), ("pizza", "cheese"), ("man", "umbrella"), ("man", "cap"), 
    ("tower", "clock"), ("building", "clock"), ("donut", "frosting"), ("man", "frisbee"), ("woman", "glasses"), 
    ("dog", "frisbee"), ("man", "tie"), ("man", "dog"), ("vase", "flower"), ("window", "blinds"), 
    ("man", "mustache"), ("person", "umbrella"), ("kite", "tail"), ("man", "skateboard"), ("man", "helmet"), 
    ("glass", "water"), ("woman", "purse"), ("woman", "sunglasses"), ("cake", "frosting"), ("man", "jeans"), 
    ("man", "shorts"), ("boy", "skateboard"), ("person", "jacket"), ("woman", "dog"), ("table", "food"), 
    ("pizza", "pepperoni"), ("woman", "racket"), ("man", "coat"), ("dog", "collar"), ("hot dog", "mustard"), 
    ("window", "curtains"), ("bowl", "food"), ("plate", "pizza"), ("man", "eyeglasses"), ("man", "snowboard"), 
    ("man", "luggage"), ("boy", "frisbee"), ("player", "bat"), ("man", "phone"), ("person", "helmet"), 
    ("bush", "flowers"), ("woman", "hat"), ("hot dog", "ketchup"), ("man", "kite"), ("man", "laptop"), 
    ("girl", "umbrella"), ("window", "curtain"), ("couch", "pillow"), ("person", "backpack"), ("cake", "icing"), 
    ("person", "surfboard"), ("donut", "icing"), ("woman", "scarf"), ("person", "hat"), ("man", "horse"), 
    ("boy", "bat"), ("plate", "sandwich"), ("people", "umbrellas"), ("bed", "pillow"), ("man", "skis"), 
    ("man", "bat"), ("woman", "phone"), ("woman", "jacket"), ("girl", "glasses"), ("person", "bag"), 
    ("plate", "cake"), ("soda", "ice"), ("girl", "racket"), ("glass", "beer"), ("pizza", "sauce"), 
    ("table", "tablecloth"), ("player", "racket"), ("couch", "pillows"), ("suitcase", "tag"), 
    ("surfer", "surfboard"), ("shirt", "collar"), ("woman", "camera"), ("boy", "shorts"), ("sandwich", "meat"), 
    ("woman", "eyeglasses"), ("woman", "child"), ("woman", "coat"), ("person", "kite"), ("plant", "flowers"), 
    ("man", "bike"), ("man", "suit"), ("tree", "flowers"), ("girl", "phone"), ("shelf", "books"), ("tray", "food"), 
    ("man", "glove"), ("boy", "hat"), ("pole", "flag"), ("man", "controller"), ("woman", "dress"), 
    ("girl", "helmet"), ("person", "coat"), ("person", "dog"), ("chair", "pillow"), ("guy", "beard"), 
    ("bowl", "soup"), ("bowl", "sauce"), ("man", "ball"), ("man", "boy"), ("man", "elephant"), ("boy", "racket"), 
    ("boy", "cap"), ("lady", "eyeglasses"), ("lady", "umbrella"), ("cake", "candle"), ("box", "donut"), 
    ("girl", "bag"), ("glass", "juice"), ("player", "glove"), ("sandwich", "lettuce"), ("cupcake", "icing"), 
    ("man", "stick"), ("woman", "baby"), ("woman", "backpack"), ("building", "balcony"), ("girl", "jacket"), 
    ("girl", "hat"), ("person", "glasses"), ("person", "camera"), ("lady", "bag"), ("pizza", "olives"), 
    ("cake", "sprinkles"), ("flower", "leaves"), ("man", "cat"), ("woman", "suitcase"), ("girl", "headband"), 
    ("pizza", "basil"), ("pizza", "vegetables"), ("bowl", "broccoli"), ("animal", "horn"), ("woman", "luggage"), 
    ("plate", "donut"), ("bowl", "spoon"), ("bike", "basket"), ("hill", "trees"), ("man", "scarf"), 
    ("man", "goggles"), ("man", "suitcase"), ("man", "vest"), ("girl", "sunglasses"), ("boy", "helmet"), 
    ("person", "laptop"), ("donut", "chocolate"), ("glass", "beverage"), ("dog", "toy"), ("mountain", "trees"), 
    ("man", "mask"), ("man", "gloves"), ("man", "motorcycle"), ("woman", "boy"), ("boy", "ball"), 
    ("plate", "bread"), ("donut", "glaze"), ("glass", "ice"), ("window", "blind"), ("cup", "handle"), 
    ("sandwich", "cheese"), ("cow", "tag"), ("sofa", "pillow"), ("camera", "strap"), ("bun", "hot dog"), 
    ("man", "watch"), ("person", "skateboard"), ("plate", "salad"), ("pizza", "mushrooms"), ("pizza", "ham"), 
    ("table", "laptop"), ("cake", "candles"), ("cat", "collar"), ("shelf", "animals"), ("boat", "people"), 
    ("cupcake", "frosting"), ("donuts", "sprinkles"), ("man", "child"), ("man", "cell phone"), 
    ("woman", "surfboard"), ("boy", "glasses"), ("boy", "backpack"), ("plate", "hot dog"), ("plate", "fries"), 
    ("lady", "purse"), ("pizza", "onion"), ("guy", "hat"), ("container", "food"), ("bowl", "fruit"), 
    ("cabinet", "drawer"), ("man", "sweater"), ("man", "socks"), ("woman", "sweater"), ("woman", "helmet"), 
    ("woman", "necklace"), ("girl", "purse"), ("pole", "clock"), ("person", "shorts"), ("person", "goggles"), 
    ("person", "horse"), ("plate", "fruit"), ("pot", "flowers"), ("donut", "candies"), ("pizza", "onions"), 
    ("pizza", "peppers"), ("table", "lamp"), ("table", "bowl"), ("player", "helmet"), ("field", "sheep"), 
    ("tray", "donut"), ("meat", "broccoli"), ("man", "bird"), ("man", "fork"), ("man", "bandana"), 
    ("man", "guitar"), ("man", "knife"), ("man", "wetsuit"), ("woman", "vest"), ("woman", "frisbee"), 
    ("woman", "cell phone"), ("building", "dome"), ("girl", "kite"), ("boy", "dog"), ("pole", "bird"), 
    ("person", "cap"), ("person", "bike"), ("person", "racket"), ("plate", "broccoli"), ("lady", "jacket"), 
    ("lady", "glasses"), ("bottle", "flower"), ("house", "chimney"), ("chair", "wheels"), ("table", "drawer"), 
    ("guy", "surfboard"), ("hot dog", "cheese"), ("field", "zebra"), ("bed", "headboard"), ("boat", "person"), 
    ("animal", "horns"), ("donuts", "frosting"), ("man", "donut"), ("man", "ring"), ("man", "microphone"), 
    ("woman", "handbag"), ("boy", "sunglasses"), ("boy", "eyeglasses"), ("person", "sweater"), ("plate", "dessert"), 
    ("plate", "waffle"), ("plate", "meat"), ("pizza", "tomatoes"), ("dog", "scarf"), ("table", "cake"), 
    ("guy", "backpack"), ("guy", "glasses"), ("horse", "carriage"), ("cake", "decoration"), ("cup", "beverage"), 
    ("field", "rocks"), ("field", "cows"), ("cabinet", "doors"), ("bear", "hat"), ("tray", "vegetables"), 
    ("box", "pizza"), ("box", "label"), ("hat", "flower"), ("basket", "bread"), ("man", "apron"), ("man", "banana"), 
    ("man", "glass"), ("man", "cup"), ("woman", "glass"), ("woman", "boots"), ("woman", "banana"), ("woman", "horse"), 
    ("woman", "cow"), ("tree", "ornament"), ("building", "chimney"), ("girl", "coat"), ("girl", "scarf"), 
    ("boy", "phone"), ("person", "sunglasses"), ("person", "skis"), ("plate", "donuts"), ("plate", "vegetables"), 
    ("pot", "flower"), ("vase", "water"), ("donut", "sugar"), ("pizza", "meat"), ("pizza", "broccoli"), 
    ("tower", "window"), ("child", "bat"), ("chair", "towel"), ("bowl", "water"), ("bowl", "salad"), 
    ("bowl", "apple"), ("bowl", "liquid"), ("player", "cap"), ("cup", "pens"), ("cup", "water"), 
    ("cup", "toothbrush"), ("bed", "pillows"), ("shirt", "pocket"), ("sandwich", "onion"), ("pillow", "flower"), 
    ("tablecloth", "flower"), ("shelves", "books"), ("chicken", "sauce"), ("man", "sandwich"), ("man", "boots"), 
    ("man", "sheep"), ("man", "headband"), ("woman", "sheep"), ("woman", "blanket"), ("woman", "parrot"), 
    ("woman", "bracelet"), ("woman", "apron"), ("girl", "sweater"), ("girl", "cat"), ("girl", "flower"), 
    ("girl", "frisbee"), ("girl", "dress"), ("girl", "necklace"), ("boy", "jacket"), ("person", "jeans"), 
    ("person", "motorcycle"), ("plate", "pastry"), ("plate", "eggs"), ("plate", "meal"), ("plate", "sauce"), 
    ("plate", "banana"), ("lady", "dog"), ("lady", "coat"), ("lady", "bottle"), ("lady", "hat"), 
    ("pizza", "spinach"), ("tower", "windows"), ("child", "helmet"), ("dog", "ball"), ("table", "book"), 
    ("guy", "luggage"), ("guy", "jacket"), ("container", "utensils"), ("cake", "flower"), ("cake", "animals"), 
    ("hot dog", "onions"), ("bowl", "pasta"), ("fence", "flag"), ("player", "headband"), ("bear", "heart"), 
    ("sandwich", "tomato"), ("jar", "flower"), ("box", "vegetable"), ("box", "lid"), ("box", "vegetables"), 
    ("cupcake", "sprinkles"), ("bench", "snow"), ("car", "snow"), ("cart", "hay"), ("meat", "sauce"), 
    ("truck", "ladder"), ("jacket", "zipper"), ("bread", "bacon"), ("bread", "meat"), ("policeman", "helmet"), 
    ("man", "uniform"), ("man", "paddle"), ("man", "rope"), ("man", "computer"), ("man", "cow"), 
    ("man", "bottle"), ("woman", "kite"), ("woman", "raincoat"), ("woman", "cat"), ("woman", "shorts"), 
    ("woman", "cap"), ("tree", "decorations"), ("girl", "bracelets"), ("girl", "cell phone"), ("girl", "skirt"), 
    ("girl", "shorts"), ("girl", "backpack"), ("girl", "glove"), ("girl", "bandana"), ("girl", "jeans"), 
    ("girl", "cup"), ("boy", "glove"), ("boy", "beer"), ("boy", "jeans"), ("person", "gloves"), 
    ("plate", "potato"), ("plate", "star"), ("plate", "crumbs"), ("pot", "vegetables"), ("lady", "horse"), 
    ("lady", "sunglasses"), ("lady", "cap"), ("pizza", "pineapple"), ("pizza", "sausage"), ("pizza", "pepper"), 
    ("dog", "stick"), ("door", "mirror"), ("window", "flowers"), ("window", "balcony"), ("guy", "dog"), 
    ("guy", "eyeglasses"), ("guy", "camera"), ("guy", "earring"), ("container", "meal"), ("elephant", "chain"), 
    ("cat", "tag"), ("bowl", "blueberry"), ("fence", "gate"), ("player", "ball"), ("player", "shorts"), 
    ("field", "giraffes"), ("field", "trees"), ("suitcase", "strap"), ("bear", "tag"), ("bear", "shirt"), 
    ("sandwich", "vegetables"), ("shelf", "napkins"), ("shelf", "donut"), ("boat", "roof"), ("box", "donuts"), 
    ("cupcake", "heart"), ("bag", "straps"), ("luggage", "tag"), ("animal", "fur"), ("animal", "mane"), 
    ("pan", "pizza"), ("basket", "biscuit"), ("basket", "flowers"), ("pillow", "flowers"), ("necklace", "flower"), 
    ("backpack", "star"), ("cone", "ice cream"), ("balcony", "fence"), ("curtain", "flowers"), ("roof", "chimney"), 
    ("wallpaper", "flower"), ("mother", "child"), ("mother", "baby"), ("dress", "flowers"), ("bandana", "star"), 
    ("bagel", "blueberry"), ("salad", "dressing"), ("passenger", "backpack"), ("pasta", "sauce"), ("man", "cigar"), 
    ("man", "football"), ("man", "cane"), ("man", "briefcase"), ("man", "cigarette"), ("man", "headphones"), 
    ("man", "toothbrush"), ("man", "book"), ("woman", "controller"), ("woman", "ball"), ("woman", "bike"), 
    ("woman", "gloves"), ("woman", "jeans"), ("woman", "headband"), ("tree", "ornaments"), ("building", "antenna"), 
    ("girl", "goggles"), ("girl", "scissors"), ("girl", "gloves"), ("girl", "surfboard"), ("girl", "dog"), 
    ("boy", "bag"), ("boy", "toothbrush"), ("boy", "kite"), ("boy", "coat"), ("boy", "umbrella"), 
    ("boy", "surfboard"), ("boy", "controller"), ("person", "vest"), ("person", "tie"), ("person", "frisbee"), 
    ("person", "mask"), ("person", "purse"), ("person", "dress"), ("person", "flag"), ("person", "boots"), 
    ("person", "phone"), ("person", "watch"), ("person", "luggage"), ("plate", "potatoes"), ("plate", "flower"), 
    ("plate", "chicken"), ("donut", "powder"), ("donut", "coconut"), ("glass", "ice cubes"), ("glass", "candle"), 
    ("lady", "backpack"), ("lady", "scarf"), ("lady", "jeans"), ("pizza", "herbs"), ("pizza", "bacon"), 
    ("tower", "clocks"), ("child", "coat"), ("child", "umbrella"), ("dog", "shoe"), ("door", "curtain"), 
    ("window", "drapes"), ("window", "bell"), ("table", "bottles"), ("table", "vegetables"), ("guy", "watch"), 
    ("guy", "cap"), ("guy", "bag"), ("guy", "skateboard"), ("container", "salad"), ("container", "hot dog"), 
    ("cake", "strawberries"), ("hot dog", "onion"), ("hot dog", "chili"), ("bowl", "shrimp"), ("bowl", "bread"), 
    ("bowl", "cheese"), ("bowl", "fruits"), ("bowl", "vegetables"), ("bowl", "beans"), ("bowl", "strawberry"), 
    ("bowl", "strawberries"), ("player", "hat"), ("water", "lemon"), ("bed", "dog"), ("bed", "backpack"), 
    ("bear", "tie"), ("bear", "cap"), ("sandwich", "ham"), ("sandwich", "sauce"), ("baby", "toothbrush"), 
    ("tray", "pizza"), ("box", "cake"), ("cupcake", "toppings"), ("dish", "broccoli"), ("hill", "bushes"), 
    ("cart", "luggage"), ("sofa", "pillows"), ("bun", "lettuce"), ("donuts", "icing"), ("pan", "food"), 
    ("pan", "lid"), ("hat", "flowers"), ("basket", "bananas"), ("basket", "fruit"), ("basket", "lid"), 
    ("jeans", "pocket"), ("chicken", "broccoli"), ("pasta", "cheese"), ("waffle", "butter"), ("flag", "star"), 
    ("pancakes", "syrup"), ("pastry", "blueberry"), ("cupcakes", "frosting"), ("pots", "flowers"), 
    ("tea", "spoon"), ("monkey", "banana"), ("man", "pen"), ("man", "cart"), ("man", "name tag"), ("woman", "flower")]
    for (s,o) in whitelist:
            return False
    return True

def filterHave(s, o):
    whitelist = [("door", "window"), ("wall", "window"), ("bear", "shirt"), ("animal", "shirt"), ("alien", "shirt"), 
        ("door", "windows"), ("wall", "windows"), ("man", "beard"), ("guy", "beard"), ("person", "beard"), 
        ("player", "beard"), ("boy", "beard"), ("father", "beard"), ("man", "hat"), ("person", "hat"), ("woman", "hat"), 
        ("boy", "hat"), ("girl", "hat"), ("bear", "hat"), ("child", "hat"), ("player", "hat"), ("dog", "hat"), 
        ("people", "hat"), ("cat", "hat"), ("spectator", "hat"), ("guy", "hat"), ("statue", "hat"), ("skateboarder", "hat"), 
        ("lady", "hat"), ("baby", "hat"), ("toy", "hat"), ("cowboy", "hat"), ("man", "glasses"), ("woman", "glasses"), 
        ("person", "glasses"), ("girl", "glasses"), ("lady", "glasses"), ("boy", "glasses"), ("child", "glasses"), 
        ("guy", "glasses"), ("dog", "glasses"), ("bear", "glasses"), ("statue", "glasses"), ("chair", "wheels"), 
        ("bag", "wheels"), ("table", "wheels"), ("horse", "wheels"), ("bear", "shoe"), ("cat", "shoe"), 
        ("shirt", "collar"), ("dog", "collar"), ("cat", "collar"), ("cow", "collar"), ("sheep", "collar"), 
        ("elephant", "collar"), ("poodle", "collar"), ("lamb", "collar"), ("horse", "collar"), ("man", "jacket"), 
        ("person", "jacket"), ("woman", "jacket"), ("girl", "jacket"), ("boy", "jacket"), ("child", "jacket"), 
        ("guy", "jacket"), ("lady", "jacket"), ("women", "jacket"), ("bear", "jacket"), ("tower", "clock"), 
        ("building", "clock"), ("pole", "clock"), ("man", "clock"), ("cup", "lid"), ("box", "lid"), ("bowl", "lid"), 
        ("sign", "arrow"), ("man", "shorts"), ("boy", "shorts"), ("person", "shorts"), ("woman", "shorts"), 
        ("girl", "shorts"), ("player", "shorts"), ("child", "shorts"), ("guy", "shorts"), ("skateboarder", "shorts"), 
        ("lady", "shorts"), ("skater", "shorts"), ("man", "helmet"), ("player", "helmet"), ("person", "helmet"), 
        ("boy", "helmet"), ("woman", "helmet"), ("child", "helmet"), ("girl", "helmet"), ("policeman", "helmet"), 
        ("biker", "helmet"), ("guy", "helmet"), ("skater", "helmet"), ("lady", "helmet"), ("sign", "number"), 
        ("pizza", "cheese"), ("hot dog", "cheese"), ("sandwich", "cheese"), ("plate", "cheese"), ("food", "cheese"), 
        ("bread", "cheese"), ("bowl", "cheese"), ("fries", "cheese"), ("man", "mustache"), ("guy", "mustache"), 
        ("plate", "food"), ("bowl", "food"), ("table", "food"), ("tray", "food"), ("container", "food"), ("jar", "food"), 
        ("pot", "food"), ("basket", "food"), ("box", "food"), ("pan", "food"), ("skillet", "food"), 
        ("hill", "grass"), ("mountain", "grass"), ("pole", "sign"), ("building", "sign"), ("window", "sign"), 
        ("door", "sign"), ("fence", "sign"), ("glass", "wine"), ("bottle", "wine"), ("cup", "wine"), ("shelf", "wine"), 
        ("man", "tie"), ("bear", "tie"), ("person", "tie"), ("boy", "tie"), ("guy", "tie"), ("girl", "tie"), 
        ("man", "cap"), ("boy", "cap"), ("person", "cap"), ("player", "cap"), ("woman", "cap"), ("skier", "cap"), 
        ("girl", "cap"), ("guy", "cap"), ("child", "cap"), ("man", "sunglasses"), ("woman", "sunglasses"), 
        ("person", "sunglasses"), ("lady", "sunglasses"), ("girl", "sunglasses"), ("guy", "sunglasses"), 
        ("dog", "sunglasses"), ("skater", "sunglasses"), ("building", "balcony"), ("house", "balcony"), 
        ("window", "balcony"), ("man", "backpack"), ("person", "backpack"), ("woman", "backpack"), ("boy", "backpack"), 
        ("skier", "backpack"), ("girl", "backpack"), ("lady", "backpack"), ("child", "backpack"), ("guy", "backpack"), 
        ("man", "watch"), ("woman", "watch"), ("person", "watch"), ("boy", "watch"), ("lady", "watch"), ("girl", "watch"), 
        ("bottle", "label"), ("wine", "label"), ("jar", "label"), ("man", "jeans"), ("boy", "jeans"), ("person", "jeans"), 
        ("woman", "jeans"), ("girl", "jeans"), ("lady", "jeans"), ("child", "jeans"), ("skateboarder", "jeans"), 
        ("guy", "jeans"), ("skater", "jeans"), ("bear", "jeans"), ("pizza", "pepperoni"), ("woman", "bag"), ("man", "bag"), 
        ("person", "bag"), ("girl", "bag"), ("lady", "bag"), ("guy", "bag"), ("boy", "bag"), ("woman", "purse"), 
        ("girl", "purse"), ("person", "purse"), ("lady", "purse"), ("man", "glove"), ("player", "glove"), 
        ("person", "glove"), ("boy", "glove"), ("woman", "glove"), ("girl", "glove"), ("child", "glove"), 
        ("guy", "glove"), ("man", "coat"), ("woman", "coat"), ("person", "coat"), ("girl", "coat"), ("lady", "coat"), 
        ("boy", "coat"), ("child", "coat"), ("bear", "coat"), ("snowboarder", "coat"), ("donut", "sprinkles"), 
        ("cupcake", "sprinkles"), ("donuts", "sprinkles"), ("vase", "flowers"), ("tree", "flowers"), 
        ("bush", "flowers"), ("plant", "flowers"), ("cake", "flowers"), ("umbrella", "flowers"), ("shirt", "flowers"), 
        ("pot", "flowers"), ("bushes", "flowers"), ("dress", "flowers"), ("plate", "flowers"), ("basket", "flowers"), 
        ("table", "flowers"), ("field", "flowers"), ("bed", "flowers"), ("pillow", "flowers"), ("box", "flowers"), 
        ("hat", "flowers"), ("person", "flowers"), ("comforter", "flowers"), ("cup", "flowers"), ("rug", "flowers"), 
        ("curtains", "flowers"), ("tablecloth", "flowers"), ("blanket", "flowers"), ("sign", "numbers"), 
        ("shirt", "numbers"), ("window", "curtain"), ("door", "curtain"), ("donut", "frosting"), ("cake", "frosting"), 
        ("cupcake", "frosting"), ("donuts", "frosting"), ("cupcakes", "frosting"), ("brownies", "frosting"), 
        ("man", "surfboard"), ("person", "surfboard"), ("woman", "surfboard"), ("girl", "surfboard"), 
        ("boy", "surfboard"), ("man", "camera"), ("woman", "camera"), ("person", "camera"), ("guy", "camera"), 
        ("girl", "camera"), ("pizza", "sauce"), ("bowl", "sauce"), ("container", "sauce"), ("bottle", "sauce"), 
        ("food", "sauce"), ("meat", "sauce"), ("chicken", "sauce"), ("sandwich", "sauce"), ("plate", "sauce"), 
        ("steak", "sauce"), ("pasta", "sauce"), ("bread", "sauce"), ("hot dog", "sauce"), ("rice", "sauce"), 
        ("broccoli", "sauce"), ("wall", "mirror"), ("door", "mirror"), ("mountain", "snow"), ("tree", "snow"), 
        ("mountains", "snow"), ("hill", "snow"), ("trees", "snow"), ("roof", "snow"), ("hills", "snow"), 
        ("bench", "snow"), ("woman", "necklace"), ("man", "necklace"), ("girl", "necklace"), ("lady", "necklace"), 
        ("child", "necklace"), ("shirt", "pocket"), ("jacket", "pocket"), ("pants", "pocket"), ("jeans", "pocket"), 
        ("coat", "pocket"), ("woman", "umbrella"), ("man", "umbrella"), ("person", "umbrella"), ("lady", "umbrella"), 
        ("girl", "umbrella"), ("child", "umbrella"), ("bed", "headboard"), ("window", "curtains"), ("vase", "flower"), 
        ("cake", "flower"), ("shirt", "flower"), ("plate", "flower"), ("pot", "flower"), ("painting", "flower"), 
        ("glass", "flower"), ("hat", "flower"), ("girl", "flower"), ("player", "bat"), ("man", "bat"), 
        ("boy", "bat"), ("girl", "bat"), ("person", "bat"), ("child", "bat"), ("bed", "pillow"), ("couch", "pillow"), 
        ("chair", "pillow"), ("sofa", "pillow"), ("glass", "water"), ("bottle", "water"), ("vase", "water"), 
        ("cup", "water"), ("bowl", "water"), ("pitcher", "water"), ("container", "water"), ("bucket", "water"), 
        ("dog", "frisbee"), ("man", "frisbee"), ("boy", "frisbee"), ("woman", "frisbee"), ("person", "frisbee"), 
        ("girl", "frisbee"), ("guy", "frisbee"), ("building", "chimney"), ("house", "chimney"), ("roof", "chimney"), 
        ("cabin", "chimney"), ("window", "blinds"), ("door", "blinds"), ("man", "phone"), ("woman", "phone"), 
        ("girl", "phone"), ("boy", "phone"), ("person", "phone"), ("lady", "phone"), ("sign", "words"), 
        ("shirt", "words"), ("woman", "ring"), ("man", "ring"), ("person", "ring"), ("lady", "ring"), 
        ("guy", "ring"), ("girl", "ring"), ("ear", "tag"), ("cow", "tag"), ("suitcase", "tag"), ("sheep", "tag"), 
        ("dog", "tag"), ("bear", "tag"), ("cat", "tag"), ("shirt", "tag"), ("basket", "tag"), ("animal", "tag"), 
        ("man", "goggles"), ("person", "goggles"), ("woman", "goggles"), ("boy", "goggles"), ("girl", "goggles"), 
        ("hot dog", "mustard"), ("sandwich", "mustard"), ("bottle", "mustard"), ("bun", "mustard"), 
        ("cupcake", "topping"), ("donut", "topping"), ("container", "liquid"), ("man", "suit"), ("person", "suit"), 
        ("cake", "candle"), ("cabinet", "drawer"), ("desk", "drawer"), ("table", "drawer"), ("bike", "basket"), 
        ("hot dog", "ketchup"), ("container", "ketchup"), ("bottle", "ketchup"), ("man", "skis"), 
        ("person", "skis"), ("woman", "skis"), ("boy", "skis"), ("child", "skis"), ("woman", "scarf"), 
        ("man", "scarf"), ("bear", "scarf"), ("person", "scarf"), ("girl", "scarf"), ("lady", "scarf"), 
        ("dinosaur", "scarf"), ("penguin", "scarf"), ("woman", "bracelet"), ("man", "bracelet"), 
        ("person", "bracelet"), ("girl", "bracelet"), ("lady", "bracelet"), ("boy", "bracelet"), 
        ("woman", "earring"), ("man", "earring"), ("girl", "earring"), ("lady", "earring"), ("person", "earring"), 
        ("child", "earring"), ("woman", "dress"), ("girl", "dress"), ("bear", "dress"), ("person", "dress"), 
        ("doll", "dress"), ("lady", "dress"), ("child", "dress"), ("pole", "flag"), ("building", "flag"), 
        ("boat", "flag"), ("train", "flag"), ("scooter", "flag"), ("tower", "flag"), ("motorcycle", "flag"), 
        ("man", "wetsuit"), ("woman", "wetsuit"), ("boy", "wetsuit"), ("person", "wetsuit"), ("guy", "wetsuit"), 
        ("girl", "wetsuit"), ("sandwich", "tomato"), ("man", "gloves"), ("person", "gloves"), ("player", "gloves"), 
        ("child", "gloves"), ("woman", "gloves"), ("girl", "gloves"), ("man", "sweater"), ("woman", "sweater"), 
        ("girl", "sweater"), ("person", "sweater"), ("lady", "sweater"), ("boy", "sweater"), ("child", "sweater"), 
        ("cake", "icing"), ("donut", "icing"), ("cupcake", "icing"), ("dessert", "icing"), ("sandwich", "meat"), 
        ("pizza", "meat"), ("plate", "meat"), ("bread", "meat"), ("dish", "meat"), ("bowl", "meat"), ("bun", "meat"), 
        ("bowl", "fruit"), ("tree", "fruit"), ("basket", "fruit"), ("cake", "fruit"), ("plate", "fruit"), 
        ("box", "fruit"), ("man", "skateboard"), ("boy", "skateboard"), ("person", "skateboard"), 
        ("woman", "skateboard"), ("guy", "skateboard"), ("glass", "juice"), ("bottle", "juice"), 
        ("cup", "juice"), ("pitcher", "juice"), ("pizza", "spinach"), ("mug", "coffee"), ("man", "snowboard"), 
        ("person", "snowboard"), ("child", "snowboard"), ("woman", "snowboard"), ("plate", "pizza"), ("box", "pizza"), 
        ("table", "pizza"), ("pan", "pizza"), ("man", "mask"), ("person", "mask"), ("horse", "mask"), ("bear", "mask"), 
        ("animal", "mask"), ("teddy bear", "mask"), ("man", "knife"), ("woman", "knife"), ("person", "knife"), 
        ("table", "tablecloth"), ("man", "wristband"), ("player", "wristband"), ("woman", "wristband"), 
        ("glass", "beer"), ("mug", "beer"), ("man", "beer"), ("cup", "beer"), ("bottle", "beer"), ("man", "boots"), 
        ("woman", "boots"), ("girl", "boots"), ("person", "boots"), ("lady", "boots"), ("cowboy", "boots"), 
        ("boy", "boots"), ("man", "eyeglasses"), ("woman", "eyeglasses"), ("person", "eyeglasses"), 
        ("lady", "eyeglasses"), ("girl", "eyeglasses"), ("boy", "eyeglasses"), ("door", "lock"), ("cabinet", "lock"), 
        ("suitcase", "lock"), ("gate", "lock"), ("man", "uniform"), ("lady", "uniform"), ("boy", "uniform"),
        ("woman", "uniform"), ("person", "uniform"), ("woman", "cell phone"), ("man", "cell phone"), 
        ("person", "cell phone"), ("boy", "cell phone"), ("donut", "chocolate"), ("bread", "chocolate"), 
        ("man", "kite"), ("woman", "kite"), ("girl", "kite"), ("person", "kite"), ("child", "kite"), 
        ("boy", "kite"), ("guy", "kite"), ("mountain", "trees"), ("hill", "trees"), ("field", "trees"), 
        ("pizza", "olives"), ("sandwich", "lettuce"), ("salad", "lettuce"), ("pizza", "lettuce"), 
        ("shelf", "books"), ("table", "books"), ("necklace", "stone"), ("bed", "blanket"), ("horse", "blanket"), 
        ("building", "dome"), ("tower", "dome"), ("man", "laptop"), ("woman", "laptop"), ("person", "laptop"), 
        ("girl", "laptop"), ("boy", "laptop"), ("pizza", "pepper"), ("wall", "painting"), ("pizza", "peppers"), 
        ("hot dog", "peppers"), ("woman", "skirt"), ("person", "skirt"), ("girl", "skirt"), ("player", "skirt"), 
        ("alien", "skirt"), ("fence", "gate"), ("pizza", "mushrooms"), ("shoe", "heel"), ("boot", "heel"), 
        ("woman", "handbag"), ("person", "handbag"), ("girl", "handbag"), ("cake", "candles"), ("bed", "pillows"), 
        ("couch", "pillows"), ("sofa", "pillows"), ("chair", "pillows"), ("seat", "pillows"), ("man", "bike"), 
        ("person", "bike"), ("guy", "bike"), ("donut", "glaze"), ("donuts", "glaze"), ("shelf", "book"), 
        ("man", "book"), ("woman", "book"), ("bear", "book"), ("plate", "cake"), ("table", "cake"), 
        ("box", "donut"), ("man", "donut"), ("tray", "donut"), ("plate", "donut"), ("boy", "donut"), 
        ("girl", "donut"), ("pizza", "ham"), ("boat", "rope"), ("man", "rope"), ("cow", "rope"), ("dog", "rope"), 
        ("horse", "rope"), ("sheep", "rope"), ("animal", "rope"), ("plate", "bread"), ("basket", "bread"), 
        ("dog", "toy"), ("cat", "toy"), ("child", "toy"), ("baby", "toy"), ("girl", "toy"), ("pizza", "tomatoes"), 
        ("sandwich", "tomatoes"), ("plate", "tomatoes"), ("man", "ball"), ("dog", "ball"), ("bag", "ball"), 
        ("boy", "ball"), ("player", "ball"), ("girl", "ball"), ("bear", "ball"), ("pizza", "vegetables"), 
        ("basket", "vegetables"), ("pot", "vegetables"), ("plate", "vegetables"), ("dish", "vegetables"), 
        ("box", "vegetables"), ("pan", "vegetables"), ("soup", "vegetables"), ("man", "headband"), 
        ("girl", "headband"), ("woman", "headband"), ("person", "headband"), ("player", "headband"), 
        ("bowl", "soup"), ("pot", "soup"), ("cup", "soup"), ("plate", "hot dog"), ("man", "hot dog"), 
        ("woman", "hot dog"), ("bun", "hot dog"), ("boy", "hot dog"), ("box", "hot dog"), ("container", "hot dog"), 
        ("tray", "hot dog"), ("man", "cigarette"), ("woman", "cigarette"), ("lady", "cigarette"), 
        ("man", "stick"), ("dog", "stick"), ("woman", "stick"), ("woman", "suitcase"), ("man", "suitcase"), 
        ("child", "suitcase"), ("lady", "suitcase"), ("boy", "suitcase"), ("passenger", "suitcase"), 
        ("girl", "suitcase"), ("person", "suitcase"), ("man", "dog"), ("woman", "dog"), ("girl", "dog"), 
        ("person", "dog"), ("guy", "dog"), ("boy", "dog"), ("pizza", "sausage"), ("plate", "sausage"), 
        ("man", "banana"), ("woman", "banana"), ("box", "banana"), ("bowl", "banana"), ("plate", "banana"),
        ("monkey", "banana"), ("child", "banana"), ("hot dog", "onion"), ("pizza", "onion"), 
        ("sandwich", "onion"), ("dish", "onion"), ("boat", "canopy"), ("bed", "canopy"), ("man", "tattoos"), 
        ("woman", "tattoos"), ("guy", "tattoos"), ("man", "bottle"), ("person", "bottle"), ("pants", "pockets"), 
        ("jacket", "pockets"), ("house", "porch"), ("pole", "lamp"), ("man", "paddle"), ("woman", "paddle"), 
        ("boy", "paddle"), ("person", "paddle"), ("donut", "nuts"), ("cake", "nuts"), ("pastry", "nuts"), 
        ("bouquet", "roses"), ("curtain", "roses"), ("vase", "roses"), ("container", "roses"), ("bush", "roses"), 
        ("woman", "roses"), ("donut", "powder"), ("woman", "cup"), ("man", "cup"), ("person", "cup"), 
        ("child", "cup"), ("boy", "cup"), ("bear", "heart"), ("cake", "heart"), ("card", "heart"), 
        ("shirt", "heart"), ("hat", "heart"), ("umbrella", "heart"), ("vase", "heart"), ("pillow", "heart"), 
        ("plate", "salad"), ("bowl", "salad"), ("elephant", "chain"), ("woman", "chain"), ("man", "chain"), 
        ("plate", "toast"), ("can", "utensil"), ("bowl", "utensil"), ("tower", "bell"), ("cow", "bell"), 
        ("collar", "bell"), ("building", "bell"), ("cat", "bell"), ("bed", "comforter"), ("woman", "apron"), 
        ("man", "apron"), ("lady", "apron"), ("man", "sneakers"), ("boy", "sneakers"), ("player", "sneakers"), 
        ("woman", "sneakers"), ("guy", "sneakers"), ("bowl", "cereal"), ("man", "luggage"), ("person", "luggage"), 
        ("woman", "luggage"), ("cart", "luggage"), ("woman", "earrings"), ("person", "earrings"), ("lady", "earrings"), 
        ("plate", "sandwich"), ("man", "sandwich"), ("tray", "sandwich"), ("bag", "sandwich"), ("platter", "sandwich"), 
        ("box", "sandwich"), ("child", "sandwich"), ("person", "sandwich"), ("container", "sandwich"), 
        ("boy", "sandwich"), ("girl", "sandwich"), ("guy", "sandwich"), ("bowl", "tangerine"), ("man", "outfit"), 
        ("woman", "outfit"), ("child", "outfit"), ("girl", "outfit"), ("person", "outfit"), ("doll", "outfit"), 
        ("pizza", "chicken"), ("plate", "chicken"), ("sandwich", "chicken"), ("salad", "chicken"), ("tree", "bananas"), 
        ("bowl", "bananas"), ("boy", "bananas"), ("lady", "bananas"), ("boat", "bananas"), ("table", "vase"), 
        ("man", "sandals"), ("woman", "sandals"), ("person", "sandals"), ("girl", "sandals"), ("boy", "sandals"), 
        ("lady", "sandals"), ("child", "sandals"), ("guy", "sandals"), ("plate", "broccoli"), ("pizza", "broccoli"), 
        ("bowl", "broccoli"), ("salad", "broccoli"), ("dish", "broccoli"), ("man", "headphones"), 
        ("person", "headphones"), ("lady", "headphones"), ("guy", "headphones"), ("woman", "headphones"), 
        ("child", "headphones"), ("boy", "headphones"), ("woman", "wig"), ("bottle", "pump"), ("dispenser", "pump"), 
        ("man", "cane"), ("woman", "cane"), ("person", "cane"), ("guy", "cane"), ("bowl", "spoon"), 
        ("glass", "spoon"), ("man", "spoon"), ("girl", "spoon"), ("boy", "spoon"), ("woman", "spoon"), 
        ("bowl", "apple"), ("box", "apple"), ("basket", "apple"), ("man", "fork"), ("girl", "fork"), ("boy", "fork"), 
        ("child", "fork"), ("woman", "fork"), ("lady", "fork"), ("woman", "blouse"), ("lady", "blouse"), 
        ("girl", "blouse"), ("person", "blouse"), ("glass", "drink"), ("man", "drink"), ("hot dog", "onions"), 
        ("pizza", "onions"), ("sandwich", "onions"), ("man", "controller"), ("girl", "controller"), 
        ("boy", "controller"), ("woman", "controller"), ("lady", "controller"), ("person", "controller"), 
        ("guy", "controller"), ("lady", "toothbrush"), ("man", "toothbrush"), ("baby", "toothbrush"), 
        ("boy", "toothbrush"), ("woman", "toothbrush"), ("child", "toothbrush"), ("guy", "toothbrush"), 
        ("toddler", "toothbrush"), ("girl", "toothbrush"), ("glass", "soda"), ("can", "soda"), ("bottle", "soda"), 
        ("tray", "cupcake"), ("man", "cupcake"), ("bag", "flour"), ("skateboard", "drawing"), ("shirt", "drawing"), 
        ("box", "tissue"), ("building", "fence"), ("tree", "fence"), ("desk", "drawers"), ("nightstand", "drawers"), 
        ("bowl", "orange"), ("pizza", "basil"), ("man", "towel"), ("woman", "towel"), ("building", "pillars"), 
        ("pizza", "spices"), ("bowl", "meal"), ("wall", "mirrors"), ("dog", "bandana"), ("man", "bandana"), 
        ("woman", "bandana"), ("boy", "bandana"), ("horse", "bandana"), ("girl", "bandana"), ("donut", "cream"), 
        ("cupcake", "cream"), ("pastries", "cream"), ("box", "donuts"), ("tray", "donuts"), ("plate", "donuts"), 
        ("tree", "bird"), ("bear", "clothes"), ("dog", "clothes"), ("man", "wristwatch"), ("woman", "wristwatch"), 
        ("person", "wristwatch"), ("man", "calf"), ("phone", "antenna"), ("car", "antenna"), ("boat", "antenna"), 
        ("building", "antenna"), ("router", "antenna"), ("tree", "blossoms"), ("man", "computer"), ("girl", "computer"), 
        ("person", "computer"), ("man", "rose"), ("vase", "rose"), ("suit", "rose"), ("flag", "rose"), ("cow", "tags"), 
        ("wall", "paintings"), ("building", "cross"), ("bus", "decoration"), ("cake", "decoration"), 
        ("elephant", "decoration"), ("roof", "decoration"), ("shirt", "decoration"), ("wall", "decoration"), 
        ("donut", "decoration"), ("mug", "decoration"), ("surfboard", "decoration"), ("snowboard", "decoration"), 
        ("cake", "decorations"), ("window", "decorations"), ("horse", "decorations"), ("plate", "decorations"), 
        ("tree", "decorations"), ("tower", "decorations"), ("building", "decorations"), ("wall", "decorations"), 
        ("clock", "decorations"), ("tower", "clocks"), ("building", "clocks"), ("wall", "clocks"), ("dish", "rice"), 
        ("bowl", "rice"), ("plate", "rice"), ("bowl", "carrots"), ("plate", "carrots"), ("container", "carrots"), 
        ("salad", "carrots"), ("bottle", "oil"), ("container", "oil"), ("pan", "oil"), ("bowl", "oil"), 
        ("glass", "oil"), ("train", "ladder"), ("truck", "ladder"), ("bed", "ladder"), ("building", "ladder"), 
        ("boat", "ladder"), ("house", "ladder"), ("woman", "heels"), ("shoes", "heels"), ("woman", "bikini"), 
        ("girl", "bikini"), ("man", "briefcase"), ("man", "sweatshirt"), ("person", "sweatshirt"), 
        ("boy", "sweatshirt"), ("woman", "sweatshirt"), ("girl", "sweatshirt"), ("mug", "tea"), ("table", "drinks"), 
        ("container", "drinks"), ("cake", "star"), ("surfboard", "star"), ("airplane", "star"), 
        ("elephant", "star"), ("shirt", "star"), ("box", "tissues"), ("shelf", "bottles"), ("man", "microphone"), 
        ("woman", "microphone"), ("lady", "microphone"), ("box", "candies"), ("bowl", "candies"), ("glass", "milk"), 
        ("bottle", "milk"), ("cup", "milk"), ("jar", "milk"), ("bowl", "milk"), ("cake", "strawberry"), ("man", "baby"), 
        ("woman", "baby"), ("tray", "buns"), ("glass", "beverage"), ("cup", "beverage"), ("man", "beverage"), 
        ("plate", "bacon"), ("pizza", "bacon"), ("salad", "bacon"), ("sandwich", "bacon"), ("necklace", "beads"), 
        ("woman", "bracelets"), ("lady", "bracelets"), ("girl", "bracelets"), ("boy", "bracelets"), ("box", "apples"), 
        ("bowl", "apples"), ("plate", "apples"), ("platter", "apples"), ("basket", "apples"), ("tree", "apples"), 
        ("bucket", "apples"), ("sandwich", "egg"), ("plate", "egg"), ("bread", "egg"), ("donut", "almonds"), 
        ("container", "almonds"), ("jar", "honey"), ("donut", "honey"), ("bottle", "honey"), 
        ("boat", "life preserver"), ("glass", "ice"), ("drink", "ice"), ("cup", "ice"), ("salad", "dressing"), 
        ("cup", "dressing"), ("wall", "art"), ("dish", "butter"), ("toast", "butter"), ("bread", "butter"), 
        ("knife", "butter"), ("mug", "spider"), ("hill", "bushes"), ("woman", "lipstick"), ("girl", "lipstick"), 
        ("house", "garage"), ("bowl", "broth"), ("pot", "broth"), ("tree", "ornaments"), ("bear", "costume"), 
        ("man", "costume"), ("woman", "costume"), ("toy", "costume"), ("cake", "berry"), ("waffles", "syrup"), 
        ("pancakes", "syrup"), ("plate", "syrup"), ("bottle", "syrup"), ("man", "pen"), ("woman", "pen"), 
        ("girl", "pen"), ("boy", "pen"), ("container", "hay"), ("cart", "hay"), ("bowl", "chips"), 
        ("plate", "chips"), ("man", "can"), ("woman", "flip flops"), ("man", "flip flops"), 
        ("person", "flip flops"), ("boy", "flip flops"), ("plate", "eggs"), ("bowl", "eggs"), 
        ("salad", "eggs"), ("basket", "eggs"), ("pan", "eggs"), ("toast", "eggs"), ("man", "wallet"), 
        ("trailer", "oranges"), ("tree", "oranges"), ("plate", "oranges"), ("window", "drapes"), 
        ("plate", "grapes"), ("plate", "fries"), ("basket", "fries"), ("bottle", "alcohol"), 
        ("shirt", "butterflies"), ("pants", "butterflies"), ("headband", "butterflies"), 
        ("plate", "dessert"), ("bowl", "dessert"), ("man", "cigar"), ("baby", "diaper"), 
        ("sandwich", "cucumber"), ("salad", "cucumber"), ("person", "magazine"), ("lady", "magazine"), 
        ("dog", "clothing"), ("wall", "vines"), ("container", "strawberries"), ("cake", "strawberries"), 
        ("cup", "strawberries"), ("dessert", "strawberries"), ("bowl", "strawberries"), 
        ("bucket", "strawberries"), ("woman", "jewelry"), ("girl", "jewelry"), ("man", "gun"), 
        ("woman", "gun"), ("woman", "child"), ("person", "child"), ("man", "child"), ("pizza", "herbs"), 
        ("chicken", "herbs"), ("wall", "television"), ("horse", "cart"), ("man", "cart"), 
        ("soda", "ice cube"), ("hot dog", "chili"), ("man", "name tag"), ("girl", "name tag"), 
        ("dog", "name tag"), ("woman", "name tag"), ("collar", "name tag"), ("man", "baseball"), 
        ("boy", "baseball"), ("person", "baseball"), ("plate", "fruits"), ("bowl", "fruits"), 
        ("table", "fruits"), ("basket", "fruits"), ("cake", "fruits"), ("bowl", "noodles"), 
        ("soup", "noodles"), ("man", "guitar"), ("boy", "guitar"), ("bear", "guitar"), ("plate", "pasta"), 
        ("box", "pasta"), ("bowl", "pasta"), ("umbrella", "cats"), ("pizza", "artichokes"), ("man", "sword"), 
        ("statue", "sword"), ("packet", "mayonnaise"), ("vase", "lily"), ("bowl", "berries"), ("bowl", "beans"), 
        ("horse", "carriage"), ("plate", "pancake"), ("man", "wii"), ("boy", "wii"), ("woman", "wii"), 
        ("elephant", "chains"), ("motorcycle", "chains"), ("blanket", "sunflowers"), ("bowl", "sunflowers"), 
        ("curtains", "sunflowers"), ("table", "sunflowers"), ("tray", "pastries"), ("plate", "pastries"), 
        ("bowl", "pastries"), ("laptop", "cables"), ("bowl", "cookies"), ("basket", "cookies"), ("plate", "cookies"), 
        ("box", "cookies"), ("sandwich", "beef")]
    for (s,o) in whitelist:
            return False
    return True

def filterBetween(s, o):
    betweenWhitelist = [("table", "chairs"), ("hot dog", "bun"), ("cigarette", "fingers"), ("houses", "trees"), ("onions", "bread"), 
    ("fence", "animals"), ("fence", "trees"), ("carrots", "bread"), ("house", "trees"), ("meat", "buns"), 
    ("river", "mountains"), ("cabinets", "windows"), ("building", "trees"), ("plant", "rocks"), ("water", "trees"), 
    ("water", "rocks"), ("art", "windows"), ("car", "trees"), ("road", "trees"), ("meat", "bread"), ("tail", "legs"), 
    ("road", "buildings"), ("bush", "cars"), ("bush", "train tracks"), ("backpack", "legs"), ("frisbee", "legs"), 
    ("frisbee", "hands"), ("ball", "legs"), ("ball", "feet"), ("street", "buildings"), ("bottle", "feet"), 
    ("plate", "legs"), ("sign", "train tracks"), ("bottles", "feet"), ("tree", "buildings"), ("tree", "houses"), 
    ("bird", "rocks"), ("dog", "legs"), ("pillow", "legs"), ("cell phone", "fingers"), ("box", "train tracks"), 
    ("cheese", "bread"), ("river", "hills"), ("steps", "bushes"), ("road", "mountains"), ("road", "bushes"), 
    ("road", "houses"), ("net", "players"), ("ball", "fingers"), ("street", "trees"), ("street", "houses"), 
    ("bottle", "legs"), ("plate", "hands"), ("bench", "trees"), ("bench", "plants"), ("door", "windows"), 
    ("sign", "windows"), ("sign", "wheels"), ("bottles", "legs"), ("tree", "zebras"), ("tree", "bushes"), 
    ("tree", "rocks"), ("bird", "trees"), ("dog", "cabinets"), ("weeds", "steps"), ("weeds", "rocks"), 
    ("motorcycle", "cars"), ("waterfall", "trees"), ("tomato", "bread"), ("luggage", "legs"), ("number", "doors"), 
    ("animal", "legs"), ("animal", "branches"), ("paper", "legs"), ("vase", "candles"), ("window", "cupboards"), 
    ("window", "cabinets"), ("window", "trees"), ("man", "trees"), ("man", "elephants"), ("man", "trains"), 
    ("man", "cars"), ("skateboard", "legs"), ("tomatoes", "bread"), ("desk", "beds"), ("can", "benches"), 
    ("hot dog", "bread"), ("flower", "towels"), ("flower", "paws"), ("chicken", "bun"), ("chicken", "bread"), 
    ("train", "bushes"), ("train", "buildings"), ("lettuce", "bread"), ("bear", "rocks"), ("toy", "paws"), 
    ("floor lamp", "chairs"), ("rope", "boats"), ("bikes", "buildings"), ("television", "windows"), ("gate", "hills"), 
    ("bridge", "buildings"), ("finger", "scissors"), ("elephants", "trees"), ("marker", "trees"), ("log", "rocks"), 
    ("bag", "arms"), ("cat", "shoes"), ("cabin", "trees"), ("bus", "cars"), ("cloud", "trees"), ("broccoli", "bowls"), 
    ("bucket", "jeans"), ("chair", "beds"), ("bacon", "carrots"), ("burger", "donuts"), ("platform", "trains"), 
    ("statue", "windows"), ("zebra", "rocks"), ("snowboard", "legs"), ("town", "mountains"), ("sauce", "bread"), 
    ("person", "chairs"), ("outlet", "windows"), ("vegetable", "bananas")]
    if (s,o) in betweenWhitelist:
        return False
    return True 

def filterBelow(s, o):
    whitelist = [("door", "window"), ("door", "oven"), ("door", "microwave"), ("goggles", "helmet"), ("tree", "bird"), ("tower", "kite"), ("door", "drawer"), 
        ("door", "sign"), ("door", "horse"), ("door", "clock"), ("bush", "clock"), ("bush", "birds"), ("bed", "computer"), ("dog", "lady"), ("step", "bench"), 
        ("plate", "hamburger"), ("motorcycle", "car"), ("motorcycle", "airplane"), ("broccoli", "carrot"), ("glasses", "counter"), ("glasses", "hat"), 
        ("handbag", "hat"), ("weeds", "train"), ("shoe", "leaves"), ("fire", "grill"), ("undershirt", "shirt"), ("bird", "leaves"), ("sweater", "basket"), 
        ("fruit", "sugar"), ("plant", "window"), ("umbrellas", "kite")]
    blacklist = [("sign", "sign"), ("sign", "stop sign"), ("stop sign", "sign"), ("stairs", "man"), ("woman", "man"), ("skier", "mountains"), 
        ("house", "mountain"), ("dugout", "spectator"), ("plate", "man"), ("bench", "man"), ("cup", "toothbrushes"), ("racket", "waist"), 
        ("river", "mountain"), ("vase", "flower"), ("sign", "road"), ("snow", "meadow"), ("grass", "rocks"), ("grass", "floor"), ("grass", "mountains"), 
        ("man", "hill"), ("table", "sink"), ("stairs", "banana"), ("girl", "trees"), ("windows", "clock tower"), ("windows", "sidewalk"), ("plate", "boy"), 
        ("house", "lighthouse"), ("house", "mountains"), ("house", "hill"), ("bench", "woman"), ("apple", "sign"), ("sand", "mountain"), ("sand", "legs"), 
        ("person", "tree"), ("paper", "sink"), ("leaves", "banana"), ("leaves", "flowers"), ("leaves", "bananas"), ("vase", "flowers"), ("train", "street"), 
        ("train", "forest"), ("lock", "knob"), ("pond", "bear"), ("bowl", "soup"), ("airport", "airplane"), ("basket", "apples"), ("basket", "bananas"), 
        ("shoes", "shorts"), ("flowers", "bush"), ("shirt", "person"), ("shirt", "frame"), ("shirt", "glasses"), ("shirt", "earring"), ("mountain", "bird"), 
        ("mountain", "train"), ("mountain", "airplane"), ("sun", "boat"), ("frosting", "cake"), ("town", "hill"), ("town", "tree"), ("cord", "label"), 
        ("tie", "glasses"), ("shrimp", "sushi"), ("bushes", "trees"), ("stones", "fence"), ("stones", "zebras"), ("guy", "sunglasses"), ("van", "man"), 
        ("shore", "rocks"), ("dress", "flower"), ("bread", "sandwich"), ("kites", "couple"), ("lawn", "picnic table"), ("arrow", "car"), ("marker", "orange"), 
        ("canopy", "person"), ("pasture", "sheep"), ("pocket", "zipper"), ("grill", "train")]
    blacklistO = ["chin", "shore", "sky", "roof", "arm", "water", "shirt", "building", "wing", "foot", "leaves", "vest", "wall", "hand", "leg", "head", 
        "feet", "house", "leaf", "log", "rock", "skier", "ceiling", "words", "tower", "clouds", "airport", "eye", "paw", "nose", "trunk", "player", "batter", 
        "roll", "crust", "hamburger", "logo", "eyes", "meal", "jeans", "fingers", "collar", "clothes", "tree trunk", "lady", "face", "mouth", "ski", "walkway", 
        "number", "ground", "handle", "pants", "neck", "arms", "lip", "tail", "patio", "rain", "cloud", "marker", "weeds"]
    blacklistS = ["base", "wood", "concrete", "court", "cement", "platform", "wave", "waves", "ground", "wheel", "water", "skateboard", "floor", "wheels", 
        "surfboard", "road", "pole", "rock", "leg", "trees", "building", "skis", "rocks", "sidewalk", "wall", "bed", "snowboard", "pavement", "tree", "tire", 
        "street", "field", "legs", "ski", "ocean", "hair", "clouds", "mountains", "post", "tower", "leaf", "plant", "hand", "dish", "beach", "bush", "fence", 
        "door", "tires", "food", "home plate", "branch", "runway", "weeds", "bricks", "handle", "head", "cloud", "motorcycle", "mound", "cake", "step", "foot", 
        "trunk", "paw", "strap", "fruit", "jet", "jacket", "feet", "word", "eye", "frisbee", "rope", "ear", "buildings", "tiles", "stone", "broccoli", "nose", 
        "finger", "cushion", "lid", "logo", "number", "pants", "mouth", "vegetable", "umbrella", "shorts", "hill", "steps", "stick", "roof", "paint", "lake", 
        "jeans", "tag", "purse", "fire", "thumb", "tail", "face", "umbrellas", "hills", "glass", "knob", "teeth", "ring", "arm", "walkway", "pillars", "feathers", 
        "words", "collar", "wristband", "wing", "numbers", "city", "airplane", "deck", "chips", "icing", "fur", "sandwich", "sky", "kite", "flag", "sticks", 
        "terrain", "sweatshirt", "mustache", "sock", "suit", "hands", "twig", "vest", "boot", "helmet", "goggles", "cap", "frame", "coat", "soup", "skirt", "porch", 
        "luggage", "fingers", "glasses", "polar bear", "bat", "petal", "parking lot", "socks", "cross", "trucks", "battery", "net", "land", "jar", "handbag", 
        "wrist", "lighthouse", "propeller", "furniture", "crust", "ship", "ceiling", "background", "surfer", "cushions", "label", "doorway", "charger", "sweater", 
        "eyes", "skin", "forest", "couch", "balcony", "arms", "rooftop", "tie"]
    blacklistScat = []
    blacklistOcat = []

    for (s, o) in whitelist:
        return False
    for (s, o) in blacklist:
        return True
    if s in blacklistS or catn(s) in blacklistScat:
        return True
    if o in blacklistO or catn(o) in blacklistOcat:
        return True

    return False

def filterUnder(s, o):
    whitelist = [("ground", "snow"), ("bedspread", "jeans"), ("mountain", "clouds"), ("couch", "window"), ("couch", "blanket"), ("mountains", "clouds"), 
        ("mountains", "snow"), ("door", "sink"), ("food", "umbrella"), ("branch", "bird"), ("branch", "owl"), ("motorcycle", "tree"), ("motorcycle", "dog"), 
        ("step", "door"), ("frisbee", "dog"), ("rope", "bridge"), ("rope", "box"), ("rope", "log"), ("balcony", "clock"), ("steps", "door"), ("lake", "bridge"),
        ("jeans", "blanket"), ("fire", "pot"), ("umbrellas", "trees"), ("flag", "tent"), ("undershirt", "shirt"), ("bench", "leaves"), ("bird", "leaves"), 
        ("giraffes", "leaves"), ("napkin", "hamburger"), ("rug", "clothes"), ("horse", "lady")]
    blacklist = [("leaves", "branches"), ("water", "man"), ("rock", "snow"), ("stop sign", "sign"), ("tower", "desk"), ("sign", "stop sign"), ("man", "post"), 
        ("fish", "shrimp"), ("carrot", "salad"), ("crate", "apples"), ("leaves", "branches"), ("leaves", "tree"), ("leaves", "rock"), ("leaves", "bananas"), 
        ("leaves", "leaves"), ("leaves", "roses"), ("leaves", "bushes"), ("leaves", "petals"), ("leaves", "branch"), ("leaves", "trees"), ("leaves", "cauliflower"), 
        ("window", "curtains"), ("skateboarder", "guy"), ("bench", "guy"), ("container", "rice"), ("spoon", "rice"), ("leaves", "branch"), ("bus", "tire"), 
        ("person", "controller"), ("window", "curtain"), ("toilet", "lid"), ("pan", "lid"), ("box", "lid"), ("person", "bus"), ("bottle", "bus"), ("sign", "pole"), 
        ("can", "pole"), ("bus", "pole"), ("tie", "suit"), ("sign", "stop sign"), ("leaves", "branches"), ("stump", "branches"), ("shoes", "people"), 
        ("stairs", "people"), ("shoe", "coat"), ("vase", "flowers"), ("chair", "boy"), ("girl", "boy"), ("chair", "man"), ("chair", "woman"), ("chair", "bear"), 
        ("scarf", "jacket"), ("tie", "jacket"), ("person", "jacket"), ("stop sign", "sign"), ("bacon", "food"), ("bowl", "food"), ("tomato", "food"), 
        ("potato", "food"), ("rice", "food"), ("plate", "man"), ("sofa", "man"), ("mattress", "bed"), ("dishes", "food"), ("stump", "branches"), ("barrier", "hedge"), 
        ("tomatoes", "leaves"), ("grass", "leaves"), ("tomato", "leaves"), ("poster", "picture"), ("screen", "laptop"), ("sandal", "foot"), 
        ("watch", "shirt"), ("bacon", "food"), ("grill", "stone"), ("stairs", "people"), ("stairs", "person"), ("stairs", "man"), ("plate", "player"), 
        ("water", "bridge"), ("water", "bird"), ("water", "birds"), ("pipe", "car"), ("bench", "building"), ("bench", "tower"), ("box", "train"), 
        ("box", "people"), ("box", "arm"), ("box", "lid"), ("window", "glass"), ("bag", "handle"), ("bowl", "banana"), ("bowl", "food"), ("mountain", "city"), 
        ("container", "rice"), ("container", "bananas"), ("container", "pizza"), ("container", "hot dog"), ("stop sign", "sign"), ("tomato", "food"), 
        ("basket", "frisbee"), ("basket", "plate"), ("basket", "food"), ("basket", "fruit"), ("basket", "pizza"), ("basket", "hot dog"), ("bag", "eye"), 
        ("bags", "eye"), ("bag", "eyes"), ("bags", "eyes"), ("vase", "flowers"), ("pot", "bush"), ("pot", "flower"), ("pot", "leaf"), ("pot", "plant"), 
        ("pot", "broccoli"), ("rice", "food"), ("bike", "man"), ("bike", "officer"), ("bridge", "street"), ("bridge", "train tracks"), ("tent", "rock"), 
        ("tent", "dog"), ("potato", "food"), ("statue", "rug"), ("statue", "tray"), ("t-shirt", "shirt"), ("seat", "person"), ("seat", "man"), 
        ("seat", "chair"), ("broccoli", "food")]
    blacklistO = ["chin", "shore", "sky", "roof", "arm", "water", "shirt", "building", "wing", "foot", "leaves", "vest", "wall", "hand", "leg", "head", 
        "feet", "house", "leaf", "log", "rock", "skier", "ceiling", "words", "tower", "clouds", "airport", "eye", "paw", "nose", "trunk", "player", "batter", 
        "roll", "crust", "hamburger", "logo", "eyes", "meal", "jeans", "fingers", "collar", "clothes", "tree trunk", "lady", "face", "mouth", "ski", "walkway", 
        "number", "ground", "handle", "pants", "neck", "arms", "lip", "tail", "patio", "rain", "cloud", "marker", "weeds"]
    blacklistS = ["base", "wood", "concrete", "court", "cement", "platform", "wave", "waves", "ground", "wheel", "water", "skateboard", "floor", "wheels", 
        "surfboard", "road", "pole", "rock", "leg", "trees", "building", "skis", "rocks", "sidewalk", "wall", "bed", "snowboard", "pavement", "tree", "tire", 
        "street", "field", "legs", "ski", "ocean", "hair", "clouds", "mountains", "post", "tower", "leaf", "plant", "hand", "dish", "beach", "bush", "fence", 
        "door", "tires", "food", "home plate", "branch", "runway", "weeds", "bricks", "handle", "head", "cloud", "motorcycle", "mound", "cake", "step", "foot", 
        "trunk", "paw", "strap", "fruit", "jet", "jacket", "feet", "word", "eye", "frisbee", "rope", "ear", "buildings", "tiles", "stone", "broccoli", "nose", 
        "finger", "cushion", "lid", "logo", "number", "pants", "mouth", "vegetable", "umbrella", "shorts", "hill", "steps", "stick", "roof", "paint", "lake", 
        "jeans", "tag", "purse", "fire", "thumb", "tail", "face", "umbrellas", "hills", "glass", "knob", "teeth", "ring", "arm", "walkway", "pillars", "feathers", 
        "words", "collar", "wristband", "wing", "numbers", "city", "airplane", "deck", "chips", "icing", "fur", "sandwich", "sky", "kite", "flag", "sticks", 
        "terrain", "sweatshirt", "mustache", "sock", "suit", "hands", "twig", "vest", "boot", "helmet", "goggles", "cap", "frame", "coat", "soup", "skirt", 
        "porch", "luggage", "fingers", "glasses", "polar bear", "bat", "petal", "parking lot", "socks", "cross", "trucks", "battery", "net", "land", "jar", 
        "handbag", "wrist", "lighthouse", "propeller", "furniture", "crust", "ship", "ceiling", "background", "surfer", "cushions", "label", "doorway", "charger", 
        "sweater", "eyes", "skin", "forest", "couch", "balcony", "arms", "rooftop", "tie"]
    blacklistScat = []
    blacklistOcat = ["road"]

    for (s, o) in whitelist:
        return False
    for (s, o) in blacklist:
        return True
    if s in blacklistS or catn(s) in blacklistScat:
        return True
    if o in blacklistO or catn(o) in blacklistOcat:
        return True
    if s == "bench" and catn(o) == "person":
        return True

    return False

def filterAbove(s, o):
    whitelist = [("tree", "cow"), ("tree", "car"), ("tree", "fence"), ("tree", "giraffe"), ("tree", "horses"), ("tree", "people"), ("tree", "house"), 
        ("tree", "truck"), ("tree", "train"), ("tree", "horse"), ("tree", "zebras"), ("tree", "bus"), ("tree", "motorcycle"), ("tree", "bear"), ("tree", "bull"), 
        ("tree", "bench"), ("tree", "bike"), ("tree", "van"), ("tree", "giraffes"), ("tree", "suv"), ("trees", "train"), ("trees", "bus"), ("trees", "cars"), 
        ("trees", "fence"), ("trees", "giraffe"), ("trees", "truck"), ("trees", "bird"), ("trees", "elephant"), ("trees", "cow"), ("trees", "sculpture"), 
        ("trees", "zebra"), ("trees", "giraffes"), ("trees", "sheep"), ("trees", "sand"), ("trees", "umbrella"), ("trees", "bus stop"), ("trees", "bushes"), 
        ("trees", "boat"), ("fence", "grass"), ("fence", "snow"), ("fence", "river"), ("fence", "giraffe"), ("fence", "boy"), ("balcony", "shop"), 
        ("balcony", "garage"), ("balcony", "clock"), ("balcony", "door"), ("balcony", "ladder"), ("balcony", "pond"), ("balcony", "bus"), ("balcony", "store"), 
        ("balcony", "cars"), ("boy", "table"), ("boy", "grass"), ("boy", "ball"), ("tower", "trees"), ("tower", "train"), ("tower", "truck"), ("tower", "baby"), 
        ("grass", "sand"), ("skateboard", "boy"), ("skateboard", "staircase"), ("skateboard", "steps"), ("glass", "plate"), ("glass", "dog"), ("glass", "stove"), 
        ("surfboard", "girl"), ("surfboard", "sand"), ("surfboard", "bridge"), ("surfboard", "car"), ("dog", "grass"), ("dog", "stones"), ("people", "building"), 
        ("people", "grass"), ("people", "dogs"), ("people", "giraffe"), ("people", "clock"), ("stop sign", "crowd"), ("door", "stove"), ("door", "stairs"), 
        ("mountains", "shore"), ("sun", "airplane"), ("sun", "water"), ("sun", "clouds"), ("sun", "forest"), ("sun", "ocean"), ("sun", "building"), ("sun", "trees"), 
        ("car", "bed"), ("car", "cat"), ("stick", "pizza"), ("player", "grass"), ("plants", "balcony"), ("plants", "cabinets"), ("dock", "water"), 
        ("seagull", "water"), ("seagull", "ocean"), ("baseball", "player"), ("cliff", "ocean"), ("cliff", "water"), ("cliff", "beach"), ("dish", "table"), 
        ("mountain", "beach"), ("mountain", "trees"), ("kites", "ocean"), ("kites", "buildings"), ("kites", "beach"), ("food", "plate"), ("antenna", "building"), 
        ("fog", "water"), ("chimney", "sign"), ("bleachers", "fence"), ("bird", "water"), ("bridge", "water"), ("kite", "water"), ("clouds", "water"), 
        ("steam", "water"), ("seagull", "water"), ("birds", "water"), ("mountains", "water"), ("airplane", "water"), ("sun", "water"), ("cliff", "water"), 
        ("fog", "water"), ("ball", "water"), ("frisbee", "water"), ("mountain", "water"), ("sign", "building"), ("airplane", "building"), ("clock", "building"), 
        ("wires", "building"), ("roof", "building"), ("flag", "building"), ("people", "building"), ("steam", "building"), ("statue", "building"), 
        ("decoration", "building"), ("antenna", "building"), ("bridge", "building"), ("lamp", "building"), ("sun", "building"), ("clouds", "trees"), 
        ("airplane", "trees"), ("wires", "trees"), ("giraffe", "trees"), ("aircraft", "trees"), ("mountain", "trees"), ("sun", "trees"), ("bird", "trees"), 
        ("bird", "ocean"), ("kite", "ocean"), ("cliff", "ocean"), ("seagull", "ocean"), ("sun", "ocean"), ("kites", "ocean"), ("birds", "ocean"), 
        ("kite", "beach"), ("bird", "beach"), ("kites", "beach"), ("cliff", "beach"), ("kite", "field"), ("bird", "field"), ("airplane", "field"), 
        ("balloon", "umbrella"), ("flowers", "umbrella"), ("airplane", "city"), ("bridge", "roadway")]
    blacklist = [("rug", "bowls"), ("crumb", "egg"), ("hat", "shirt"), ("leaves", "flowers"), ("basket", "animals"), ("window", "curtain"), 
        ("paper", "can"), ("bed", "sofa"), ("man", "cake"), ("sign", "buildings"), ("man", "buildings"), ("woman", "pizza"), ("man", "pizza"), 
        ("canopy", "tent"), ("sign", "container"), ("man", "lake"), ("sign", "apple"), ("grill", "doors"), ("boots", "bike"), ("leaves", "bananas"), 
        ("weeds", "bear"), ("twigs", "bear"), ("screen", "platform"), ("windows", "platform"), ("orange", "fruit"), ("man", "bench"), ("leaves", "tree"), 
        ("window", "tree"), ("curtain", "window"), ("sign", "buildings"), ("candle", "number"), ("noodles", "bowl"), ("soup", "bowl"), ("hedge", "bricks"), 
        ("magazines", "flower"), ("tray", "plate"), ("clothes", "pants"), ("horse", "beach"), ("train", "wheel"), ("pants", "shoes"), ("stars", "tie"), 
        ("jacket", "pants"), ("jacket", "snow pants"), ("snow", "man"), ("blinds", "windows"), ("blinds", "window"), ("orange", "fruit"), ("tent", "entrance"), 
        ("sun", "rock"), ("sun", "boy"), ("flower", "vase"), ("plant", "wall"), ("plant", "grass"), ("curtain", "window"), ("curtain", "train"), ("counter", "sink"), 
        ("counter", "counter"), ("counter", "street"), ("counter", "dishwasher"), ("counter", "floor"), ("counter", "ground"), ("sink", "counter"), 
        ("sink", "bathroom"), ("woman", "beach"), ("woman", "ocean"), ("woman", "floor"), ("woman", "sidewalk"), ("woman", "pants"), ("woman", "ground"), 
        ("woman", "shoes"), ("branches", "trunk"), ("basket", "wheel"), ("plate", "plate"), ("plate", "tire"), ("branch", "grass"), ("branch", "building"), 
        ("leaves", "tree"), ("leaves", "building"), ("leaves", "flowers"), ("leaves", "bananas"), ("person", "water"), ("person", "skateboard"), 
        ("person", "steps"), ("person", "wall"), ("person", "ground"), ("person", "beach"), ("person", "gloves"), ("person", "floor"), ("person", "skis"), 
        ("person", "pavement"), ("person", "road"), ("man", "water"), ("man", "ground"), ("man", "skateboard"), ("man", "ocean"), ("man", "steps"), 
        ("man", "road"), ("man", "ground"), ("man", "skateboard"), ("man", "steps"), ("man", "bench"), ("man", "pole"), ("man", "floor"), ("man", "arm"), 
        ("man", "lake"), ("man", "locomotive"), ("man", "air"), ("man", "hill"), ("man", "skis"), ("man", "couch"), ("man", "stones"), ("man", "hand"), 
        ("man", "field"), ("man", "plate"), ("sign", "sign"), ("sign", "road"), ("sign", "building"), ("sign", "street"), ("sign", "apple"), ("sign", "stop sign"), 
        ("sign", "building"), ("sign", "sidewalk"), ("sign", "ground"), ("sign", "fruit"), ("sign", "highway"), ("stop sign", "sign")]
    blacklistO = ["water", "ground", "street", "road", "building", "head", "floor", "ocean", "beach", "wall", "sidewalk", "field", "stop sign", "donut", 
        "skateboard", "hand", "steps", "highway", "umbrella", "wheel", "city", "nose", "bathroom", "oranges", "airport", "land", "pants", "walkway", "number", 
        "garage", "vase", "stones", "pavement", "runway", "station", "shoes", "post", "lemons", "logo", "lounge", "kite", "pole", "tire", "roadway", 
        "bag", "skis", "face", "porch", "air"]
    blacklistS = ["sky", "clouds", "tree", "cloud", "wall", "trees", "ceiling", "pole", "building", "hand", "fence", "roof", "number", "frame", "head", 
        "balcony", "letter", "boy", "tower", "grass", "hair", "skateboard", "rock", "glass", "surfboard", "dog", "handle", "logo", "toilet", "leaf", "walkway", 
        "knob", "foot", "word", "people", "rocks", "stop sign", "ski", "feet", "hill", "door", "mountains", "arm", "tiles", "car", "bush", "water", "bus", "horn", 
        "fruit", "post", "wallpaper", "words", "gate", "eye", "glasses", "nose", "wing", "leg", "stick", "background", "teeth", "decorations", "motorcycle", 
        "display", "hands", "shirt", "mustache", "skateboarder", "player", "plants", "road", "buildings", "baseball", "boat", "guy", "dish", "platform", 
        "mountain", "tail", "wristband", "mane", "fur", "surfer", "face", "lamp shade", "bushes", "shoe", "trunk", "collar", "seat", "zebra", "food", "skier", 
        "paw", "wheel", "house", "hot dog", "tree branch", "log", "magazine", "ear", "socks", "crowd", "paint", "fans", "lock", "table", "zipper", "logs", 
        "ceiling light", "wings", "highway", "numbers", "forest", "ring", "stone", "land", "animal", "fog", "sidewalk", "chimney", "belt", "feathers", "bleachers", 
        "shorts", "fireplace", "train tracks", "curtains", "skin", "goggles", "air", "legs", "runway", "finger", "neck", "street"]
    blacklistScat = []
    blacklistOcat = []

    for (s, o) in whitelist:
        return False
    for (s, o) in blacklist:
        return True
    if s in blacklistS or catn(s) in blacklistScat:
        return True
    if o in blacklistO or catn(o) in blacklistOcat:
        return True

    return False

prepFilters = {
    "under": filterUnder,
    "underneath": filterUnder,
    "beneath": filterUnder,
    "below": filterBelow,
    "above": filterAbove,
    "on": filterOn,
    "in": filterIn,
    "inside": filterInside,
    "with": filterWith,
    "between": filterBetween,
    "in between": filterBetween,
    "have": filterHave,
} 


# looks better|nicer: [[ugly],[beautiful]]
#softer: [[soft], [hard]]
# more fresh [[rotten], [fresh]] 
# "look": { 
#     "ugly": {"more": "less", "most": "softest", "cd": False, "olist": unhealthyO, "alist": ["soft"]}
#     "beautiful": {"more": "harder", "most": "hardest", "cd": False, "olist": healthyO, "alist": ["hard"]}
# }

femaleO = ["women", "girls", "woman", "girl", "lady", "mother", "daughter", "waitress"]
maleO = ["man", "men", "guy", "boy", "boys", "guys", "gentleman", "father", "son"]
youngO = ["kid", "child", "boy", "girl", "baby", "toddler", "kids", "children", "boys", "girls", "babies", 
    "toddlers", "calf"]
adultO = ["man", "men", "woman", "women", "guy", "guys", "lady", "ladies"]
healthyO = ['almond', 'almonds', 'cereal', 'cheese', 'coleslaw', 'ginger', 'granola', 'nut', 'nuts', 'oatmeal', 
'omelette', 'pecan', 'pecan', 'pistachio', 'salad', 'yogurt', 'fruit', 'fruits', 'apple', 'apples', 'banana', 
'bananas', 'berry', 'berries', 'blackberries', 'blueberries', 'blueberry', 'cherries', 'cherry', 'citrus', 
'cranberries', 'cranberry', 'gourd', 'grape', 'grapefruit', 'grapes', 'kiwi', 'mango', 'mangoes', 'melon', 'melons', 
'orange', 'oranges', 'papaya', 'peach', 'peaches', 'pear', 'pears', 'pineapple', 'pineapples', 'pomegranate', 
'raisins', 'raspberries', 'raspberry', 'strawberries', 'strawberry', 'tangerine', 'watermelon', 'watermelons', 
'vegetable', 'vegetables', 'artichoke', 'artichokes', 'asparagus', 'avocado', 'avocados', 'basil', 'beet', 'beets', 
'broccoli', 'cabbage', 'carrot', 'carrots', 'celery', 'chickpeas', 'cucumber', 'cucumbers', 'lemon', 'lemons', 
'lettuce', 'lime', 'parsley', 'pea', 'pepper', 'peppers', 'pickles', 'spinach', 'tomato', 'tomatoes', 'zucchini']
unhealthyO = ['gummy bear', 'candies', 'candy', 'cotton candy', 'chocolate chips', 'potato chips', 'whipped cream', 
'marshmallow', 'nutella', 'popcorn', 'milkshake', 'donut', 'donuts', 'muffin', 'muffins', 'croissant', 'croissants', 
'hot dog', 'hot dogs', 'fries', 'cheeseburger', 'hamburger', 'pizza', 'pizzas', 'pizza slice', 'pizza slices', 
'ketchup', 'butter', 'sugar', 'brownie', 'brownies', 'cake', 'cakes', 'cookie', 'cookies', 'oreo', 'ice cream', 
'cupcake', 'cupcakes', 'fudge', 'pudding', 'cake slice']
indoorsO = ["classroom", "gym", "hallway", "hospital", "library", "lobby", "lounge", "museum", "pub", "restroom", 
"salon", "theater", "room", "attic", "bathroom", "bedroom", "kitchen", "office", "pantry", "dining room", "living room"]
outdoorsO = ["beach", "cemetery", "city", "courtyard", "desert", "field", "forest", "garden", "hill", "hills", 
"hillside", "hilltop", "intersection", "lake", "swamp", "lawn", "mountain", "ocean", "park", "skate park", 
"mountain peak", "plain", "pond", "river", "sea", "shore", "street", "town", "village", "meadow"]
# flavorFoods = ["cake", "ice cream", "syrup", "sauce", "cupcake", "milkshake", "donut", "frosting", "icing", "cookie"]
# flavors = ["chocolate", "cheese", "vanilla", "strawberry"]
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

# short old light thin
# CD REFERS JUST TO ADJS! 
mAttrs = {
    "brightness": { 
        "dull": {"more": "less bright", "most": [], "cd": False, "alist": ["dull"]},
        "bright": {"more": "brighter", "most": "brightest", "cd": False, "alist": ["bright"]}
    },
    "darkness": { # Has darker color??
        "light": {"more": [], "most": [], "cd": False, "alist": ["light_tone", "white", "beige", "cream colored", "light blue", "light brown", "blond"]},
        "dark": {"more": "darker", "most": "darkest", "cd": False, "alist": ["dark", "dark blue", "dark brown", "black", "dark"]}
    },
    "size": { 
        "small": {"more": "smaller", "most": "smallest", "cd": True, "alist": ["small", "tiny", "little_size"]},
        "large": {"more": ["larger", "bigger"], "most": ["largest", "biggest"], "cd": True, "alist": ["large", "huge", "giant"]}
    },
    "height": { 
        "short": {"more": "shorter", "most": "shortest", "cd": True, "alist": ["short_height"]},
        "long": {"more": "tall", "most": "tallest", "cd": True, "alist": ["tall"]}
    },
    "length": { 
        "short": {"more": "shorter", "most": "shortest", "cd": True, "alist": ["short_length"]},
        "long": {"more": "longer", "most": "longest", "cd": True, "alist": ["long"]}
    },
    "weight": { 
        "light": {"more": ["lighter", "less heavy"], "most": ["lightest", "least heavy"], "cd": True, "alist": ["light_weight"]},
        "heavy": {"more": "heavier", "most": "heaviest", "cd": True, "alist": ["heavy"]}
    },
    "thickness": { 
        "thin": {"more": ["thinner", "less think"], "most": "thinnest", "cd": True, "alist": ["thin_thickness"]},
        "thick": {"more": ["thicker", "less thin"], "most": "thickest", "cd": True, "alist": ["thick"]}
    },
    "width": { 
        "narrow": {"more": ["narrower", "less wide"], "most": "narrowest", "cd": True, "alist": ["narrow"]},
        "wide": {"more": "wider", "most": "widest", "cd": True, "alist": ["wide"]}
    },
    "fatness": { 
        "thin": {"more": "thinner", "most": "thinnest", "cd": True, "alist": ["skinny", "thin_fatness"]},
        "fat": {"more": "fatter", "most": "fattest", "cd": True, "alist": ["fat"]}
    },
    "level": { 
        "low": {"more": "lower", "most": "lowest", "cd": True, "alist": ["low"]},
        "high": {"more": "higher", "most": "highest", "cd": True, "alist": ["high"]}
    },
    "depth": { 
        "shallow": {"more": ["more shallow", "less deep"], "most": ["most shallow", "least deep"], "cd": True, "alist": ["shallow"]},
        "deep": {"more": "deeper", "most": "deepest", "cd": True, "alist": ["deep"]}
    },
    "oldnew": { 
        "old": {"more": ["older", "less new"], "most": "oldest", "cd": False, "alist": ["old_4"]},
        "new": {"more": "newer", "most": "newest", "cd": False, "alist": ["new"]}
    },
    "modernity": { 
        "old": {"more": ["more antique", "less modern", "older"], "most": ["least modern", "oldest"], "cd": True, "alist": ["antique", "vintage", "old fashioned"]},
        "new": {"more": ["newer", "more modern"], "most": ["newest", "most modern"], "cd": False, "alist": ["modern"]}
    },
    "softness": { 
        "soft": {"more": "softer", "most": "softest", "cd": False, "alist": ["soft"]},
        "hard": {"more": "harder", "most": "hardest", "cd": False, "alist": ["hard"]}
    },
    "healthiness": { 
        "unhealthy": {"more": "less healthy", "most": "least healthy", "cd": True, "alist": ["unhealthy"]},
        "healthy": {"more": "healthier", "most": "healthiest", "cd": True, "alist": ["healthy"]}
    },
    "fullness": {
        "empty": {"more": "contain less {drink}", "most": "contain least {drink}", "cd": True, "alist": ["empty"]},
        "full": {"more": "contain more {drink}", "most": "contain most {drink}", "cd": True, "alist": ["full"]}
    },
    "cleanliness": {
        "dirty": {"more": ["more dirty", "less clean"], "most": ["most dirty", "least clean"], "cd": True, "alist": ["dirty", "tinted", "stained"]},
        "clean": {"more": "cleaner", "most": "cleanest", "cd": False, "alist": ["clean"]}
    },
    "clearness": {
        "murky": {"more": "less clear", "most": None, "cd": True, "alist": ["murky"]},
        "clear": {"more": "clearer", "most": "clearest", "cd": False, "alist": ["clean"]}
    },
    "happier": {
        "sad": {"more": "less happy", "most": "least happy", "cd": True, "alist": ["sad", "angry", "unhappy"]},
        "happy": {"more": "happier", "most": "happiest", "cd": True, "alist": ["happy"]}
    },
    "age": {
        "young": {"more": "younger", "most": "youngest", "cd": True, "alist": ["young", "little_age", "baby"]},
        "adult": {"more": "older", "most": "oldest", "cd": True, "alist": ["old_age", "adult"]}
    }
}

attr2mtype = {}

for mtype in mAttrs:
    for mAttr in mAttrs[mtype]:
        for attr in mAttrs[mtype][mAttr]["alist"]:
            attr2mtype[attr] = (mtype, mAttr)

def attr2mattr(attr, obj):
    msense = ["short", "old", "light", "thin"]
    key = attr
    if attr in msense:
        key = "{}_{}".format(attr, obj["senses"].get(attr,""))
    if key in attr2mtype:
        mt, ma = attr2mtype[key]
        if mt == "fullness":
            if obj["name"] in ["glass", "cup", "bottle", "glasses", "cups", "bottles"]:
                return attr2mtype[key]
            return None
        return attr2mtype[key]
    return None

# FIX DUPLICATES!!
wsd = {
    "short": {"height": ["tall"], "length": ["long"]},
    "little": {"age": ["young", "old"], "size": ["large"]},
    "thin": {"fatness": ["skinny", "fat"], "thickness": ["thick"]},
    "bright": {"18": ["dark"], "12": ["dull"]},
    "old": {"age": ["young"], "4": ["new"]},
    "clear": {"weather": ["sunny", "cloudy"], "21": ["murky"]},
    "bare": {"25": ["leafy", "bushy"], "27": ["rocky", "sandy"]},
    "light": {"tone": ["dark"], "weight": ["heavy"]},
    "dark": {"tone": ["light"], "brightness": ["bright"], "weather": ["sunny", "cloudy"], "color": ["blond", "blue", "brown", "black", "green"]},
    "straight": {"28":["curved"], "29":["rounded"], "30":["crooked"], "31":["curly"]}
}

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
    embeddings = config.wrdEmbScale * np.random.randn(num, dim)
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
            symEmb = self.sentenceEmb(sym, wordVectors)
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

# def isplural(word):
#     lemma = wnl.lemmatize(word, 'n')
#     plural = True if word is not lemma else False
#     return plural, lemma

WN_NOUN = 'n'
WN_VERB = 'v'
WN_ADJECTIVE = 'a'
WN_ADJECTIVE_SATELLITE = 's'
WN_ADVERB = 'r'

def convert(word, from_pos, to_pos, verbose=False, synset=False):
    """ Transform words given from/to POS tags """

    synsets = wn.synsets(word, pos=from_pos)
    # Word not found
    if not synsets:
        return []

    # Get all lemmas of the word (consider 'a'and 's' equivalent)
    lemmas = [l for s in synsets
                for l in s.lemmas()
                if s.name().split('.')[1] == from_pos
                    or from_pos in (WN_ADJECTIVE, WN_ADJECTIVE_SATELLITE)
                        and s.name().split('.')[1] in (WN_ADJECTIVE, WN_ADJECTIVE_SATELLITE)]

    # Get related forms
    derivationally_related_forms = [(l, l.derivationally_related_forms()) for l in lemmas]

    # filter only the desired pos (consider 'a' and 's' equivalent)
    related_noun_lemmas = [l for drf in derivationally_related_forms
                             for l in drf[1]
                             if l.synset().name().split('.')[1] == to_pos
                                or to_pos in (WN_ADJECTIVE, WN_ADJECTIVE_SATELLITE)
                                    and l.synset().name().split('.')[1] in (WN_ADJECTIVE, WN_ADJECTIVE_SATELLITE)]

    # Extract the words from the lemmas
    words = [l.name() for l in related_noun_lemmas]
    if verbose:
        print(words)
    if synset:
        words = [l.synset() for l in related_noun_lemmas]
    len_words = len(words)

    if to_pos is WN_ADJECTIVE or to_pos is WN_ADJECTIVE_SATELLITE:
        return words

    # Build the result in the form of a list containing tuples (word, probability)
    result = [(w, float(words.count(w))/len_words) for w in set(words)]
    result.sort(key=lambda w: -w[1])

    if verbose:
        print(result)

    if len(result) == 0:
        return None
    else:
        if synset:
            return result
        else:
            return wn.synsets(result[0][0])[0]

def gather_all_hyponyms(synset, physical=False):
    hypos = []
    for hyponym in synset.hyponyms():
        hypos += convert(hyponym.lemmas()[0].name(), WN_NOUN, WN_ADJECTIVE_SATELLITE, synset=True)
        hypos += convert(hyponym.lemmas()[0].name(), WN_NOUN, WN_ADJECTIVE, synset=True)
        # Adverb too?
        if physical:
            hypos.append(hyponym)
        if len(hyponym.hyponyms()) > 0:
            hypos += gather_all_hyponyms(hyponym)
    return hypos

def collect_helper(synset, attr2syn, attribute_categories, key):
    for hyponym in synset.hyponyms():
        total_syns = []
        attrkey = hyponym.name()
        # Found a parent category we're looking for, so don't use finer grained keys
        if hyponym.lemmas()[0].name() in attribute_categories or hyponym.name() in attribute_categories:
            key = hyponym.name()
            # But also get all the hyponyms, which belong to this parent category
            total_syns += gather_all_hyponyms(hyponym)
            attrkey = key

        # Collect attributes for this category
        attributes = hyponym.attributes()
        total_syns += attributes

        # If this category does have attributes or we found parent, add to map
        if len(total_syns) > 0 or key is not "":
            if len(total_syns) > 0:
                if attrkey not in attr2syn:
                    attr2syn[attrkey] = total_syns
                else:
                    if total_syns[0] not in attr2syn[attrkey]:
                        attr2syn[attrkey] += total_syns

        # Look for more categories, or if parent found, find more attributes
        attr2syn = collect_helper(hyponym, attr2syn, attribute_categories, key)
        key = ""
    return attr2syn

def collect_attribute_categories(attribute_categories):
    attr2syn = {}
    # abstract entity attributes, e.g. state, length, cleanness
    abstract = wn.synset('attribute.n.02')
    attr2syn = collect_helper(abstract, attr2syn, attribute_categories, "")
    # physical entity attributes, e.g. material
    physical_attributes = [wn.synset('building_material.n.01'), wn.synset('fabric.n.01'), wn.synset('material.n.01'), wn.synset('material.n.04')]
    for attribute in physical_attributes:
        attr2syn[attribute.name()] = gather_all_hyponyms(attribute, physical=True)

    for key in attr2syn:
        attr2syn[key] = list(set(attr2syn[key]))
    return attr2syn

def isAnimate(obj):
    alive = wn.synsets("living_thing")[0]
    artifact = wn.synsets("artifact")[0]
    physical = wn.synset("object.n.01")
    if len(wn.synsets(obj, pos='n')) == 0:
        return False
    objsyn = wn.synsets(obj, pos='n')[0]
    if objsyn.res_similarity(alive, brown_ic) > objsyn.res_similarity(artifact, brown_ic):
        return True
    elif objsyn.res_similarity(alive, brown_ic) < objsyn.res_similarity(artifact, brown_ic):
        return False
    else:
        if objsyn.res_similarity(alive, brown_ic) > objsyn.res_similarity(physical, brown_ic):
            return True
        else:
            return False

def find_closest_category(attr, obj, verbose=False):
    synMap = animate2syn if isAnimate(obj) else inanimate2syn
    lemmaMap = animate2lemmas if isAnimate(obj) else inanimate2lemmas
    for key in lemmaMap:
        if attr in lemmaMap[key]:
            return key

    attr_synset = convert(attr, WN_ADJECTIVE, WN_NOUN, verbose=verbose)
    if not attr_synset:
        attr_synset = convert(attr, WN_ADVERB, WN_NOUN)
        if not attr_synset:
            return None
    if verbose:
        print(attr_synset)

    max_idx = -1
    max_sim = -1

    for idx, cat in enumerate(synMap.keys()):
        sim = attr_synset.path_similarity(wn.synset(cat))
        if sim >= max_sim:
            max_idx = idx
            max_sim = sim
            if verbose:
                print(synMap.keys()[idx], sim)
    if max_sim == -1:
        return None
    return synMap.keys()[max_idx]

def generate_questions(obj, attr):
    attr_cat = find_closest_category(attr, obj)
    # print attr_cat
    if attr_cat:
        attr_cat_word = attr_cat.split(".")[0].replace("_", " ")
    else:
        attr_cat_word = None

    if attr_cat_word in ["building material", "fabric", "material"]:
        objective = "Hey, what's the <object> made of?"
        objective_compliment_obj = "Cool <object>! What is it made out of?"
        personal = "What would you say the <object> is made out of?"
        personal_unsure = "I can't tell but what would you say the <object> is made out of?"
        guess = "Random question but is the <object> made out of <guess>?"
        personal_guess = "Do you think the <object> is made out of <guess>?"
        personal_guess_solidarity = "Is it just me or is that a <guess> <object>? lol"
    elif "on" in attr or "off" in attr:
        objective = "Hey, is the <object> on or off?"
        objective_compliment_obj = "Nice <object>! Is it on or off?"
        personal = "Would you say the <object> is on or off?"
        personal_unsure = "I can't tell but would you say the <object> is on or off?"
        guess = "Random question but is the <object> on or off?"
        personal_guess = "Do you think the <object> is on or. off?"
        personal_guess_solidarity = "The <object> look <guess> to me, do you think so too? lol"
    else:
        compliment_obj = "Cool <object>! "

        if attr_cat_word and 'quality' in attr_cat_word:
            objective = "What kind of <object> is that?"
            attr_cat_word = "type"
        else:
            objective = "Hey, what <attribute> is the <object>?"

        objective_compliment_obj = compliment_obj + "What <attribute> is it?"

        personal = "What would you say is the <attribute> of the <object>?"
        personal_unsure = "I can't tell but what would you say is the <attribute> of the <object>?"

        guess = "Random question but is the <object> <guess>?"
        personal_guess = "Do you think the <object> is <guess>?"
        personal_guess_solidarity = "Is it just me or is that a <guess> <object>? lol"

    templates = [objective, objective_compliment_obj, personal, personal_unsure, guess, personal_guess, personal_guess_solidarity]
    template_names = ["objective", "objective_compliment_obj", "personal", "personal_unsure", "guess", "personal_guess", "personal_guess_solidarity"]

    questions = []
    question_map = {}
    attr_cat = find_closest_category(attr, obj)
    if attr_cat:
        for i,t in enumerate(templates):
            q = t
            q = q.replace("<attribute>", attr_cat_word)
            q = q.replace("<object>", obj)
            q = q.replace("<guess>", attr)
            if isplural(obj)[0]:
                q = q.replace(" is ", " are ")
            questions.append(q)
            question_map[template_names[i]] = q
    else:
        q = "Random question but is that <object> <guess>?"
        q = q.replace("<object>", obj)
        q = q.replace("<guess>", attr)
        if isplural(obj)[0]:
            q = q.replace("is", "are")
        questions.append(q)
        question_map["guess"] = q
        q = "Would you say the <object> is <guess>?"
        q = q.replace("<object>", obj)
        q = q.replace("<guess>", attr)
        if isplural(obj)[0]:
            q = q.replace("is", "are")
        questions.append(q)
        question_map["personal_guess"] = q

        q = "I can't tell but would you say the <object> is <guess>?"
        q = q.replace("<object>", obj)
        q = q.replace("<guess>", attr)
        if isplural(obj)[0]:
            q = q.replace("is", "are")
        questions.append(q)
        question_map["personal_unsure_guess"] = q

    return question_map

def generate_attribute_questions(scene_graph_dir='../data/scene_graphs/'):
    jsons = os.listdir(scene_graph_dir)
    num_jsons = len(jsons)
    bar = Bar('Processing scene graphs', max=num_jsons)

    for filename in os.listdir(scene_graph_dir):
        if filename.endswith(".json"):
            idx = filename.split(".")[0]
            f_open = open(scene_graph_dir + filename)
            data = json.load(f_open)

            task = {}
            task['questions'] = {}

            attributes = data['attributes']
            objects = data['objects']
            for i,obj in enumerate(objects):
                objname = obj['name']
                if len(wn.synsets(objname, pos='n')) is 0:
                    continue
                task['questions'][objname] = {}
                attrs = set([x['attribute'] for x in attributes if x['object'] == i])
                for a in attrs:
                    task['questions'][objname][a] = generate_questions(objname, a)

            task['url'] = data['url']
            task['image_id'] = data['image_id']

            with open('../data/scene_graph_questions/' + idx + '_questions.json', 'w') as outfile:
                json.dump(task, outfile, indent=4)
        bar.next()
    bar.finish()

# def cats():
#     #if __name__=='__main__':
#     cats = ['color', 'shape.n.01','size.n.01','feeling', 'quality.n.01', 'quality.n.02']
#     attr2syn = collect_attribute_categories(cats)
#     for x in attr2syn:
#         if len(attr2syn[x]) == 2:
#             for y in attr2syn[x]:
#                 print(y.lemmas()[0].name())
#             print("\n")

#     for x in attr2syn:
#         if len(attr2syn[x]) != 2:
#             for y in attr2syn[x]:
#                 print(y.lemmas()[0].name())
#             print("\n")   

#     # pp.pprint(attr2syn)

#     animate2syn = {}
#     inanimate2syn = {}
#     animate2lemmas = {}
#     inanimate2lemmas = {}
#     for key in attr2syn:
#         if key in animate_cats:
#             animate2syn[key] = attr2syn[key]
#             lemmas = [syn.name().split(".")[0] for syn in attr2syn[key]]
#             animate2lemmas[key] = lemmas
#         elif key in inanimate_cats:
#             inanimate2syn[key] = attr2syn[key]
#             lemmas = [syn.name().split(".")[0] for syn in attr2syn[key]]
#             inanimate2lemmas[key] = lemmas

#generate_attribute_questions()

def GetImageData(id=61512):
  data = utils.retrieve_data('/api/v0/images/' + str(id))
  if 'detail' in data and data['detail'] == 'Not found.':
    return None
  image = utils.parse_image_data(data)
  response = requests.get(image.url, verify=False)
  img = PIL_Image.open(io.BytesIO(response.content))  
  return img

parser = argparse.ArgumentParser()
parser.add_argument('--dir', default="vg14", type = str)

# parser.add_argument('--inDir', required=True, type = str)
# parser.add_argument('--tier', required=True)
parser.add_argument('--outputName', default = "info", type = str)
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
parser.add_argument('--mSize', default=0.3, type = float) # ???
parser.add_argument('--normalize', action="store_true")

# parser.add_argument('--normal', default=0.05, type = float)

parser.add_argument('--vis', action="store_true")

# parser.add_argument('--cont', action = "store_true")
# parser.add_argument('--features', action = "store_true")
# parser.add_argument('--maxObjectNum', default = 100, type = int)
# parser.add_argument('--featuresDim', default = 2048, type = int)
# parser.add_argument('--inEnd', default = [""], nargs = "*")

# parser.add_argument('--imagesNum', default = _, type = int)

args = parser.parse_args()

out = "{dir}/{outputName}".format(dir = args.dir, outputName = args.outputName)
idFilename = "{dir}/image_data.json".format(dir = args.dir)
objectsFilename = "{dir}/objects.json".format(dir = args.dir)
attributesFilename = "{dir}/attributes.json".format(dir = args.dir)
relationsFilename = "{dir}/relationships.json".format(dir = args.dir)
descriptionsFilename = "{dir}/region_descriptions.json".format(dir = args.dir)
outDict = lambda dictName: out + "_{dictName}.pkl".format(dictName = dictName)
outJson = lambda dictName: out + "_{dictName}.json".format(dictName = dictName)
outTxt = lambda dictName: out + "_{dictName}.txt".format(dictName = dictName)

# dataFilename = out + "_annotations.json"
# dataFilenameNew = out + "_annotationsNew.json"
dataFilename = "info.json"
dataFilenameNew = "infoNew.json"

data = {}
vgId2Id = {}

allPunct = ["?", "!", "\\", "/", ")", "(", ".", ",", ";", ":"]
fullPunct = [";", r"/", "[", "]", '"', "{", "}", "(", ")", "=", 
                "+", "\\", "_", "-",">", "<", "@", "`", ",", "?", "!", "%", 
                "^", "&", "*", "~", "#", "$"]
contractions = {"aint": "ain't", "arent": "aren't", "cant": "can't", "couldve": "could've", "couldnt": "couldn't", \
                 "couldn'tve": "couldn't've", "couldnt've": "couldn't've", "didnt": "didn't", "doesnt": "doesn't", "dont": "don't", "hadnt": "hadn't", \
                 "hadnt've": "hadn't've", "hadn'tve": "hadn't've", "hasnt": "hasn't", "havent": "haven't", "hed": "he'd", "hed've": "he'd've", \
                 "he'dve": "he'd've", "hes": "he's", "howd": "how'd", "howll": "how'll", "hows": "how's", "Id've": "I'd've", "I'dve": "I'd've", \
                 "Im": "I'm", "Ive": "I've", "isnt": "isn't", "itd": "it'd", "itd've": "it'd've", "it'dve": "it'd've", "itll": "it'll", "let's": "let's", \
                 "maam": "ma'am", "mightnt": "mightn't", "mightnt've": "mightn't've", "mightn'tve": "mightn't've", "mightve": "might've", \
                 "mustnt": "mustn't", "mustve": "must've", "neednt": "needn't", "notve": "not've", "oclock": "o'clock", "oughtnt": "oughtn't", \
                 "ow's'at": "'ow's'at", "'ows'at": "'ow's'at", "'ow'sat": "'ow's'at", "shant": "shan't", "shed've": "she'd've", "she'dve": "she'd've", \
                 "she's": "she's", "shouldve": "should've", "shouldnt": "shouldn't", "shouldnt've": "shouldn't've", "shouldn'tve": "shouldn't've", \
                 "somebody'd": "somebodyd", "somebodyd've": "somebody'd've", "somebody'dve": "somebody'd've", "somebodyll": "somebody'll", \
                 "somebodys": "somebody's", "someoned": "someone'd", "someoned've": "someone'd've", "someone'dve": "someone'd've", \
                 "someonell": "someone'll", "someones": "someone's", "somethingd": "something'd", "somethingd've": "something'd've", \
                 "something'dve": "something'd've", "somethingll": "something'll", "thats": "that's", "thered": "there'd", "thered've": "there'd've", \
                 "there'dve": "there'd've", "therere": "there're", "theres": "there's", "theyd": "they'd", "theyd've": "they'd've", \
                 "they'dve": "they'd've", "theyll": "they'll", "theyre": "they're", "theyve": "they've", "twas": "'twas", "wasnt": "wasn't", \
                 "wed've": "we'd've", "we'dve": "we'd've", "weve": "we've", "werent": "weren't", "whatll": "what'll", "whatre": "what're", \
                 "whats": "what's", "whatve": "what've", "whens": "when's", "whered": "where'd", "wheres": "where's", "whereve": "where've", \
                 "whod": "who'd", "whod've": "who'd've", "who'dve": "who'd've", "wholl": "who'll", "whos": "who's", "whove": "who've", "whyll": "why'll", \
                 "whyre": "why're", "whys": "why's", "wont": "won't", "wouldve": "would've", "wouldnt": "wouldn't", "wouldnt've": "wouldn't've", \
                 "wouldn'tve": "wouldn't've", "yall": "y'all", "yall'll": "y'all'll", "y'allll": "y'all'll", "yall'd've": "y'all'd've", \
                 "y'alld've": "y'all'd've", "y'all'dve": "y'all'd've", "youd": "you'd", "youd've": "you'd've", "you'dve": "you'd've", \
                 "youll": "you'll", "youre": "you're", "youve": "you've"}
nums = { "none": "0", "zero": "0", "one": "1", "two": "2", "three": "3", "four": "4",
         "five": "5", "six": "6", "seven": "7", "eight": "8", "nine": "9", "ten": "10"}
articles = {"a": "", "an": "", "the": ""}
allReplaceQ = {}
for replace in [contractions, nums, articles]: # , 
    allReplaceQ.update(replace)

allReplaceA = {}
for replace in [contractions, nums]: # , 
    allReplaceA.update(replace)

periodStrip = lambda s: re.sub(r"(?!<=\d)(\.)(?!\d)", " ", s) # :,' ?
collonStrip = lambda s: re.sub(r"(?!<=\d)(:)(?!\d)", " ", s) # replace with " " or ""?
commaNumStrip = lambda s: re.sub(r"(\d)(\,)(\d)", r"\1\3", s)

# remove any non a-zA-Z0-9?
vqaProcessText = lambda text, tokenize, question: processText(text, ignoredPunct = [], keptPunct = [], 
    endPunct = [], delimPunct = fullPunct, replacelistPost = allReplaceQ if question else allReplaceA, reClean = True, tokenize = tokenize)

def processText(text, ignoredPunct = ["?", "!", "\\", "/", ")", "("], 
    keptPunct = [".", ",", ";", ":"], endPunct = [">", "<", ":"], delimPunct = [],
    delim = " ", clean = False, replacelistPre = dict(), replacelistPost = dict(),
    reClean = False, tokenize = True):

    if reClean:
        text = periodStrip(text)
        text = collonStrip(text)
        text = commaNumStrip(text)

    if clean:
        for word in replacelistPre:
            origText = text
            text = text.replace(word, replacelistPre[word])
            if (origText != text):
                print(origText)
                print(text)
                print("")

        for punct in endPunct:
            if text[-1] == punct:
                print(text)
                text = text[:-1]
                print(text)
                print("")

    for punct in keptPunct:
        text = text.replace(punct, delim + punct + delim)           
    
    for punct in ignoredPunct:
        text = text.replace(punct, "")

    for punct in delimPunct:
        text = text.replace(punct, delim)

    text = text.lower()

    if config.tokenizer == "stanford":
        ret = StanfordTokenizer().tokenize(text)
    elif config.tokenizer == "nltk":
        ret = word_tokenize(text)
    else:    
        ret = text.split() # delim

    # origRet = ret
    ret = [replacelistPost.get(word, word) for word in ret]
    # if origRet != ret:
    #     print(origRet)
    #     print(ret)

    ret = [t for t in ret if t != ""]
    if not tokenize:
        ret = delim.join(ret)

    return ret

class SymbolDict(object):
    def __init__(self, empty = False): 
        self.padding = "<PAD>"
        self.unknown = "<UNK>"
        self.start = "<START>"
        self.end = "<END>"

        self.invalidSymbols = [self.padding, self.unknown, self.start, self.end]

        if empty:
            self.sym2id = {self.padding: 0} 
            self.id2sym = [self.padding]            
        else:
            self.sym2id = {self.padding: 0, self.unknown: 1, self.start: 2, self.end: 3} 
            self.id2sym = [self.padding, self.unknown, self.start, self.end]
        self.allSeqs = []

    def getNumSymbols(self):
        return len(self.sym2id)

    def isValid(self, enc):
        return enc not in self.invalidSymbols

    def resetSeqs(self):
        self.allSeqs = []

    def addSymbols(self, seq):
        if type(seq) is not list:
            seq = [seq]
        self.allSeqs += seq

    # Call to create the words-to-integers vocabulary after (reading word sequences with addSymbols). 
    def addToVocab(self, symbol):
        if symbol not in self.sym2id:
            self.sym2id[symbol] = self.getNumSymbols()
            self.id2sym.append(symbol)

    # create vocab only if not existing..?
    def createVocab(self, minCount = 0, top = 0, addUnk = False):
        counter = {}
        for symbol in self.allSeqs:
            counter[symbol] = counter.get(symbol, 0) + 1
        
        isTop = lambda symbol: True
        if top > 0:
            topItems = sorted(counter.items(), key = lambda x: x[1], reverse = True)[:top]
            tops = [k for k,v in topItems]
            isTop = lambda symbol: symbol in tops 

        if addUnk:
            self.addToVocab(self.unknown)

        for symbol in counter:
            if counter[symbol] > minCount and isTop(symbol):
                self.addToVocab(symbol)

        self.counter = counter
        self.sortCounter()
        
    def sortCounter(self):
        for symbol in self.counter:
            # if counter[symbol] > minCount and isTop(symbol):
            self.addToVocab(symbol)
        self.sortedCounter = sorted(self.counter.items(), key = lambda x: x[1], reverse = True)[:]

    # Encodes a symbol. Returns the matching integer.
    def encodeSym(self, symbol):
        if symbol not in self.sym2id:
            symbol = self.unknown
        return self.sym2id[symbol] # self.sym2id.get(symbol, None) # # -1 VQA MAKE SURE IT DOESNT CAUSE BUGS

    # '''
    # Encodes a sequence of symbols.
    # Optionally add start, or end symbols. 
    # Optionally reverse sequence 
    # '''
    # def encodeSeq(self, decoded, addStart = False, addEnd = False, reverse = False):
    #     if reverse:
    #         decoded.reverse()
    #     if addStart:
    #         decoded = [self.start] + decoded
    #     if addEnd:
    #         decoded = decoded + [self.end]
    #     encoded = [self.encodeSym(symbol) for symbol in decoded]
    #     return encoded

    # Decodes an integer into its symbol 
    def decodeId(self, enc):
        return self.id2sym[enc] if enc < self.getNumSymbols() else self.unknown

    # '''
    # Decodes a sequence of integers into their symbols.
    # If delim is given, joins the symbols using delim,
    # Optionally reverse the resulted sequence 
    # '''
    # def decodeSeq(self, encoded, delim = None, reverse = False, stopAtInvalid = True):
    #     length = 0
    #     for i in range(len(encoded)):
    #         if not self.isValid(self.decodeId(encoded[i])) and stopAtInvalid:
    #         #if not self.isValid(encoded[i]) and stopAtInvalid:
    #             break
    #         length += 1
    #     encoded = encoded[:length]

    #     decoded = [self.decodeId(enc) for enc in encoded]
    #     if reverse:
    #         decoded.reverse()

    #     if delim is not None:
    #         return delim.join(decoded)
        
    #     return decoded

# objsDict = SymbolDict(empty = True)
# attrsDict = SymbolDict(empty = True) 
# relsDict = SymbolDict(empty = True)
# descDict = SymbolDict()
# # # TODO: AVG SENTENCE WORDS!!

# with open(idFilename, "r") as idFile:
#     imgsInfo = json.load(idFile)
#     for i in tqdm(range(len(imgsInfo))):
#         imgInfo = imgsInfo[i]
#         vgId = str(imgInfo["image_id"])
#         cocoId = str(imgInfo["coco_id"])
#         #data[cocoId] = {}
#         data[vgId] = {}
#         vgId2Id[vgId] = cocoId

# with open("vg2coco.json", "w") as outFile:
#     json.dump(vgId2Id, outFile)

# with open(objectsFilename, "r") as objectsFile:
#     imgsInfo = json.load(objectsFile)
#     for i in tqdm(range(len(imgsInfo))):
#         imgInfo = imgsInfo[i]
#         vgId = str(imgInfo["image_id"])
#         # cocoId = vgId
#         #cocoId = vgId2Id[vgId]
#         instance = data[vgId]
#         instance["coco"] = imgInfo["coco_id"]
#         instance["objects"] = {}
#         instance["refs"] = {}
#         for obj in imgInfo["objects"]:
#             objId = str(obj["object_id"])
#             instance["objects"][objId] = {
#                 "x0": obj["x"],
#                 "y0": obj["y"],
#                 "w": obj["w"],
#                 "h": obj["h"],
#                 "size": obj["w"] * obj["h"],
#                 "x1": obj["x"] + obj["w"],
#                 "y1": obj["y"] + obj["h"],
#                 "xc": float(x1 + x0) / 2,
#                 "yc": float(y1 + y0) / 2,
#                 "name": obj["names"][0],# obj.get("name", obj.get("names", ["NoName"])[0]),
#                 "outRels": [],
#                 "inRels": []
#             }
#             if len(obj["names"]) > 1:
#                 print(obj["names"])

#             if "merged_object_ids" in obj:
#                 for otherId in obj["merged_object_ids"]:
#                     instance["refs"][str(otherId)] = objId

#             #print(obj)
#             # if "name" in obj:
#             #     print(obj)

#             # if "name" not in obj and "names" not in obj:
#             #     print(obj)
#             if len(obj["names"]) > 1:
#                 print(obj)
#             objsDict.addSymbols(obj["names"][0]) # obj.get("name", "NoName")

# with open(attributesFilename, "r") as attributesFile:
#     imgsInfo = json.load(attributesFile)
#     for i in tqdm(range(len(imgsInfo))):
#         imgInfo = imgsInfo[i]
#         vgId = str(imgInfo["image_id"])
#         # cocoId = vgId
#         #cocoId = vgId2Id[vgId]
#         instance = data[vgId]
#         for obj in imgInfo["attributes"]:
#             objId = str(obj["object_id"])
#             if objId in instance["objects"]:
#                 o = instance["objects"][objId]
#             elif objId in instance["refs"]:
#                 o = instance["objects"][instance["refs"][objId]]
#             else:
#                 continue  
                             
#             if "attributes" in obj:
#                 o["attributes"] = obj.get("attributes",[])
#                 attrsDict.addSymbols(obj.get("attributes",[]))           

# with open(relationsFilename, "r") as relationsFile:
#     imgsInfo = json.load(relationsFile)
#     for i in tqdm(range(len(imgsInfo))):
#         imgInfo = imgsInfo[i]
#         vgId = str(imgInfo["image_id"])
#         # cocoId = vgId
#         #cocoId = vgId2Id[vgId]
#         instance = data[vgId]
#         for rel in imgInfo["relationships"]:
#             relName = rel["predicate"]
#             subjId = str(rel["subject"]["object_id"])
#             objId = str(rel["object"]["object_id"])
#             subjId = subjId if subjId in instance["objects"] else instance["refs"].get(subjId)
#             if subjId is None:
#                 continue
#             objId = objId if objId in instance["objects"] else instance["refs"].get(objId)
#             if objId is None:
#                 continue
#             # subjN = instance["objects"][subjId]["name"]
#             # objN = instance["objects"][objId]["name"]
#             rel = {"rel": relName, "subj": subjId, "obj": objId} # , "subjN": subjN, "objN": objN
#             #s = 
#             # instance["objects"].get(subjId, instance["objects"][instance["refs"][subjId]])
#             #o = 
#             # instance["objects"].get(objId, instance["objects"][instance["refs"][objId]])
#             if subjId is not None and objId is not None:
#                 instance["objects"][subjId]["outRels"].append(rel)
#                 instance["objects"][objId]["inRels"].append(rel)
#             # if (subjId is not None and objId is None) or (objId is not None and subjId is None):
#             #     print(rel)
#             relsDict.addSymbols(relName)

# descriptions
# with open(objectsFilename, "r") as objectsFile:
#     imgsInfo = json.load(objectsFile)
#     for i in tqdm(range(len(imgsInfo))):
#         imgInfo = imgsInfo[i]
#         vgId = str(imgInfo["image_id"])
#         cocoId = vgId
#         #cocoId = vgId2Id[vgId]
#         instance = data[cocoId]
#         instance["descriptions"] = {}
#         if "regions" in imgInfo:
#             for region in imgInfo["regions"]:
#                 regionId = str(region["region_id"])
#                 desc = vqaProcessText(region["phrase"], True, True)
#                 instance["descriptions"][regionId] = {
#                     "x": region["x"],
#                     "y": region["y"],
#                     "w": region["w"],
#                     "h": region["h"],
#                     "desc": desc,
#                 }
#                 descDict.addSymbols(desc)
        # else:
        #     print([k for k in imgInfo])

# writeVocabs()

# def writeVocabs():
# objsDict.createVocab()
# attrsDict.createVocab()
# relsDict.createVocab()
# descDict.createVocab()
#"objs"

def toStr(synset):
    return str(synset)[8:-2]

# def toTxt(name, pos):
#     with open(outJson(name), "r") as f:
#         count = json.load(f)

#     with open(outTxt(name), "w") as f:
#         for i in tqdm(range(len(count))):
#             try:
#                 f.write(count[i][0]+","+str(count[i][1])+"\t"*4)

#                 f.write(str(en.noun.antonym(count[i][0]))+"\t")
#                 f.write(str(en.is_noun(count[i][0]))+" ")
#                 f.write(str(en.is_adjective(count[i][0]))+" ")
#                 f.write(str(en.is_verb(count[i][0]))+"\t")
#                 if en.is_verb(count[i][0]):
#                     try:
#                         f.write(str(en.verb.is_past_participle(count[i][0]))+"\t")
#                         f.write(str(en.verb.infinitive(count[i][0]))+"\t")
#                     except:
#                         pass                
#                 wn = wn.synsets(count[i][0])
#                 wn = [toStr(w) for w in wn][:1]
#                 f.write(" ".join(wn)+"\t")      
#                 typedWn = wn.synsets(count[i][0], pos = pos)
#                 flag = False
#                 if len(typedWn) > 0:
#                     typedWn = typedWn[0]
#                     flag = True
#                 else:
#                     typedWn = wn.synsets(count[i][0])
#                     if len(typedWn) > 0:
#                         typedWn = typedWn[0]
#                         flag = True
#                 if flag:
#                     # str(lemma.name()) for lemma in wn.synset('dog.n.01').lemmas()
#                     f.write(toStr(typedWn)+"\t")
#                     try:
#                         lemmas = typedWn.lemmas()
#                         if len(lemmas) > 0:
#                             lemma = lemmas[0].name()
#                             f.write(lemma+"\t")
#                             #f.write(" ".join(map(toStr, typedWn.antonyms()))+"\t")
#                     except:
#                         f.write("_\t")
                    
#                     try:
#                         attributes = typedWn.attributes()
#                         if len(attributes) > 0:
#                             f.write("A-")
#                             f.write("-".join(map(toStr, attributes))+"\t")
#                     except:
#                         f.write("-\t")          
#                     f.write(str(en.noun.hypernyms(count[i][0])))
#                     # f.write("->".join(map(toStr, typedWn.hypernyms()))+"\t")                        
#                     # f.write("->".join(map(toStr, typedWn.hypernyms()))+"\t")
#             except:
#                 f.write("_"+","+str(count[i][1])+"\t"*4)
#             f.write("\n")

# toTxt("objs", wordnet.NOUN)
# toTxt("attrs", wordnet.ADJ)
# toTxt("rels", wordnet.VERB) 

# with open(outJson("attrs"), "r") as f:
#     attrsCount = json.load(f)

# attrsDict = {}
# for a in attrsCount:
#   attrsDict[a[0]] = {}

# with open(outJson("rels"), "rb") as f:
#     relsCount = json.load(f)

with open("combs.json") as f:
   combList = json.load(f)

combDict = defaultdict(list)
for comb in combList:
    a, o = comb.split(" ")
    combDict[o].append(a)

if args.normalize:
    with open(dataFilename) as f:
       data = json.load(f)

objCats = {
    "None": ['thing', 'meal', 'drink', 'alive', 'building', 'part', 'symbol', 'place', 'env', 'sign', ""],
    'env': ["nature environment", "urban environment"],
    'thing': ['food', "object", 'clothing', "office supplies", 'sauce', 'ingredient', 'textile', 'label'],
    "object": ['furniture', 'appliance', 'device', "toy", 'tableware', 'container', 'bottle', 'bag',
               'cooking utensil', 'footwear', 'accessory', 'vehicle', 'instrument', 'weapon'],
    'food': ["fruit", "vegetable", "dessert", 'baked good', 'meat', 'fast food'],
    'fruit': [], 'vegetable': [], 'pastry': [], 'fast food': [], 'dessert': [], 'baked good': ["pastry"], 
    'meat': [], 'sauce': [], 'meal': [], 'drink': [], 'ingredient': [], "textile": [],
    'furniture': [], 'appliance': [], 'device': [], "toy": [],
    'tableware': ["utensil"], 'utensil': [], 'cooking utensil': [],
    'alive': ['person', 'animal', 'plant', 'pokemon'], "pokemon": [],
    'person': [], 'animal': ['bird'], 'plant': ['tree'], 'tree': [], 'bird': [], 'sign': [], 'bag': [], 
    'clothing': [], 'footwear': [], 'accessory': [],
    'vehicle': ['watercraft', 'aircraft'],
    'watercraft': [], 'aircraft': [], 'building':[],
    'part': ["body part", "vehicle part"],
    "body part": [], "vehicle part": [],
    'place': ["room", 'road'], 
    "room": [], 'road': [], 'nature environment': [], 'urban environment': [], 'symbol': [],
    "": [], 'label': [], "office supplies": [], "container": [], 'bottle': [], 'instrument': [], 'weapon': []
}

parent = {}
for p in objCats:
    for c in objCats[p]:
        parent[c] = p

opposites = {
    ("orange", "apple"),
    ("oranges", "apples"),
    ("apple", "pier"),
    ("strawberry", "cherry"),
    ("fruit", "vegetable"),
    ("salad", "soup"),
    ("hamburger", "pizza"),
    ("chicken", "meat"),
    #("egg", "cheese"),
    ("pasta", "noodles"),
    ("pasta", "rice"),
    ("muffin", "croissant") ,
    ("ketchup", "mustard"),
    ("tomato", "cucumber"),
    ("olives", "mushrooms"),
    ("lettuce", "broccoli") ,
    ("wine", "beer"),
    ("water", "juice"),
    ("coffee", "tea"),
    ("sofa", "bed"),
    ("cookie", "cake"),
    ("fork", "knife"),
    ("girl", "boy"),
    ("girls", "boys"),
    ("man", "woman"),
    ("men", "women"),
    ("goat", "sheep"),
    ("horse", "donkey"),
    ("horses", "donkeys"),
    ("horse", "cow"),
    ("horses", "cows"),
    ("dog", "cat"),
    ("dogs", "cats"),
    ("swan", "duck"),
    ("horse", "zebra"),
    ("horses", "zebras"),
    ("boots", "sandals"),
    ("bus", "train"),
    ("bus", "truck"),
    ("bike", "motorcycle")
}

oppositesDict = {}
for pair in opposites:
    x,y = pair
    oppositesDict[x] = y
    oppositesDict[y] = x

# def pluralOf(objname):
#     return en.noun.plural(singularOf(objname))

# def singularOf(objname):
#     return en.noun.singular(objname)

# # good?
# def isPluralUnk(objName):
#     return pluralOf(objName) != objName

# # def isSingular(objName):
# #     if not isSingular(objName)

def mod(o):
    if o in objDict:
        return  objDict[o]["mod"]
    return None

def isPlural(o):
    return mod(o) == "plural"

def isSingular(o):
    return mod(o) == "singular"

def isMass(o):
    return mod(o) == "mass"

def singularOf(objname):
    return en.noun.singular(objname)

def pluralOf(objname):
    return en.noun.plural(singularOf(objname))

def type(a,o):
    if o is not None and a in o["senses"]:
        return o["senses"][a]
    if a in attrDict:
        clist = attrDict[a]["cat"]
        if len(clist) == 1:
            return clist[0]
    return None

def cat(o):
    oname = o["name"] 
    if "senses" in o and "o_" + oname in o["senses"]:
        return o["senses"]["o_" + oname]
    if oname in objDict:
        return objDict[oname]["cat"]
    return None

def catn(oname):
    if oname in objDict:
        return objDict[oname]["cat"]
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

def commonAns(c1, c2):
    p1 = ancestors(c1)
    p2 = ancestors(c2)
    i = 0
    while i < min(len(p1), len(p2)) and p1[i] == p2[i]:
        i += 1
    i -= 1
    return p1[i]

def isA(o, cq):
    c = cat(o)
    if c is None:
        return False
    ans = ancestors(c)
    return cq in ans #() or (c == o)

def isAlist(o, clist): # return sublist?
    c = cat(o)
    if c is None:
        return False    
    ans = ancestors(c)
    for cq in clist:
        if cq in ans:
            return True
    return False

def partOfRate(o1, o2):
    if (isA(o1, "body part") and isA(o2, "alive")) or \
        (isA(o1, "vehicle part") and isA(o2, "vehicle")):
        return inclusionRate(coords(o1), coords(o2))
    return 0.0

def objs(c, main = True):
    objList = []
    objList += cats["o"]["main" if main else "extra"]
    for s in objCats[c]:
        objList += objs(s, main)
    return objList

def allObjs(c):
    return objs(c, True) + objs(c, False)

def removeSubword(inputStr, blacklist):
    inputStr.replace(".", "")
    inputStr.replace("made of", "madeof")
    words = inputStr.split()
    words = [w for w in words if w not in blacklist]
    ret = " ".join(words)
    return ret

def numsNormalize(inputStr):
    if unicode(inputStr).isnumeric():
        return "number"
    return inputStr

def coords(o):
    return (o["x0"], o["y0"], o["x1"], o["y1"])

def valid(c):
    for cc in c:
        if cc < 0:
            return False
    return True

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

def overlapRelaxed(r1, r2):
    i = intersection(r1, r2)
    if i is None:
        return False
    p1 = percent(i, r1)
    p2 = percent(i, r2)
    p = max(p1,p2)
    return p > args.interThrRelaxed

def relativeleft(c1, c2):
    return overlap(yrange(c1), yrange(c2)) and leftrange(xrange(c1), xrange(c2)) and closerange(xrange(c1), xrange(c2))

def relativeright(c1, c2):
    return overlap(yrange(c1), yrange(c2)) and rightrange(xrange(c1), xrange(c2)) and closerange(xrange(c2), xrange(c1))

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

def allImage(c):
    return size(c) > args.aSize

def mainImage(c):
    return size(c) > args.mSize

def main(c1, c2):
    return size(c1) > args.bigSizeThr * size(c2)

def inclusionRate(c1, c2):
    if size(c1) == 0:
        return 0
    isize = length(intersection(xrange(c1), xrange(c2))) * length(intersection(yrange(c1), yrange(c2)))
    inclusionRate = float(isize) / size(c1)
    return inclusionRate

def inside(c1, c2):
    return inclusionRate(c1, c2) > args.iSize

def onMargin(c):
    x = xrange(c)
    y = yrange(c)
    xm = x[1] < args.margin or x[0] > 1 - args.margin
    ym = y[1] < args.margin or y[0] > 1 - args.margin
    return xm or ym

def addAttr(hashTable, objId, name, score):
    if name not in hashTable:
        hashTable[name] = {}     
    hashTable[name][objId] = score
    # hashTable[name].append((objId, score))

def addObjCat(hashTable, objId, name, score, obj):
    if name not in hashTable:
        hashTable[name] = {"objs": {}, "attr2obj": {}}
    hashTable[name]["objs"][objId] = score
    # hashTable[name]["objs"].append((objId, score))

    if "attributes" in obj:
        for attr in obj["attributes"]:
            addAttr(hashTable[name]["attr2obj"], objId, attr, score)

    if "pos" in obj:
        for pos in obj["pos"]:
            addAttr(hashTable[name]["attr2obj"], objId, pos, score)

    if "predAttributes" in obj:
        for attr, attrScore in obj["predAttributes"]:
            addAttr(hashTable[name]["attr2obj"], objId, attr, score * attrScore)

def addObj(hashTable, objId, name, score, obj):
    name = singularOf(name) if isPlural(name) else name
    addObjCat(hashTable, objId, name, score, obj)

    parents = ancestors(cat(obj)) #name
    for p in parents:
        addObjCat(hashTable, objId, p, score, obj)

def hashObjs(hashTable, objDict):
    for objId in objDict:
        obj = objDict[objId]
        if "name" in obj:
            addObj(hashTable, objId, obj["name"], 1.0, obj)
        if "preds" in obj:
            for pred in obj["preds"]:
                addObj(hashTable, objId, pred[0], pred[1], obj)

    return hashTable

def addItem2set(d, k, v):
    if k not in d:
        d[k] = set()
    d[k].add(v)

def addItem2dict(d, k, vk, vv):
    if k not in d:
        d[k] = {}
    d[k][vk] = vv

# objList = set()
# with open("classes_vocab.txt", "r") as f:
#     for obj in f.readlines():
#         objList.add(obj.split(",")[0].lower().strip())

# # if args.attr:
# attrList = set() 
# with open("attrs_vocab.txt", "r") as f:
#     for obj in f.readlines():
#         attrList.add(obj.split(",")[0].lower().strip())

# # if args.attr:
# relList = set()
# with open("relations_vocab.txt", "r") as f:
#     for obj in f.readlines():
#         relList.add(obj.split(",")[0].lower().strip())

with open("vg14/cObjsNV.json", "r") as f:
    objDict = json.load(f)

with open("vg14/cAttrsNV.json", "r") as f:
    attrDict = json.load(f)

with open("vg14/cRelsNV.json", "r") as f:
    relDict = json.load(f)

with open("vg14/info_relObjDictNew.json", "r") as f:
    roDict = json.load(f)

with open("vg14/info_attrsObjsNew.json", "r") as f:
    aoDict = json.load(f)

objList = objDict.keys() # ["main"] + objDict["extra"].keys()
attrList = attrDict.keys()
relList = relDict.keys()

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
        #text = obj["name"] + ("({})".format(",".join([x["rel"]+"-"+x["subjN"]+"-"+x["objN"] for x in obj["relations"]])) if "relations" in obj and len(obj["relations"]) > 0 else "")
        #ax.text(obj["x"], obj["y"], text, style='italic', bbox={'facecolor':'white', 'alpha':0.7, 'pad':10})
        # i += 1
    # fig = plt.gcf()
    plt.tick_params(labelbottom='off', labelleft='off')
    #plt.show()
    plt.savefig("photos/"+imageId+"Data.jpg", dpi = 720) # +"_"+str(j)
    plt.close(fig)

def oName(instance, rel):
    return instance["objects"][rel["obj"]]["name"]

def sName(instance, rel):
    return instance["objects"][rel["subj"]]["name"]

opsList = [
    (["covering"], ["covered by"]),
    (["behind", "in back of"], ["in front of"]),
    (["above"], ["below", "under", "beneath", "underneath"]),
    (["left of"], ["right of"]),
    (["near", "next to"], ["near", "next to"]),
    # (["surrounding"], ["surrounded by"]),
    # (["supporting"], ["supported by"]),
    (["decorating"], ["decorated with"])
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

def normalize():
    translateDict = {
        "icecream": "ice cream",
        "sprinkle": "sprinkles",
        "snowpants": "snow pants",
        "handbag": "purse",
        "cab": "taxi",
        "grey": "gray",
        "big": "large",
        "wooden": "wood",
        "blonde": "blond",
        "doughnut": "donut",
        "racquet": "racket",
        "doughnuts": "donuts",
        "t shirt": "t-shirt",
        "tshirt": "t-shirt",
        "brocolli": "broccoli",
        # "moustache": "mustache",
        "hotdog": "hot dog",
        "back pack": "backpack",
        "tee shirt": "t-shirt",
        "potatoe": "potato",
        "tomatoe": "tomato",
        "teddy": "teddy bear",
        "racquet": "racket",
        "sandwhich": "sandwich",
        "googles": "goggles",
        "lot": "parking lot",
        "disk": "disc",
        "omelet": "omelette",
        "coffe table": "coffee table",
        "whip cream": "whipped cream",
        "wild flowers": "wildflowers",
        "flower bouquet": "bouquet",
        "flower vase": "vase",
        "coffe maker": "coffee maker",
        "hot dog bun": "hotdog bun",
        "m&m candy": "candy",
        "eye glass": "eye glasses",
        "powder sugar": "powdered sugar",
        "coca cola": "coke",
        "coca-cola": "coke",
        "cola": "coke",
        "coffee machine": "coffee maker",
        "jump suit": "jumpsuit",
        "news paper": "newspaper",
        "book shelf": "bookshelf",
        "book shelves": "bookshelves",
        "cup cake": "cupcake",
        "plane": "airplane",
        "planes": "airplanes",
        "hill side": "hillside",
        "fire place": "fireplace",
        "art work": "artwork",
        "hill top": "hilltop",
        "licence plate": "license plate",
        "motor bike": "motorbike",
        "taxi cab": "taxi",
        "wheel chair": "wheelchair",
        "mom": "mother",
        "cheese cake": "cheesecake",
        "brief case": "briefcase",
        "coffeemaker": "coffee maker",
        "freezer": "refrigerator",
        "fridge": "refrigerator",
        "dish washer": "dishwasher",
        "bicyclist": "cyclist",
        "human": "person",
        "kid": "child",
        "kids": "children",
        "motorcyclist": "biker",
        "bus station": "bus stop",
        "bus terminal": "bus stop",
        "airport terminal": "airport",
        "arm rest": "armrest",
        "doorknob": "knob",
        "door knob": "knob",
        "door handle": "handle",
        "oven handle": "handle",
        "moustache": "mustache",
        "elephant trunk": "trunk",
        "light house": "lighthouse",
        "night stand": "nightstand",
        "cheese grater": "grater",
        "wii control": "wii controller",
        "remote controller": "remote control",
        "tv remote": "remote control",
        "control": "remote control",
        "remote": "remote control",
        "controls": "controllers",
        "computer keyboard": "keyboard",
        "laptop computer": "laptop",
        "cellphones": "cell phones",
        "mobile phone": "cell phone",
        "cellphone": "cell phone",
        #"dvd": "dvd player",
        "wii remote": "wii controller",
        "tv": "television",
        "computer speaker": "speaker",
        "police officer": "policeman",
        "mangos": "mangoes",
        "wrist watch": "wristwatch",
        "neck tie": "tie",
        "necktie": "tie",
        "sun glasses": "sunglasses",
        "wrist band": "wristband",
        "hair band": "headband",
        "head band": "headband",
        "candy cane": "candy",
        "candy corn": "candy",
        "cheerios": "cereal",
        "asian food": "chinese food",
        "fry": "french fry",
        "sandwhich": "sandwich",
        "veggie": "vegetable",
        "veggies": "vegetables",
        "condiments": "spices",
        "spaghetti": "pasta",
        "slice of bread": "bread",
        "slice of pizza": "pizza slice",
        "apple slice": "apple",
        "bread slice": "bread",
        "lemon slice": "lemon",
        "potato slice": "potato",
        "pickle slice": "pickle",
        "banana slice": "banana",
        "carrot slice": "carrot",
        "cucumber slice": "cucumber",
        "mushroom slice": "mushroom",
        "olive slice": "olive",
        "onion slice": "onion",
        "pepper slice": "pepper",
        "pepperoni slice": "pepperoni",
        "tomato slice": "tomato",
        "cake slice": "cake",
        "mozzarella cheese": "mozzarella",
        "shrub": "bush",
        "shrubs": "bushes",
        "sea weed": "seaweed",
        "bicycle": "bike",
        "bicycles": "bikes",
        "motorbike": "motorcycle",
        "motorbikes": "motorcycles",
        "bell pepper": "pepper",
        "bell peppers": "peppers",
        "cherry tomato": "tomato",
        "grape tomato": "tomato",
        "cherry tomatoes": "tomatoes",
        "chop sticks": "chopsticks",
        "teaspoon": "spoon",
        "serving spoon": "spoon",
        "crocodile": "alligator",
        "sea gull": "seagull",
        "meat ball": "meatball",
        "kayak": "canoe",
        "palm": "palm tree",
        "palms": "palm trees",
        "pine": "pine tree",
        "pines": "pine trees",
        "oak": "oak tree",
        "french fries": "fries",
        "wineglass": "wine glass",
        "food tray": "serving tray",
        "kitchen utensil": "cooking utensil",
        "kitchen utensils": "cooking utensils",
        "snow suit": "snowsuit",
        "swim suit": "swimsuit",
        "wet suit": "wetsuit",
        "trousers": "pants",
        "eraser": "rubber",
        "rubber ducky": "rubber duck",
        "cookie sheet": "baking sheet",
        "condiment": "spice",
        "mouse": "computer mouse", #???????????
        "side walk": "sidewalk",
        "dry erase board": "dry-erase board",
        "streetlight": "street light",
        "street lamp": "street light",
        "park bench": "bench",
        # "wire": "cord",
        "traffic signal": "traffic light",
        "signal light": "traffic light",
        "stop light": "traffic light",
        "sea shore": "shore",
        "train track": "train tracks",
        "railway track": "train tracks",
        "railroad track": "train tracks",
        "railroad tracks": "train tracks",
        "shoe strings": "shoe lace", # sole
        "bed spread": "bedspread",
        "bed sheet": "sheet",
        "table cloth": "tablecloth",
        "snow board": "snowboard",
        "surf board": "surfboard",
        "drapery": "drape",
        "draperies": "drapes",
        "pillow case": "pillowcase",
        "skate board": "skateboard",
        "safety cone": "cone",
        "traffic cone": "cone",
        "hydrant": "fire hydrant",
        "extinguisher": "fire extinguisher",
        "mousepad": "mouse pad",
        "beach sand": "sand",
        "bulb": "light bulb",
        "bulbs": "light bulbs",
        "pepper grinder": "pepper shaker",
        "tissue paper": "tissue",
        "lamp post": "street light",
        "light post": "street light",
        "utility pole": "telephone pole",
        "counter top": "countertop",
        "bath tub": "bathtub",
        "tub": "bathtub",
        "fish tank": "aquarium",
        "satellite": "satellite dish",
        "pier": "dock",
        "place mat": "placemat",
        "water hose": "hose",
        "ice cream cone": "ice-cream cone",
        "movies": "dvds",
        "head board": "headboard",
        "switch": "light switch",
        "stove burner": "burner",
        "stove top": "burner",
        "bathing suit": "swimsuit",
        "garbage": "trash",
        "litter": "trash",
        "life vest": "life jacket",
        "plant pot": "flower pot",
        "clay pot": "flower pot",
        "crock pot": "cooker",
        "trashcan": "trash can",
        "train engine": "locomotive",
        "tap": "faucet",
        "garbage can": "trash can",
        "trash bin": "trash can",
        "waste bin": "trash can",
        "dog collar": "collar",
        "telephone": "phone",
        "eyeglasses": "eye glasses",
        "sunglasses": "sun glasses",
        "basil leaf": "basil",
        "spinach leaf": "spinach",
        "vegetable leaf": "vegetable",
        "lettuce leaf": "lettuce",
        "broccoli leaf": "broccoli",
        "basil leaves": "basil",
        "spinach leaves": "spinach",
        "vegetable leaves": "vegetable",
        "lettuce leaves": "lettuce",
        "broccoli leaves": "broccoli",
        "skatepark": "skate park",
        "shoelace": "shoe lace",
        "pool": "swimming pool",
        "oar": "paddle",
        "eggshell": "egg shell",
        "bouy": "buoy",
        "suit case": "suitcase",
        "powerline": "power line",
        "powerlines": "power lines",
        "lightbulb": "light bulb",
        "treee": "tree",
        "scissor": "scissors",
        "shoreline": "shore line",
        "quilt": "comforter",
        "bed cover": "comforter",
        "frying pan": "pan",
        "dish towel": "towel",
        "hand towel": "towel",
        "dishtowel": "towel",
        "wreath": "garland",
        "smartphone": "cell phone",
        "smart phone": "cell phone",
        "iphone": "cell phone",
        "duvet": "comforter"
    }

    # TODO: remove very / is / are
    translateDictA = {
        "racquet": "racket",
        "grey": "gray",
        "big": "large",
        "wooden": "wood",
        "blonde": "blond",
        "doughnut": "donut",
            # "dirt": "dirty",
        "metallic": "metal",
        "cement": "concrete",
        "golden": "gold",
        "circular": "round",
        "rusted": "rusty",
        "snow covered":"snowy",
        "snow-covered":"snowy",
        "multicolored": "colorful",
        "multi-colored": "colorful",
        "multi colored": "colorful",
        "electrical": "electric",
        "oval": "round",
        "squared": "square",
             # "grass": "grassy",
        "pointed": "pointy",
        "opened": "open",
        "unopened": "closed",
        "long sleeve": "long sleeved",
        "short sleeve": "short sleeved",
        "short-sleeved": "short sleeved",
        "long-sleeved": "long sleeved",
        "rectangle": "rectangular",
        "circle": "round",
        "light green": "green",
        "bright green": "green",
        "bright blue": "blue",
        "dark green": "green",
        "blurred": "blurry",
            # "tile": "tiled",
        "upside-down": "upside down",
        "cream": "cream colored",
        "dark grey": "gray",
        "seated": "sitting",
        "sitting down": "sitting",
        "burgundy": "maroon",
        "turquoise": "teal",
        "stainless": "stainless steel",
        "turned off": "off",
        "turned on": "on",
        "colorfull": "colorful",
        "cream-colored": "cream colored",
        "not healthy": "unhealthy",
        "dark gray": "gray",
        "navy blue": "blue",
        "rainbow": "rainbow colored",
        "white color": "white",
        "light pink": "pink",
        "neon green": "green",
        "greenish": "green",
            # "stripes": "striped",
        "clear blue": "blue",
              # "decoration": "decorative",
        "brownish": "brown",
        "bright yellow": "yellow",
        "light grey": "gray",
        "bright red": "red",
        "reddish": "red",
        "dark red": "red",
        "bright orange": "orange",
        "white colored": "white",
        "light gray": "gray",
        "polka dot": "dotted",
        "deep blue": "blue",
        "half-full": "half full",
             # "bricks": "brick",
        "checked": "checkered",
              # "stack": "stacked",
        "laying": "lying",
        "laying down": "lying",
        "lying down": "lying",
        "triangle": "triangular",
        "octagon": "octagonal",
        "chain link": "chain-link",
        "chainlink": "chain-link",
        "light-colored": "light colored",
        "dark-colored": "dark colored",
        "knitted": "knit",
        "glassy": "glass",
               # "sand": "sandy",
        "whtie": "white",
        "gree": "green",
        "burned": "burnt",
        "bricked": "brick",
        "jean": "denim",
        "turned on": "on",
        "old-fashioned": "old fashioned",
        "oval shaped": "round",
        "marbled": "marble"
    }    
    translateDictR = {
        "wears": "wearing",
        "rides": "riding",        
        "beside": "next to",
        "has": "have",
        "holds": "holding",
        "inside of": "inside",
        "next": "next to",
        "has on": "wears",
        "atop": "on top of",
        "containing": "contain",
        "contains": "contain",
        "on top": "on top of",
        "covers": "covering",
        "front": "in front of",
        "at front of": "in front of",
        "front of": "in front of",
        "wearing blue": "wearing",
        "outside of": "outside",
        "on side": "on side of",
        "surrounds": "surrounding",
        "beside of": "next to",
        "besides": "next to",
        "sits in": "sitting in",
        "carries": "carrying",
        "to right of": "right of",
        "to left of": "left of",
        "left to": "left of",
        "right to": "right of",
        "on h": "on",
        "hold": "holding",
        "at bottom of": "at the bottom of",
        "casts": "casting",
        "i": "in",
        "stand in": "standing in",
        "in h": "in",
        "carry": "carrying",
        "swings": "swinging",
        "in front": "in front of",
        "eats": "eating",
        "wear": "wearing",
        "watches": "watching",
        "supports": "supporting",
        "on side": "on side of",
        "on her": "on",
        "casted on": "cast on",
        "part of": "a part of",
        "apart of": "a part of",
        "looks at": "looking at",
        "laying on": "lying on",
        "laying in": "lying in",
        "laying": "lying",
        "on mans": "on",
        "at end of": "at the end of",
        "hits": "hitting",
        "reads": "reading",
        "watch": "watching",
        "plays": "playing",
        "stands on": "standing on",
        "uses": "using",
        "surround": "surrounding",
        "in corner of": "in the corner of",
        "in middle of": "in the middle of",
        "in back of": "in the back of",
        "in center of": "in the center of",
        "on back of": "on the back of",
        "on bottom of": "on the bottom of",
        "on edge of": "on the edge of",
        "on front of": "on the front of",
        "on left side of": "on the left side of",
        "on right side of": "on the right side of",
        "on side of": "on the side of",
        "on surface of": "on the surface of",
        "cover": "covering",
        "at top of": "at the top of",
        "on edge of": "on the edge of",
        "attached": "attached to",
        "at edge of": "at the edge of",
        "on front": "on the front of",
        "sits on": "sitting on",
        "hangs from": "hanging from",
        "hangs on": "hanging on",
        "hang on": "hanging on",
        "belongs to": "belong to",
        "belonging to": "belong to",
        "touches": "touching",
        "sells": "selling",
        "faces": "facing",
        "pulls": "pulling",
        "throws": "throwing",
        "laying down on": "lying on",
        "catches": "catching",
        "cuts": "cutting",
        "leading to": "lead to",
        "leads to": "lead to",
        "eat": "eating",
        "walks on": "walking on",
        "attatched to": "attached to",
        "feeds": "feeding",
        "takes": "taking",
        "drinks": "drinking",
        "on other side of": "on the other side of",
        # "in between": "between"
        # "rests on": "resting on",
        # "stands in": "standing in",
        # "sit on": "sitting on",
        # "crosses": "crossing"
    }

    commonAdjs = ['white','black','blue','green','red','brown','yellow',
        'small','large','silver','wooden','orange','gray','grey','metal','pink','tall',
        'long','dark',"short", 'front','right','left','glass','stone','brick','wooden','plastic',
        "blonde","blond","grassy","leafy","tennis","baseball","soccer","football"]

    matDict = {"bricks": "brick", "stones":"stone", "rocks": "rock"}
    matList = ["wood", "brick", "stone", "rock", "glass", "wire", "concrete",
               "metal", "iron", "cobblestone", "cement", "leather", "steel", "hardwood"]
    # actList = ["sitting", "standing", "walking", "riding", "eating", "playing", "sitting", "parked", "flying", "enjoying"]
    colors = ["white", "black", "blue", "red", "brown", "orange", "green", "yellow", "gray", "silver", "tan", "pink", "gold"]
    directions = ["down", "up", "left", "right", "away", "forward", "ahead", "out", "outside", "behind", "back", "upward", "straight", 
                  "downward", "sideways", "at camera", "in mirror", "downwards", "upwards", "backwards"]
    facingDirections = ["left", "right", "the same direction", "the camera", "away", "front", "back"]

    passive = {"reflecting": "reflected by", "pulled by": "pulling", "being held by": "holding", "displaying": "displayed on", "carried by": "carrying", "worn by": "wearing",
               "held by": "holding", "surrounding": "surrounded by", "topping": "topped with", "cast by": "casting", 
               "covered by": "covering", "forming": "formed by"}
    fixV = ["walking", "standing", "parked", "sitting", "laying"]

    mRelsDict = {
        "pointing": directions,
        "looking": directions,
        "facing": facingDirections,
        "casting": ["shadow"],
        "playing": ["frisbee", "tennis", "baseball", "wii", "music", "soccer", "video games", 
            "games", "football", "volleyball", "basketball", "badminton", "cricket"], # game?
        "brushing": ["teeth"],
        "making": ["face"],
        "cut into": ["slices", "squares", "pieces"],
        "taking": ["picture", "photo", "pictures", "photograph", "notes", "photos", "bath"],
        "looking for": ["food", "waves", "fish", "luggage", "shoe", "wave", "seat"],
        "shaking": ["hand", "hands"],
        "holding up": ["peace sign"]
    }

    mRelsObjsDict = {
        "shadow": "a shadow",
        "face": "a face",
        "picture": "a picture",
        "photo": "a photo",
        "photograph": "a photograph",
        "camera": "at the camera",
        "at camera": "at the camera",
        "in mirror": "in the mirror",
        "luggage": "the luggage",
        "shoe": "the shoe",
        "wave": "a wave",
        "seat": "a seat",
        "hand": "hands",
        # "air": "the air"
    }  

    lights = ["light", "sunlight", "lights", "outlet", "colors", "mirror", "shadow", "light", "lights", "shadow", 
        "reflection", "shadow", "glass", "reflection", "sunlight", "lights", "glare", "mirror", "flash"]
    underSubjectBList = ["base", "wood", "concrete", "court", "cement", "platform", "wave", "waves", "ground", "wheel", "water", "skateboard", "floor", 
        "wheels", "surfboard", "road", "pole", "rock", "leg", "trees", "building", "skis", "rocks", "sidewalk", "wall", "bed", "snowboard", "pavement", "tree", 
        "tire", "street", "field", "legs", "ski", "ocean", "hair", "clouds", "mountains", "post", "tower", "leaf", "plant", "hand", "dish", "beach", "bush", 
        "fence", "door", "tires", "food", "home plate", "branch", "runway", "weeds", "bricks", "handle", "head", "cloud", "motorcycle", "mound", "cake", "step", 
        "foot", "trunk", "paw", "strap", "fruit", "jet", "jacket", "feet", "word", "eye", "frisbee", "rope", "ear", "buildings", "tiles", "stone", "broccoli", 
        "nose", "finger", "cushion", "lid", "logo", "number", "pants", "mouth", "vegetable", "umbrella", "shorts", "hill", "steps", "stick", "roof", "paint", 
        "lake", "jeans", "tag", "purse", "fire", "thumb", "tail", "face", "umbrellas", "hills", "glass", "knob", "teeth", "ring", "arm", "walkway", "pillars", 
        "feathers", "words", "collar", "wristband", "wing", "numbers", "city", "airplane", "deck", "chips", "icing", "fur", "sandwich", "sky", "kite", "flag", 
        "sticks", "terrain", "sweatshirt", "mustache", "sock", "suit", "hands", "twig", "vest", "boot", "helmet", "goggles", "cap", "frame", "coat", "soup", 
        "skirt", "porch", "luggage", "fingers", "glasses", "polar bear", "bat", "petal", "parking lot", "socks", "cross", "trucks", "battery", "net", "land", 
        "jar", "handbag", "wrist", "lighthouse", "propeller", "furniture", "crust", "ship", "ceiling", "background", "surfer", "cushions", "label", "doorway", 
        "charger", "sweater", "eyes", "skin", "forest", "couch", "balcony", "arms", "rooftop", "tie"]
    underObjectBList = ["chin", "shore", "sky", "roof", "arm", "water", "shirt", "building", "wing", "foot", "leaves", "vest", "wall", "hand", "leg", "head", 
        "feet", "house", "leaf", "log", "rock", "skier", "ceiling", "words", "tower", "clouds", "airport", "eye", "paw", "nose", "trunk", "player", "batter", 
        "roll", "crust", "hamburger", "logo", "eyes", "meal", "jeans", "fingers", "collar", "clothes", "tree trunk", "lady", "face", "mouth", "ski", "walkway", 
        "number", "ground", "handle", "pants", "neck", "arms", "lip", "tail", "patio", "rain", "cloud", "marker", "weeds"]
    byBlack = ["ground", "dirt", "ground", "weed", "rock", "stone", "leaf", "land", "words", "wood", "waves", "wave"]

    relListing = {
        "standing around": [("w", "s", ["people", "crowd", "mice", "herd", "children"])],
        "sitting around": [("w", "s", ["people", "family", "spectators", "kids", "men", "guys"])],
        "cooking": [("b", "o", ["silver"]), ("w", "s", ["man", "woman", "people", "chef", "guy"])],
        "pulled by": [("b", "o", ["ski"])],
        "jumping in": [("w", "o", ["sky", "snow", "water", "sand", "grass"])],
        "enclosing": [("w", "s", ["fence", "wall", "rocks", "gate", "cable"])],
        "at": [("b", "o", ["curb", "bottom", "night", "light", "edge", "base", "top", "bat", "sand", "end"])],
        "playing": [("b", "o", ["entertainment center", "outside", "indoors", "outdoors", "video", "television", 
            "player", "disk", "players"])],
        "playing in": [("b", "o", ["ground", "hen", "photo", "uniform", "shoes", "shirt", "group"])],
        "talking on": [("w", "o", ["phone", "cell phone"])], # , "banana"
        "topped with": [("b", "o", ["chunk", "antennae", "cross", "sky", "spec", "shaving", "triangle", "bar", 
            "eyebrow", "steeple", "tower", "steak", "meal", "horn", "chef", "candle", 
            "wire", "leaf", "section", "spire", "toppings", "top", "bun", "child", "tile", "building", "man", "hot dog"])],
        "driving": [("b", "o", ["intersection"])],
        "flying": [("b", "o", ["air", "sky", "colors"])],
        "playing on": [("b", "o", ["skateboard", "television", "team", "monitor", "tv", "elephant", "tennis", 
            "controller", "sign", "sheep"])],
        "mixed with": [("b", "o", ["zebra", "dirt", "bowl", "vegetable"]), ("b", "s", ["pea", "giraffe", "brush", "grass"])],
        "running on": [("b", "o", ["wheels", "man", "player", "screen", "person", "player", "boulder"])],
        "pouring": [("w", "o", ["drink", "glass", "bottle"])],
        "selling": [("b", "s", ["sign", "cart", "building", "signs", "watermelons"])],
        "served on": [("b", "o", ["airplane", "plant", "bowl"])],
        "serving": [("b", "o", ["man", "customers", "circles", "spoon", "spatula", "woman", "bears", "plate", 
            "glass", "person"])],
        "displayed in": [("w", "o", ["store", "window", "museum", "exhibit", "room", "cabinet"])],
        "growing on": [("w", "s", ["leaves", "grass", "tree", "trees", "moss", "bush", "bushes", "flower", 
            "flowers", "weeds", "vines", "vine", "bananas", "berry", "blossom", "pear", "oranges", "sunflower", "fruit"])], # "leaf", "weed"
        "walking on": [("b", "o", ["passenger"])],
        "reflecting in": [("b", "s", lights)],
        "reflected in": [("b", "s", lights)],
        "reflected on": [("b", "s", lights)],
        "swimming in": [("w", "o", ["water", "ocean", "lake", "river", "pond", "pool", "aquarium"])],
        "swinging": [("w", "o", ["bat", "racket", "controller", "stick"])],
        "kept in": [("w", "o", ["table", "pot", "zoo", "bed", "box", "case", "cupboard", "desk", "kitchen"])],
        "moving": [("w", "o", ["luggage", "refrigerator", "boat", "bike", "fridge", "bicycle", "freezer", "tail", "furniture", "toothbrush"]), ("w", "s", ["man", "worker", "person", "woman", "girl", "horse", "cars", "chain"])],
        "pointing at": [("w", "s", ["man", "woman", "boy", "person", "child", "girl", "knife", "people", "camera", "arrow"])],
        "growing behind": [("b", "s", ["area", "forest"])],
        "walking to": [("b", "o", ["lot", "steps", "ski", "lift", "left", "track"])],
        "preparing": [("b", "o", ["elephant", "pepper", "good", "batter", "catch", "frisbee", "bat", "ball", "parachute", "drawer", "bikes", "moves"])],
        "wading in": [("b", "o", ["wave"])],
        "smoking": [("w", "o", ["cigarette", "cigar"])],
        "cleaning": [("b", "s", ["paint"])],
        "exiting": [("b", "o", ["wave"])],
        "buying": [("b", "o", ["fruit stands"])],
        "trying to catch": [("b", "o", ["wave"])],
        "dragging": [("b", "o", ["hand"])],
        "eating": [("b", "o", ["pasture", "bird", "building", "fields", "hill", "zebra", "cone", "water", "beer", 
            "bowl", "bag", "hand", "dinning table", "cup", "sky", "plate", "elephant", "people", "phone", "outside", 
            "restaurant", "table", "post", "friend", "fork", "decorations", "controller", "seed", "couch"])],      
        "feeding": [("b", "o", ["trough"])],
        "cooked in": [("b", "o", ["food", "meal", "stir", "fry"])],
        "looking toward": [("b", "o", ["right", "left"])],
        "adjusting": [("b", "o", ["cow"])],
        "eating in": [("b", "o", ["center", "chair"])], 
        "stuck in": [("b", "o", ["slope"])], 
        "looking in": [("b", "o", ["distance", "sky", "field", "door", "bedroom", "airplane", "air"])],
        "riding in": [("b", "o", ["water", "street", "base", "arena", "shallows", "snow", "dirt", "traffic", "road", "ocean", "zoo"])],
        "leading to": [("b", "o", ["sand", "cabinet", "dock", "trolley", "horse", "beam", "fridge", "cars", "computer", "outlet", "foot", "area", "tank", "floor"])],
        "kicking": [("b", "o", ["leg"])],
        "balancing on": [("b", "o", ["finger", "wall"])],
        "growing from": [("b", "o", ["tree", "forest", "plant", "head", "carrot", "bush", "branch", "elephant"])],
        "worn on": [("b", "o", ["man", "person", "woman", "dog", "player", "bear", "skier", "horse", "lady", "male", "girl", "kid", "surfer", "batter", "boy"])],
        "piled on": [("b", "o", ["banana", "orange"]), ("b", "s", ["banana", "box", "apple", "item", "orange", "rock"])],
        "going through": [("b", "o", ["wall", "sidewalk"])],
        "getting on": [("b", "o", ["woman"])],
        "looking into": [("b", "o", ["distance"])],
        "watching": [("b", "o", ["uniform"])],
        "walking with": [("b", "o", ["shirt", "tree", "dinning table"])],
        "walking through": [("b", "o", ["ground"])],
        "wearing": [("b", "o", ["ponytail", "number", "chain", "sleeve", "shades", "jean", "hair", "lipstick", "sleeves", "foot", "saddle", "leash", "stripes", 
            "beard", "makeup", "pair", "head", "man", "feet", "glass", "wrist", "straps", "person", "guard", "guards", "flower", "mustache", "leather", "cup", 
            "eyes"]), ("b", "s", ["skateboard", "snowboard"])],
        "walking down": [("b", "o", ["bricks", "people", "pier", "cobblestone"])],
        "walking behind": [("b", "o", ["grass"])],
        "walking across": [("b", "o", ["concrete", "bricks"])],
        "using": [("b", "o", ["hand", "numerals", "arm", "ramp", "trunk", "arms", "skate park", "sea animal"]), ("b", "s", ["clock"])],
        "touching": [("b", "o", ["wave", "woman", "field", "court", "street", "ocean", "music", "person", "ramp", "mountain"]), ("w", "s", ["man", "hand", 
            "woman", "trunk", "person", "boy", "thumb", "girl", "finger", "cat", "elephant", "foot", "head", "baby", "tail", "paw", "fingers", "giraffe", 
            "people", "child", "fork", "player", "bear", "zebra", "surfer", "horse", "lady", "cow", "kid", "umpire", "toddler", "dog", "pigeon", "kitten", 
            "animal", "donut", "broccoli"])],
        "talking to": [("b", "s", ["gear", "conductor"])],
        "surrounded by": [("b", "o", ["tree", "rock", "hill", "star", "flower", "chair", "tile", "brush", 
            "cloud", "cone", "mountain", "doll", "plastic", "brick", "potato", "fur", "forest", "waves", "broccoli"])],
        "stuck on": [("b", "o", ["stick", "motorcycle"])],
        "standing under": [("b", "o", ["sky", "bathtub"])],
        "standing on top of": [("b", "o", ["court", "snow", "field", "sand", "ground", "floor", "beach", "grass"]), ("b", "s", ["chimney"])],
        "standing next to": [("b", "o", ["game", "branch", "rock",  "boulder", "log", "head", "sticks"]), ("b", "s", ["building", "trees", "flower", "stool", 
            "pole", "light", "lamp", "vase", "suitcase", "container", "utility pole", "can", "bush", "desk", "sofa", "pillar", "fence", "appliance", "shrub", 
            "surfboard"])],
        "standing near": [("b", "o", ["stair"]), ("b", "s", ["pole", "shoe", "sign", "coat"])],
        "standing in front of": [("b", "o", ["brick", "book", "weed", "background", "banana", "grass", "picture"]), ("b", "s", ["pole", "trees", "sign", "bush", 
            "vase", "basket", "pot", "trunk"])],
        "standing by": [("b", "o", ["rock", "belt", "cement", "sand", "wire", "stand", "can", "edge"]), ("b", "s", ["trees"])],
        "standing beside": [("b", "s", ["trees"])],
        "sewn on": [("b", "s", ["scissor"])],
        "resting on": [("b", "o", ["leg", "back", "arm", "knees", "man", "face", "bear", "shoulder", "hand", "cat", "branch", "lap", "nails", "hip", "head", 
            "knee", "beak", "rest", "nose", "paw", "dog"]), ("b", "s", ["hand", "head", "arm", "paw", "leaf", "foot", "elbow", "hands", "arms", "leg", "trunk", 
            "hoof", "paws", "thumb", "tail", "feet", "stick", "ear", "handle", "fingers", "finger", "log", "photograph", "face"])],
        "riding on": [("b", "o", ["road", "street", "water", "beach", "ramp", "sidewalk", "dirt", "highway", "snow", "ocean", "ground", "back", "area", "line", 
            "bridge", "asphalt", "sky", "wave", "waves"]), ("b", "s", ["car", "donut", "stripe"])],
        "shining through": [("b", "o", ["attic", "chair", "bowl"]), ("b", "s", ["sky"])],
        "reading": [("w", "o", ["book", "newspaper", "paper", "magazine", "menu", "brochure", "letters", "map"])],
        "printed on": [("w", "s", ["letter", "logo", "number", "flower", "word", "text", "letters", "words", "arrow", "star", "numbers", "character", "flowers", 
            "symbol"]), ("b", "o", ["clock"])],
        "biting": [("b", "s", ["mouth", "teeth"])],
        "boarding": [("w", "o", ["plane", "bus", "train", "airplane", "boats", "platform"]), ("b", "s", ["fence"])],
        "brushing": [("w", "o", ["teeth", "hair", "lamb", "dog", "elephant", "goat"])],
        "catching": [("w", "o", ["frisbee", "ball", "wave", "baseball", "disk", "bird", "football", "fruit", "softball", "bus", "fish", "waves", "train"]), 
            ("b", "s", ["wave", "arm", "hand", "glove", "sail"])],
        "drawn on": [("b", "o", ["face", "skin", "clock"])],
        "facing": [("b", "o", ["sky"])],
        "making": [("w", "o", ["pizza", "food", "donuts", "sandwich", "kite", "donut", "sandwiches", "pot", "vase", "bread", "cookies", "pancake", "hot dog", 
            "dough", "toast", "bubbles", "fish", "pizzas", "pie", "juice", "snack"])],
        "mounted on": [("w", "s", ["sign", "clock", "mirror", "lamp", "tv", "urinal", "stop sign", "faucet", "television", "outlet", "shelf", "camera", "holder", 
            "engine", "pole", "air conditioner", "sink", "banner", "screen", "speaker", "basket", "dispenser", "cross", "projector", "picture", "weapon", "towel", 
            "knife", "towel dispenser", "shelves", "antenna", "fan", "umbrella", "saddle", "flag", "statue", "burner", "cabinet", "engines", "radiator"])],
        "displayed on": [("b", "o", ["man"]), ("w", "s", ["flower", "sign", "logo", "cake", "pictures", "name", "map", "video game", "game", "item", "award", 
            "decoration", "bananas", "items", "glass"])],
        "driving on": [("b", "o", ["intersection"])],
        "entering": [("b", "o", ["wall"]), ("b", "s", ["suitcase"])],
        "crossing": [("b", "o", ["leg", "arm", "neck", "racket", "ski", "head", "hand",  "bricks"])],  # "arms", "legs", "hands",
        "covered with": [("b", "o", ["animal", "ground", "mountain top", "stripe", "mountain", "spot"])],
        "covered in": [("b", "o", ["slope", "chair", "carpet", "rock", "sticker", "mountain", "tablecloth", "wetsuit", "brush", "forest", "beach", "plant", "cover"])],
        "standing behind": [("b", "s", ["building", "trees", "bush", "wall", "buildings", "pole", "counter"])],
        "standing at": [("b", "o", ["cake", "ocean", "line"])], 
        "stacked on": [("b", "s", ["album",  "pot", "paper", "microwave", "rock", "can", "surfboard", "cell phone", "orange", "microwaves", "case", "pear"])], # "book",  "shirt", "bowl", "t-shirt", "towel", "cup", 
        "skiing in": [("b", "o", ["area", "ground", "pants", "air", "slope", "people"])],
        "skiing down": [("b", "o", ["snow", "shoes"])],
        "sitting with": [("b", "o", ["legs"]), ("b", "s", ["candles"])],
        "sitting under": [("b", "o", ["glass"]), ("b", "s", ["menu", "plate", "train", "shoes", "mirror", "van"])],
        "sitting on top of": [("b", "o", ["floor", "grass", "carpet", "ground", "stand", "sidewalk", "post", "wall", "pavement", "sink", "wood", "can"]), 
            ("b", "s", ["olive", "plant", "boat", "train", "foot", "paint", "shade", "water", "meal", "papers"])],
        "sitting near": [("b", "s", ["crust"])],
        "painted on": [("w", "s", ["graffiti", "logo", "flower", "crosswalk", "picture", "symbol", "star", "bird", "character", "flowers", "heart", "tree", 
            "cloud", "cross", "bear", "clouds", "zebra", "sun", "artwork", "penguin"])],
        "parked along": [("b", "o", ["parking lot", "field", "ground", "grass"])],
        "petting": [("b", "s", ["hand", "arm"])],
        "perched on": [("b", "o", ["perch", "line", "back"]), ("b", "s", ["train track", "sunglasses", "houses", "building"])],
        "parked on": [("b", "o", ["intersection", "pole", "corner", "shoulder", "airport", "car"]), ("b", "s", ["engine", "bug", "man"])],
        "parked beside": [("b", "o", ["ground"])],
        "parked by": [("b", "o", ["dirt", "car", "rock", "back"])],
        "parked in front of": [("b", "o", ["car", "stone", "cars"])],
        "parked in": [("b", "o", ["ground", "line", "distance", "area", "spot", "car"])],
        "parked near": [("b", "s", ["container"])],
        "full of": [("b", "o", ["apple", "microphone", "ground", "tracks", "doll", "plant", "vase", "man", "hot dog", "place", "teeth"])],
        "grazing on": [("w", "o", ["grass", "hill", "field", "leaves", "plain", "hay", "hillside", "mountain", "wildflowers", "plants", "lawn"])],
        "grazing in": [("w", "o", ["field", "grass", "snow", "meadow", "forest", "hill", "farm"])],
        "grabbing": [("w", "o", ["frisbee", "pizza", "food", "skateboard", "handle", "apple", "snowboard", "slice", "umbrella", "glass", "jar", "board", "donut"])],
        "going down": [("b", "o", ["track", "pizza", "snow", "escalator", "face"]), ("b", "s", ["fence", "snowboard", "stripe"])],
        "growing next to": [("b", "o", ["leaf"]), ("b", "s", ["field", "brush", "leaf"])],
        "growing in": [("b", "o", ["plane", "corn", "tree"]), ("b", "s", ["stick", "tree trunk", "branch"])],
        "herding": [("b", "o", ["dog", "herd"])],
        "hitting": [("b", "o", ["ocean", "fence", "street", "building", "bed", "wave"]), ("b", "s", ["water", "light", "sunlight", "sun", "arm", "spray", 
            "ocean", "sunshine"])],
        "hugging": [("b", "s", ["arm"])],
        "jumping off": [("b", "s", ["foot"])],
        "picking up": [("b", "s", ["hand"])],
        "adjusting": [("b", "s", ["hand"])],
        "typing on": [("b", "s", ["hand", "hands", "fingers"])],
        "chewing": [("b", "s", ["mouth", "beak"])],
        "sleeping in": [("b", "s", ["hair"])],
        "going into": [("b", "s", ["door", "doorway"])],
        "tying": [("b", "s", ["hand", "hands"])],
        "going through": [("b", "s", ["window", "tree"])],
        "looking down at": [("b", "s", ["trunks"])],
        "looking into": [("b", "s", ["door"])],
        "opening": [("b", "s", ["hand"])],
        "balancing on": [("b", "s", ["frisbee", "skateboard", "eye glasses"])],
        "approaching": [("b", "s", ["water"])],
        "staring at": [("b", "s", ["back"])],
        "looking over": [("b", "s", ["building"])],
        "hanging out of": [("b", "o", ["feeder"])], 
        "hanging out of": [("b", "s", ["arm", "head"])],
        "growing from": [("b", "s", ["root", "branch", "foliage", "tree trunk", "trunks", "trunk", "twig"])],
        "wrapped around": [("b", "s", ["fence"])],
        "worn on": [("b", "s", ["ski", "arrow", "moustache", "strap"])],
        "jumping on": [("b", "s", ["feet"])],
        "jumping over": [("b", "o", ["sign", "wood"])], # water snow pool
        "leading": [("b", "s", ["door", "stairs", "doorway", "doors", "staircase"])],
        "leaning over": [("b", "o", ["water", "shoes"]), ("b", "s", ["head", "foot"])],
        "leaning on": [("b", "o", ["hand", "bear", "leg", "toilet", "elephant", "knee", "bridge", "zebra", "head", "can", "elbow", "polar bear"]), ("b", "s", ["sign", "pole", "hand", "arm", "foot", "zebra", "pool", "elbow"])],
        "leaning against": [("b", "o", ["plate", "man", "sign", "zebra", "step", "countertop", "counter", "woman", "cow", "book"]), ("b", "s", ["wood", "stick", "poles", "sink", "table", "handles", "head"])],
        "sitting in front of": [("b", "o", ["shed", "home"])],
        "sitting by": [("b", "s", ["hand"])],
        "sitting at": [("b", "o", ["chair", "deck", "counter top", "island"]), ("b", "s", ["car", "airplane", "train", "shirt", "bar stool"])], # "boat", 
        "lying inside": [("b", "s", ["fry", "noodle"])],
        "lying next to": [("b", "s", ["rock", "gravel", "stones"])],
        "floating on": [("b", "o", ["wave"])],
        "floating on": [("b", "s", ["leaf", "branches", "wave"])],
        "flying over": [("b", "o", ["sky"])],
        "flying in": [("w", "o", ["sky", "air"]), ("b", "s", ["snow flake", "man", "streamer", "snow", "flying"])],
        "floating in": [("b", "o", ["harbor", "sticks", "bay", "room"]), ("b", "s", ["leaf", "bird", "grass", "sticks", "airplane", "tail", "ripple", "bubble"])],
        "flying through": [("w", "o", ["sky", "air", "clouds"]), ("b", "s", ["man"])],
        "riding": [("b", "o", ["wave", "board", "waves", "lift", "water", "rail", "street", "subway", "hill", "skateboarder", "tracks", "benches", "horns", 
            "boy", "ramp", "engine", "helmet", "boot", "shoes", "kite", "crest", "back", "bicyclist", "sand", "wheels", "people", "ripples", "cat", "curl", 
            "escalator", "beach", "foam", "jacket"]), ("b", "s", ["surfboard", "train", "wetsuit", "horse", "motorcycle", "car", "shirt", "shoes", "back", 
            "hair", "skateboard", "feet", "bike"])],
        "lying on top of": [("b", "o", ["floor",  "crust", "holder", "band", "parking lot", "field", "fruit"]), ("b", "s", ["crumb", "topping", "noodle", 
            "bean", "meal", "shoe"])], # "letter", # orange, apple brush cloth paper ground
        "on top of": [("b", "o", ["bowl"])],
        "sitting in": [("b", "o", ["stand", "window", "seat", "room", "tree", "seats", "door", "shade", "ground", "lap", "person", "sky", "ocean", "lake", 
            "road", "rocks", "traffic", "roof", "holder", "trees", "river", "table", "hand", "back", "woods", "bike", "sun", "carpet", "luggage", "food", 
            "horse", "doorway", "wall", "floor", "hill", "sidewalk", "stool", "deck", "windshield", "orange", "dock", "front", "umbrella", "feeder", "wrapper", 
            "shorts", "stairs", "jeans", "shirt", "outdoor", "shadow", "lady", "tube", "pew", "pen", "walkway", "spectators", "pile", "stack"]), 
            ("b", "s", ["car", "rock", "stone", "bus", "toilet", "table", "vehicle", "truck", "hydrant", "plane", "bed", "cone", "trinket", "train", 
            "root", "airplane", "card", "purse", "straw", "cloud", "bushes", "pole", "seats", "water", "coffee", "tree", "boulder", "leaf", "leaves", 
            "plant", "paper", "rocks", "umbrella", "couch", "tent", "bathtub", "broccoli"])], # bouquet television bin
        "coming from": [("b", "o", ["wave", "hydrant", "ceiling", "bottom", "kite", "water", "mouth", "laptop", "fountain", "shirt", "man", "surfboard", "ocean"]), 
            ("w", "s", ["smoke", "steam", "water", "flames", "train"])],
        "coming out of": [("w", "o", ["train", "wall", "hydrant", "plane", "engine", "faucet", "jet", "briefcase", "oven", "ground", "smoke stack", "grill", 
            "tunnel", "jets", "boat", "airplane", "chimney", "hose", "train engine", "pot", "dispenser", "pipe"]), ("w", "s", ["smoke", "water", "steam", "pipe", 
            "money", "donut", "train", "bus", "pipes", "tissues"])],
        "connected to": [("b", "o", ["building", "wing", "airplane", "plane", "pipe", "door", "hand", "bed", "wire", "horse", "man", "motorcycle", "giraffe", 
            "sign", "cord", "engine", "table", "bus", "elephant", "wires", "chain", "door", "foot", "tower", "bicycle", "car", "handle", "cable", "car", "key", 
            "train", "cat", "bowl", "clock", "tire", "watch", "fan", "fence", "bag", "poles", "hose", "umbrella", "suitcase", "socket", "urinal", "ropes", 
            "leash", "ankle", "line", "anchor", "skateboard", "freezer", "collar"]), ("w", "s", ["wire", "cord", "wires", "pipe", "chain", "cable", "hose", 
            "mouse", "rope", "string", "cables", "ropes", "keyboard", "cords", "strings", "pipes", "headphones"])],
        "holding": [("b", "o", ["tennis"]), ("b", "s", ["hand", "pole", "hands", "plate", "post", "table", "arm", "finger", "bolt", "fingers", "tray", "screw", 
            "rack", "stand", "thumb", "bracket", "glove", "dish", "trunk", "poles", "desk", "strap", "pillar", "holder", "wall", "fence", "bolts", "board", 
            "posts", "paper", "wire", "pan", "counter", "tower", "chair", "cable", "magnet", "cord", "stick", "shelves", "paw", "platter", "mouth", "brackets", 
            "branch", "compartment", "beam", "gloves", "case", "spoon", "ring", "toy", "foil", "ground", "handle", "structure", "toothpick", "nail", "arms", 
            "signpost", "straps", "screws", "beams", "belt", "bench", "stem", "picnic table", "blanket", "wood", "carrot", "apartments", "hanger", "towel holder", 
            "plush", "nut", "shirt", "napkin", "pin", "tin", "building", "ribbon", "stands", "clock", "water", "racks", "base", "support", "rivets", "plastic", 
            "leash", "couch", "planks", "chock", "planter", "platform", "column", "head", "pipe", "sticks", "button", "sign", "stool", "leg", "tracks", "cap", 
            "paws", "blocks", "held", "motorcycle", "wires", "horse", "cloth", "ottoman", "rivet", "claws", "anchor", "pinky", "rim", "cement", "sign pole", 
            "surfboard", "block", "toilet", "tie", "bike", "crossbar", "mortar", "lock", "gate", "coat", "wing", "signs", "rock", "fist", "wheels", "supports", 
            "sidewalk", "tennis", "feet", "flowers", "tree", "mitt", "track", "racket", "cutting board", "sky", "jeans", "ropes", "cone", "balloon", "uniform", 
            "fruit", "drawing", "stake", "photo", "laptop", "zoo", "cooling rack", "shoulder", "part", "spoke", "mirror", "pen", "knife", "toothpicks", "bus", 
            "magnets", "boot", "field", "picture"])],
        "holding onto": [("b", "o", ["horn", "cabinet", "knob"]), ("b", "s", ["hands", "arm", "claw"])],
        "hanging above": [("b", "s", ["leaf", "sky", "cloud", "boulder", "tree", "shelf", "microwave", "lampshade", "pot", "bridge", "box"])],
        "hanging from": [("b", "o", ["surfboard", "elephant", "lamp", "man", "mouth", "sign", "bag", "back", "backpack", "bed", "dispenser", "mirror", "train", 
            "hoodie", "horse", "trunk", "strap", "overhead", "room", "parachute", "trees", "fruit", "head", "tv", "vase", "stick", "platform", "fixture", "plant", 
            "curtains", "blinds", "bear", "display", "roll", "skis", "blanket", "fan", "chandelier", "sink", "apple", "lock", "animal", "plane", "cage", "bread", 
            "container", "toy", "sheet", "station", "coat", "sculpture", "dog", "hip", "tiles", "outlet", "ears", "monument", "tub", "kitchen", "pot", "bags", 
            "hand", "person", "glove", "hair", "saddle", "column", "carriage", "suitcase", "stove top"]), ("b", "s", ["leaf", "leaves", "strap", "paper", "bulb", 
            "tusk", "tail", "plants", "flower", "bottle", "signal", "hose", "bike", "fixtures", "branches", "flowers", "snow", "handle", "earring", "branch", 
            "apple", "star", "item", "bird", "balls", "hay", "tongue", "pig", "gadgets", "disc", "feathers", "leg", "straps", "card", "feeder", "hook", "moss", 
            "beads", "vent", "pole", "twig", "case", "tissue", "letter", "fish", "grass", "washcloth", "crest", "bicycle", "limb", "stick", "heart", "heart tag", 
            "produce", "shade", "shoes", "orange", "food", "ring", "shelf", "sconce", "scissor", "napkin", "cover", "sleeve", "calendar", "stoplight", "controller", 
            "cone", "lightbulb", "hair", "clock face", "brush", "poster", "shower head", "phone"])],
        "hanging in": [("b", "o", ["sky", "clouds", "wall", "air", "background", "room", "bunch", "line", "row", "bananas", "group", "area", "ceiling", "cluster", 
            "building", "water", "case", "set", "frame", "back", "stand", "eye", "door", "ear", "face"]), ("b", "s", ["cloud", "clouds", "window", "branch", 
            "cabinet", "handle", "hair", "tie", "lightbulb", "giraffe", "earring", "frame", "sun", "moon", "bulb", "flowers", "shelf", "frisbee"])],
        "hanging off": [("b", "o", ["plate", "couch", "pizza", "bench", "tree trunk", "hair dryer", "spoon", "dog", "truck", "toilet", "bowl", "bicycle"]), 
        ("b", "s", ["feet", "paw", "tail", "slice", "leg", "leaves", "strap", "zipper", "cheese", "lettuce", "icicle", "straps"])],
        "hanging over": [("b", "o", ["man", "bowl", "plate", "bat", "ground", "vase", "kitten", "lady", "side", "back", "horse", "head", "grass", "face", 
            "frisbee", "shelf"]), ("b", "s", ["tree", "leaf", "sky", "branch", "trees", "hair", "pole", "paw", "glove", "fixture", "clouds", "arm", "lettuce", 
            "brush", "arms", "head", "airplane", "tooth", "jersey", "mane"])],
        "contain": [("b", "o", ["clouds", "window", "chip", "sheep", "numeral", "slice", "stone", "person", "wave", "substance", "glass", "hole", "giraffe", 
            "number", "sign", "windows", "chair", "can", "spot", "letter", "brick", "people", "tracks", "luggage", "slices", "cloud", "balls", "animal", 
            "rock", "key", "object", "leaves", "animals", "car", "blocks", "man", "green", "bunch", "writing", "arrow", "stairs", "dog", "meat ball", "greens", 
            "plates", "numerals", "photo", "leaf", "panel", "planes", "sticks", "cleats", "chain", "clock", "drink", "beverage", "hot dog", "knife", "bottle", 
            "meal", "dinner"]), ("b", "s", ["container", "fence", "clock", "sky", "building", "wall", "room", "tower", "shelf", "sign post", "scene", "label", 
            "rope", "cart", "water", "pole", "table", "tree", "order", "ground", "tray", "sign", "butcher block", "boat", "door", "code", "sand", "rack", 
            "call phone", "area", "grass", "parking lot", "toilet", "field", "laptop", "foot", "pile", "photo", "house", "puddle", "hair", "wetsuit", "pen", 
            "screen", "panel", "head", "flight", "cap", "floor", "bus", "beach", "park", "ocean"])],
        "filled with": [("b", "o", ["drink", "object", "photo", "bag", "brush", "edge", "bottle"]), ("b", "s", ["woods", "space", "foreground", "stroller"])], # "leaves", 
        "lying in": [("b", "o", ["pile", "group", "stack", "ground", "bundle", "collection", "shade", "bunch", "food", "onion", "rocks", "window", "stone", 
            "shadow", "arm", "sunlight", "compartment", "floor"]), ("b", "s", ["rock", "log", "paper", "vase", "stick", "branch", "leaf", "rocks", "object", 
            "boulder", "bean", "stuff", "leaves", "debris", "stone", "phone", "flooring", "poles", "base", "pole", "tree", "cell phone", "liquid"])],
        "across": [("b", "s", ["tile"])],
        "close to": [("w", "s", ["man", "person", "tree", "boat", "giraffe", "building", "people", "bird", "trees", "woman", "boy", "sheep", "chair", "wall", 
            "horse", "girl", "pole", "door", "elephant", "zebra", "vehicle", "animal", "guy", "motorcycle", "bicycle", "house", "hill", "cow", "window", "cabinet", 
            "child", "homes", "car"]), ("b", "o", ["ocean", "ground", "beach", "road", "marina", "grass", "shore", "snow", "sand", "city", "head", "park", "town", 
            "street", "sky", "body", "leg", "trunk", "seat", "mountains", "court", "floor", "mouth", "land"])],
        "around": [("b", "o", ["eye", "tracks", "ankle", "face", "track", "mouth", "edge", "base", "handle", "trunk", "area", "road", "nose", "windows", "body", 
            "light", "dirt", "wall", "ground", "log", "beach", "nail", "train tracks", "runway", "sidewalk", "collar", "room", "rock", "seat", "leaves", "plant", 
            "cockpit", "bushes", "bat", "plants", "doorway", "ice", "sand", "chin", "eyes", "knee", "photo", "racket", "screen", "bathroom", "forehead", "front", 
            "leaf", "poles", "paper", "top", "stalk", "dot", "corner", "ring", "stem", "structure", "branch", "string", "button", "posts", "habitat", "shoreline", 
            "arena", "property", "limb", "phone", "stick", "fighter", "tile", "pitch", "arrow", "flower", "shorts", "sculpture", "letter", "cellphone", "barrel", 
            "pillar", "monument", "toothbrush", "bulb", "case", "ski", "soil", "rim", "railroad", "back", "ear", "brick", "balcony", "floor", "whisk", "street", 
            "path", "frame", "handlebar", "drape", "scissor", "river", "tennis", "number", "plastic", "rails", "part", "manhole", "stall", "concrete", "lip", 
            "object", "wood", "tiles", "oven", "signs", "wetsuit", "engine", "mound", "hills", "mouse", "ship", "wires", "edges", "surf board", "dock", "sky", 
            "pile", "desk", "saucer", "sunglasses", "sock", "courts", "walkway", "shin", "wrinkle", "remote"]), ("b", "s", ["chair", "strap", "trim", "railing", 
            "stripe", "arm", "border", "circle", "dirt", "lanyard", "brick", "bow", "tile", "line", "gate", "bush", "tag", "light", "fencing", "rock", "ground", 
            "wire", "lights", "man", "lines", "tree", "barrier", "rail", "straps", "rim", "hair", "bird", "floor", "bricks", "person", "sky", "balcony", "cloud", 
            "window", "stripes", "stone", "wave", "flower", "padding", "footprint", "area", "engine", "foliage", "rods", "plant", "wood", "handle", "finger", 
            "leaf", "mulch", "building", "woman", "design", "arms", "spot", "pattern", "purse", "bib", "lady", "white", "patch", "pole", "cone", "bench", "reign", 
            "arch", "bar", "hydrant", "bracket", "tiles", "bead", "bars", "post", "sash", "waves", "branches", "counter", "strip", "metal", "boat", "petal", 
            "id", "numerals", "shape", "molding", "wrinkles", "road", "bun", "rust", "cover", "curb", "posts", "sidewalk", "flag", "forest", "mat", "bear", 
            "number", "girl", "base", "barriers", "dust", "ripples", "paint", "facial hair", "edge", "rose", "wrinkle", "pass", "blue", "glass", "car", "male", 
            "basket", "red", "track", "gold", "chicken", "columns", "plate", "stitching", "rein", "toothpaste", "dots", "air", "mound", "pack", "shadow", "lips", 
            "panel", "sock", "cabinet", "countertop", "tail", "fireplace", "skin", "haze", "leg", "boy", "stain", "passenger", "seagull", "heart", "paws", "neck", 
            "shoes", "walls", "giraffe", "bread", "square", "river", "thing", "feet", "beard", "juice", "couch", "brace", "zucchini", "object", "reins", "pants", 
            "sandal", "zipper", "child", "twigs", "cement", "broccoli", "mother", "paneling", "hands", "knot", "grip", "ledge", "pillar", "shutter", "claw", "guard", 
            "buckle", "vehicle", "marking", "field", "branch", "structure"])],
        "attached to": [("w", "s", ["rope", "tag", "chain", "flag", "lamp", "pipe", "horse", "mouse"])], 
        "carrying": [("b", "o", ["carriage", "strap", "beach", "electricity", "train", "benches", "light", "horse", "driver", "stack", "back", "toilet", 
            "shirt", "shoes", "shoe", "hat"]), ("b", "s", ["hand", "pole", "carriage", "wave", "bag", "ramp", "basket", "crowd", "book shelf", "rock", "tray", 
            "cable", "line", "arm", "wire", "wetsuit", "body", "table", "number", "head", "blond"])],
        "covering": [("b", "o", ["foot", "leg", "eye", "hand", "area", "surface", "mouth", "branch", "concrete", "arm", "body", "legs", "side", "bottle", "neck", 
            "snow", "sand", "curtains", "back", "light", "bean", "ears", "forehead", "ear", "evergreen", "fry", "shoulder", "hair", "needles", "entrance", "hole", 
            "can", "chip", "windshield", "avocado", "container", "feet", "top", "chest", "blinds", "paw", "fruit", "cup", "torso", "skin", "booth", "uniform", 
            "bird", "room", "vases", "entryway", "motorcycle", "base", "station", "object", "earth", "handle", "craft", "flooring", "board", "infield", "nose", 
            "hooves", "bottom", "pavement", "microwave", "brush", "sock", "cables"]), ("b", "s", ["tree", "spot", "ground",  "topping", "slope", "sleeve", "branch", 
            "seat", "sky", "cockpit", "dot", "weed", "ocean", "road", "river", "hand", "fur", "hair", "shoe", "pants", "stripe", "jeans", "awning", "mane", "sock", 
            "slab", "shirt", "fence", "tent", "ceiling", "cushion", "bar", "bars", "shadow", "slices", "squares", "grate", "line", "stockings", "stripes", "surface", 
            "bangs", "glass", "animal", "window", "material", "blinder", "lettuce", "shorts", "shoes", "plywood", "duct tape", "rope", "sandal", "picture", "jacket", 
            "fleece", "feathers", "poles", "box", "door", "egg shell", "mesh", "lines", "hands", "shadows", "dead grass", "white", "siding", "bridge", "bark", 
            "screen", "case", "area rug", "ivy", "beanie", "fringe", "shutters", "boot"])],
        "hanging on": [("b", "o", ["towel ring", "car", "door knob", "plant", "towel bar", "handlebars", "woman", "horse's head", "poles", "bunch", "side", 
            "umbrella", "paper", "tree branch", "flag pole", "display rack", "couch", "chest", "coat rack", "picture", "plane", "collar", "metal", "range", "row", 
            "chain", "plate", "clothes hook", "magnet", "pants", "shed", "arm", "peg", "lamp", "cart", "streetlight", "stand", "ground", "elephant", "suit", 
            "flagpole", "curtains", "stall", "clothes line", "buildings", "cables", "light", "coat hanger", "bar", "rod", "hook", "handle", "post", "towel rack", 
            "string", "holder", "shelf", "display", "man", "stick", "rail", "board", "hanger", "line", "railing", "house", "racks", "hooks", "necklace", "wing", 
            "wood", "knob", "ring", "sign", "porch", "bus", "bridge", "curtain rod", "walls", "surfboard", "horse", "ear", "bat", "room", "airplane", "bush"]), 
        ("b", "s", ["light", "leaf", "art", "shelf", "lights", "leaves", "print", "pot holder", "board", "advertisement", "fixture", "urinal", "hook", "plaque", 
            "cabinet", "rack", "plant", "holder", "awning", "branch", "man", "tile", "hanger", "tarp", "tail", "sink", "shelves", "card", "horse", "outlet", "bar", 
            "cards", "engine", "row", "strap", "lock", "airplane", "switch", "faucet", "leash", "border", "valance", "planter", "handle", "towel rack", "person", 
            "lady", "pillar", "signal", "trousers", "chair", "objects", "bow", "permit", "doorknob", "certificate", "sticker", "shade", "oven", "denim", "bunch", 
            "medicine cabinet", "advertisments", "stuff", "flower pot", "canopy", "wall", "child", "bulb", "lift chair", "bib", "hair", "hot pad", "gargoyle", 
            "letters", "deer head", "line", "piece", "cabinets"])],
        "looking at": [("b", "o", ["wave", "hand", "cell", "eyes", "tail", "spot", "material", "feet", "distance", "art", "mound", "foot", "board", "nose", "hair", 
            "head"]), ("b", "s", ["eyes", "ground", "group", "eye", "head", "lad", "face"])],
        "lying on": [("b", "o", ["side", "stomach", "surface", "wood", "woman", "stool", "man", "back", "animal", "lap", "hood", "bar", "forehead", "background", 
            "hospital bed", "rack", "apple", "block", "edge", "bottom", "panel", "beans", "fork", "leg", "tank", "building", "arm", "pattern", "mound", "belly", 
            "blood orange", "pile", "area", "line", "rod", "pet bed", "gravel", "cat bed", "window sill", "path", "cat", "tile", "one", "hydrant", "legs", "tummy", 
            "dog", "boulder", "bowl", "blackberry", "doll", "nails", "boards", "head", "display", "curb"]), ("b", "s", ["leaf", "rock", "log", "twig", "stick", 
            "branch", "sign", "clothing", "food", "dirt", "head", "seaweed", "plank", "tree", "cloth", "rice", "tie", "debris", "straw", "boulder", "pole", "hand", 
            "cup", "grass", "sticks", "bread crumb", "tree trunk", "posts", "snow pea", "blueberry", "branches", "sauce", "board", "cone", "laptop", "ski", "hair", 
            "boards", "bangs", "marker", "paperwork", "case", "sandal", "disc", "item", "trunk", "container", "clump", "rind", "fence", "shell", "cards", "bark", 
            "necktie", "wood", "chips", "pets", "ram", "paw", "foal", "strawberry", "coat", "chair", "tail", "gravel", "speck", "booklet", "body", "herb", "water", 
            "strap", "wool", "cup holder", "tablecloth", "light", "shoes", "artwork", "silver", "fabric", "gym sneaker", "sheet", "top", "leash", "legs", 
            "bassett hound", "arm", "track", "eggs", "barrel", "shoe", "ground", "cushion", "pebble", "plywood", "bathmat", "piece", "tree stump", "ruble", 
            "parasail", "party favor", "petal", "dead tree", "statue", "sandals", "doily", "mop", "cape", "tag", "brick", "feet", "char", "parking meter"])],
        "in front of": [("b", "s", ["window", "stone", "leaf", "dirt", "windshield", "wave", "waves", "windows", "wall", "walls", "sky", "branch", "beach", 
            "ground", "wheel", "wheels", "tire", "ocean", "tile"]), ("b", "o", ["stone", "rock", "leaf", "dirt", "windshield", "wave", "waves", "sky", "branch", 
            "wheel", "ground", "wheels", "tire", "tile", "grass"])],
        "behind": [("b", "o", ["sky", "stone", "rock", "leaf", "dirt", "windshield", "branch", "wheel", "wheels", "ground", "tile", "field", "grass", "waves", 
            "road", "court", "sidewalk", "branches", "snow", "trunk", "road", "sidewalk", "cloud", "brush", "roof", "sink", "back", "street"]), 
        ("b", "o", ["sky", "stone", "rock", "leaf", "dirt", "windshield", "branch", "branches", "wheel", "wheels", "ground", "tile", "waves", "snow", "trunk", 
            "grass", "ocean", "road", "cloud", "brush", "roof", "back", "street"])],
        # "above": [("b", "s", ["sky", "clouds", "tree", "cloud", "wall", "trees", "ceiling", "pole", "building", "hand", "fence", "roof", "number", "frame", 
        # "head", "balcony", "letter", "boy", "tower", "grass", "hair", "skateboard", "rock", "glass", "surfboard", "dog", "handle", "logo", "toilet", "leaf", 
        # "walkway", "knob", "foot", "word", "people", "rocks", "stop sign", "ski", "feet", "hill", "door", "mountains", "arm", "tiles", "car", "bush", "water", 
        # "bus", "horn", "fruit", "post", "wallpaper", "words", "gate", "eye", "glasses", "nose", "wing", "leg", "stick", "background", "teeth", "decorations", 
        # "motorcycle", "display", "hands", "shirt", "mustache", "skateboarder", "player", "plants", "road", "buildings", "baseball", "boat", "guy", "dish", 
        # "platform", "mountain", "tail", "wristband", "mane", "fur", "surfer", "face", "lamp shade", "bushes", "shoe", "trunk", "collar", "seat", "zebra", "food", 
        # "skier", "paw", "wheel", "house", "hot dog", "tree branch", "log", "magazine", "ear", "socks", "crowd", "paint", "fans", "lock", "table", "zipper", 
        # "logs", "ceiling light", "wings", "highway", "numbers", "forest", "ring", "stone", "land", "animal", "fog", "sidewalk", "chimney", "belt", "feathers", 
        # "bleachers", "shorts", "fireplace", "train tracks", "curtains", "skin", "goggles", "air", "legs", "runway", "finger", "neck", "street"]), ("b", "o", 
        # ["water", "ground", "street", "road", "building", "head", "floor", "ocean", "beach", "wall", "sidewalk", "field", "stop sign", "donut", "skateboard", 
        # "hand", "steps", "highway", "umbrella", "wheel", "city", "nose", "bathroom", "oranges", "airport", "land", "pants", "walkway", "number", "garage", 
        # "vase", "stones", "pavement", "runway", "station", "shoes", "post", "lemons", "logo", "lounge", "kite", "pole", "tire", "roadway", "bag", "skis", 
        # "face", "porch", "air"])],
        # "under": [("b", "s", underSubjectBList), ("b", "o", underObjectBList)],
        # "underneath": [("b", "s", underSubjectBList), ("b", "o", underObjectBList)],
        # "beneath": [("b", "s", underSubjectBList), ("b", "o", underObjectBList)],
        "by": [("o", "b", byBlack), ("s", "b", byBlack)]
    }

    relRepListing = {
        "cooking": [("cooked in", "s", ["hot dog", "pepper", "eggs", "food", "hot dogs", "chicken", "onions"])],
        "eating": [("eating from", "o", ["field", "tree", "bush", "feeder", "ground", "bin", "spoon", "pond"])],
        "grazing in": [("grazing on", "o", ["grass"])],
        "drinking from": [("drinking", "o", ["water"])],
        "drinking": [("drinking from", "o", ["lake", "cup", "river", "bottle", "glass", "pool", "juice box", "jar", 
            "puddle", "pond", "toilet"])],
        "driving": [("driving on", "o", ["street", "highway"])],
        "playing on": [("playing", "o", ["piano", "guitar", "keyboard", "keys"])],
        "hanging in": [("hanging on", "o", ["wall"])],
        "holding": [("holding up", "s", ["pole"])],
        "playing": [("playing on", "o", ["court", "field"]),
                    ("playing with", "o", ["ball", "controller", "racket", "remote", "snow", "controllers", "console", 
                        "water", "person", "game controller", "woman", "bat", "boy", "board", "sand", "balls"])],
        "grazing": [("grazing on", "o", ["grass", "hillside", "lawn"]), ("grazing in", "o", ["field"])],
        "riding": [("riding on", "o", ["skateboard", "surfboard", "snowboard", "skis", "ski"])]
    }
    
    stop = {
        "topped with": ("o", ["tomato", "onion", "olive", "potato", "candy", "blueberry", "seed", "vegetable", 
            "apple", "mushroom", "pickle"]),
        "mixed with": ("o", ["raisin", "bean"]),
        "scattered on": ("s", ["leaf", "paper", "flower", "rock"]), 
        "falling of": ("s", ["sprinkle"]),
        "herding": ("o", ["cow", "elephant", "goat"]),
        "covered with": ("o", ["tree", "tile", "rock", "brick", "cloud"]),
        "covered in": ("o", ["leaf", "tile", "topping", "cloud", "tree", "magnet", "banana", "sprinkle", "stone", "brick"]), 
        "full of": ("o", ["donut", "orange", "flower", "utensil", "book", "drink", "cloud", "boat", "player", "hat", "glass", "carrot", "bagel", 
            "gadget", "leaf", "ornament", "bird", "wave", "vegetable", "lemon", "lamb", "bean", "egg"]),
        "contains": ("o", ["utensil", "bean", "apple", "banana", "vegetable", "tomato", "orange", "condiment"]),
        "filled with": ("o", ["book", "flower", "cloud", "apple", "banana", "bear", "rock", "car", "orange", "zebra", "plane", "condiment", "sticker", 
            "topping", "fern", "animal", "donut", "kite", "pastry", "vegetable"]), 
        "covering": ("s", ["tile", "brick", "cloud", "leaf", "rock", "vine", "stone", "plant"])
    }

    pairs = {
        "sticking out of": ("w", [("pole", "ground"), ("pole", "water"), ("pole", "grass"), ("straw", "cup"), ("money", "briefcase"), ("pole", "boat"), 
            ("book", "shelf"), ("hot dog", "bun"), ("pen", "pocket"), ("toothpick", "sandwich"), ("pole", "snow"), ("lettuce", "sandwich"), ("knife", "jar"), 
            ("magazine", "basket")]),
        "placed on": ("w",  [("flowers", "table"), ("dish", "table"), ("donut", "newspaper"), ("camera", "pole"), ("items", "shelf"), ("flower", "table"), 
            ("sticker", "banana"), ("sticker", "window"), ("mirror", "wall"), ("items", "table"), ("towel", "bathtub"), ("suitcase", "sidewalk"), 
            ("label", "bottle"), ("bottle", "table"), ("cherry", "dessert"), ("painting", "wall"), 
                ("video games", "bookshelf"), ("books", "shelf"), ("basket", "floor"), ("pillow", "sofa"), ("cone", "floor"), ("brownie", "foil"), 
                ("bag", "shoulder"), ("call phone", "table"), ("pot", "floor"), ("rose", "bed"), ("book", "shelf"), ("knife", "pizza"), 
                ("container", "table"), ("pen", "table"), ("towel", "tub"), ("bottle", "ground"), ("cake", "table"), 
                ("sculpture", "table"), ("sticker", "apple"), ("glass", "table")]),
        "across from": ("w", [("car", "bench"), ("bottle", "scissors"), ("building", "park"), ("house", "water"), ("sign", "sidewalk"), 
            ("building", "train"), ("fireplace", "couch"), ("woman", "window"), ("house", "sign"), ("mirror", "bed"), ("chair", "table"), 
            ("trees", "train"), ("gate", "house"), ("mountains", "island"), ("cat", "shower"), ("men", "boy"), 
                ("house", "benches"), ("television", "couch"), ("keyboard", "box"), ("monkey", "water"), ("man", "calf"), ("grass", "houses"), 
                ("island", "boat"), ("birds", "tree"), ("sidewalk", "building"), ("deer", "elephant"), ("bush", "tree"), ("shops", "bus"), 
                ("tv", "comforter"), ("buildings", "beach"), ("trees", "lake"), ("man", "girl"), ("chair", "window"), 
                ("monkey", "deer"), ("building", "hydrant"), ("bottle", "glass"), ("man", "cars"), ("tree", "buildings"), ("buildings", "ocean"), 
                ("trees", "cow"), ("elephant", "water"), ("car", "bus"), ("trees", "field"), ("building", "parking meter"), ("house", "fence"), 
                ("wall", "man"), ("woman", "trees"), ("bush", "lawn"), ("keyboard", "pizza"), ("couch", "television"), 
                ("shower", "sink"), ("house", "store"), ("trees", "grass"), ("man", "tv"), ("buildings", "trees"), ("buildings", "pond"), 
                ("glass", "pizza"), ("building", "sign"), ("houses", "field"), ("gate", "stop sign"), ("trees", "river"), ("houses", "grass"), 
                ("motorcycle", "building"), ("bench", "ocean"), ("car", "building"), ("counter", "television"), ("tree", "building"), 
                ("tree", "bus"), ("tree", "bench"), ("sink", "toilet"), ("man", "boat"), ("buildings", "park"), ("bridge", "highway"), 
                ("building", "airplane"), ("tree", "train station"), ("boat", "bridge")]),
        "filled with": ("b", [("tree", "branches")]),
        "attached to": ("b", [("pipe", "bowl")]),
        "within": ("w", [("window", "balcony"), ("broccoli", "container"), ("tree", "building"), ("rice", "container")]),
        "over": ("w", [("bridge", "water"), ("mirror", "sink"), ("bridge", "river"), ("bridge", "tracks"), ("bird", "water"), ("bag", "shoulder"), 
            ("bridge", "train"), ("flags", "street"), ("bridge", "road"), ("canopy", "boat"), ("birds", "water"), ("blanket", "couch"), 
            ("mirror", "sink"), ("canopy", "bed"), ("pot", "fire"), ("towel", "shoulder"), ("bridge", "lake"), 
                ("cabinets", "counter"), ("clock", "door"), ("tree", "fence"), ("hair", "shoulder"), ("mirror", "counter")]),
        "on the back of": ("b", [("faucet", "sink"), ("paper", "toilet"), ("tank", "toilet"), ("balcony", "building"), ("tail", "elephant"), 
            ("tail", "dog"), ("backpack", "man"), ("mane", "giraffe"), ("headboard", "bed"), ("tail", "ducky"), ("lid", "toilet"), 
            ("backpack", "person"), ("pole", "seat"), ("tail", "zebra"), ("bar", "chair"), ("handle", "train"), 
                ("backpack", "woman"), ("wing", "plane"), ("wing", "jetliner"), ("hair", "neck")]),
        "on the bottom of": ("b", [("bolt", "stop sign"), ("panel", "plane"), ("banana", "pile"), ("stitching", "glove"), ("stripe", "pants"), 
            ("handle", "scissors"), ("jeans", "man"), ("leg", "side table"), ("target", "jet"), ("bolt", "sign"), ("hinge", "briefcase"), 
            ("hoof", "giraffe"), ("root", "carrot"), ("wall", "train"), ("stripe", "train"), ("opening", "nose"), 
                ("line", "surfboard"), ("legs", "chair"), ("handle", "racket"), ("tiles", "wall"), ("line", "ski"), ("floor", "kitchen"), ("handle", "windows")]),
        "on the edge of": ("b", [("symbol", "clock"), ("line", "road"), ("plant", "river"), ("pole", "course"), ("line", "platform"), 
            ("trees", "field"), ("trees", "grass"), ("tree", "field"), ("crust", "bread")]),
        "on the surface of": ("w", [("sticker", "orange"), ("pattern", "towel"), ("sticker", "apple")]),
        "outside": ("w", [("tree", "window"), ("trees", "window"), ("building", "window"), ("girl", "tent"), ("car", "window"), ("grass", "window"), 
            ("clock", "window"), ("plant", "window"), ("bench", "building"), ("leaves", "window"), ("buildings", "window"), ("flowers", "window"), 
            ("clock", "building"), ("bird", "window"), ("bike", "building"), ("chair", "house"), ("mountain", "window")]),
        "on the side of": ("b", [("brick", "pavement"), ("ear", "head"), ("people", "outdoors"), ("brick", "building"), ("bolt", "hydrant"), 
            ("rock", "mountain"), ("tree", "water"), ("tree", "hill"), ("eye", "head"), ("post", "street"), ("stripe", "zebra"), ("line", "road"), 
            ("stripe", "shorts"), ("stripe", "train"), ("oar", "boat"), ("stripe", "plane"), 
            ("stripe", "pants"), ("light", "pole"), ("shadow", "wall"), ("spot", "banana"), ("eye", "face"), ("handle", "door"), ("wing", "bird"), 
            ("shadow", "building"), ("tag", "suitcase"), ("stripe", "shirt"), ("tree", "mountain"), ("spot", "dog"), ("tree", "bus"), ("tree", "car"),
            ("post", "road"), ("wall", "church"), ("handle", "toilet"), ("rock", "road"), ("handle", "train"), ("switch", "wall"), ("shrub", "hill")]),
        "on the front of": ("b", [("knob", "stove"), ("handle", "door"), ("grill", "truck"), ("grill", "bus"), ("handle", "cabinet door"), ("eye", "face"), 
            ("button", "shirt"), ("nose", "face"), ("handle", "cabinet"), ("knob", "toaster"), ("glasses", "face"), ("bar", "train"), ("window", "microwave"), 
            ("button", "microwave"), ("handle", "drawer"), ("nose", "airplane"), 
            ("knob", "door"), ("knob", "microwave"), ("button", "appliance"), ("zipper", "luggage"), ("knob", "tv"), ("paint", "train"), 
            ("handle", "refrigerator"), ("nose", "bear"), ("window", "housing"), ("tree", "tie"), ("hands", "clock"), ("handles", "cabinets"), 
            ("writing", "bus"), ("doorknob", "door"), ("handle", "suitcase"), ("bars", "window"), ("knobs", "range"), ("display", "microwave")]),
        "next to": ("b", [("sidewalk", "road"), ("curb", "street"), ("curb", "road"), ("beach", "water"), ("grass", "dirt"), ("water", "boat"), ("water", "sand")]),
        "near": ("b", [("sand", "water"), ("water", "beach"), ("beach", "water"), ("sidewalk", "road"), ("water", "sand"), ("sidewalk", "street")]),
        "across": ("w", [("net", "court"), ("building", "street"), ("building", "road"), ("bridge", "water"), ("building", "water"), ("car", "street"), 
            ("trees", "water"), ("tree", "water"), ("tree", "street"), ("house", "street"), ("ketchup", "hot dog"), ("tree", "road"), ("bridge", "river"), 
            ("hill", "water"), ("sign", "street"), ("buildings", "water"), ("trees", "river"), ("store", "street"), 
            ("people", "street"), ("man", "street"), ("mountains", "water"), ("trees", "road"), ("paper", "floor"), ("fence", "street"), ("house", "road"), 
            ("person", "street"), ("houses", "street"), ("buildings", "street"), ("chain", "door"), ("truck", "street"), ("hills", "water"), ("fence", "road"), 
            ("land", "ocean"), ("umbrella", "street"), ("building", "field"), ("sign", "road"), 
            ("building", "lake"), ("pole", "street"), ("buildings", "river"), ("fence", "field"), ("car", "road"), ("snow", "trees"), ("snow", "beach"), 
            ("house", "water"), ("boat", "lake"), ("signs", "street"), ("house", "field"), ("suv", "street"), ("bus", "street"), ("house", "lake"), 
            ("cones", "road"), ("horse", "river"), ("grass", "street"), ("net", "field"), ("pipe", "ceiling"), 
            ("boat", "water"), ("trees", "field"), ("field", "water"), ("bicycle", "road"), ("trees", "lake"), ("trees", "street"), ("flowers", "street"), 
            ("house", "bridge"), ("mailbox", "road"), ("houses", "road"), ("houses", "river"), ("man", "bridge"), ("tree", "river"), ("elephant", "water"), 
            ("van", "road"), ("building", "tracks"), ("car", "bridge"), ("castle", "water"), ("mountains", "lake"), 
            ("trees", "tracks"), ("water", "fence"), ("flags", "road"), ("building", "bridge"), ("buildings", "road"), ("chairs", "street")]),
        "in front of": ("b", [("window", "building"), ("leaf", "vase"), ("window", "train"), ("headlight", "bus"), ("windshield", "train"), ("bus", "bus"), 
            ("door", "building"), ("lights", "train"), ("windshield", "bus"), ("window", "bus"), ("water", "wave"), ("window", "airplane"), ("water", "man"), 
            ("balcony", "window"), ("clock", "building"), ("window", "house"), ("windows", "train"), 
            ("sand", "water"), ("plate", "bus"), ("wall", "building"), ("chair", "bleachers"), ("stone", "sheep"), ("windows", "building"), 
            ("pillar", "building"), ("headlights", "bus"), ("columns", "building"), ("tire", "motorcycle"), ("headlight", "truck"), ("giraffe", "giraffe"), 
            ("arm", "body"), ("wall", "house"), ("headlight", "car"), ("sheep", "sheep"), ("dirt", "fence"), ("elephant", "elephant"), 
            ("clouds", "sky"), ("window", "apartment"), ("grill", "truck"), ("surfer", "wave"), ("window", "store"), ("window", "car"), ("branch", "giraffe"), 
            ("water", "boat"), ("plate", "car"), ("beach", "water"), ("cow", "cow"), ("horse", "horse"), ("hand", "body"), ("rock", "building"),
            ("dirt", "bench"), ("bumper", "train"), ("tree", "sky"), ("stone", "fence"), ("water", "sand"), ("leaf", "chair"), 
            ("truck", "truck"), ("hills", "mountain"), ("field", "cow"), ("windshield", "car"), ("clock", "tower"), ("spot", "animal"), ("window", "tower"), 
            ("tile", "building"), ("glass", "building"), ("windows", "plane"), ("pole", "banana"), ("leg", "leg"), ("branch", "elephant"), ("fog", "tree"), 
            ("building", "man"), ("drawer", "desk"), ("wall", "bench"), ("man", "crowd"), ("clock", "window"), 
            ("balcony", "windows"), ("water", "waves"), ("water", "surfer"), ("plate", "truck"), ("motorcycle", "wheel"), ("plate", "train"), ("plate", "plate"), 
            ("water", "duck"), ("clock", "wall"), ("balcony", "doors"), ("water", "surfboard"), ("water", "city"), ("sand", "ocean"), ("sand", "man"), 
            ("glass", "window"), ("glass", "microwave"), ("clock", "curtain"), ("balcony", "beach")]),
        "by": ("b", [("sidewalk", "street"), ("pole", "road"), ("car", "curb"), ("pole", "street"), ("beach", "ocean"), ("sidewalk", "road"), ("zebra", "zebra"), 
            ("elephant", "elephant"), ("beach", "water"), ("water", "beach"), ("tracks", "train"), ("ocean", "beach"), ("water", "sand"), ("rock", "river"), 
            ("giraffe", "giraffe"), ("dirt", "road"), ("elephant", "rock"), ("cat", "cat"), ("dirt", "grass"), 
            ("tooth", "tooth"), ("rock", "tree"), ("wall", "bench"), ("sheep", "sheep"), ("light", "street"), ("land", "water"), ("tree", "ground"), 
            ("man", "man"), ("stone", "grass"), ("wall", "water"), ("wall", "road"), ("water", "shore"), ("leaf", "cow"), ("leaf", "animal"), ("boat", "boat"), 
            ("grass", "dirt"), ("ground", "water"), ("weed", "fence"), ("leaf", "bird"), ("tree", "tree"), ("bunch", "bunch"), ("dirt", "water"), 
            ("grass", "tree"), ("laptop", "computer"), ("toilet", "wall"), ("bench", "rock"), ("grass", "rock"), ("window", "balcony"), ("wire", "laptop"), 
            ("hand", "fruit"), ("window", "airplane"), ("toilet", "tub"), ("wall", "sidewalk"), ("rock", "train"), ("device", "man"), ("hill", "people"), 
            ("road", "elephant"), ("water", "man"), ("lemon", "lemon"), ("bench", "land"), ("words", "glass"), ("orange", "orange"), ("clock", "wood"), 
            ("leaf", "alligator"), ("waves", "beach"), ("truck", "rock"), ("bush", "field"), ("plant", "tree"), ("leaf", "line"), ("person", "man"), 
            ("window", "train"), ("bush", "leaves"), ("rock", "bench"), ("bear", "rock"), ("marker", "airplane"), ("leaf", "elephant"), ("evergreen", "ground"), 
            ("fence", "ground"), ("leaf", "curb"), ("grass", "ground")]),
        "in the corner of": ("w", [("shower", "bathroom"), ("lamp", "room"), ("plant", "room"), ("refrigerator", "kitchen"), ("chair", "room"), ("bed", "room"), 
            ("vase", "table"), ("desk", "room"), ("speaker", "living room"), ("cabinet", "classroom"), ("microwave", "kitchen"), ("windows", "kitchen"), 
            ("lamp", "desk"), ("picture", "bathroom"), ("desk", "living room"), ("toilet", "bathroom"), ("bathtub", "bathroom"), 
            ("bottles", "kitchen"), ("chair", "bedroom"), ("bookshelf", "living room"), ("tv", "kitchen"), ("lamp", "hotel room"), ("man", "bedroom"), 
            ("person", "building"), ("lamp", "bedroom"), ("desk", "bedroom"), ("television", "house"), ("sofa", "room"), ("television", "room"), 
            ("man", "room"), ("tree", "room"), ("tree", "living room"), ("shelf", "room"), ("table", "room"), ("vase", "living room"), ("pot", "room")]),
        "in the center of": ("w", [("table", "room"), ("hole", "donut"), ("net", "court"), ("rug", "room"), ("table", "kitchen"), ("table", "shop"), 
            ("hole", "bagel"), ("hole", "frisbee"), ("pizza", "table"), ("cherry", "cake"), ("sofa", "room"), ("basket", "shop"), ("chair", "room"), 
            ("table", "apartment"), ("flowers", "table"), ("peach", "cake"), ("cake", "table"), ("bed", "bedroom"), ("leaves", "pizza"), ("ottoman", "room")]),
        "behind": ("b", [("sky", "tree"), ("sky", "trees"), ("wave", "man"), ("trees", "field"), ("tree", "field"), ("fence", "court"), ("water", "man"), 
            ("elephant", "elephant"), ("people", "man"), ("car", "car"), ("fence", "field"), ("grass", "man"), ("sky", "building"), ("grass", "zebra"), 
            ("bus", "bus"), ("water", "wave"), ("cow", "cow"), ("grass", "elephant"), ("rock", "bear"), ("grass", "giraffe"), ("tile", "toilet"), 
            ("rock", "giraffe"), ("mountain", "tree"), ("pole", "sign"), ("building", "field"), ("wave", "surfer"), ("rock", "zebra"), ("sky", "man"), 
            ("trees", "grass"), ("waves", "man"), ("ocean", "man"), ("headboard", "bed"), ("horse", "horse"), ("leaves", "bear"), ("mountain", "man"), 
            ("light", "bus"), ("giraffe", "giraffe"), ("tree", "court"), ("grass", "bear"), ("trees", "court"), ("zebra", "zebra"), ("grass", "boy"), 
            ("hands", "back"), ("rock", "elephant"), ("water", "bird"), ("tree", "grass"), ("wall", "clock"), ("mountain", "giraffe"), ("tree", "tree"), 
            ("grass", "cow"), ("mirror", "sink"), ("plane", "plane"), ("field", "tree"), ("bead", "pack"), ("shadow", "man"), ("building", "light"), 
            ("mountains", "man"), ("sky", "clouds"), ("branches", "sign"), ("house", "field"), ("sky", "tower"), ("water", "boat"), ("trees", "road"), 
            ("grass", "woman"), ("pillow", "pillow"), ("background", "man"), ("wall", "sink"), ("wall", "court"), ("sky", "airplane"), ("snow", "man"), 
            ("trees", "slope"), ("grass", "horse"), ("building", "court"), ("trees", "snow"), ("trunk", "bench"), ("building", "grass"), ("tree", "light"), 
            ("building", "tower"), ("fence", "grass"), ("mountain", "plane"), ("sky", "horse"), ("sheep", "sheep"), ("sky", "sign"), ("road", "sign"), 
            ("sidewalk", "man"), ("sky", "plane"), ("trunk", "boy"), ("building", "building"), ("land", "water"), ("arm", "man"), ("sign", "sign"), 
            ("person", "person"), ("brush", "elephant"), ("tower", "building"), ("window", "bus"), ("tile", "table"), ("wall", "stove"), ("leaf", "bird"), 
            ("ocean", "wave"), ("grass", "bird"), ("water", "waves"), ("water", "surfer"), ("mountain", "horse"), ("grass", "girl"), ("grass", "motorcycle"), 
            ("grass", "player"), ("snow", "person"), ("grass", "plane"), ("water", "beach"), ("grass", "animal"), ("building", "sidewalk"), ("grass", "court"), 
            ("pole", "road"), ("grass", "sand"), ("house", "road"), ("ocean", "horse"), ("field", "man"), ("mountain", "truck"), ("mountain", "airplane"), 
            ("mountain", "cow"), ("water", "surfboard"), ("ocean", "surfer"), ("field", "giraffe"), ("grass", "zebras"), ("field", "animal"), 
            ("grass", "person"), ("snow", "skier"), ("water", "boats"), ("mountain", "animal"), ("grass", "sheep"), ("grass", "dirt"), ("ocean", "beach"), 
            ("grass", "dog"), ("waves", "boat"), ("grass", "ground"), ("mountain", "road"), ("waves", "surfer"), ("grass", "water"), ("tree", "road"), 
            ("grass", "street"), ("field", "horse"), ("grass", "road"), ("fence", "road"), ("water", "field"), ("water", "umbrella"), ("grass", "sidewalk"), 
            ("beach", "man"), ("water", "animal"), ("ocean", "sand"), ("buildings", "road"), ("field", "girl"), ("field", "boy"), ("field", "bull"), 
            ("ocean", "woman")]),
        "along": ("w", [("trees", "road"), ("fence", "sidewalk"), ("buildings", "street"), ("grass", "road"), ("fence", "road"), ("trees", "sidewalk"), 
            ("trees", "water"), ("grass", "fence"), ("trees", "tracks"), ("fence", "field"), ("grass", "sidewalk"), ("trees", "street"), ("trees", "slope"), 
            ("trees", "river"), ("grass", "runway"), ("trees", "shore"), ("trees", "path"), ("rocks", "water"), ("fence", "grass"), ("grass", "water"), 
            ("pipe", "wall"), ("fence", "street"), ("trees", "roadside"), ("signs", "road"), ("fence", "tracks"), ("trees", "coast"), ("flowers", "fence"), 
            ("grass", "roadway"), ("buildings", "road"), ("trees", "shoreline"), ("trees", "walkway"), ("trees", "fence"), ("rocks", "shore"), 
            ("rocks", "tracks"), ("bushes", "fence"), ("bushes", "road"), ("buildings", "beach"), ("wall", "road"), ("fence", "water"), ("grass", "tracks"), 
            ("fence", "hill"), ("cars", "street"), ("poles", "tracks"), ("windows", "wall"), ("grass", "shore"), ("buildings", "water"), ("rocks", "shoreline"), 
            ("buildings", "shore"), ("houses", "water"), ("cars", "road"), ("fence", "walkway"), ("rocks", "fence"), ("boat", "river"), ("trees", "beach"), 
            ("fence", "trees"), ("fence", "path"), ("wall", "sidewalk"), ("sheep", "fence"), ("river", "homes"), ("fence", "bridge"), 
            ("shops", "road"), ("houses", "street"), ("rocks", "sand"), ("windows", "building"), ("grass", "street"), ("grass", "shoreline"), ("cows", "fence"), 
            ("buildings", "shoreline"), ("rocks", "beach"), ("hedges", "sidewalk"), ("snow", "road"), ("fence", "platform"), ("vehicles", "road"), 
            ("rocks", "ocean"), ("wires", "wall"), ("waves", "shore"), ("trees", "lake"), ("shrubs", "sidewalk"), ("people", "lake"), ("vehicles", "street"), 
            ("trees", "park"), ("people", "street"), ("bushes", "shoreline"), ("houses", "shore"), ("bushes", "street"), ("boats", "river"), 
            ("sofa", "wall"), ("shrubs", "tracks"), ("fence", "roadside"), ("bushes", "wall"), ("wire", "wall"), ("leaves", "fence"), ("lamps", "street"), 
            ("forest", "river"), ("shrubs", "river"), ("fence", "train"), ("plants", "fence"), ("buildings", "sidewalk"), ("weeds", "fence"), ("trees", "train"), 
            ("grass", "river"), ("shrubs", "street"), ("benches", "fence"), ("sand", "ocean"), ("boat", "shore"), ("sidewalk", "river"), ("plants", "roadside"), 
            ("homes", "water"), ("trees", "highway"), ("fence", "pier"), ("cords", "wall"), ("footprints", "sand")]),
        "on top of": ("b", [("hair", "head"), ("leaf", "grass"), ("line", "court"), ("window", "building"), ("ear", "head"), ("sink", "counter"), 
            ("line", "road"), ("wave", "ocean"), ("line", "street"), ("lid", "toilet"), ("man", "court"), ("wave", "water"), ("glasses", "face"), ("ball", "court"), ("light", "ceiling"), ("window", "bus"), ("man", "ocean"), ("grass", "field"), ("glasses", "head"), ("dirt", "ground"), ("lines", "court"), 
            ("tile", "floor"), ("brick", "ground"), ("numeral", "clock"), ("bolt", "hydrant"), ("watch", "arm"), ("chair", "floor"), ("player", "field"), 
            ("foam", "wave"), ("line", "ground"), ("key", "keyboard"), ("ripples", "ocean"), ("man", "sidewalk"), ("waves", "water"), ("net", "court"), 
            ("man", "field"), ("spot", "road"), ("house", "land"), ("person", "field"), ("tree", "grass"), ("seed", "bread"), ("girl", "field"), 
            ("motorcycle", "road"), ("watch", "wrist"), ("lines", "road"), ("stripes", "zebra"), ("man", "beach"), ("shelf", "wall"), ("key", "computer"), 
            ("person", "sidewalk"), ("sunglasses", "face"), ("zebra", "field"), ("bench", "grass"), ("flower", "bedroom"), ("arrow", "hand"), ("dirt", "field"), 
            ("bus", "street"), ("hair", "woman"), ("person", "road"), ("airplane", "runway"), ("tree", "sidewalk"), ("frame", "table"), 
            ("shade", "lamp"), ("stair", "hallway"), ("keys", "keyboard")]),
        "in the back of": ("w", [("dog", "truck"), ("hole", "chair"), ("window", "building"), ("window", "car"), ("banana", "truck"), ("girl", "car"), 
            ("tool box", "truck"), ("surfboard", "suv"), ("man", "truck"), ("bottle", "fridge"), ("surf board", "car"), ("dog", "car"), ("cord", "computer"), 
            ("fence", "field"), ("plate", "car"), ("window", "room"), ("bread", "oven"), ("tire", "plane"), ("person", "truck"), ("engine", "airplane"), 
            ("flag", "truck"), ("wheel", "plane"), ("door", "trailer"), ("house", "park"), ("pipes", "train car"), ("outlet", "room"), ("doors", "truck"), 
            ("horse", "truck"), ("boat", "truck"), ("tire", "bicycle"), ("wires", "laptop"), ("guy", "plane")]),
        "down": ("w", [("car", "street"), ("person", "sidewalk"), ("car", "road"), ("man", "hill"), ("skier", "slope"), ("man", "sidewalk"), ("window", "side"), 
            ("building", "street"), ("people", "people"), ("people", "street"), ("train", "track"), ("bus", "street"), ("person", "slope"), ("pipe", "wall"), 
            ("fence", "hill"), ("bicycle", "street"), ("fence", "street"), ("building", "road"), ("woman", "sidewalk"), ("trees", "street"), 
            ("van", "road"), ("cars", "tracks"), ("lights", "road"), ("train", "tracks"), ("skiers", "hill"), ("bushes", "street"), ("person", "street"), 
            ("streaks", "wall"), ("path", "hill"), ("suv", "road"), ("elephant", "trail"), ("person", "mountain"), ("sign", "mountain"), ("river", "hill")]),
        "in the middle of": ("w", [("cloud", "sky"), ("jet", "sky"), ("net", "court"), ("plane", "sky"), ("footprint", "sand"), ("clouds", "sky"), 
            ("person", "water"), ("hole", "donut"), ("sheep", "field"), ("tree stump", "grass"), ("zebra", "field"), ("sign", "road"), ("boat", "water"), 
            ("tree", "field"), ("rock", "beach"), ("donut", "shelf"), ("hole", "dough"), ("sign", "snow"), ("bus", "road"), ("table", "room"), 
            ("island", "kitchen"), 
            ("sign", "street"), ("person", "slope"), ("window", "wall"), ("flower", "grass"), ("bench", "ground"), ("man", "ocean"), ("animal", "road"), 
            ("clock", "building"), ("man", "street"), ("spot", "seat"), ("rock", "field"), ("ham", "pizza"), ("mushroom", "burger"), ("couch", "room"), 
            ("rock", "ocean"), ("guy", "street"), ("vase", "table"), ("island", "lake"), ("bed", "bedroom"), ("spot", "road"), ("apple", "container"), 
            ("grass", "field"), ("cow", "field"), ("manhole cover", "street"), ("pedestrian", "street"), ("rocks", "field"), ("bus", "street"), 
            ("fountain", "plaza"), ("egg", "pizza"), ("broccoli", "bowl"), ("ski", "snow"), ("tree", "snow"), ("rug", "room"), ("grand piano", "stage"), 
            ("mushrooms", "burger"), ("bike", "parking lot"), ("pole", "room"), ("cake", "table"), ("goat", "road"), ("vase", "room"), ("lettuce", "sandwich"), 
            ("tree", "park"), ("stop sign", "road"), ("lamp", "road"), ("counter", "kitchen"), ("giraffe", "field"), ("candle", "table"), ("door", "plane"), 
            ("puddle", "road"), ("house", "trees"), ("bed", "room"), ("kite", "sky"), ("orange", "tangerines"), ("hydrant", "street"), ("crack", "ground"), 
            ("pole", "sidewalk"), ("chair", "room"), ("car", "road"), ("bowl", "table"), ("pillow", "bed"), ("cow", "road"), ("statue", "table"), 
            ("island", "ocean"), ("clock", "tower"), ("table", "living room"), ("spoon", "bowl"), ("woman", "court"), ("cheese", "sandwich"), ("island", "sea"), 
            ("strawberry", "bowl"), ("stone", "grass"), ("rocks", "ocean"), ("island", "water"), ("tracks", "snow"), ("clock tower", "street"), 
            ("statue", "plaza")]),
        "at the end of": ("w", [("building", "street"), ("hair", "tail"), ("chair", "bed"), ("building", "road"), ("chair", "table"), ("door", "hallway"), 
            ("bench", "bed"), ("trees", "street"), ("box", "airplane"), ("doorway", "hallway"), ("car", "street"), ("tree", "tunnel"), ("man", "table"), 
            ("house", "street"), ("window", "hall"), ("person", "table"), ("door", "hall"), ("doors", "hallway"), ("door", "train"), ("trees", "road"), 
            ("homes", "street"), ("rope", "boat")]),
        "at the edge of": ("w", [("trees", "field"), ("animal", "water"), ("grass", "water"), ("house", "water"), ("fence", "field"), 
            ("child", "ocean"), ("man", "pool"), ("post", "sidewalk"), ("fence", "court"), ("elephant", "river"), ("fence", "yard"), 
            ("tent", "water"), ("rocks", "ocean"), ("bear", "water"), ("sidewalk", "lawn"), ("trees", "airport"), ("rocks", "field"), 
            ("post", "yard"), ("boat", "ocean"), ("church", "water"), 
            ("buildings", "water"), ("weeds", "pond"), ("hut", "river"), ("fence", "water"), ("bushes", "court"), ("tents", "field"), 
            ("house", "park"), ("trees", "ocean"), ("dog", "lake"), ("grape", "plate"), ("fence", "path"), ("bench", "road"), ("bird", "water")]),
        "alongside": ("w", [("vehicle", "road"), ("tree", "road"), ("trees", "road"), ("car", "road"), ("building", "road"), ("dock", "lake"), 
            ("vehicles", "road"), ("tree", "street"), ("bush", "road"), ("cars", "road"), ("building", "shore"), ("bench", "beach"), 
            ("woman", "train"), ("grass", "road"), ("rocks", "water"), ("tree", "tracks"), ("tree", "water"), ("fence", "street"), 
            ("trees", "train"), ("fence", "train"), 
            ("windows", "train"), ("path", "water"), ("canoe", "shore"), ("fence", "road"), ("pole", "track"), ("grass", "sidewalk"), 
            ("boat", "shore"), ("grass", "pool"), ("bus", "street"), ("bike", "road"), ("grass", "train"), ("bushes", "road"), 
            ("bushes", "building"), ("bench", "road"), ("train", "platform"), ("wires", "building"), ("flowers", "train tracks"), 
            ("man", "train"), ("stores", "street"), ("plants", "train tracks"), 
            ("pots", "sidewalk"), ("pipe", "building"), ("chair", "court"), ("shrub", "tracks"), ("window", "train"), ("car", "street"), 
            ("trees", "beach"), ("trees", "water"), ("tree", "wall"), ("mountain", "beach"), ("powerline", "tracks"), ("shrubs", "rails"), 
            ("street", "building"), ("horses", "fence"), ("shrubs", "fence"), ("dumpster", "road"), ("buildings", "beach"), ("grass", "runway"), 
            ("fork", "knife"), ("fence", "yard"), 
            ("trees", "lake"), ("grass", "street"), ("rocks", "ocean"), ("bicycle", "court"), ("van", "street"), ("gravel", "train tracks"), 
            ("bushes", "tracks"), ("fence", "sidewalk"), ("trunk", "street"), ("dirt", "tracks"), ("bush", "sidewalk"), ("grass", "highway"), 
            ("minivan", "road"), ("tracks", "platform"), ("road", "snow"), ("bench", "street"), ("lake", "road"), ("dirt", "field"), 
            ("man", "road"), ("buildings", "street"), 
            ("rock", "shore"), ("rocks", "road"), ("trees", "bridge"), ("trailer", "street"), ("bin", "road"), ("rocks", "tracks"), 
            ("stones", "tracks"), ("van", "building"), ("post", "tracks"), ("tree", "train"), ("trees", "railway"), ("boulders", "track"), 
            ("plants", "building"), ("buses", "road"), ("building", "track"), ("fence", "building"), ("houses", "beach"), ("tree", "building"), 
            ("fence", "tracks"), ("flowers", "yard"), 
            ("sign", "bus"), ("bush", "tracks"), ("fence", "path"), ("car", "path"), ("trees", "tracks"), ("eggs", "plate"), ("fence", "field"), 
            ("poles", "road"), ("railroad", "platform"), ("person", "train"), ("grass", "building"), ("truck", "street"), ("trees", "path"), 
            ("buildings", "train tracks")]),
        "beyond": ("w", [("trees", "fence"), ("mountains", "water"), ("city", "water"), ("trees", "field"), ("tree", "river"), ("land", "water"), 
            ("tree", "water"), ("bridge", "tree"), ("hill", "building"), ("mountain", "bridge"), ("grass", "fence"), ("mountains", "field"), 
            ("trees", "grass"), ("trees", "water"), ("water", "fence"), ("trees", "court"), ("building", "bridge"), ("mountains", "trees"), ("building", "trees"), 
            ("tree", "fence"), ("trees", "snow"), ("trees", "runway"), ("tower", "train"), ("trees", "wall"), ("home", "tree"), 
            ("grass", "water"), ("water", "grass"), ("mountain", "water"), ("forest", "fence"), ("mountains", "train"), ("buildings", "fence"), 
            ("tree", "window"), ("field", "fence"), ("van", "tree"), ("hills", "water"), ("mountans", "trees"), ("water", "field"), 
            ("chair", "fence"), ("hill", "ocean"), ("home", "fence"), 
            ("trees", "elephants"), ("lake", "trees"), ("ocean", "cliff"), ("buildings", "trees"), ("buildings", "field"), ("building", "window"), 
            ("mountain", "trees"), ("mountains", "beach"), ("trees", "window"), ("hill", "water"), ("trees", "airport"), ("hill", "highway"), 
            ("buildings", "beach"), ("can", "fence"), ("tree", "bridge"), ("mountains", "bushes"), ("court", "fence"), ("buildings", "grass"), 
            ("mountains", "buildings"), 
            ("trees", "umbrellas"), ("rocks", "beach"), ("house", "field"), ("mountains", "city"), ("building", "fence"), ("mound", "fence"), 
            ("building", "bushes"), ("roof", "trees"), ("snow", "trees"), ("field", "trees"), ("car", "tree"), ("tree", "train tracks"), 
            ("house", "tree"), ("tower", "trees"), ("trees", "cows"), ("buildings", "water"), ("road", "tree"), ("hills", "trees"), ("trees", "tents"), 
            ("flowers", "table"), 
            ("bushes", "fence"), ("puddle", "trees"), ("trees", "shelter"), ("hills", "field"), ("mountain", "road"), ("house", "water"), 
            ("tent", "fence"), ("vehicle", "fence"), ("buildings", "bridge"), ("mountains", "park"), ("hill", "train"), ("trees", "train"),
            ("ambulance", "fence"), ("hills", "lake"), ("buildings", "park"), ("hills", "beach"), ("hills", "road"), ("boat", "bushes"), ("trees", "tent"), 
            ("houses", "castle")]),
    }

    # room
    # outdoors
    # indoors

    # adjsDict = json.load(open("objs/cAttrs.json"))
    # commonAdjs += adjsDict.keys()
    # ????? commonAdjs += attrList


    blacklist = ["is", "are", "very", "a", "an", "the", "madeof"] ### the ????????????
    blacklistR = ["is", "are", "very", "a", "an", "madeof"]
    # blacklistR = ["is", "are", "very", "a", "an", "madeof"] ### the ????????????
    for i, imageId in enumerate(data):
        instance = data[imageId]
        
        if i % 1000 == 0:
            print (i)
        for obj in instance["objects"].values():
            #### DS init
            if "attributes" not in obj:
                obj["attributes"] = []

            if "mAttributes" not in obj:
                obj["mAttributes"] = {}

            if "mRels" not in obj:
                obj["mRels"] = {}

            if "senses" not in obj:
                obj["senses"] = {}

            if "opposites" not in obj:
                obj["opposites"] = []

        for obj in instance["objects"].values():
            #### remove common attributes from obj name
            words = obj["name"].split()
            newWords = []
            if len(words) > 1:
                for cand in words[:-1]:
                    if cand in commonAdjs:
                        obj["attributes"].append(cand)
                    else:
                        newWords.append(cand)
            newWords.append(words[-1])
            obj["name"] = " ".join(newWords)

            #### add back attrs needed
            if obj["name"] in combDict:
                for a in combDict[obj["name"]]:
                    if a in obj["attributes"]:
                        obj["name"] = "{} {}".format(a, obj["name"])
                        obj["attributes"].remove(a)

            #### translation dict and num normalization
            obj["name"] = translateDict.get(obj["name"], obj["name"])
            obj["name"] = numsNormalize(obj["name"])

            chickenAnimalObjs = ["ground", "head", "grass", "feather", "feathers", "sheep", "cage", "bird", "fence", "birds"]
            chickenFoodCats = ["food", "tableware", "appliance"] # table 

            if obj["name"] in ["chicken", "turkey"]:
                isAnimal = len([ob["name"] for ob in instance["objects"].values() if ob["name"] in chickenAnimalObjs]) > 0
                isFood = len([ob["name"] for ob in instance["objects"].values() if isAlist(ob, chickenFoodCats)]) > 0

                if isAnimal and not isFood:
                    obj["senses"]["o_" + obj["name"]] = "animal"
                elif isFood and not isAnimal:
                    # print(obj)
                    obj["senses"]["o_" + obj["name"]] = "meat"                    
                else:
                    obj["senses"]["o_" + obj["name"]] = ""

            penOfficeObjs = ["table", "desk", "paper", "keyboard", "mouse", "laptop", "book", "monitor", "key", "computer", "cord", "pencil", "notebook"]
            penPlaceObjs = ["fence", "grass", "sheep", "giraffe", "elephant", "zebra"] # table 

            if obj["name"] == "pen":
                isOffice = len([ob["name"] for ob in instance["objects"].values() if ob["name"] in penOfficeObjs]) > 0
                isPlace = len([ob["name"] for ob in instance["objects"].values() if ob["name"] in penPlaceObjs]) > 0

                if isOffice and not isPlace:
                    obj["senses"]["o_pen"] = "office supplies"
                elif isPlace and not isOffice:
                    # print(obj)
                    obj["senses"]["o_pen"] = "place"                    
                else:
                    obj["name"] += " removed"

            if obj["name"] == "plate":
                sports = ["player", "helmet", "bat", "catcher", "batter", "jersey", "umpire"]
                isSports = len([ob["name"] for ob in instance["objects"].values() if ob["name"] in sports]) > 0
                if isSports:
                    obj["name"] = "home plate"

            if obj["name"] == "desert":
                sports = []
                isFood = len([ob["name"] for ob in instance["objects"].values() if isAlist(ob, ["food", "tableware"])]) > 0
                if isFood:
                    obj["name"] += " removed" # ??????

            if obj["name"] == ["roll"]:
                objNames = [ob["name"] for ob in instance["objects"].values()]
                if "toilet" not in objNames and "bathroom" not in objNames:
                    obj["name"] = "food roll"

            # instance["objects"][ 
            toDel  = []
            toAdd = []

            # # self loops, TODO needed?
            # #### translation relations + blacklist
            # # for rel in obj["outRels"].values():
            #     rel["rel"] = removeSubword(rel["rel"],blacklist)
            #     rel["rel"] = translateDictR.get(rel["rel"], rel["rel"])

            for i, relId in enumerate(obj["outRels"]):
                rel = obj["outRels"][relId]
                o = instance["objects"][rel["obj"]]

                # self loops, TODO needed?
                #### translation relations + blacklist
                # for rel in obj["outRels"].values():
                rel["rel"] = removeSubword(rel["rel"],blacklistR)
                rel["rel"] = translateDictR.get(rel["rel"], rel["rel"])

                #### directions
                if rel["rel"] in mRelsDict and o["name"] in mRelsDict[rel["rel"]]:
                    toDel.append(relId)
                    field = rel["rel"]
                    value = mRelsObjsDict.get(o["name"], o["name"])
                    if field not in obj["mRels"]:
                        obj["mRels"][field] = value 

                if rel["rel"] == "looking at" and o["name"] == "camera":
                    toDel.append(relId)
                    if "looking" not in obj["mRels"]:
                        obj["mRels"]["looking"] = "at the camera" 

                if (rel["rel"] in ["dressed in", "wearing", "in"] and type(o["name"], None) == "color") or \
                    (rel["rel"] in ["made of"] and type(o["name"], None) == "material"):
                    toDel.append(relId)
                    if "dressed in" not in obj["mRels"]:
                        obj["mRels"]["dressed in"] = o["name"] 

                if "playing tennis" in obj["attributes"]:
                    if "playing" not in obj["mRels"]:
                        obj["mRels"]["playing"] = "tennis"

                if rel["rel"] == "cast on" and obj["name"] == "shadow":
                    if rel["rel"] not in o["mRels"]:
                        o["mRels"]["cast on"] = "shadow"                    

                if rel["rel"] in relRepListing:
                    for config in relRepListing[rel["rel"]]:
                        replaceTo, subjS, wordlist = config
                        subj = (subjS == "s")
                        cand = obj["name"] if subj else o["name"] 
                        if cand in wordlist:
                            rel["rel"] = replaceTo

                if rel["rel"] == "looking":
                    rel["rel"] = "looking at"

                # if rel["rel"] in ["piled on"]: # , "stacked on"
                #     m = mod(obj["name"])
                #     if m not in ["plural", "mass"]:
                #         if m == "singular":
                #             obj["name"] = pluralOf(obj["name"])# ???
                #         else:
                #             toDel.append(relId)

                # if rel["rel"] in ["filled of", "filled with"]:
                #     m = mod(o["name"])
                #     if m not in ["plural", "mass"]:
                #         if m == "singular":
                #             o["name"] = pluralOf(o["name"])# ???
                #         else:
                #             toDel.append(relId)

                # if rel["rel"] in ["between", "in between"]:
                #     if (not isPlural(o["name"])) and (o["name"] not in ["bread", "bun"]):
                #         toDel.append(relId)

                # if rel["rel"] == "making":
                #     if (not isA(o,"food")):
                #         toDel.append(relId)

                if rel["rel"] == "reading":
                    if (not isAlist(obj, ["person","animal"])):
                        toDel.append(relId)

                if rel["rel"] in stop:
                    subjectS, nounList = stop[rel["rel"]]
                    subject = (subjectS == "s")
                    if subject:
                        if obj["name"] in nounList:
                            obj["name"] = pluralOf(obj["name"])                        
                    else:
                        if o["name"] in nounList:
                            o["name"] = pluralOf(o["name"])

                #### material rel->att
                if rel["rel"] in ["made of","made from"] and o["name"] in matList:
                    obj["attributes"].append(o["name"])
                
                if rel["rel"] in ["made of","made from"] and o["name"]in matDict:
                    obj["attributes"].append(matDict[o["name"]])
                
                #### activity rel->att
                # for act in actList:
                #     if act in rel["rel"]:
                #         obj["attributes"].append(act)

                #### color rel->att
                for color in colors: 
                    if rel["rel"] in ["wearing "+color, "wearing a "+color, "has "+color]:
                        if color not in o["attributes"]:
                            o["attributes"].append(color)
                        #o["attributes"] = list(set(o["attributes"]))

                if rel["rel"] in ["color", "colored", "painted"] and o["name"] in colors:
                    obj["attributes"].append(o["name"])

                #### activity rel->att (surfing)
                if rel["rel"] in ["surfing", "surfing on", "surfing in"]:
                    obj["attributes"].append("surfing")

                #### typo
                # if obj["name"] == "light" and rel["rel"] == "reflected on":
                #     rel["rel"] = "reflected in"

                #### activity rel->att (meeting)
                if rel["rel"] == "having" and o["name"] == "meeting":
                    obj["attributes"].append("having meeting")

                #### activity rel->att (trick)
                if rel["rel"] == "performing" and o["name"] in ["trick", "tricks", "stunt"]:
                    obj["attributes"].append("performing trick")

                #### activity rel->att (waiting)
                if rel["rel"] == "waiting on":
                    obj["attributes"].append("waiting")

                #### flip passive
                if rel["rel"] in passive:
                    newRelId = "new_" + str(i)
                    newRel = {"rel": passive[rel["rel"]], "subj": rel["obj"], "obj": rel["subj"]}
                    toAdd.append((newRelId, newRel, o, obj))

                if rel["rel"] in ops:
                    newRelId = "new_" + str(i)
                    newRel = {"rel": ops[rel["rel"]], "subj": rel["obj"], "obj": rel["subj"]}
                    toAdd.append((newRelId, newRel, o, obj))
                    rel["sym"] = newRelId
                    newRel["sym"] = relId

                relwords = rel["rel"].split(" ")
                if relwords[-1] == "in":
                    if o["name"] in ["line", "group", "team", "herd", "pile", "stack", "person"]:
                        o["name"] += " removed"

                if relwords[-1] == "on":
                    if o["name"] in ["line", "group", "team", "herd"]:
                        o["name"] += " removed"

                if relwords[-1] == "in" and len(relwords) > 1:
                    if isA(o, "clothing"):
                        toDel.append(relId)

                if rel["rel"] in ["walking on", "standing on", "going on", "running on", "traveling on", "balancing on"]:
                    if o["name"] in ["leg", "legs", "shoe", "shoes", "foot", "feet"]:
                        toDel.append(relId)

                #### self loops
                if rel["obj"] == rel["subj"]:
                    toDel.append(relId)
                    # del obj["outRels"][relId]
                    # del obj["inRels"][relId]

                if rel["rel"] in fixV:
                    preps = [(p, roDict["{} {}".format(rel["rel"],p)].get(oName(instance,rel), 0)) for p in ["on", "in", "at"]]
                    p, c = max(preps, key = lambda x: x[1])
                    if c > 0:
                        rel["rel"] = "{} {}".format(rel["rel"],p)

                if rel["rel"] == "top of":
                    preps = [(p, roDict["{} {}".format(p,rel["rel"])].get(oName(instance,rel), 0)) for p in ["on", "at"]]
                    p, c = max(preps, key = lambda x: x[1])
                    if c > 0:
                        if p == "at":
                            p = "at the"
                        rel["rel"] = "{} {}".format(p, rel["rel"])

                if rel["rel"] == "hanging":
                    rels = [(r, roDict[r].get(oName(instance,rel), 0)) for r in ["hanging from", "hang on"]]
                    r, c = max(rels, key = lambda x: x[1])
                    if c > 0:
                        rel["rel"] = r

                if rel["rel"] == "looking":
                    c = roDict["{} at".format(rel["rel"])].get(oName(instance,rel), 0)
                    if c > 10:
                        rel["rel"] = "{} at".format(rel["rel"])

                if rel["rel"] == "covered":
                    preps = [(p, roDict["{} {}".format(rel["rel"], p)].get(oName(instance,rel), 0)) for p in ["in", "with", "by"]]
                    p1, c1 = max(preps, key = lambda x: x[1])

                    c2 = roDict["covered by"].get(sName(instance,rel), 0)

                    if max(c1,c2) > 0:
                        if c1 > c2:
                            rel["rel"] = "{} {}".format(rel["rel"],p)
                        else:
                            newRelId = "covered_" + str(i)
                            newRel = {"rel": "covered by", "subj": rel["obj"], "obj": rel["subj"]}
                            toAdd.append((newRelId, newRel, o, obj))                            

                if isA(o, "vehicle") and obj["name"] == "plate":
                    obj["name"] = "license plate" # ???????????

                if isA(obj, "vehicle") and o["name"] == "plate":
                    o["name"] = "license plate" # ???????????

                if rel["rel"] in relListing:
                    for condition in relListing[rel["rel"]]:
                        whiteS, subjS, wordlist = condition
                        white = (whiteS == "w")
                        subj = (subjS == "s")
                        cand = obj["name"] if subj else o["name"]
                        cond = (cand in wordlist) if white else (cand not in wordlist)
                        if not cond:
                            toDel.append(relId)

                if rel["rel"] in pairs:
                    whiteS, pairlist = pairs[rel["rel"]]
                    white = (whiteS == "w")
                    cand = (obj["name"], o["name"])
                    cond = (cand in wordlist) if white else (cand not in wordlist)
                    if not cond:
                        toDel.append(relId)

                if rel["rel"].startswith("growing"):
                    if obj["name"] in ["hair", "weed", "leaf"]:
                        toDel.append(relId)

                if rel["rel"] == "washing":
                    if obj["name"] in ["water", "wave", "waves", "toilet"] or o["name"] == "game":
                        toDel.append(relId)

                if rel["rel"] == "splashing":
                    splashingWhite = ["man", "zebra", "elephant", "dog", "horse", "surfer", "boy", "girl"] 
                    if obj["name"] not in splashingWhite or o["name"] != "water":
                        toDel.append(relId)

                if rel["rel"] in ["in front of", "behind"]:
                    if isA(obj, "part") or isA(o, "part"):
                        toDel.append(relId)

                if rel["rel"] == "holding":
                    if isA(obj, "body part") or isA(o, "body part"):
                        toDel.append(relId)

                if rel["rel"] in prepFilters:
                    filter = prepFilters[rel["rel"]]
                    if filter(obj["name"], o["name"]):
                        toDel.append(relId)

                if rel["rel"] == "at":
                    s = obj["name"]
                    o = o["name"]

                    toOn = ["beach", "sidewalk", "platform", "island", "tarmac", "podium", "shore", "pathway", 
                            "street", "pavement", "stairs", "sea"]
                    toIn = ["park", "skate park", "restaurant", "field", "harbor", "river", "market", "room", "water", "area", "court", "parking lot", 
                            "stadium", "bleachers", "parade", "store"]
                    
                    blacklist = [("water", "beach"), ("runway", "airport"), ("car", "curb"), ("player", "bat"), ("tarmac", "airport"), 
                        ("ocean", "beach"), ("curtain", "window"), ("man", "bat"), ("tree", "edge"), ("streetlamp", "night"), 
                        ("curtains", "window"), ("waves", "beach"), ("water", "sand"), ("sky", "sunset"), ("arm", "side"), 
                        ("building", "water"), ("trees", "edge"), ("faucet", "sink"), ("tree", "bottom"), ("light", "night"), 
                        ("window", "building"), ("foaming wave", "sea"), ("people", "terrain"), ("cow", "camera"), 
                        ("trees", "parking"), ("bear", "terrain"), ("glass", "table"), ("flower", "circle"), ("cars", "curb"), 
                        ("person", "slope"), ("batter", "bat"), ("stripe", "top"), ("pot", "windowsil"), ("man", "base"), 
                        ("plane", "airfield"), ("lights", "night"), ("boat", "anchor"), ("batter", "base")]

                    for (s, o) in blacklist:
                        toDel.append(relId)

                    if o in toOn:
                        rel["rel"] = "on"
                    if o in toIn:
                        rel["rel"] = "in"
                    if o == "zoo" and isA(s, "animal"):
                        rel["rel"] = "in"

            for relId in toDel:
                obj["outRels"].pop(relId, None)
                obj["inRels"].pop(relId, None)

            for item in toAdd:
                newRelId, newRel, o, s = item
                o["outRels"][newRelId] = newRel
                s["inRels"][newRelId] = newRel
            
            #### translation attributes + blacklist + set
            obj["attributes"] = [removeSubword(attr,blacklist) for attr in obj["attributes"]]
            obj["attributes"] = [translateDictA.get(attr, attr) for attr in obj["attributes"]]
            obj["attributes"] = list(set(obj["attributes"]))

            if "baby" in obj["attributes"] and not isAlist(obj, ["animal", "person"]):
                obj["attributes"].remove("baby")

            if "light" in obj["attributes"] and isA(obj, "person"):
                obj["attributes"].remove("light")
            if "dark" in obj["attributes"] and isA(obj, "person"):
                obj["attributes"].remove("dark")

            toRemove = []
            for a in obj["attributes"]:
                if type(a, obj) == "color" and (a not in ["blond", "brunette"]) and isA(obj, "person"):
                    toRemove.append(a)                    
            for a in toRemove:
                obj["attributes"].remove(a)

            if obj["name"] == "parking lot" and "parking" in obj["attributes"]:
                obj["attributes"].remove("parking")

            if obj["name"] in ["light", "lights", "signal"] and "traffic" in obj["attributes"]:
                obj["name"] = "traffic {}".format(obj["name"])
                obj["attributes"].remove("traffic")

            if obj["name"] == "drink" and "soft" in obj["attributes"]:
                obj["name"] = "soft drink"
                obj["attributes"].remove("soft")

            if obj["name"] in ["bear", "bears"] and "teddy" in obj["attributes"]:
                obj["name"] = "teddy {}".format(obj["name"])
                obj["attributes"].remove("teddy")

            if obj["name"] in ["floor", "drive"] and "hard" in obj["attributes"]:
                obj["name"] = "hard {}".format(obj["name"])
                obj["attributes"].remove("hard")

            if obj["name"] == "baby elephant":
                obj["name"] = "elephant"
                if "baby" not in obj["attributes"]:
                    obj["attributes"].append("baby")

            if obj["name"] == "smiling woman":
                obj["name"] = "woman"
                if "smiling" not in obj["attributes"]:
                    obj["attributes"].append("smiling")

            if "smiling" in obj["attributes"] and "happy" not in obj["attributes"]:
                obj["attributes"].append("happy")

            for attr in obj["attributes"]:
                if attr in wsd:
                    candidates = [(sense, sum([aoDict[w].get(obj["name"], 0) for w in wsd[attr][sense]])) for sense in wsd[attr]]
                    sense, count = max(candidates, key = lambda x: x[1]) 
                    if count > 0:
                        obj["senses"][attr] = sense 

            weatherObj = ["sky", "day", "scene", "outside", "photo", "air", "weather", "skies", 
                "outdoors", "outdoor", "picture", "background", "area"]
            for attr in obj["attributes"]:
                if type(attr, obj) == "weather" and isA(obj, "place") or obj["name"] in weatherObj:
                    instance["weather"] = attr

                if type(attr, obj) == "room":
                    instance["place"] = attr                 

            # if obj["name"] in rooms: #and allImage(coords(obj)):
            #     instance["room"] = obj["name"]

            if isA(obj, "place"): #allImage(coords(obj)):
                instance["place"] = (obj["name"], size(coords(obj)))

            # relNames = [rel["rel"] for rel in obj["outRels"].values()] 

            #### add male/female
            if obj["name"] in femaleO or "female" in obj["attributes"]:
                #if "female" not in obj["mAttributes"]:
                obj["mAttributes"]["gender"] = "female" ## ????????
            if obj["name"] in maleO or "male" in obj["attributes"]:
                #if "male" not in obj["mAttributes"]:
                obj["mAttributes"]["gender"] = "male"

            if obj["name"] in youngO or "young" in obj["attributes"]:
                #if "female" not in obj["mAttributes"]:
                obj["mAttributes"]["age"] = "young"
            if obj["name"] in adultO  or "old" in obj["attributes"]:
                #if "male" not in obj["mAttributes"]:
                obj["mAttributes"]["age"] = "old"

            if obj["name"] in healthyO or "healthy" in obj["attributes"]:
                #if "female" not in obj["mAttributes"]:
                obj["mAttributes"]["healthiness"] = "healthy"
            if obj["name"] in unhealthyO or "unhealthy" in obj["attributes"]:
                #if "male" not in obj["mAttributes"]:
                obj["mAttributes"]["healthiness"] = "unhealthy"

            if obj["name"] in indoorsO:
                instance["location"] = "indoors"
            if obj["name"] in outdoorsO:
                instance["location"] = "outdoors"

            if obj["name"] in subtypes:
                for t in subtypes[obj["name"]]:
                    if t in obj["attributes"]:
                        obj["mAttributes"]["type"] = t

            for attr in obj["attributes"]:
                m = attr2mattr(attr, obj) 
                if m is not None:
                    mtype, mattr = m
                    obj["mAttributes"][mtype] = mattr


            # objsDict.addSymbols(obj["name"])
            # attrsDict.addSymbols(obj["attributes"])
            # relsDict.addSymbols(relNames)
            if obj["name"] in oppositesDict:
                obj["opposites"].append((obj["name"], oppositesDict[obj["name"]]))

            if cat(obj) == "fruit":
                obj["opposites"].append(("fruit", "vegetable"))

            if cat(obj) == "vegetable":
                obj["opposites"].append(("vegetable", "fruit"))



        #### add positional information
        instance["posRels"] = {}

        posRelId = 0
        for objId in instance["objects"]:
            obj = instance["objects"][objId]

            #### global
            c = coords(obj)
            if not valid(c):
                continue            
            obj["pos"] = []
            if globalleft(c):
                 obj["pos"].append("left") # on the left [side] of
            if globalright(c):
                 obj["pos"].append("right") # on the right [side] of
            if globaltop(c):
                 obj["pos"].append("top") # at the top of #upper part
            if globalbottom(c):
                 obj["pos"].append("bottom") # at the bottom of # lower part
            if globalmiddle(c):
                 obj["pos"].append("middle") # in the middle|center of  

            obj["posRels"] = []

            #### relative
            for otherObjId in instance["objects"]:
                otherObj = instance["objects"][otherObjId]
                otherC = coords(otherObj)
                if not valid(otherC):
                    continue
                isLeft = relativeleft(c, otherC)
                isRight = relativeright(c, otherC)

                if isLeft or isRight:
                    direction = "left of" if isLeft else "right of"
                    posRel = {"rel": direction, "subj": objId, "obj": otherObjId} 
                    
                    obj["outRels"]["pr{}".format(posRelId)] = posRel
                    otherObj["inRels"]["pr{}".format(posRelId)] = posRel

                    if "backpointers" not in otherObj:
                        otherObj["backpointers"] = {}
                    otherObj["backpointers"][objId] = posRelId
                    
                    if "backpointers" in obj and otherObjId in obj["backpointers"]:
                        symRelId = obj["backpointers"][otherObjId]
                        if symRelId not in instance["posRels"]:
                            print (symRelId)
                            print (c, otherC)
                            print(isLeft, isRight)
                            print(posRel)
                        symRel = instance["posRels"][symRelId]
                        posRel["sym"] = symRelId
                        symRel["sym"] = posRelId

                    instance["posRels"][posRelId] = posRel
                    obj["posRels"].append(posRelId)
                    posRelId += 1

            hasOf = False
            for rel in obj["outRels"].values():
                if rel["rel"] == "of":
                    obj["of"] = rel["obj"]
                    obj["strongOf"] = True
                    hasOf = True
            if not hasOf:
                for rel in obj["inRels"].values():
                    if rel["rel"] == "have":
                        obj["of"] = rel["subj"]
                        obj["strongOf"] = False
                        hasOf = True                
            if not hasOf:
                candidates = [(otherObjId, partOfRate(obj, otherObj)) for otherObjId in instance["objects"]]
                contain = max(candidates, key = lambda x: x[1])
                if contain[1] > args.iSize:
                    obj["of"] = contain[0]
                    obj["strongOf"] = False

        ######################################################### TODO
        instance["uobjects"] = copy.deepcopy(instance["objects"])
        instance["uposRels"] = copy.deepcopy(instance["posRels"])

        #### remove unrecognized entities
        instance["objects"] = {objId: obj for objId, obj in instance["uobjects"].items() if obj["name"] in objList}
        instance["posRels"] = {posRelId: posRel for posRelId, posRel in instance["posRels"].items() if (posRel["subj"] in instance["objects"]) and (posRel["obj"] in instance["objects"])}
        for objId in instance["objects"]:
            obj = instance["objects"][objId]
            obj["attributes"] = [attr for attr in obj["attributes"] if attr in attrList]
            obj["outRels"] = {relId: rel for relId, rel in obj["outRels"].items() if rel["rel"] in relList and rel["obj"] in instance["objects"]}
            obj["inRels"] = {relId: rel for relId, rel in obj["inRels"].items() if rel["rel"] in relList and rel["subj"] in instance["objects"]}
            obj["posRels"] = [posRelId for posRelId in instance["posRels"]]
            if "of" in obj and obj["of"] not in instance["objects"]:
                obj.pop("of")
                obj.pop("strongOf")

        #### compute name2obj
        instance["name2obj"] = hashObjs({}, instance["objects"])
        if "predObjects" in instance:
            instance["name2obj"] = hashObjs(instance["name2obj"], instance["predObjects"])

        # try:
        if args.vis:
            vis(imageId)
        # except:
        #     pass

if args.normalize:
    normalize()

# attrsDict.createVocab()

# objsDict.createVocab()
# attrsDict.createVocab()
# relsDict.createVocab()

def createAttrsDict():
    oDict = defaultdict(lambda: 0)
    oaDict = defaultdict(lambda: defaultdict(lambda: 0))
    noaDict = defaultdict(dict)
    noaList = {}
    for i, instance in enumerate(data.values()):
        if i % 1000 == 0:
            print (i)
        for obj in instance["objects"].values():
            o = obj["name"]
            oDict[o] += 1
            for a in obj["attributes"]:
                oaDict[o][a] += 1 # attrsObjDict[a].get(obj["name"], 0) + 1
    
    for o in oaDict:
        for a in oaDict[o]:
            noaDict[o][a] = oaDict[o][a] / oDict[o]

        # candidates = [c for c in oaDict[o].items() ] # if c[1] < 0.9
        noaList[o] = sorted(noaDict[o].items(), reverse = True, key = lambda x: x[1])[:20]

    return oaDict, noaDict, noaList

# def createObjs2Dict():
#     attrsObjDict = {}
#     for a in attrsDict.sortedCounter:
#         attrsObjDict[a[0]] = {}

#     for i, instance in enumerate(data.values()):
#         if i % 1000 == 0:
#             print (i)
#         for obj in instance["objects"].values():
#             for a in obj["attributes"]:
#                 attrsObjDict[a][obj["name"]] = attrsObjDict[a].get(obj["name"], 0) + 1
#     return attrsObjDict

def createRelsDict():
    relCombDict = defaultdict(lambda: defaultdict(lambda: 0))
    relSubjDict = defaultdict(lambda: defaultdict(lambda: 0))
    relObjDict = defaultdict(lambda: defaultdict(lambda: 0))

    for i, instance in enumerate(data.values()):
        if i % 1000 == 0:
            print (i)
        for obj in instance["objects"].values():
            for rel in obj["outRels"].values():
                relName = rel["rel"]
                subjName = instance["objects"][rel["subj"]]["name"]
                objName = instance["objects"][rel["obj"]]["name"]
                combination = "_".join([subjName, objName])
                relSubjDict[relName][subjName] += 1 #relSubjDict[relName].get(subjName, 0) + 1
                relObjDict[relName][objName] += 1 #relObjDict[relName].get(objName, 0) + 1
                relCombDict[relName][combination] += 1 #relCombDict[relName].get(combination, 0) + 1

    return relCombDict, relSubjDict, relObjDict

def createObjsDict():
    retDict = defaultdict(dict)

    for i, instance in enumerate(data.values()):
        if i % 1000 == 0:
            print (i)
        for obj in instance["objects"].values():
            for a in obj["attributes"]:
                retDict[obj["name"]][a] += 1 #retDict[obj["name"]].get(a, 0) + 1
    return retDict

def createObjs2Dict():
    retDict = defaultdict(dict)

    for i, instance in enumerate(data.values()):
        if i % 1000 == 0:
            print (i)
        for obj in instance["objects"].values():

            for obj2 in instance["objects"].values():
                retDict[obj["name"]][obj2["name"]] += 1 #retDict[obj["name"]].get(obj2["name"], 0) + 1

    # for obj in instance["objects"].values():
    #     for obj2 in instance["objects"].values():
    #         retDict[obj["name"]][obj2["name"]] = #retDict[obj["name"]].get(obj2["name"], 0) + 1

    return retDict

def createObjsCODict():
    oDict = defaultdict(lambda: defaultdict(lambda: 0))
    cDict = defaultdict(dict)
    mDict = defaultdict(lambda: 0)
    fList = {}
    # for o in objsDict.sortedCounter:
    #     oDict[o[0]] = {}
    #     cDict[o[0]] = {}
    #     mDict[o[0]] = {}

    for i, instance in enumerate(data.values()):
        if i % 1000 == 0:
            print (i)
        objSet = set([obj["name"] for obj in instance["objects"].values()])
        for objN in objSet:
            mDict[objN] += 1 # mDict.get(obj["name"], 0) +

            for objN2 in objSet:
                if objN2 != objN:
                    oDict[objN][objN2] += 1 # = oDict[obj["name"]].get(obj2["name"], 0) 

    for objName in oDict:
        for objName2 in oDict[objName]:
            cDict[objName][objName2] = oDict[objName][objName2] / mDict[objName2]

        candidates = [c for c in cDict[objName].items() ] # if c[1] < 0.9
        fList[objName] = sorted(candidates, reverse = True, key = lambda x: x[1])[:50]
            # .get(obj2["name"], 0) objName2
            # cDict[obj["name"]][obj2["name"]] = oDict[obj["name"]].get(obj2["name"], 0) + 1
    # oDict, cDict, mDict, 
    
    otDict = {}
    for o in oDict:
        for o2 in oDict[o]:
            if (o, o2) not in otDict:
                otDict[(o, o2)] = oDict[o][o2]

    otPerCatDict = defaultdict(dict)
    for o in oDict:
        for o2 in oDict[o]:
            c = commonAns(catn(o), catn(o2))
            # if cat is not None:
            if (o, o2) not in otPerCatDict[c]:
                otPerCatDict[c][(o, o2)] = oDict[o][o2]

    otList = sorted(otDict.items(), reverse = True, key = lambda x: x[1])[:2000]
    
    otPerCatList = {}    
    for c in otPerCatDict:
        otPerCatList[c] = sorted(otPerCatDict[c].items(), reverse = True, key = lambda x: x[1])[:2000]

    return oDict, cDict, fList, otList, otPerCatList

def createObjsSRODict():
    sroDict = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda:0)))
    orsDict = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda:0)))
    sorDict = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda:0)))

    sroList = defaultdict(dict)
    orsList = defaultdict(dict)
    sorList = defaultdict(dict)

    opsDict = {}
    opsList = []

    topSORDict = defaultdict(lambda:0)
    topSORList = []
    topOonDict = defaultdict(lambda:0)
    topOonList = []
    # srhisto = avg

    srmultiDict = defaultdict(lambda:0)
    ormultiDict = defaultdict(lambda:0)

    srmultiODict = defaultdict(lambda:0)
    ormultiODict = defaultdict(lambda:0)

    # for o in objsDict.sortedCounter:
    #     # sroDict[o[0]] = {}
    #     # orsDict[o[0]] = {}
    #     # sorDict[o[0]] = {}

    #     # sroList[o[0]] = {}
    #     # orsList[o[0]] = {}
    #     # sorList[o[0]] = {}

    #     for r in relsDict.sortedCounter:
    #         sroDict[o[0]][o[0]] = {}
    #     for r in relsDict.sortedCounter:
    #         orsDict[o[0]][r[0]] = {}
    #     for o in objsDict.sortedCounter:
    #         sorDict[o[0]][o[0]] = {}

    for i, instance in enumerate(data.values()):
        srCount = defaultdict(lambda:0)
        orCount = defaultdict(lambda:0)
        if i % 1000 == 0:
            print (i)
        for subj in instance["objects"].values():
            srCountO = defaultdict(lambda:0)
            for rel in subj["outRels"].values():
                obj = instance["objects"][rel["obj"]]
                s = subj["name"]
                r = rel["rel"]
                o = obj["name"]

                sroDict[s][r][o] += 1 #sroDict[s][r].get(o,0) + 1
                orsDict[o][r][s] += 1 #orsDict[o][r].get(s,0) + 1
                sorDict[s][o][r] += 1 #sorDict[s][o].get(r,0) + 1
                topSORDict[(s,o,r)] += 1
                topOonDict[(s,o)] += 1
                srCount[(s,r)] += 1
                orCount[(o,r)] += 1
                srCountO[(s,r)] += 1

            for s,r in srCountO:
                if srCountO[(s,r)] > 2:
                    srmultiODict[(s,r)] += 1
        
        for obj in instance["objects"].values():
            orCountO = defaultdict(lambda:0)
            for rel in obj["inRels"].values():
                orCountO[(obj["name"],rel["rel"])] += 1
            
            for o,r in orCountO:
                if orCountO[(o,r)] > 2:                
                    ormultiODict[(o,r)] += 1    

        for s,r in srCount:
            if srCount[(s,r)] > 1:
                srmultiDict[(s,r)] += 1
                
        for o,r in orCount:
            if orCount[(o,r)] > 1:                
                ormultiDict[(o,r)] += 1

    for s in sroDict:
        for r in sroDict[s]:
            for o in sroDict[s][r]:
                if (o,r,s) not in opsDict and o in sroDict and r in sroDict[o] and s in sroDict[o][r]:
                    opsDict[(s,r,o)] = (min(sroDict[s][r][o], sroDict[o][r][s]), sroDict[s][r][o], sroDict[o][r][s]) 

    for s in sroDict:
        for r in sroDict[s]:
            sroList[s][r] = sorted(sroDict[s][r].items(), reverse = True, key = lambda x: x[1])[:50]

    for o in orsDict:
        for r in sroDict[o]:
            orsList[o][r] = sorted(orsDict[o][r].items(), reverse = True, key = lambda x: x[1])[:50]

    for s in sorDict:
        for o in sorDict[s]:
            sorList[s][o] = sorted(sorDict[s][o].items(), reverse = True, key = lambda x: x[1])[:50]

    opsList = sorted(opsDict.items(), reverse = True, key = lambda x: x[1][0])[:2000]
    topSORList = sorted(topSORDict.items(), reverse = True, key = lambda x: x[1])[:2000]
    topOonList = sorted(topOonDict.items(), reverse = True, key = lambda x: x[1])[:2000]

    # fix to be count of multi per unique object
    srmultiList = sorted(srmultiDict.items(), reverse = True, key = lambda x: x[1])[:2000]
    ormultiList = sorted(ormultiDict.items(), reverse = True, key = lambda x: x[1])[:2000]

    srmultiOList = sorted(srmultiODict.items(), reverse = True, key = lambda x: x[1])[:2000]
    ormultiOList = sorted(ormultiODict.items(), reverse = True, key = lambda x: x[1])[:2000]

        # for objName2 in oDict[objName]:
        #     cDict[objName][objName2] = oDict[objName][objName2] / mDict[objName2]

        # fDict[objName] = 
            # .get(obj2["name"], 0) objName2
            # cDict[obj["name"]][obj2["name"]] = oDict[obj["name"]].get(obj2["name"], 0) + 1

    ooNDict = defaultdict(lambda:0)
    ooDict = defaultdict(lambda:0)
    for i, instance in enumerate(data.values()):
        if i % 1000 == 0:
            print (i)
        objSet = set([obj["name"] for obj in instance["objects"].values()])
        for s in objSet:
            for o in objSet:
                if s != o:
                    ooNDict[(s,o)] += 1
                    ooDict[(s,o)] += 1

    for i, instance in enumerate(data.values()):
        sorSet = set()
        for subj in instance["objects"].values():
            for rel in subj["outRels"].values():
                obj = instance["objects"][rel["obj"]]
                s = subj["name"]
                # r = rel["rel"]
                o = obj["name"]
                if s != o:
                    sorSet.add((s,o))

            for (s,o) in sorSet:
                ooNDict[(s,o)] -= 1

    ooTFDict = {}
    for s,o in ooDict:
        ooTFDict[(s,o)] = (min(ooDict[(s,o)] - ooNDict[(s,o)], ooNDict[(s,o)]), ooDict[(s,o)] - ooNDict[(s,o)], ooNDict[(s,o)]) 

    ooTFList = sorted(ooTFDict.items(), reverse = True, key = lambda x: x[1][0])[:2000]

    oorr = {}
    for s in sorList:
        for o in sorList[s]:
            if len(sorList[s][o]) > 1:
                oorr[(s,o)] = (sorList[s][o][1][1], sorList[s][o][0], sorList[s][o][1])
    oorrList = sorted(oorr.items(), reverse = True, key = lambda x: x[1][0])[:2000]

    return sroDict, sroList, orsList, sorList, opsList, topSORList, topOonList, \
        ooTFList, oorrList, srmultiList, ormultiList, srmultiOList, ormultiOList

def diff(a, b):
    return [x for x in a if x not in b]

def createObjs2ImgDict():
    oDict = defaultdict(list)
    ooDict = defaultdict(lambda: defaultdict(list))
    oorDict = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
    oonDict = defaultdict(lambda: defaultdict(list))
    # oODict = defaultdict(dict)
    # ooRDict = defaultdict(lambda: defaultdict(dict))
    # ooNDict = defaultdict(lambda: defaultdict(list))
    # for o in objsDict.sortedCounter:
    #     oDict[o[0]] = {}
    #     ooDict[o[0]] = {}
    #     oorDict[o[0]] = {}
    #     oODict[o[0]] = {}
    #     ooRDict[o[0]] = {}

    #     for o in relsDict.sortedCounter:
    #         sroDict[o[0]][o[0]] = {}
    #     for r in relsDict.sortedCounter:
    #         orsDict[o[0]][r[0]] = {}
    #     for o in objsDict.sortedCounter:
    #         sorDict[o[0]][o[0]] = {}

    for i, imgId in enumerate(data):
        instance = data[imgId]
        if i % 1000 == 0:
            print (i)
        for subj in instance["objects"].values():
            s = subj["name"]
            oDict[s].append(imgId)
            for rel in subj["outRels"].values():
                obj = instance["objects"][rel["obj"]]
                r = rel["rel"]
                o = obj["name"]
                oorDict[s][o][r].append(imgId)
                oonDict[s][o].append(imgId)

        for subj in instance["objects"].values():
            for obj in instance["objects"].values():
                s = subj["name"]
                o = obj["name"]
                ooDict[s][o].append(imgId)

        # for s in ooDict:
        #     for o in ooDict[s]:
        #         oODict[s][o] = diff(oDict[s], ooDict[s][o])
        #         for r in oorDict[s][o]:
        #             ooRDict[s][o][r] = diff(ooDict[s][o],oorDict[s][o][r])
        #             ooNDict[s][o] = diff(ooNDict[s][o],oorDict[s][o][r])

        # ops o <-r-> s  

        # for objName2 in oDict[objName]:
        #     cDict[objName][objName2] = oDict[objName][objName2] / mDict[objName2]

        # fDict[objName] = 
            # .get(obj2["name"], 0) objName2
            # cDict[obj["name"]][obj2["name"]] = oDict[obj["name"]].get(obj2["name"], 0) + 1

    # for o in oDict:
    #     oDict[o] = list(oDict[o])

    # for o1 in oDict:
    #     for o2 in oDict[o1]:
    #         oDict[o1][o2] = list(oDict[o1][o2])

    # for o1 in oDict:
    #     for o2 in oDict[o1]:
    #         oDict[o1][o2] = list(oDict[o1][o2])

    # for o1 in oDict:
    #     for o2 in oDict[o1]:
    #         for r in oDict[o1][o2]:
    #         oDict[o1][o2][r] = list(oDict[o1][o2][r])    

    # for o1 in oDict:
    #     for o2 in oDict[o1]:
    #         ooNDict[o1][o2] = list(ooNDict[o1][o2])

    return oDict, ooDict, oorDict, oonDict #,oODict, ooRDict, ooNDict


# def createObjsCODict():
#     oDict = {}
#     ooDict = {}
#     orDict = {}
#     oorDict = {}
#     oroDict = {}
#     for o in objsDict.sortedCounter:
#         oDict[o[0]] = {}
#         ooDict[o[0]] = {}
#         orDict[o[0]] = {}
#         oorDict[o[0]] = {}
#         oroDict[o[0]] = {}
#         for o in objsDict.sortedCounter:
#             oorDict[o[0]][o[0]] = {}
#         for r in relsDict.sortedCounter:
#             oroDict[o[0]][r[0]] = {}

#     for i, instance in enumerate(data.values()):
#         if i % 1000 == 0:
#             print (i)
#         for obj in instance["objects"].values():
#             oDict[obj["name"]] += 1 # mDict.get(obj["name"], 0) +

#             for rel in obj["outRels"].values():
#                 obj2 = instance["objects"][rel["obj"]]

#                 orDict[obj["name"]][rel["rel"]] = orDict[obj["name"]].get(rel["rel"], 0) + 1
#                 oorDict[obj["name"]][obj2["name"]][rel["rel"]] = oorDict[obj["name"]][obj2["name"]].get(rel["rel"], 0) + 1

#     for objName in oDict:
#         for objName2 in oDict[objName]:
#             cDict[objName][objName2] = oDict[objName][objName2] / mDict[objName2]

#         fDict[objName] = sorted(cDict[objName].items(), reverse = True, key = lambda x: x[1])[:20]
#             # .get(obj2["name"], 0) objName2
#             # cDict[obj["name"]][obj2["name"]] = oDict[obj["name"]].get(obj2["name"], 0) + 1

#     return oDict, cDict, mDict, fDict

# def createObjsDict():
#     retDict = {}
#     cDict = {}
#     for o in objsDict.sortedCounter:
#         retDict[o[0]] = {}
#     mDict = {}

#     for i, instance in enumerate(data.values()):
#         if i % 1000 == 0:
#             print (i)
#         for obj in instance["objects"].values():
#             mDict[obj["name"]] = mDict.get(obj["name"], 0) + 1
#             for a in obj["attributes"]:
#                 retDict[obj["name"]][a] = retDict[obj["name"]].get(a, 0) + 1


#     for i, instance in enumerate(data.values()):
#         if i % 1000 == 0:
#             print (i)
#         for obj in instance["objects"].values():
#             mDict[obj["name"]] = mDict.get(obj["name"], 0) + 1
#             for a in obj["attributes"]:
#                 retDict[obj["name"]][a] = retDict[obj["name"]].get(a, 0) + 1

#     return retDict


def createObjAttrCat():
    catDict = {}
    for i, instance in enumerate(data.values()):
        if i % 1000 == 0:
            print (i)
        for obj in instance["objects"].values():
            for a in obj["attributes"]:
                cat = find_closest_category(a, obj["name"])
                if obj["name"] not in catDict:
                    catDict[obj["name"]] = {}
                catDict[obj["name"]][a] = catDict[obj["name"]].get(a,[]) + [cat]
    return catDict

#       longNum = attrsDict["long"].get(obj, 0)

#       tallNum = attrsDict["tall"].get(obj, 0)

# attrsObjDict = createAttrsDict()
# objAttrsDict = createObjsDict()
#relCombDict, relSubjDict, relObjDict = createRelsDict()
# obj2Dict = createObjs2Dict()

# oaList = createAttrsDict()
# ooList = createObjsCODict() # _,_,_,
# sroList, orsList, sorList, opsList = createObjsSRODict()
# oImg, ooImg, oorImg, oOImg, ooRImg, ooNImg = createObjs2ImgDict()

# objAttrCat = createObjAttrCat()

def fixWSD(attr, senses):
    attrsDict.counter[attr] = 0
    for sense in senses:
        attrsDict.counter["_".join([attr, sense[1]])] = 0
        
    objsToSense = {}
    for obj in attrsObjDict[attr]:
        senseCounts = [(sense[0], sense[1], attrsObjDict[sense[0]].get(obj,0)) for sense in senses]
        maxSense = max(senseCounts, key = lambda s: s[2])
        if maxSense[2] > 0:
            objsToSense[obj] = maxSense[1]

    for i, instance in enumerate(data.values()):
        if i % 1000 == 0:
            print (i)
        for obj in instance["objects"].values():
            if attr in obj["attributes"]:
                if obj["name"] in objsToSense:
                    suffix = objsToSense[obj["name"]]
                    if suffix != "":
                        newAttr = "_".join([attr, sufix])
                    else:
                        newAttr = attr
                    obj["attributes"].remove(attr)
                    obj["attributes"].append(newAttr)
                else:
                    newAttr = attr
                attrsDict.counter[newAttr] += 1
                # for sense in senses:

                # if maxSense > 0:
                #   obj["attributes"].remove()

# fixWSD("short", [("long", ""), ("tall", "h")])
# fixWSD("light", [("dark", ""), ("heavy", "w")])
# fixWSD("little", [("young", "a"), ("large", "")])

### SAVE DATA

# attrsDict.sortCounter() 

# with open(dataFilenameNew, "w") as f:
#    json.dump(data, f)

if args.normalize:
    with open(dataFilenameNew, "w") as f:
       json.dump(data, f)
else:
    with open(dataFilenameNew) as f:
       data = json.load(f)

# with open(outDict("attrsNew"), "wb") as outFile:
#     pickle.dump(attrsDict, outFile)

oaCount, oaProb, oaList = createAttrsDict()
ooCount, ooProb, ooList, topOO, topCOO = createObjsCODict() # _,_,_,
sroCount, sroList, orsList, sorList, opsList, topSORList, topOonList, \
    ooTFList, oorrList, srmultiList, ormultiList, srmultiOList, ormultiOList = createObjsSRODict() # needed also probs or too low to be statistically significant??
oImg, ooImg, oorImg, oonImg = createObjs2ImgDict() #, oOImg, ooRImg, ooNImg 
relCombDict, relSubjDict, relObjDict = createRelsDict()

# with open(outJson("relCombDict"), "w") as outFile:
#     json.dump(relCombDict, outFile)

# with open(outJson("relSubjDict"), "w") as outFile:
#     json.dump(relSubjDict, outFile)

# with open(outJson("relObjDict"), "w") as outFile:
#     json.dump(relObjDict, outFile)

with open(outJson("rcCount"), "w") as outFile:
    json.dump(relCombDict, outFile)

with open(outJson("rsCount"), "w") as outFile:
    json.dump(relSubjDict, outFile)

with open(outJson("roCount"), "w") as outFile:
    json.dump(relObjDict, outFile)
            
with open(outJson("oaCount"), "w") as outFile:
    json.dump(oaCount, outFile)

with open(outJson("oaProb"), "w") as outFile:
    json.dump(oaProb, outFile)

with open(outJson("ooCount"), "w") as outFile:
    json.dump(ooCount, outFile)

with open(outJson("ooProb"), "w") as outFile:
    json.dump(ooProb, outFile)

with open(outJson("sroCount"), "w") as outFile:
    json.dump(sroCount, outFile)

with open(outJson("oaList"), "w") as outFile:
    json.dump(oaList, outFile)

with open(outJson("ooList"), "w") as outFile:
    json.dump(ooList, outFile)

with open(outJson("sroList"), "w") as outFile:
    json.dump(sroList, outFile)

with open(outJson("orsList"), "w") as outFile:
    json.dump(orsList, outFile)

with open(outJson("sorList"), "w") as outFile:
    json.dump(sorList, outFile)

with open(outJson("opsList"), "w") as outFile:
    json.dump(opsList, outFile) 

with open(outJson("topSORList"), "w") as outFile:
    json.dump(topSORList, outFile) 

with open(outJson("topOonList"), "w") as outFile:
    json.dump(topOonList, outFile) 

with open(outJson("ooTFList"), "w") as outFile:
    json.dump(ooTFList, outFile) 

with open(outJson("oorrList"), "w") as outFile:
    json.dump(oorrList, outFile) 

with open(outJson("srmultiList"), "w") as outFile:
    json.dump(srmultiList, outFile) 

with open(outJson("ormultiList"), "w") as outFile:
    json.dump(ormultiList, outFile) 

with open(outJson("srmultiOList"), "w") as outFile:
    json.dump(srmultiOList, outFile) 

with open(outJson("ormultiOList"), "w") as outFile:
    json.dump(ormultiOList, outFile) 

with open(outJson("oImg"), "w") as outFile:
    json.dump(oImg, outFile) 

with open(outJson("ooImg"), "w") as outFile:
    json.dump(ooImg, outFile) 

with open(outJson("oorImg"), "w") as outFile:
    json.dump(oorImg, outFile) 

with open(outJson("oonImg"), "w") as outFile:
    json.dump(oonImg, outFile) 

# with open(outJson("oOImg"), "w") as outFile:
#     json.dump(oOImg, outFile) 

# with open(outJson("ooRImg"), "w") as outFile:
#     json.dump(ooRImg, outFile) 

# with open(outJson("ooNImg"), "w") as outFile:
#     json.dump(ooNImg, outFile) 

def printCombs(name, combsDict, marginalDict):
    with open(outTxt(name), "w") as f:
        for x in combsDict:
            try:
              f.write("- "+x + "," + str(marginalDict[x]))
              f.write("\n")
              s = sorted(combsDict[x].items(), reverse = True, key = lambda i: i[1])
              for y, num in s:
                  try:
                    f.write("-- "+y + "," + str(num))
                  except:
                    pass
                  f.write("\n")
            except:
                pass
            f.write("\n")

def printList(name, combsDict):
    with open(outTxt(name), "w") as f:
        for x in combsDict:
            try:
              f.write("- "+x)
              f.write("\n")
              for y, num in combsDict[x]:
                  try:
                    f.write("-- "+y + "," + str(num))
                  except:
                    pass
                  f.write("\n")
            except:
                pass
            f.write("\n")

def printList2(name, combsDict):
    with open(outTxt(name), "w") as f:
        for x in combsDict:
            try:
                f.write("- "+x)
                f.write("\n")
                for z in combsDict[x]:
                    try:
                        f.write("-- "+z)
                        f.write("\n")
                        for y, num in combsDict[x][z]:
                            try:
                                f.write("--- "+y + "," + str(num))
                            except:
                                pass
                            f.write("\n")
                    except:
                        pass
                f.write("\n")
            except:
                pass
            f.write("\n")

printList("oaList", oaList)
printList("ooList", ooList)
printList2("sroList", sroList)
printList2("orsList", orsList)
printList2("sorList", sorList)
printList("opsList", opsList)
# printList("oImg", oImg)
# printList("ooImg", ooImg)
# printList("oorImg", oorImg)
# printList("oOImg", oOImg)
# printList("ooRImg", ooRImg)
# printList("ooNImg", ooNImg)

# with open(outDict("objsNew"), "wb") as outFile:
#     pickle.dump(objsDict, outFile)

# with open(outJson("objsNew"), "w") as outFile:
#     json.dump(objsDict.sortedCounter, outFile)

# with open(outDict("relsNew"), "wb") as outFile:
#     pickle.dump(relsDict, outFile)

# with open(outJson("relsNew"), "w") as outFile:
#     json.dump(relsDict.sortedCounter, outFile)

# with open(outJson("cat"), "w") as outFile:
#     json.dump(objAttrCat, outFile)

# toTxt("objsNew", wn.NOUN)
# toTxt("attrsNew", wn.ADJ)
# toTxt("rels", wn.VERB)

# printCombs("ao", attrsObjDict, attrsDict.counter)
# printCombs("oa", objAttrsDict, objsDict.counter)
# printCombs("o2", obj2Dict, objsDict.counter)
# printCombs("rc", relCombDict, relsDict.counter)
# printCombs("rs", relSubjDict, relsDict.counter)
# printCombs("ro", relObjDict, relsDict.counter)

# key2img, obj2key = createKey2img()

# with open("key2img.json", "w") as f:
#     json.dump(key2img, f)
    
# with open("obj2key.json", "w") as f:
#     json.dump(obj2key, f)

# w = open("outNew.txt","w")
# for x in y:
#     w.write("_"+x+"\n")
#     for z in y[x]:
#         w.write(x+"+"+z+"\t"+str(list(set(y[x][z])))+"\n")

# with open(outJson("attrsObjs"), "r") as f:
#    attrsDict = json.load(f)

# aCounter = {}
# with open(outTxt("attrsObjs"), "w") as f:
#     for a in attrsDict:
#       counter = 0
#       for obj, num in sorted(attrsDict[a].items(), reverse = True, key = lambda i: i[1]):
#           counter += num
#       aCounter[a] = counter

#     for a in attrsDict:
#       f.write(a + "," + str(aCounter[a]))
#       f.write("\n")
#       for obj, num in sorted(attrsDict[a].items(), reverse = True, key = lambda i: i[1]):
#           f.write("  "+obj + "," + str(num))
#           f.write("\n")
#       f.write("\n")

# with open(outTxt("short"), "w") as f:

#   for obj, num in sorted(attrsDict["short"].items(), reverse = True, key = lambda i: i[1]):
#       f.write("  "+obj + "," + str(num))
#       longNum = attrsDict["long"].get(obj, 0)
#       tallNum = attrsDict["tall"].get(obj, 0)
#       f.write("  "+("length" if longNum > tallNum else "height")+" {} > {}".format(max(longNum, tallNum), min(longNum, tallNum)))
#       f.write("\n")
#   f.write("\n")


# with open(outJson("rels"), "rb") as f:
#     relsCount = json.load(f)

# with open(outDict("desc"), "wb") as outFile:
#     pickle.dump(descDict, outFile)    

# sample = {}
# count = 0
# for k in data:
#     sample[k] = data[k]
#     count += 1
#     if count > 200:
#         break

# with open(dataFilename) as f:
#     data = json.load(f)

# with open(outIdFilename, "r") as inFile:
#    sample = json.load(inFile)

# for imageId in sample:
#     image = GetImageData(id=imageId)
#     print ("The url of the image is: %s" % image.url)

#     fig = plt.gcf()
#     fig.set_size_inches(18.5, 10.5)
#     response = requests.get(image.url)
#     objs = list(sample[imageId]["objects"].values())
#     img = PIL_Image.open(io.BytesIO(response.content))
#     i = 0
#     j = 0
#     # if len(objs) == 0: 
#     plt.imshow(img)
#     ax = plt.gca()
#     print(len(objs))
#     for obj in objs:
#         # if i >= len(objs):
#         #     break
#         # obj = objs[i]
#         if "relations" not in obj or len(obj["relations"]) == 0:
#             continue        
#         print(obj)
#         ax.add_patch(Rectangle((obj["x"], obj["y"]),
#                                obj["w"],
#                                obj["h"],
#                                fill=False,
#                                edgecolor='red',
#                                linewidth=3))
#         text = obj["name"] + ("({})".format(",".join([x["rel"]+"-"+x["subjN"]+"-"+x["objN"] for x in obj["relations"]])) if "relations" in obj and len(obj["relations"]) > 0 else "")
#         ax.text(obj["x"], obj["y"], text, style='italic', bbox={'facecolor':'white', 'alpha':0.7, 'pad':10})
#         # i += 1
#     fig = plt.gcf()
#     plt.tick_params(labelbottom='off', labelleft='off')
#     #plt.show()
#     plt.savefig(imageId+"_rel.jpg", dpi = 720) # +"_"+str(j)
#     plt.close(fig)
#     j += 1


