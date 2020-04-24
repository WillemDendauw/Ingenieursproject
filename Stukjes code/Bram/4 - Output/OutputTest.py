from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton  # QPushButton is voor de test
from OutputNode import OutputNode


class OutputTest(QWidget):
    def __init__(self, amount=10, labeled=True):
        super().__init__()
        self.__amount = amount
        self.__labeled = labeled

        self.__outputVector = list()
        self.i = 0  # Dit is voor de test
        # Dit is voor de test
        self.list1 = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
        self.list2 = [0.6, 0.2, 0.0, 0.1, 0.5, 0.3, 0.8, 0.4, 0.7, 0.9]
        self.list3 = [0.3, 0.9, 0.4, 0.6, 0.7, 0.321, 0.5, 0.1, 0.2, 0.8]
        self.listOflists = [self.list1, self.list2, self.list3]
        self.__initUI()

        self.setFixedSize(200, 800)

    def __initUI(self):
        layout = QVBoxLayout()
        for i in range(self.__amount):
            output = OutputNode(number=i)
            self.__outputVector.append(output)
            layout.addWidget(output)

        # Dit is voor de test
        tempButton = QPushButton("Druk op mij en de nodes veranderen")
        tempButton.clicked.connect(self.changeOutputNodes)

        layout.addWidget(tempButton)

        self.setLayout(layout)

    def setOutputNodes(self, output=list()):
        if len(output) != self.__amount:
            raise Exception("len(ouptput) = {} moet gelijk zijn aan het aantal OutputNodes"
                            "deze Output QWidget moet krijgen ({})".format(len(output), self.__amount))
        for i in range(len(output)):
            self.__outputVector[i].changeValue(output[i])

    # Dit is voor de test
    def changeOutputNodes(self):
        self.setOutputNodes(self.listOflists[self.i])
        self.i = (self.i + 1) % 3


if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    main = OutputTest()
    main.show()
    sys.exit(app.exec_())
