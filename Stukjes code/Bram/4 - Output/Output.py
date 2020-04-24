from PyQt5.QtWidgets import QWidget, QVBoxLayout
from OutputNode import OutputNode


class Output(QWidget):
    def __init__(self, amount=10, labeled=True):
        super().__init__()
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
