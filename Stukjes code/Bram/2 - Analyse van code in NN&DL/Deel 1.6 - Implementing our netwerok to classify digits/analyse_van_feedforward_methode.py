"""
In dit bestand onderzoek ik hoe de feedforward methode werkt.

Ik vergelijk de methode van het boek met mijn eigen redenering.
Ik gebruikte voor de input-array (hier a genoemd) en voor de 
bias array arrays met shape (n,). In het boek gebruikt men echter 
arrays met shape (n, 1). De reden hiervoor was me eerst niet duidelijk maar
na een uitgebreide analyse begrijp ik waarom hiervoor werd gekozen.
Het is zo dat door een arrays met shape (n, 1) te gebruiken, heel gemakkelijk
meerdere input-vectoren kunnen meegegeven worden, zo kan een 
batch in een keer meegegeven worden.

Zie #EURECA om dit te zien met dezelfde biases en weights en sizes

LET OP: de variabelen in het eerste deel worden niet consistent overgenomen
in het tweede deel (waarin meerdere inputs worden getest)

MERK OP: het gaat hem niet over de methode zelf, want die zijn identiek dezelfde
(want de formule blijft uiteraard dezelfde) maar het gaat hem dus over de 
shapes van input en bias
"""

import numpy as np

def sigmoid(z):
    return 1.0/(1.0+np.exp(-z))

"""
==================================Deel 1=============================================
-> analyse van feedforward
"""
print("DEEL 1: FEEDFORWARD ANALYSEREN")
sizes = [2, 3, 2]
biases = [np.array([[0.71287369],
       [0.82896046],
       [1.21977412]]), np.array([[-0.49327953],
       [-0.79531425]])]
#print("biases => {}".format(biases))
weights = [np.array([[-0.16987179,  1.08275004],
       [-0.94837886, -0.0089863 ],
       [-1.16241791, -1.24710357]]), np.array([[ 0.39993848,  1.2621809 ,  0.59251325],
       [ 0.49517811,  1.82632591, -1.49465569]])]
#print("weights => {}".format(weights))
a = sigmoid(np.array([[1.321], [4.654]]))
#print("a => {}".format(a))
def feedforward_book(_a, _biases, _weights):
    for b, w in zip(_biases, _weights):
        _a = sigmoid(np.dot(w, _a)+b)
    return _a

y = feedforward_book(a, biases, weights)
print("Met feedforward, 1 input:\t y = [{} {}]".format(y[0][0], y[1][0]))
biases = [[biases[0][0][0], biases[0][1][0], biases[0][2][0]], [biases[1][0][0], biases[1][1][0]]]
a = sigmoid(np.array([1.321, 4.654]))
#print("biases => {}".format(biases))
#print("weights => {}".format(weights))
#print("a => {}".format(a))

def output(_a, _biases, _weights):
    for b, w in zip(_biases, _weights):
        _a = sigmoid(np.dot(w, _a) + b)
    return _a

print("Met output, 1 input:\t\t y = {}".format(output(a, biases, weights)))

print()
print()

# ----------------------------------------------------------------------------------------------------------
# --------------------------------------------------EURECA--------------------------------------------------
# ----------------------------------------------------------------------------------------------------------
"""
==================================Deel 2=============================================
-> beide methodes (eigen en uit boek) testen op meerdere inputs
-> die van het boek is korter
-> die van mij lijkt natuurlijker

LET OP: bij een keuze voor het een of het ander moet je uiteraard consequent zijn!
"""
print("DEEL 2: MEERDERE INPUTS")
sizes = [2, 3, 2]
biases = [np.array([[0.71287369],
       [0.82896046],
       [1.21977412]]), np.array([[-0.49327953],
       [-0.79531425]])]
weights = [np.array([[-0.16987179,  1.08275004],
       [-0.94837886, -0.0089863 ],
       [-1.16241791, -1.24710357]]), np.array([[ 0.39993848,  1.2621809 ,  0.59251325],
       [ 0.49517811,  1.82632591, -1.49465569]])]
# nu kunnen we gemakkelijk alles berekenen voor 3 input-vectoren:
a = np.array([[1.321, 3.211, 2.113], [4.654, 6.544, 5.446]])
# met de drie input-vectoren, zijnde:
    # [1.321, 4.654]
    # [3.211, 6.544]
    # [2.113, 5.446]
matrix = feedforward_book(a, biases, weights)
print("Alle outputs zijn:\n-\t[{} {}]\n-\t[{} {}]\n-\t[{} {}]".format(matrix[0][0], matrix[1][0],matrix[0][1], matrix[1][1],matrix[0][2], matrix[1][2]))

# Terwijl je met mijn redenering een extra for-lus moet doorlopen en alles in een nieuwe
# matrix opslaan:
matrix = []
inputs = [[1.321, 4.654], [3.211, 6.544], [2.113, 5.446]]
biases = [[biases[0][0][0], biases[0][1][0], biases[0][2][0]], [biases[1][0][0], biases[1][1][0]]]
for a in inputs:
    matrix.append(output(a, biases, weights))
print("Alle outputs zijn:\n-\t[{} {}]\n-\t[{} {}]\n-\t[{} {}]".format(matrix[0][0], matrix[0][1],matrix[1][0], matrix[1][1],matrix[2][0], matrix[2][1]))
