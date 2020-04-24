from PyQt5.QtWidgets import QWidget, QVBoxLayout
from GUI.Output.OutputNode import OutputNode


class Output(QWidget):
    """
    De klasse Output is een container voor OutputNode's in een QVBoxLayout.
    De klasse wordt gebruikt om de output van een neuraal netwerk visueel
    te kunnen voorstellen a.d.h.v. rode en groene nodes. Indien het neuraal
    netwerk denkt dat de gebruiker een 7 tekende, dan zal de kleur van de
    node horende bij het cijfer 7 groen zijn terwijl alle andere nodes rood
    zijn.
    """
    def __init__(self, parent=None, amount=10, labeled=True):
        super().__init__()
        self.setParent(parent)

        self.__amount = amount
        self.__labeled = labeled

        self.__outputVector = list()

        self.__initUI()

    def __initUI(self):
        layout = QVBoxLayout()
        for i in range(self.__amount):
            output = OutputNode(number=i)
            self.__outputVector.append(output)
            layout.addWidget(output)

        self.setLayout(layout)

    def setOutputNodes(self, output=list()):
        if len(output) != self.__amount:
            raise Exception("len(ouptput) = {} moet gelijk zijn aan het aantal OutputNodes"
                            "deze Output QWidget moet krijgen ({})".format(len(output), self.__amount))
        for i in range(len(output)):
            self.__outputVector[i].changeValue(output[i])


if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    main = Output()
    main.show()
    sys.exit(app.exec_())
