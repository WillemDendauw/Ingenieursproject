import sys
from PyQt5.QtWidgets import QApplication
from GUI.MainGUI import MainGUI


def main():
    app = QApplication(sys.argv)
    mainGUI = MainGUI(parent=None)
    mainGUI.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
