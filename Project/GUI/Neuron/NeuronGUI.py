# =================================================================================================================================
# ============================================   API VAN DE KLASSE NeuronGui    ===================================================
# =================================================================================================================================
# - input : tuple(int)                              hardgecodeerde input van de neuron
# - weight0: double                                 weight0 wordt aangepast met sliderW0
# - weight1: double                                 weight1 wordt aangepast met sliderW1
# - weight2: double                                 weight2 wordt aangepast met sliderW2
# - bias : double                                   bias wordt aangepast met sliderB
# - activation : double                             Dit is de activatie van de neuron, wordt berekent met sliderChange(int) methode
# - neuronVisualization: NeuronVisualization        De neuron wordt hier geïllustreerd
# - lblActivation : QLabel                          dit label toont de z- en a- waarde van de neuron op elk moment
# - sliderW0 : QSlider                              deze slider geeft de waarde van weight0 aan
# - sliderW1 : QSlider                              deze slider geeft de waarde van weight1 aan
# - sliderW2 : QSlider                              deze slider geeft de waarde van weight2 aan
# - sliderB : QSlider                               deze slider geeft de waarde van de bias aan
# - lblSliderW0 : QLabel                            deze slider toont de waarde van weight0 bij de slider
# - lblSliderW1 : QLabel                            deze slider toont de waarde van weight1 bij de slider
# - lblSliderW2 : QLabel                            deze slider toont de waarde van weight2 bij de slider
# - lbsSliderB : QLabel                             deze slider toont de waarde van de bias bij de slider
# ----------------------------------------------------------------------------------------------------------------------------------
# - initGUI(): void                                 Zal alles initialiseren, met behulp van de createSliderGroup() methode
#                                                   en de createVisualizationAndExplanation() methode.
# - createVisualizationAndExplanation()             Hier zal de NeuronVisualization gecreëert worden, ernaast wordt er
#                :  QWidget                         ook nog gezorgt voor de uitleg over de neuron zelf. Hierin wordt de 
#                                                   werking uitgelegt, hoe de activatie van een neuron wordt berekent.
# - createSliderGroup() : QWidget                   Het linker deel van de GUI wordt hier in detail gemaakt, alle sliders en labels
#                                                   worden hier gemaakt en op de juiste plaats gezet. De sliders worden gemaakt in
#                                                   de methode makeSlider. Daarna gelinkt aan sliderChange(int) om daar het 
#                                                   bijhorende label te veranderen en ook de neuronVisualization.
# - makeSlider() : QSlider                          Een slider wordt hier gemaakt met zijn bijhorende max en min waarden.
# - sliderChange(int) : void                        Methode om de labels en de neuronVisualization te veranderen en erna de activation
#                                                   berkenen.
# - goBack() : void                                 De methode om terug te kunnen keren naar de MainGUI

import sys
import math
from PyQt5.QtCore import *
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QVBoxLayout, QTextEdit, QGridLayout, QPushButton, QSlider

from GUI.Neuron.NeuronVisualization import NeuronVisualization


