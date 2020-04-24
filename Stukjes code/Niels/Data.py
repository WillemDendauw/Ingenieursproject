# ======================================================================================================================
# ===========================================   API VAN DE KLASSE Data   ===============================================
# ======================================================================================================================
# - training_data : list(tuple(list(float),int))    Houdt een lijst bij van tuples, waarbij elke tuple 1 afbeelding
#                                                   voorstelt. Deze tuple bevat als eerste waarde een lijst van floats,
#                                                   die de pixels van de afbeelding bijhouden. De tweede waarde van de
#                                                   tuple bevat een lijst waarbij alle waarden 0 zijn, behalve de waarde
#                                                   met de index die de afbeelding voorsteld.
# - validation_data : list(tuple(list(float),int))  Houdt hetzelfde bij als de training data, maar dan voor de
#                                                   validatie data.
# ----------------------------------------------------------------------------------------------------------------------
# + loader(data_file : str) : void                  Laadt de training en validatie data van het bestand in de variabelen
#                                                   training_data en validation_data.
# + vectorize(y : int) : list(float)                Maakt een vector waarbij vector[y] 1.0 is en de andere waarden 0.0
#                                                   zijn.

import gzip
import pickle
import numpy as np


class Data:

    def __init__(self):
        self.trainingData = ()
        self.validationData = ()
        self.loader("mnist.pkl.gz")

    def loader(self, mnistfile):

        file = gzip.open(mnistfile, 'rb')
        tData, vData, eData = pickle.load(file, encoding='latin1')
        file.close()

        trainingInput = [np.reshape(x, (784, 1)) for x in tData[0]]
        trainingResults = [self.vectorize(y) for y in tData[1]]
        trainingTuple = zip(trainingInput, trainingResults)

        validationInput = [np.reshape(x, (784, 1)) for x in vData[0]]
        validationResults = [self.vectorize(y) for y in vData[1]]
        validationTuple = zip(validationInput, validationResults)

        self.trainingData = trainingTuple
        self.validationData = validationTuple

        return

    def vectorize(self, y):
        v = np.zeros((10, 1))
        v[y] = 1.0
        return v
