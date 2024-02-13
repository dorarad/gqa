from collections import defaultdict
import argparse
import json
import math

# Evaluation code for GQA. 
# Computes a suite of metrics such as accuracy, consistency, plausibility and scores per question type and length.
# See https://gqadataset.org/ for all information about the data, including examples, evaluation, visualizations and slides.
#
#
# Metrics:
# - Accuracy: Standard accuracy, computed over the balanced version of the dataset, which is more robust against 
#             cheating by making educated guesses. For each question-answer pair (q,a), we give 1 point if the 
#             predicted answer p matches a and 0 otherwise, and average over all questions in the dataset. 
#
# - Consistency: A metric for the level of model's consistency across different questions. Has two versions,
#                for entailed questions and equivalent questions. For each question-answer pair (q,a), we define 
#                a set Eq={q1, q2, ..., qn} of entailed questions, the answers to which can be unambiguously 
#                inferred given (q,a). 
#                Denote Q the set of all questions the model answered correctly. For each question q in Q, we 
#                measure the model's accuracy over the entailed questions Eq to get the score sq and finally 
#                average these results across all questions in Q. 
#                We similarly do the same for the equivalent questions set - question which are semantically 
#                identical to q.
#
# - Validity: Measures whether the model gives a "valid" answer - one that can theoretically be an answer
#             to the question (e.g. a color to a color question, yes/no to a binary question etc.).
#             We provide a set of valid answers to each questions over the final answer vocabulary, in
#             the choices file, and use it to compute average validity across the dataset.
# 
# - Plausibility: Measures whether the model answers are plausible, e.g. one that make sense in the real world,
#                 e.g. not answering "purple" to a question about apple color (unless it's really purple).
#                 We provide a set of all plausible answers to each questions, computed by looking at all
#                 attributes and relations hold for various objects throughout the whole dataset scene graphs, 
#                 and use it to compute average model plausibility across the data.
#
# - Grounding: Only for attention models. Measures whether the model looks at the relevant regions in the 
#              image when answering a question. Each question in the dataset is annotated with the visual regions
#              they refer to, which are then used to compute the level to which the model has a correct visual attention,
#              which will allow to identify whether it really answers based on the image of by language-based guesses.
#              Current evaluation supports only spatial features but can easily be expanded to support object-based 
#              features (planning to add support shortly).
#
# - Distribution: Measures the overall match between the true answer distribution for different questions,
#                 vs the overall distribution predicted by the model through its answers for all the data.
#                 We use chi-square statistic to measure the degree of similarity between the distributions,
#                 giving indication to the level of overall world-knowledge of the model
# 
# - Accuracy per type: accuracy per question structural types (logic, compare, choose), and semantic type
#                      (questions about attributes, relations, categories, objects or the whole scene).
# - Accuracy for length: accuracy as a function of the question length, in terms of (1) words number, and semantic
#                        complexity - number of reasoning steps.
#
# We may support additional metrics (e.g. coverage) in the future.
#
#
# Files format:
# - predictions file format: JSON array: [{"questionId": str, "prediction": str}]
# - attentions file format: JSON array: [{"questionId": str, "attention": [float] }]. 
#   array length: featureSize * featureSize (currently supporting only for spatial features)
# - questions and choices files are provided as part of the dataset.
#   see https://gqadataset.org/download.html for information about their format.
#
#
# If you have any questions or comments, please feel free to send an email,
# at dorarad@cs.stanford.edu. We hope you'll enjoy using the GQA dataset! :)
#
#

##### arguments
##########################################################################################

parser = argparse.ArgumentParser()
parser.add_argument('--tier',           default = "val",                   type = str,  help = "Tier, e.g. train, val") # ???
parser.add_argument('--scenes',         default="{tier}_sceneGraphs.json",   type = str,  help = "Scene graphs file name format.")
parser.add_argument('--questions',      default="{tier}_questions.json",   type = str,  help = "Questions file name format.")
parser.add_argument('--choices',        default="{tier}_choices.json",     type = str,  help = "Choices file name format.")
parser.add_argument('--predictions',    default="{tier}_predictions.json", type = str,  help = "Answers file name format.")
parser.add_argument('--attentions',     default="",     type = str, help = "Attentions file name format.") # ???
parser.add_argument('--featureSize',    default = 7,    type = int, help = "Optional, only to get attention score. Images features map size, featureSize * featureSize") # ???
args = parser.parse_args()


##### load files
##########################################################################################

# Load scene graphs
with open(args.scenes.format(tier = args.tier)) as scenesFile:
    scenes = json.load(scenesFile)

# Load questions
with open(args.questions.format(tier = args.tier)) as questionsFile:
    questions = json.load(questionsFile)

# Load choices
with open(args.choices.format(tier = args.tier)) as choicesFile:
    choices = json.load(choicesFile)