class NeuronGui(QWidget):
    def __init__(self, input, parent=None):
        # de input wordt meegegeven.
        super(NeuronGui, self).__init__(parent)

        self.__input = input
        self.__bias = 0
        self.__weight0 = 0
        self.__weight1 = 0
        self.__weight2 = 0
        self.__activation = 0
        self.__neuronVisualization = None

        self.__initGui()

        self.setWindowTitle("Leer over een neuron")
        self.showFullScreen()

    def __initGui(self):
        """
        Hier wordt de opstelling gecreëerd aan de hand van QHBoxLayouts en twee andere methodes om deze layout op te vullen.
        """
        layout = QHBoxLayout(self)
        self.__lblActivation = QLabel()
        layout.addWidget(self.__createSliderGroup())
        layout.addWidget(self.__createVisualizationAndExplanation())

        self.setLayout(layout)
    
    def __createVisualizationAndExplanation(self):

        """
        In deze methode wordt een NeuronVisualization gemaakt, zodat de neuron mooi wordt getoond. Dit is door een QVBoxLayout, een QLabel en een QTextEdit.
        """
        visualizationAndExplanation = QWidget(self)
        vert = QVBoxLayout()

        self.__neuronVisualization = NeuronVisualization(parent=self, w0=0, w1=0, w2=0, b=0)

        self.__lblActivation = QLabel("z = {:.4f} → a = {:.4f}".format(0.0, 0.5))
        self.__lblActivation.setAlignment(Qt.AlignCenter)
        self.__lblActivation.setFont(QFont("Calibir", 20, QFont.Bold))

        explanation = QTextEdit()

        font = QFont()
        font.setFamily("Calibri")
        font.setPointSize(10)
        explanation.setFont(font)

        explanation.setText("<p>"
                            "<p>Een neuron bestaat uit hoofdzakelijk vier elementen:"
                            "<ul>"
                            "   <li>input</li>"
                            "   <li>weights</li>"
                            "   <li>biases</li>"
                            "   <li>activation</li>"
                            "</ul>"
                            "</p>"

                            "<p>Bij elke input hoort een weight. Een input van een neuron kan de eigenlijke input zijn "
                            "van een neuraal netwerk (zie \"leren over de werking van een neuraal netwerk\") maar het "
                            "kan ook de activation zijn van een andere neuron waarmee het verbonden is.</p>"
                            
                            "<p>De activiteit van een neuron wordt bepaald door de som van alle input-waarden, "
                            "vermenigvuldigd met hun bijhorende weight te bepalen en daarbij de bias van de neuron op "
                            "te tellen. Het bekomen resultaat is de activatie van de neuron. In een formule gegoten "
                            "wordt dit:"
                            "<p style=\"margin-left: 4em\">"
                            "z = Σ(w*i) + b"
                            "</p>met w de weight horende bij input i en bias b van de neuron, de verklaring waarom "
                            "met een intermediaire parameter 'z' i.p.v. onmiddellijk met 'a' (van activation) te "
                            "werken wordt in de volgende paragraaf duidelijk.</p>"
                            ""

                            "<p>Omdat de activiteit (tot nog toe 'z') van een neuron tussen in het netwerk dat "
                            "gebruikt wordt in het hoofdmenu tussen 0 en 1 moet liggen, wordt de sigmoid functie "
                            "gebruikt op 'z' losgelaten en we bekomen 'a'. "
                            "Deze functie mapt een input-waarde (de x-as) op een reëel getal tussen 0 en 1 "
                            "(de y-as). In de limiet naar plus oneindig is de waarde van de sigmoid functie 1, in de "
                            "limiet naar min oneindig is de waarde van de sigmoid functie gelijk aan 0. Dit is precies "
                            "wat we nodig hebben. Er zijn nog andere functies die hiervoor kunnen gebruikt worden, de "
                            "verzamelnaam van functies die alle reële x-waarden mappen op een ondergrens en bovengrens "
                            "noemen we in de context van neurale netwerken <i>activation functions</i><br>"
                            "Het functievoorschrift van de sigmoid functie is:"
                            "<p style=\"margin-left: 4em\">"
                            "a = 1 / (1 + exp(-z))"
                            "</p>"
                            
                            "<p>In deze GUI tonen we welk effect de weights en bias heeft op de neuron. "
                            "Sommige weights zullen een grotere invloed hebben op de activiteit "
                            "dan anderen doordat het een grotere input heeft."
                            "</p></p>")
        explanation.setAlignment(Qt.AlignLeft)
        explanation.setReadOnly(True)

        vert.addWidget(self.__neuronVisualization)
        vert.addWidget(self.__lblActivation)
        vert.addWidget(explanation)
        visualizationAndExplanation.setLayout(vert)

        return visualizationAndExplanation

    def __createSliderGroup(self):
        """
        Het linker deel van de Gui wordt hier gemaakt, alle initialisaties van de vier sliders. Met elk drie labels, een voor het minimum, een voor het maximum
        en een voor de aangewezen waarde van de slider. De sliders worden hier ook gebonden met een methode voor het veranderen van de labels, als de slider van
        waarde veranderd. Er is ook een BackButton om terug te keren naar de MainGui.
        """
        sliderWidget = QWidget()
        layoutS = QGridLayout()

        label0 = QLabel("Weight horende bij input '3' (w0):")
        label1 = QLabel("Weight horende bij input '-2' (w1):")
        label2 = QLabel("Weight horende bij input '1' (w2):")
        labelb = QLabel("Bias van de neuron (b):")

        self.__lblSliderW0 = QLabel("0")
        self.__lblSliderW1 = QLabel("0")
        self.__lblSliderW2 = QLabel("0")
        self.__lblSliderB = QLabel("0")

        labelSliderMin0 = QLabel("-2.50")
        labelSliderMax0 = QLabel("2.50")

        labelSliderMin1 = QLabel("-2.50")
        labelSliderMax1 = QLabel("2.50")

        labelSliderMin2 = QLabel("-2.50")
        labelSliderMax2 = QLabel("2.50")
    
        labelSliderMinb = QLabel("-2.50")
        labelSliderMaxb = QLabel("2.50")

        self.__sliderW0 = self.__makeSlider()
        self.__sliderW1 = self.__makeSlider()
        self.__sliderW2 = self.__makeSlider()
        self.__sliderB = self.__makeSlider()

        # door een int mee te geven juiste weight/bias veranderen
        self.__sliderW0.valueChanged.connect(lambda: self.__sliderChange(0))
        self.__sliderW1.valueChanged.connect(lambda: self.__sliderChange(1))
        self.__sliderW2.valueChanged.connect(lambda: self.__sliderChange(2))
        self.__sliderB.valueChanged.connect(lambda: self.__sliderChange(3))
                                  
        layoutS.addWidget(label0, 0, 0)
        layoutS.addWidget(self.__lblSliderW0, 0, 2, Qt.AlignRight)
        layoutS.addWidget(self.__sliderW0, 1, 0, 1, 3)
        layoutS.addWidget(labelSliderMin0, 2, 0)
        layoutS.addWidget(labelSliderMax0, 2, 2, Qt.AlignRight)

        layoutS.addWidget(label1, 3, 0)
        layoutS.addWidget(self.__lblSliderW1, 3, 2, Qt.AlignRight)
        layoutS.addWidget(self.__sliderW1, 4, 0, 1, 3)
        layoutS.addWidget(labelSliderMin1, 5, 0)
        layoutS.addWidget(labelSliderMax1, 5, 2, Qt.AlignRight)

        layoutS.addWidget(label2, 6, 0)
        layoutS.addWidget(self.__lblSliderW2, 6, 2, Qt.AlignRight)
        layoutS.addWidget(self.__sliderW2, 7, 0, 1, 3)
        layoutS.addWidget(labelSliderMin2, 8, 0)
        layoutS.addWidget(labelSliderMax2, 8, 2, Qt.AlignRight)

        layoutS.addWidget(labelb, 9, 0)
        layoutS.addWidget(self.__lblSliderB, 9, 2, Qt.AlignRight)
        layoutS.addWidget(self.__sliderB, 10, 0, 1, 3)
        layoutS.addWidget(labelSliderMinb, 11, 0)
        layoutS.addWidget(labelSliderMaxb, 11, 2, Qt.AlignRight)

        layoutS.setRowMinimumHeight(9, 20)

        buttonBack = QPushButton("Back")
        buttonBack.setFixedWidth(100)
        layoutS.setRowStretch(17, 20)
        layoutS.addWidget(buttonBack, 17, 0)

        buttonBack.clicked.connect(lambda: self.__goBack())

        sliderWidget.setFixedHeight(1000)
        sliderWidget.setFixedWidth(900)
        sliderWidget.setLayout(layoutS)

        return sliderWidget

    def __makeSlider(self):
        """
        Slider wordt geïnitialiseerd met de standaard waarden.
        """
        slider = QSlider(Qt.Horizontal)
        slider.setFocusPolicy(Qt.StrongFocus)
        slider.setTickPosition(QSlider.TicksBelow)
        slider.setTickInterval(10)
        slider.setSingleStep(0.1)
        slider.setMinimum(-250)
        slider.setMaximum(250)

        return slider

    def __sliderChange(self, sliderNum):
        """
        Dit is de methode die gebruikt wordt wanneer een slider van waarde veranderd. Door een int mee te geven weet de methode welke slider het is
        en kan men het juiste label van de NeuronVisualization en het label van de value van de slider veranderen.
        Daarna wordt de activation van de Neuron berekent met behulp van de math import.
        """
        if sliderNum == 0:
            string = str(self.__sliderW0.value() / 100)
            self.__lblSliderW0.setText(string)
            self.__weight0 = self.__sliderW0.value() / 100
        elif sliderNum == 1:
            string = str(self.__sliderW1.value() / 100)
            self.__lblSliderW1.setText(string)
            self.__weight1 = self.__sliderW1.value() / 100
        elif sliderNum == 2:
            string = str(self.__sliderW2.value() / 100)
            self.__lblSliderW2.setText(string)
            self.__weight2 = self.__sliderW2.value() / 100
        elif sliderNum == 3:
            string = str(self.__sliderB.value() / 100)
            self.__lblSliderB.setText(string)
            self.__bias = self.__sliderB.value() / 100.0

        z = 0
        weights = (self.__weight0, self.__weight1, self.__weight2)
        for sliderNum in range(3):
            z += weights[sliderNum] * self.__input[sliderNum]
        z += self.__bias
        a = 1 / (1 + math.exp(-1 * z))
        self.__activation = a
        self.__lblActivation.setText("z = {:.4f} → a = {:.4f}".format(z, a))

        self.__neuronVisualization.changeParameters(w0=self.__sliderW0.value() / 100,
                                                    w1=self.__sliderW1.value() / 100,
                                                    w2=self.__sliderW2.value() / 100,
                                                    b=self.__sliderB.value() / 100)
        self.paintEvent(self.repaint())


    def __goBack(self):
        # terug naar MainGUI
        self.close()
