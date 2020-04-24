# ======================================================================================================================
# ============================================   API VAN DE KLASSE TrainenGUI   ========================================
# ======================================================================================================================
# - sliderrate : QSlider                slider om de learning rate aan te passen
# - sliderbatch : QSlider               slider om de batch grootte aan te passen
# - sliderepochs : QSlider              slider om het aantal epochs aan te passen
# - logOutput : QTextEdit               een editeerbaar tekstveld voor het wegschrijven van de output van het netwerk
# - thread : TrainingThread             Een QThread die de training afhandeld.
# ----------------------------------------------------------------------------------------------------------------------
# - initGUI() : void                    Initialiseerd de GUI met links een QWidget aangemaakt met intiSliderContainer,
#                                       deze QWidget bevat de sliders en uitleg over de variabelen. Centraal een QWidget
#                                       gemaakt met initNeuralNet. Deze QWidget bevat een netwerk uit de klasse
#                                       NNVisualisatie. Rechts staat een QWidget gemaakt met initOutput, deze QWidget
#                                       bevat de output als het netwerk getraind wordt.
# - initSliderContainer() : void        In deze methode wordt een QWidget aangemaakt met een QVBoxLayout. In deze widget
#                                       zullen er 3 sliders komen die de variabelen(learning rate, batch grootte en
#                                       aantal epochs) kunnen beïnvloeden. Ook komt hier de 'Train' knop die het netwerk
#                                       kan laten trainen en uitleg over de variabelen.
# - initNeuralNet() : void              In deze widget zal een visuele voorstelling van een neuraal netwerk te vinden
#                                       zijn. Dit is een object van de klasse NNVisualisatie.
# - initOutput() : void                 In deze widget zal de output van het getrainde netwerk komen. Initieel staat
#                                       hier wat meer info over de GUI en extra informatie over het trainen van het
#                                       netwerk.
# - makeSlider() : void                 Hulpmethode die sliders aanmaakt en juist instelt.
# - sliderChange() : void               Methode die de veranderingen van de sliders doorvoert.
# - buttonClicked() : void              Deze methode maakt een QThread aan die de taak opzich neemt om het netwerk te
#                                       trainen. hiervoor wordt ook de data van de sliders doorgeven met een methode van
#                                       de klasse TrainingThread.
# - finished(): void                    Deze methode behandeld het ontvangen signaal van de TrainingThead. Dit signaal
#                                       bevat de tekst met info over het getrainde netwerk en zet deze in de output.
# + goBack() : void                     De methode om terug te kunnen keren naar de MainGUI


import sys

from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (QApplication, QVBoxLayout, QHBoxLayout, QWidget, QSlider, QGroupBox, QLabel,
                             QTextEdit, QPushButton, QGridLayout, QStackedLayout)
from PyQt5.QtCore import *
from GUI.Trainen.NNVisualisatie import NNVisualisatie
from Algoritme.Network import Network
import pickle
from GUI.Trainen.TrainingThread import TrainingThread


