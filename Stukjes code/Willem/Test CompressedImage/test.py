import pickle

from PyQt5.QtWidgets import QWidget, QGridLayout, QPushButton
from GUI.Painter.Painter import Painter


def check(p=Painter):
    p.clearPunten()


def output(p=Painter):
    # p geeft een veelvoud van 28x28 terug
    lijst = []
    image = p.getImage().getImage()
    deler = len(image) / 28

    sum = [0 for i in range(28)]
    for rij in range(0, len(image), 28):
        for col in range(0, len(image), 28):
            for i in range(deler):
                sum[col] += image[rij][col + i]
        for i in range(0, 28):
            lijst.append(sum[i] / (deler*deler))
        sum = [0 for i in range(28)]
    return lijst


class Main(QWidget):
    def __init__(self):
        super().__init__()

        layout = QGridLayout()

        painter = Painter(parent=self, pen_width=5)

        button = QPushButton("Check CompressedImage")
        button.clicked.connect(lambda: check(painter))
        button.setMaximumWidth(200)

        layout.addWidget(painter, 0, 0)
        layout.setRowMinimumHeight(0, 420)
        layout.setColumnMinimumWidth(0, 640)
        layout.addWidget(button, 1, 0)

        self.setLayout(layout)
        self.show()


if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    main = Main()
    main.show()
    sys.exit(app.exec_())
