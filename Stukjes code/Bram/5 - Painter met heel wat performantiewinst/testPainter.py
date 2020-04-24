from PyQt5.QtWidgets import QWidget, QPushButton, QGridLayout

# noodzakelijk om de imports vanuit command line goed te laten verlopen
import os
import sys
dir_path = os.path.dirname(os.path.realpath(__file__))
dir_GUI = dir_path[0:dir_path.rfind("#Stukjes")]
print(dir_GUI)
sys.path.append(dir_GUI)
from Project.GUI.Painter.Painter import Painter


class Main(QWidget):
    def __init__(self):
        super(Main, self).__init__()

        layout = QGridLayout()

        self.painter = Painter()

        self.btnClear = QPushButton("Clear", self)
        self.btnClear.clicked.connect(lambda: self.painter.clearPunten(True))

        layout.addWidget(self.painter, 0, 0, 1, 1)
        layout.setColumnMinimumWidth(0, 400)
        layout.setRowMinimumHeight(0, 250)
        layout.addWidget(self.btnClear, 1, 0)

        self.setLayout(layout)


if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    main = Main()
    main.show()
    sys.exit(app.exec_())
