"""
Om een neuraal netwerk te kunnen trainen, hebben we data nodig. Om op een gebruiksvriendelijke manier data te maken
hebben we een hulpapplicatie voorzien. Met deze applicatie kan je twee soorten data maken: trainingdata en testdata.
Beide zijn lijsten van tuples met twee ingangen. Het effectieve cijfer, de eerste ingang van elke tuple, is in beide
soorten data dezelfde (een 784-dimensionele numpy.ndarray) maar de tweede entry is verschillen (respectievelijk een
10-dimensionale numpy.ndarray wat de verwachte outputvector voorstelt, en een integer wat gewoon het getal voorstelt
dat de data voorstelt). Trainingdata zal in /Project/CollectTrainingData/Data/TrainingData terechtkomen en testdata in
/Project/CollectTrainingData/Data/TestData. De gebruiker van deze applicatie moet dus zeker zijn dat deze twee
directories bestaan, anders kan de data niet worden opgeslagen.
TODO: geef nog een foutboodschap indien de directories niet gevonden worden, doe dit bij het opstarten van de applicatie
  en als ze niet blijken te bestaan, geef een popup-message

Default wordt verwacht dat er trainingdata wordt gemaakt, maar met de checkbox kan dit aangepast worden naar testdata.

Automatisch wordt tussentijds de data opgeslagen in de Project/CollectTrainingData/Data/Backup folder, dit is om ervoor
te zorgen dat als je heel veel data tegelijk genereert en er loopt iets fout, dat je niet alles gewoon kwijt bent.

Als je klaar bent, druk je op de save-knop. Die zal de data in de correcte map steken die je hebt opgegeven in het
tekstveld, relatief t.o.v. /Project/CollectTrainingData/Data.

Heb je per ongeluk een lelijk cijfer getekend kan je die verwijderen door op de clear-knop te drukken.

De next-knop zorgt dat je cijfer wordt toegevoegd aan de datastructuur die uiteindelijk zal worden opgeslagen en het
label zal worden aangepast.

Belangrijk: in het label staat "num" en "aantal". "num is het cijfer dat je nu moet tekenen, "aantal" is het totaal
aantal cijfers die zal worden opgeslagen als je op dit moment zal saven.
"""

import numpy
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QGridLayout, QLineEdit, QMessageBox, QCheckBox

import pickle
import platform

# noodzakelijk om de imports vanuit command line goed te laten verlopen
import os
import sys
dir_path = os.path.dirname(os.path.realpath(__file__))
dir_GUI = dir_path[0:dir_path.rfind("CollectTrainingData")]
sys.path.append(dir_GUI)
from GUI.Painter.Painter import Painter


class Main(QWidget):
    def __init__(self):
        super().__init__()

        self.y = 0
        self.aantal = 0
        self.aantalI = 0
        self.label = QLabel("Num = {}\tAantal = {}".format(self.y, self.aantal))

        self.training_data = []

        self.p = Painter(self)

        self.btnDone = QPushButton("Save")
        self.btnDone.clicked.connect(lambda: self.opslaan())

        self.btnNext = QPushButton("Next")
        self.btnNext.clicked.connect(lambda: self.next())
        self.btnNext.setShortcut("Space")

        self.btnClear = QPushButton("Clear")
        self.btnClear.clicked.connect(lambda: self.p.clearPunten())

        self.checkTestData = QCheckBox()
        self.checkTestData.setText("Enable test data")

        self.textField = QLineEdit("TrainingData/training_data00.bin")

        layout = QGridLayout()

        layout.addWidget(self.p, 0, 0, 1, 3)
        layout.addWidget(self.label, 1, 0)
        layout.addWidget(self.textField, 1, 1)
        layout.addWidget(self.checkTestData, 1, 2)

        layout.setColumnMinimumWidth(0, 200)
        layout.setColumnMinimumWidth(1, 200)
        layout.setColumnMinimumWidth(2, 200)
        layout.setRowMinimumHeight(0, 400)

        layout.addWidget(self.btnDone, 2, 0)
        layout.addWidget(self.btnNext, 2, 1)
        layout.addWidget(self.btnClear, 2, 2)

        self.setLayout(layout)

    def next(self):
        training_inputs = numpy.reshape(numpy.array(self.p.getInput()), (784, 1))
        # alle data komt als tuple (x, y)
        # bij zowel trainingdata als testdata moet x een 784 dimensionale numpy.ndarray zijn
        # bij trainingsdata moet y een 10-dimensionale numpy.ndarray zijn die de te verwachten output is
        # bij testdata moet y daarentegen gewoon de waarde zijn die het getal voorstelt
        if not self.checkTestData.isChecked():
            self.training_data.append((training_inputs, self.vectorized_result(self.y)))
        else:
            self.training_data.append((training_inputs, self.y))

        self.aantal += 1
        self.aantalI += 1
        if self.aantalI == 2:
            self.aantalI = 0
            self.y = (self.y + 1) % 10
            # alle 10 cijfers eens opnieuw opslaan voor de zekerheid
            self.opslaan(True)
        self.p.clearPunten()
        self.label.setText("Num = {}\tAantal = {}".format(self.y, self.aantal))

    def vectorized_result(self, i=0):
        """
        Geeft een numpy.ndarray van 10 dimensies weer met op de y-de index een 1, dit wordt voor het neuraal netwerk
        aanschouwd als de "te verwachten uitkomst" bij het trainen ervan

        :return: numpy.ndarray()
        """
        e = numpy.zeros((10, 1))
        e[i] = 1.0
        return e

    def opslaan(self, tussentijds=False):
        import platform
        import sys
        if not tussentijds:
            fileName = self.textField.displayText()

            msgBox = QMessageBox()
            msgBox.setText("De ingegeven data (aantal = {}) zal worden opgeslagen\n"
                           "in het bestand {}.\n\n"
                           "Dit programma zal worden afgesloten.".format(self.aantal, self.textField.displayText()))
            msgBox.setIcon(QMessageBox.Warning)

            msgBox.addButton(QMessageBox.Ok)
            msgBox.addButton(QMessageBox.Cancel)

            # als returnwaarde 1024 is, wil dat zeggen dat gebruiker op "Ok" drukte, anders op Cancel of close
            ret = msgBox.exec_()
            if ret == 1024:
                print("===========   START MET OPSLAAN VAN DATA   ===========")
                pickle.dump(self.training_data, open("../Data/" + self.textField.displayText(), "wb"))
                print("len(self.data) = {}".format(len(self.training_data)))
                print("===========   KLAAR MET OPSLAAN VAN DATA   ===========")
                sys.exit(0)
        else:
            print("===========   START MET OPSLAAN VAN DATA   ===========")
            pickle.dump(self.training_data, open("../Data/Backup/tussentijdse_backup_" + platform.node() + ".bin", "wb"))
            print("len(self.data) = {}".format(len(self.training_data)))
            print("===========   KLAAR MET OPSLAAN VAN DATA   ===========")


if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    main = Main()
    main.show()
    sys.exit(app.exec_())
