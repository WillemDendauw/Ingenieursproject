"""
Dit is de module die zorgt dat het netwerk getraind is. Om het netwerk te kunnen trainen moet er data zijn om
het netwerk mee te kunnen trainen. Daarom moet in de directory /Project/CollectTrainingData/Data/TrainingData
minstens 1 source file zitten. In de source files moet een gepickelde lijst van tuples zitten, van de vorm (x, y).
    - x is een 784-dimensionale numpy.ndarray die het cijfer voorstelt
    - y is een 10-dimensionale numpy.ndarray die de verwachtte outputvector voorstelt
Als je tijdens het trainen, het netwerk elke epoch al eens wil testen dan moet in de directory
/Project/CollectTrainingData/Data/TestData minstens 1 source file zitten. Ook die source files moeten gepickelde lijsten
bevatten van tuples, ook van de vorm (x, y). x heeft dezelfde betekenis als in de trainingdata maar y moet gewoon een
integer zijn dat het cijfer is dat x zou moeten voorstellen. Op die manier kan vergeleken worden wat op dat moment
de output is van het netwerk, en wat het eigenlijk zou moeten zijn.

Om de data te generen moet je de module MakeTrainingData.py gebruiken. Voor meer uitleg over hoe je dit moet realiseren,
zie de uitleg bovenaan de module.
"""

# noodzakelijk om de imports vanuit command line goed te laten verlopen
import os
import sys
dir_path = os.path.dirname(os.path.realpath(__file__))
dir_GUI = dir_path[0:dir_path.rfind("CollectTrainingData")]
sys.path.append(dir_GUI)

from Algoritme.Network import Network
import pickle

trainingDataDir = "../Data/TrainingData/"
testDataDir = "../Data/TestData/"

# eerst verzamelen we alle data uit ./Data/TrainingData en steken alle inhoud in een lijst training_data
(dirpath, dirnames, filenames) = next(os.walk(trainingDataDir))
if len(filenames) < 1:
    print("=============================================================\n"
          "==========================  ERROR  ==========================\n"
          "=============================================================\n"
          "Er wordt minstens 1 source file verwacht!\n"
          "In die source file moeten de gepickelde cijfers staan\n"
          "die door dit programma worden omgezet in bruikbare data\n"
          "voor het neurale netwerk te kunnen trainen."
          "\nDe source files voor de testdata moeten in "
          "./Data/TrainingData/ zitten"
          "\n\nVoor meer info, zie de TODO\n"  # TODO: vul aan: "zie de TODO"
          "=============================================================")
    exit(0)

training_data = []
for filename in filenames:
    file = open(trainingDataDir + filename, "rb")
    data = pickle.load(file)
    for tuple in data:
        training_data.append(tuple)

# hetzelfde doen we voor alle data uit ./Data/TestData en steken de inhoud in een lijst test_data
(dirpath, dirnames, filenames) = next(os.walk(testDataDir))
if len(filenames) < 1:
    print("=============================================================\n"
          "==========================  ERROR  ==========================\n"
          "=============================================================\n"
          "Er wordt minstens 1 source file verwacht!\n"
          "In die source file moeten de gepickelde cijfers staan\n"
          "die door dit programma worden omgezet in bruikbare data\n"
          "voor het neurale netwerk te kunnen testen tijdens het trainen."
          "\nDe source files voor de testdata moeten in "
          "./Data/TestData/ zitten"
          "\n\nVoor meer info, zie de TODO\n"  # TODO: vul aan: "zie de TODO"
          "=============================================================")
    exit(0)

test_data = []
for filename in filenames:
    file = open(testDataDir + filename, "rb")
    data = pickle.load(file)
    for tuple in data:
        test_data.append(tuple)


def expectedOutput(y):
    i = 0
    while y[i] < 0.5:
        i += 1
    return i


print("Aanmaken van netwerk")
net = Network([784, 30, 10])
print("Aanmaken netwerk voltooid\n")

# alles wat in de blok hieronder staat is gewoon voor de code te testen
# ik schrijf bij de test alles eens naar een file om gemakkelijker te kunnen controleren
# test_file = open("C:\\Users\\bram_\\Desktop\\data.txt", "w")
# test_file.write("Lengte van training_data: {}\n".format(len(training_data)))
# test_file.write("Lengte van test_data: {}\n".format(len(test_data)))
# for (x, y) in training_data:
#    test_file.write("Verwacht cijfer = {}\n".format(expectedOutput(y)))
#    te_printen = ""
#    for i in range(28):
#        for j in range(28):
#            te_printen += "{:4}".format(int(255 * x[i*28 + j][0]))
#        te_printen += "\n"
#    test_file.write(te_printen)


print("Algoritme wordt getraind")
net.gradientDescent(training_data, 30, 10, 3.0, test_data, 0.25)
print("Algoritme werd succesvol getraind\n")

print("Parameters van netwerk opslaan")
net.saveNetwork()
print("Parameters opgeslagen\n")