# Load predictions and turn them into a dictionary
with open(args.predictions) as predictionsFile:
    predictions = json.load(predictionsFile)
    predictions = {p["questionId"]: p["prediction"] for p in predictions}

# Make sure all question have predictions
for qid in questions:
    if qid not in predictions:
        raise Exception("no prediction for question {}. Please add prediction for all questions.".format(qid))

# Load attentions and turn them into a dictionary
attentions = None
if args.attentions != ""
    with open(args.attentions) as attentionsFile:
        attentions = {a["questionId"]: np.array(a).reshape((args.featureSize, args.featureSize)) for a in attentions}


##### scores data structures initialization
##########################################################################################

# Compute average of a list
def avg(l):
    if len(l) == 0:
        return 0
    return float(sum(l)) / len(l)

# Initialize data structure to track all metrics: e.g. accuracy, validity and plausibility, as well as 
# accuracy per question type, length and number of reasoning steps.
scores = {
    "accuracy": [], # list of accuracies per question (1 if correct else 0). Will be averages ultimately.
    "validity": [], # list of validity per question (1 if valid else 0).
    "plausibility": [], # list of plausibility per question (1 if plausible else 0) 
    "entailedConsistency": [], # list of consistency scores for entailed questions.
    "equivalentConsistency": [], # list of consistency scores for equivalent questions.
    "accuracyPerStructuralType": defaultdict(list), # list of question accuracies for each structural type (e.g. compare, logic questions)
    "accuracyPerSemanticType": defaultdict(list), # list of question accuracies for each semantic type (e.g. questions about an object, an attribute, a relation)
    "accuracyPerLength": defaultdict(list), # list of question accuracies per question's word number
    "accuracyPerSteps": defaultdict(list), # list of question accuracies per question's reasoning length (steps number)
    "grounding": [] # list of grounding scores for each question.
}

# Initialize golden and predicted histograms per question global and local types. Used to compute distribution metric
dist = {
    "global": {
        "gold": defaultdict(lambda: defaultdict(int)),
        "predicted": defaultdict(lambda: defaultdict(int))
    },
    "local": {
        "gold": defaultdict(lambda: defaultdict(lambda: defaultdict(int))),
        "predicted": defaultdict(lambda: defaultdict(lambda: defaultdict(int)))
    }
}


##### Question lengths - words numbers and reasoning steps number
##########################################################################################

# Compute question length (words number)
def getWordsNum(question):
    return len(question["question"].split())

# Compute number of reasoning steps (excluding the final "querying" step which doesn't increase effective reasoning length)
def getStepsNum(question):
    return len([c for c in question["code"] if not (any([o in c for o in ["exist", "query: name", "choose name"]]))])


##### Functions for question annotations
##########################################################################################

# Utility function for converting question annotations string keys to slices
def toSlice(strSlice):
    sliceLims = (int(n) for n in strSlice.split(':'))
    return apply(slice, sliceLims)

# Utility function for converting question annotations string keys to indexes list:
# "1" => [0]
# "1:3" => [1, 2]
# "4:9:2" => [4, 6, 8]
def intsFromSlice(strSlice):
    slice_obj = get_slice_obj(slicearg)
    return(range(slice_obj.start or 0, slice_obj.stop or -1, slice_obj.step or 1))


##### Functions for consistency scores (for entailed  and equivalent questions ("inferred"))
##########################################################################################

def updateConsistency(question, consistencyType):
    inferredQuestions = [e for e in question[consistencyType] if e != qid]
    
    if correct and len(inferredQuestions) > 0:        
        
        cosnsitencyScores = []
        for qid in inferredQuestions:
            gold = questions[qid]["answer"]
            predicted = predictions[qid]
            score = float(1 if (predicted == gold) else 0)
            cosnsitencyScores.append(score)
        
        scores["{}Consistency".format(consistencyType)].append(avg(cosnsitencyScores))


##### Functions for grounding score (optional, only for attention models)
##########################################################################################

# Utility functions for working with bounding boxes. 
# c = (x0, y0, x1, y1), r = (r0, r1)

def yrange(c):
    return (c[1], c[3])

def xrange(c):
    return (c[0], c[2])

def length(r):
    if r is None:
        return 0    
    return float(r[1] - r[0])

def intersection(r1, r2):
    ir = (max(r1[0], r2[0]), min(r1[1], r2[1]))
    if ir[1] > ir[0]:
        return ir
    return None

def intersectionSize(c1, c2):
    return length(intersection(xrange(c1), xrange(c2))) * length(intersection(yrange(c1), yrange(c2)))

def getCell(i, j):
    edge = float(1) / args.featureSize
    return (edge * i, edge * j, edge * (i + 1), edge * (j + 1))

