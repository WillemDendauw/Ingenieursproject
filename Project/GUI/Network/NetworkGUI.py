# ======================================================================================================================
# ============================================   API VAN DE KLASSE networkGUI   ========================================
# ======================================================================================================================
# - initGUI()                           Zet de 2 QWidgets met de visuele respresentaties onder elkaar. Het neuraal
#                                       network komt uit de klasse NNVisualisatie. Hoe een mens denkt komt uit de klasse
#                                       HumanCanvas. Daarnaast komt de text met uileg en eronder de back knop om terug
#                                       naar het hoofdscherm te gaan.
# + makeVisuals()                       Vanuit deze methode worden alle visuele
# - makeExplanationWindow()             Creëert een QLabel met daarin de volledige uitleg voor deze GUI en geeft deze
#                                       als returnwaarde terug.

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from GUI.Network.HumanCanvas import HumanCanvas
from GUI.Trainen.NNVisualisatie import NNVisualisatie


class NetworkGUI(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.setWindowTitle("Leer over de werking van een neuraal netwerk")
        self.__initGUI()
        self.showFullScreen()

    def __initGUI(self):
        """
        De opstelling wordt hier creeert aan de hand van QVBoxLayouts en QHBoxLayouts en opgevuld met de nodige QWidgets
        en QLabels en QPushButtons.
        """
        layout = QVBoxLayout(self)
        division = QHBoxLayout(self)
        # visuals = QVBoxLayout(self)

        # visuals.addWidget(HumanCanvas())
        # visuals.addWidget(NNVisualisatie(2, 9))

        backButton = QPushButton("Back")
        backButton.setFixedSize(100, 25)
        backButton.clicked.connect(lambda: self.close())

        division.addWidget(self.__makeVisuals())
        division.addWidget(self.__makeExplanationWindow())
        layout.addLayout(division)
        layout.addWidget(backButton)
        self.setLayout(layout)

    def __makeVisuals(self):
        layout = QVBoxLayout()
        layout.addWidget(HumanCanvas())
        layout.addWidget(NNVisualisatie(2, 9))

        widget = QWidget(self)
        widget.setLayout(layout)
        widget.setMinimumWidth(1300)

        return widget

    def __makeExplanationWindow(self):
        """
        Met deze methode wordt een String met uitleg teruggegeven.
        """
        text = QTextEdit()

        text.setReadOnly(True)
        # text.setLineWrapMode(QTextEdit.NoWrap)

        font = QFont()
        font.setFamily("Calibri")
        font.setPointSize(10)
        text.setFont(font)

        text.setText("<h1>Uitleg over de werking van een neuraal netwerk</h1>"
                     "<p>Op de eerste figuur staat een simplistische voorstelling van hoe het menselijk brein een "
                     "cijfer zou kunnen interpreteren en zo bepaalt welk cijfer we zien. "
                     "We analyseren gewoon de lijnen en in welke structuur ze staan om zo het cijfer te bepalen.</p>"

                     "<p>Een computer deze taak laten uitvoeren is een moeilijke opdracht. In deze applicatie wordt "
                     "gebruik gemaakt van een convolutioneel neuraal netwerk om precies die opdracht te voltooien.</p>"

                     "<p>Zo’n netwerk werkt op basis van neuronen, die we ook (welliswaar in een andere vorm) in onze "
                     "hersenen terugvinden. Op die manier trachten we de menselijke manier van denken na te bootsen "
                     "en dankzij de grotere rekenkracht van computers, wordt de mens soms overtroffen. "
                     "Meer info over hoe de neuronen, die hier worden gebruikt en samen een neuraal netwerk vormen, "
                     "vindt u op de infopagina over neuronen (\"Neuron...\" op het hoofdscherm).</p>"

                     "<p>Neuronen in een neuraal netwerk worden met alle buren verbonden, zoals te zien in de tekening, "
                     "links onderaan. De opstelling die voor deze applicatie wordt gebruikt is vrij eenvoudig en bestaat "
                     "uit 3 layers. De eerste layer bevat de input-neuronen, hier komt de informatie terecht van alle "
                     "pixels die samen een cijfer voorstellen. In de tekening links onderaan staat er slechts 1 rode "
                     "neuron om het simpel voor te stellen, vaak worden (heel) veel meer input-neuronen gebruikt. "
                     "De volgende layer wordt een ‘onzichtbare’ of ‘hidden’ layer genoemd. In de figuur links "
                     "onderaan staan er twee getekend, in het grijs, om aan te tonen dat je meerdere hidden layers kan "
                     "hebben in een neuraal netwerk. De laatste layer is de output-layer, de bedoeling ervan, in deze "
                     "applicatie, is dat het de juiste waarde aangeeft van het door de gebruiker getekende cijfer.</p>"

                     "<p>Alle informatie over deze neuronen en de verbindingen die ze hebben wordt door het netwerk "
                     "aangepast in het leerproces (zie \"Trainen van het netwerk...\" op het hoofdscherm). De weights en "
                     "biases van de hidden layers en output layer worden aangepast wanneer het netwerk traint. Het "
                     "netwerk gebruikt in de hoofdpagina bevat 784 input-neuronen (een foto van 28x28 bevat 784 "
                     "pixels, 30 neuronen in de hidden layer en 10 output-neuronen. De 10 output-neuronen stellen de "
                     "10 (cijfers 0-9) mogelijke uitkomsten voor die de gebruiker kan laten berekenen.</p>"
                     )
        return text
