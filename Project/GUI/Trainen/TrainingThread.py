# ======================================================================================================================
# ============================================   API VAN DE KLASSE TrainingThread   ====================================
# ======================================================================================================================
# + signal : pyqtSignal                         Het uiteindelijke signaal dat zal worden uitgestuurd met de info over
#                                               het netwerk.
# - network : Network                           neuraal netwerk van klasse Network
# - training_data :                             de data waarmee het netwerk wordt getraind
#       list(tuple(numpy.ndarray,numpy.ndarray))
# - validation_data :                           de data waarmee gecontroleerd wordt hoe accuraat het netwerk is
#       list(tuple(numpy.ndarray, int))
# ----------------------------------------------------------------------------------------------------------------------
# + run : void                                  Doet al het werk om het netwerk te trainen en zet alle informatie die
#                                               hij erover krijgt in een String die wordt uitgezonden met het signaal
# + initData : void                              zorgt ervoor dat de data van de 3 sliders in de TrainingGUI in deze
#                                               klasse terechtkomen, dit gebeurt via een aparte klasse omdat je via
#                                               de run methode geen parameters kan meegeven.

from PyQt5.QtCore import *
from PyQt5.QtWidgets import QTextEdit
from Algoritme.Network import Network
import pickle


class TrainingThread(QThread):
    signal = pyqtSignal(str)

    def __init__(self, parent=None):
        QThread.__init__(self, parent)
        self.__network = None
        self.__trainingData = None
        self.__validationData = None

        self.epochs = 0
        self.batch = 0
        self.rate = 0

        self.amountOfTrainingData = 1000
        self.amountOfValidationData = 100

        self.__output = QTextEdit()

    def run(self):
        print("Run methode van Thread gestart")
        self.__network = Network([784, 30, 10])
        print("Netwerk is succesvol aangemaakt")
        # Als vanuit Project de Main.py wordt geopend, dan is dirPath gezet op het pad naar Project
        self.__trainingData = pickle.load(
            open("Data/TrainingGUIData/mnist_training_data.bin", "rb"))
        self.__validationData = pickle.load(
            open("Data/TrainingGUIData/mnist_validation_data.bin", "rb"))

        print("Trainingdata en validatiedata succesvol geladen")

        self.__trainingData = list(self.__trainingData)[
                              0:self.amountOfTrainingData]
        self.__validationData = list(self.__validationData)[
                                0:self.amountOfValidationData]

        print("Data succesvol in lists geplaatst")

        print("epochs = {}".format(self.epochs))
        print("mini-batch size = {}".format(self.batch))
        print("rate = {}".format(self.rate / 10))
        print("Gradient descent nu uitvoeren...")
        self.__network.gradientDescent(self.__trainingData, self.epochs, self.batch,
                                       self.rate / 10, self.__validationData, 0.25,
                                       txtField=self.__output)
        print("Gradient descent succesvol uitgevoerd")
        text = self.__output.toPlainText()
        text += "\n\nKLAAR!"
        print("Signaal met uitkomsten doorsturen naar de GUI")
        self.signal.emit(text)

    def initData(self, epochs, batch, rate):
        print("DATA succesvol doorgegeven aan de Thread")
        self.epochs = epochs
        self.batch = batch
        self.rate = rate