def getRegion(sceneGraph, objectId):
    obj = sceneGraph["objects"][objectId]
    x0 = float(obj["x0"]) / instance["width"]
    y0 = float(obj["y0"]) / instance["height"]
    x1 = float(obj["x0"] + obj["w"]) / instance["width"]
    y1 = float(obj["y0"] + obj["h"]) / instance["height"]
    return (x0, y0, x1, y1)

# Computes grounding score. Computer amount of attention (probability) given to each of the regions
# the question and answers refer to.
def computeGroundingScore(question, sceneGraph, attentionMap):
    regions = []
    # add question regions
    regions += [getRegion(sceneGraph, pointer) for pointer in question["annotations"]["question"]]
    # add answer regions
    regions += [getRegion(sceneGraph, pointer) for pointer in question["annotations"]["fullAnswer"]]
    # add all the image if the question refers to the whole scene
    if any(("scene" in c) for c in question["semantic"]):
        regions.append((0, 0, 1, 1))
    
    scores = []
    for region in regions:
        for i in range(args.featureSize):
            for j in range(args.featureSize):
                if len(area) > 0:
                    scores.append(attentionMap[i][j] * intersectionSize(getCell(i, j), region))
    
    return avg(scores)

##### Functions for distribution score
##########################################################################################

# Compute chi square statistic of gold distribution vs predicted distribution,
# averaged over all question groups
def chiSquare(goldDist, predictedDist):
    sumScore, sumOverall = 0, 0
    
    for group in goldDist:
        score, overall = 0, 0
        
        for ans in goldDist[group]:
            e = goldDist[group][ans]
            o = predictedDist[group].get(ans, 0)
            score += ((float(o - e) ** 2) / e)
            overall += goldDist[group][ans]
        
        sumScore += score * overall
        sumOverall += overall

    avgScore = sumScore / sumOverall
    
    return avgScore


##### Main score computation 
##########################################################################################

# Loop over the questions and compute mterics
for qid in questions:
    question = questions[qid]
    
    gold = question["answer"]
    predicted = predictions[qid]

    correct = (predicted == gold)
    score = float(1 if correct else 0)

    wordsNum = getWordsNum(question)
    stepsNum = getStepsNum(question)
    
    # Compute scores over the balanced dataset (more robust against cheating by making educated guesses)
    if question["isBalanced"]:
        # Update accuracy
        scores["overall"].append(score)
        scores["accuracyPerLength"][str(wordsNum)].append(score)
        scores["accuracyPerSteps"][str(stepsNum)].append(score)
        scores["accuracyPerStructuralType"][question["type"]["structural"]].append(score)
        scores["accuracyPerSemanticType"][question["type"]["semantic"]].append(score)
        
        # Update validity score
        valid = predicted in choices[qid]["valid"]:
        scores["validity"].appennd(valid)

        # Update plausibility score
        plausible = predicted in choices[qid]["plausible"]:
        scores["plausibility"].append(plausible)

    # Compute consistency (for entailed and equivalent questions)
    updateConsistency(question, "entailedConsistency")
    updateConsistency(question, "equivalentConsistency")

    # Optionally compute grounding (attention) score
    if attentions is not None:
        groundingScore = computeGroundingScore(question, scenes[question["imageId"]], attentions[qid])
        if groundingScore is not None:
            scores["grounding"].append(groundingScore)
    
    # Update histograms for gold and predicted answers
    globalGroup = question["groups"]["global"]
    localGroup = question["groups"]["local"]

    dist["global"]["gold"][globalGroup][gold] += 1
    dist["local"]["gold"][localGroup][gold] += 1 

    dist["global"]["predicted"][globalGroup][predicted] += 1
    dist["local"]["predicted"][localGroup][predicted] += 1

# Compute distribution score
scores["globalDistMatch"] = chiSquare(goldGlobalHisto, predictedGlobalHisto)
scores["localDistMatch"] = chiSquare(goldLobalHisto, predictedLocalHisto)
scores["distMatch"] = scores["globalDistMatch"] * 2/3 + scores["localDistMatch"] * 1/3

# Average scores over all questions (in the balanced dataset)
metrics = ["accuracy", "validity", "plausibility", "entailedConsistency", "equivalentConsistency", "grounding"]
detailedMetrics = ["accuracyPerStructuralType", "accuracyPerSemanticType", "accuracyPerLength", "accuracyPerSteps"]

for k in metrics:
    scores[k] = avg(scores[k])

for k in detailedMetrics:
    for t in scores[k]:
        scores[k][t] = avg(scores[k][t])

# Print scores
for k in metrics:
    print("{}: {}".format(k, scores[k]))

for k in detailedMetrics:
    print("{}:".format(k))
    for t in detailedMetrics[k]:
        print(" {}: {}".format(t, detailedMetrics[k][t]))    