class TrainingGUI(QWidget):
    """
    In deze klasse wordt de TrainenGUI aangemaakt, dit is een GUI om uit te leggen hoe een neuraal netwerk
    getrained wordt en hoe de variabelen (learning rate, batch grootte en aantal epochs) invloed hebben op
    de training en de accuratie van het netwerk.
    Deze klasse maakt gebruik van een object van de klasse NNVisualisatie, die een grafische voorstelling
    geeft van een neuraal netwerk met 1 input node en 10 output nodes.
    """

    def __init__(self, parent):
        super(TrainingGUI, self).__init__(parent)
        self.setWindowTitle("Leer over het trainen")
        self.__logOutput = QTextEdit()
        self.__initGUI()
        self.showFullScreen()

    def __initGUI(self):
        layout = QHBoxLayout(self)

        layout.addWidget(self.__initSliderContainer())
        layout.addWidget(self.__initNeuralNet())
        layout.addWidget(self.__initOutput())

        self.setLayout(layout)

    """
    In deze methode wordt een QWidget aangemaakt met een QVBoxLayout. In deze widget zullen er 3 sliders
    komen die de variabelen (learning rate, batch grootte en aantal epochs) kunnen beïnvloeden. Ook komt
    hier de 'Train' knop die het netwerk kan laten trainen en uitleg over de variabelen.
    """

    def __initSliderContainer(self):
        sliderContainer = QWidget()
        layout = QVBoxLayout()

        sliders = QWidget()
        sliderLayout = QGridLayout()

        # Labels van sliders
        labelrate = QLabel("Learning rate η:")
        labelbatch = QLabel("Mini-batch size:")
        labelepochs = QLabel("Aantal epochs:")

        # Veranderlijke label bij sliders
        self.labelSrate = QLabel("3")
        self.labelSbatch = QLabel("10")
        self.labelSepochs = QLabel("30")

        # Labels die min en max van sliders aanduiden
        labelSliderMin0 = QLabel("0.1")
        labelSliderMax0 = QLabel("10")

        labelSliderMin1 = QLabel("5")
        labelSliderMax1 = QLabel("50")

        labelSliderMin2 = QLabel("1")
        labelSliderMax2 = QLabel("50")

        # Initialisatie van sliders
        self.__sliderrate = self.__makeSlider(
            min=1, max=100, interval=10, step=1, value=30)
        self.__sliderbatch = self.__makeSlider(
            min=5, max=50, interval=5, step=5, value=10)
        self.__sliderepochs = self.__makeSlider(
            min=1, max=50, interval=5, step=1, value=30)

        self.__sliderrate.valueChanged.connect(lambda: self.__sliderChange(0))
        self.__sliderbatch.valueChanged.connect(lambda: self.__sliderChange(1))
        self.__sliderepochs.valueChanged.connect(
            lambda: self.__sliderChange(2))

        # Button om neuraal netwerk te trainen
        self.__buttonRun = QPushButton("Train")
        self.__buttonRun.setFixedWidth(100)
        self.__buttonRun.clicked.connect(lambda: self.__buttonClicked())


        # Layout
        sliderLayout.addWidget(labelrate, 0, 0)
        sliderLayout.addWidget(self.labelSrate, 0, 2, Qt.AlignRight)
        sliderLayout.addWidget(self.__sliderrate, 1, 0, 1, 3)
        sliderLayout.addWidget(labelSliderMin0, 2, 0)
        sliderLayout.addWidget(labelSliderMax0, 2, 2, Qt.AlignRight)

        sliderLayout.addWidget(labelbatch, 3, 0)
        sliderLayout.addWidget(self.labelSbatch, 3, 2, Qt.AlignRight)
        sliderLayout.addWidget(self.__sliderbatch, 4, 0, 1, 3)
        sliderLayout.addWidget(labelSliderMin1, 5, 0)
        sliderLayout.addWidget(labelSliderMax1, 5, 2, Qt.AlignRight)

        sliderLayout.addWidget(labelepochs, 6, 0)
        sliderLayout.addWidget(self.labelSepochs, 6, 2, Qt.AlignRight)
        sliderLayout.addWidget(self.__sliderepochs, 7, 0, 1, 3)
        sliderLayout.addWidget(labelSliderMin2, 8, 0)
        sliderLayout.addWidget(labelSliderMax2, 8, 2, Qt.AlignRight)

        sliderLayout.addWidget(self.__buttonRun, 10, 2)

        sliderLayout.setRowMinimumHeight(9, 50)

        sliders.setFixedHeight(400)
        sliders.setLayout(sliderLayout)

        # Opmaak uitleg
        explanation = QTextEdit(self)
        explanation.setReadOnly(True)

        font = QFont()
        font.setFamily("Calibri")
        font.setPointSize(10)
        explanation.setFont(font)

        # Uitleg over de variabelen (learning rate, batch grootte en aantal epochs)
        explanation.setText("<p><b>\"Learing rate η\"</b>"
                            "<p>De learing rate is een parameter die het tempo bepaalt waarmee het netwerk zal "
                            "worden getraind. Om de bestaansreden van deze parameter goed te begrijpen moet je "
                            "weten dat een <i>gradiënt van een functie</i>, de richting uitdrukt hoe de "
                            "onafhankelijke variabelen moeten wijzigen opdat de functie het meeste zal stijgen.<br>"
                            "In mensentaal: als je een berg als 3 dimensionale functie zou omschrijven, dan zal "
                            "de gradiënt van de berg zeggen in welke richting je moet stappen om het meest te "
                            "stijgen. Als je precies de andere kant op zou gaan dan ga je de richting op die het "
                            "stijlste daalt.</p>"

                            "<p>In het trainen van een neuraal netwerk gebeurt dat laatste, je wil dat het neuraal "
                            "netwerk het stijlst daalt. Niet op een fysieke berg maar je wil dat de <i>cost function"
                            "</i>  het meeste daalt. Een <i>cost function</i> is een functie die beschrijft hoe goed "
                            "het netwerk presteert (een hoge waarde is een slechte prestatie en een lage waarde is "
                            "een goede prestatie). Door de gradiënt van de kostfunctie te berekenen kunnen we bepalen "
                            "hoe de onafhankelijke veranderlijken (weights en biases) moeten veranderen zodat de "
                            "kostfunctie het meeste daalt. Die negatieve gradiënt wordt vermenigvuldigd met de <i>"
                            "learning rate</i> die weergeeft in welke mate de weights en biases zullen aangepast "
                            "worden. De learning rate mag niet te groot zijn (als je een bal in een put duwt mag "
                            "ze er niet weer uit rollen) maar ze mag niet te klein zijn (je wil wel in het minimum "
                            "geraken). Een learning-rate van 3 levert globaal gezien in het gebruikte netwerk de "
                            "beste resultaten.</p></p>"

                            "<p><b>\"Mini-batch size\"</b>"
                            "<p>De kostenfunctie is de som van de kwadratische afwijking van de verwachte output "
                            "t.o.v. de gegenereerde output, voor alle data in de gebruikte dataset. "
                            "Bij grote aantallen in "
                            "trainingdata (grootte-ordes van 50,000) zou het zeer lang duren vooralleer het neuraal "
                            "netwerk getraind is als we de som over alle data nemen, want pas na het bepalen van de "
                            "kostenfunctie kunnen de onafhankelijke veranderlijken geüpdatet worden. Daarom "
                            "wordt de dataset verdeeld in mini-batches en wordt de som niet bepaald over de volledige "
                            "dataset maar over een mini-batch, na een mini-batch worden de weights en biases al eens "
                            "aangepast. Bij een mini-batch size van 10 en een trainingset van grootte 50,000 worden "
                            "de weights en biases al na 10 termen aangepast i.p.v. pas na 50,000.</p></p>"

                            "<p><b>\"Aantal epochs\"</b></p>"
                            "<p>Het aantal epochs vertelt hoeveel keer de volledige dataset wordt behandeld bij het "
                            "trainen. Bij elke epoch wordt de trainingdata opgesplitst in mini-batches. "
                            "Na de laatste epoch zit het trainen er op.</p>"
                            )

        # We steken explanation in een GroupBox voor de layout:
        explanationBox = QGroupBox("Uitleg over bovenstaande parameters")
        explanationLayout = QStackedLayout()
        explanationLayout.addWidget(explanation)
        explanationBox.setLayout(explanationLayout)

        # Terugknop
        buttonBack = QPushButton("Back")
        buttonBack.setFixedWidth(100)
        buttonBack.clicked.connect(lambda: self.__goBack())

        layout.addWidget(sliders)
        layout.addWidget(explanationBox)
        layout.addWidget(buttonBack)

        sliderContainer.setFixedWidth(500)
        sliderContainer.setLayout(layout)

        return sliderContainer

    """
    In deze widget zal een visuele voorstelling van een neuraal netwerk te vinden zijn.
    Dit is een object van de klasse NNVisualisatie.
    """

    def __initNeuralNet(self):
        box = QWidget()
        layout = QHBoxLayout()
        # Maakt een object aan van de klasse NNVisualisatie
        layout.addWidget(NNVisualisatie())
        box.setLayout(layout)

        return box

    """
    In deze widget zal de output van het getrainde netwerk komen.
    Initieel staat hier wat meer info over de GUI en extra informatie over het trainen van het netwerk.
    """

    def __initOutput(self):
        groupBox = QGroupBox("Output:")

        hor = QHBoxLayout()

        self.__logOutput.setReadOnly(True)

        font = QFont()
        font.setFamily("Calibri")
        font.setPointSize(10)
        self.__logOutput.setFont(font)

        self.__logOutput.setText("<b><i><u>DOEL VAN DEZE PAGINA</b></i></u>"
                                 "<p>Het doel van deze educatieve GUI is om de gebruiker enkele "
                                 "parameters te laten aanpassen om te zien welk effect dit "
                                 "heeft op de resultaten na het trainen van een netwerk. "
                                 "De gebruiker stelt de sliders links boven in naar wens "
                                 "en drukt vervolgens op de Train-knop. Na enkele seconden verschijnt in dit "
                                 "tekstveld de tussenresultaten na elke epoch.</p>"
                                 ""
                                 "<p>De data die gebruikt wordt tijdens het trainen in deze pagina is afkomstig "
                                 "van de MNIST-dataset. Het netwerk wordt getraind met 1000 cijfers, en wordt elke "
                                 "epoch getest met validatiedata bestaande uit 100 cijfers. "
                                 "We gebruikten deze data niet voor het trainen "
                                 "van het netwerk dat gebruikt wordt in het hoofdprogramma omdat dit "
                                 "heel povere resultaten haalde, we hebben dus onze eigen trainingdata gemaakt. "
                                 "De data van de MNIST-dataset is afkomstig van cijfers geschreven op papier. "
                                 "In deze applicatie wordt niet met een pen geschreven maar met de muis, "
                                 "dit genereert andere data-waarden. Vandaar de povere resultaten.</p>"
                                 ""
                                 "<p>Het netwerk dat wordt gebruikt is een netwerk met 784 "
                                 "ingangen, een hidden layer van 30 neuronen en een "
                                 "output-layer van 10 neuronen (getallen tussen 0 en 9). "
                                 "In deze sectie zal na het drukken op de Train-knop, na enkele seconden, voor "
                                 "elke epoch tevoorschijn komen hoeveel cijfers van de validatiedata het netwerk "
                                 "met het tot dan toe getrainde netwerk juist heeft berekent.</p>"

                                 "De waarden van de parameters gebruikt in het effectief "
                                 "trainen van het netwerk van het hoofdprogramma zijn: "
                                 "<ul>"
                                 "  <li>learning rate: 3</li>"
                                 "  <li>mini-batch size: 10</li>"
                                 "  <li>epochs: 30</li>"
                                 "</ul><br>"

                                 "<b><i><u>BELANGRIJKE OPMERKINGEN VOOR HET TRAINEN</b></i></u>"
                                 "<p>Als u op de Train-knop drukt zal het netwerk beginnen trainen. "
                                 "Het probleem is dat dit tekstveld zich niet onmiddellijk "
                                 "wil aanpassen wanneer er tekst naartoe wordt geschreven door "
                                 "de applicatie zelf. Een gekende oplossing is hier voorlopig "
                                 "nog niet voor gevonden. We vragen dus uw geduld wanneer u "
                                 "het netwerk hier traint. Het zou kunnen zijn dat de muis na "
                                 "enkele seconden verandert in een draaiende blauwe cirkel. "
                                 "Dit komt omdat het netwerk lang bezig is met berekeningen uit te "
                                 "voeren en dus niet reageert tot wanneer de berekeningen afgerond zijn.</p>"

                                 "<p>Onze excuses voor beide ongemakken!</p>"

                                 "<p>Indien u koos voor 50 epochs, duurt het ongeveer "
                                 "15 seconden vooralleer alles berekend is en de tekst hier zal "
                                 "verschijnen.</p>"
                                 ""
                                 "<p>Merk bovendien op dat de resultaten rond 85% liggen met de beste configuratie van "
                                 "de parameters, in realiteit worden veel grotere datasets gebruikt om een neuraal "
                                 "netwerk te trainen. Om handgeschreven cijfers te herkennen worden resultaten van 97% "
                                 "behaald met de trainingset van de MNIST-dataset, bestaande uit 60,000 cijfers. "
                                 "Veel meer dan de 1000 die hier gebruikt worden.")

        hor.addWidget(self.__logOutput)
        groupBox.setFixedWidth(400)
        groupBox.setLayout(hor)

        return groupBox

    """
    Hulpmethode die sliders aanmaakt en juist instelt.
    """

    def __makeSlider(self, min, max, interval, step, value):
        slider = QSlider(Qt.Horizontal)
        slider.setValue(value)
        slider.setFocusPolicy(Qt.StrongFocus)
        slider.setTickPosition(QSlider.TicksBelow)
        slider.setTickInterval(interval)
        slider.setSingleStep(step)
        slider.setRange(min, max)
        return slider

    """
    Methode die de veranderingen van de sliders doorvoert.
    """

    def __sliderChange(self, sliderNum):
        if sliderNum == 0:
            # /10 om aan double values te komen
            string = str(self.__sliderrate.value()/10)
            self.labelSrate.setText(string)
        elif sliderNum == 1:
            string = str(self.__sliderbatch.value())
            self.labelSbatch.setText(string)
        elif sliderNum == 2:
            string = str(self.__sliderepochs.value())
            self.labelSepochs.setText(string)

    """
    Methode die een TrainingThread aanmaakt die en de parameters van de sliders eraan doorgeeft zodat die QThread kan
    beginnne trainen.
    """

    def __buttonClicked(self):
        self.__thread = TrainingThread()
        self.__logOutput.setText("Het netwerk wordt getraind...\n\n")
        self.__buttonRun.setEnabled(False)
        self.__thread.initData(self.__sliderepochs.value(), self.__sliderbatch.value(), self.__sliderrate.value())
        self.__thread.signal.connect(self.__finished)
        self.__thread.start()

    """
    De methode die het signaal van de TrainingThread ontvangt en dan ervoor zorgt dat de tekst in de output komt
    """

    def __finished(self, result):
        print("Finished methode is opgeroepen met het resultaat")
        self.__buttonRun.setEnabled(True)
        print("knop is terug ingeschakeld nu gaan we resultaat printen")
        print(result)
        print("resultaat is geprint")
        self.__logOutput.setText(result)
        print("finished methode volbracht")

    """
    Knop om terug te keren naar de MainGUI
    """

    def __goBack(self):
        self.close()
