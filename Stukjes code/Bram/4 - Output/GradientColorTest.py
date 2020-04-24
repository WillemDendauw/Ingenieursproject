"""
In deze klasse ben ik op zoek gegaan naar het zoeken hoe je op een mooie manier een lineair effect in transitie
tussen twee willekeurige kleuren kan vinden.

Je wil van color1 naar color2 gaan.

Met betrekking tot dit project gaat het over de kleur die een OutputNode krijgt wanneer die een bepaalde waarde
tussen 0 en 1 krijgt (de output van het neurale netwerk).
color2 komt overeen met een output waarde 1 voor het betreffende cijfer (met 100% zekerheid is het niet
dat bepaalde cijfer dat de gebruiker tekende in Painter)
color1 komt overeen met een output waarde 0 voor het betreffende cijfer (met 100% zekerheid is het niet
dat bepaalde cijfer dat de gebruiker tekende in Painter)
"""

from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QVBoxLayout, QWidget, QLabel


class GradientColorTest(QWidget):
    def __init__(self, color1=QColor(255, 0, 0), color2=QColor(0, 0, 255)):
        super().__init__()

        n = 100

        ricoRed = (color2.red() - color1.red()) / n
        ricoGreen = (color2.green() - color1.green()) / n
        ricoBlue = (color2.blue() - color1.blue()) / n

        currentRed = color1.red()
        currentGreen = color1.green()
        currentBlue = color1.blue()

        layout = QVBoxLayout()
        layout.setSpacing(0)
        for i in range(n):
            label = QLabel()
            label.setAutoFillBackground(True)
            label.setStyleSheet("background-color : rgb({r}, {g}, {b})".format(r = currentRed,
                                                                                g = currentGreen,
                                                                                b = currentBlue))
            label.setFixedHeight(self.height()/n)
            label.setFixedWidth(700)
            layout.addWidget(label)
            currentRed += ricoRed
            currentGreen += ricoGreen
            currentBlue += ricoBlue
        self.setLayout(layout)


if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    import sys
    app = QApplication(sys.argv)
    # TODO: met de kleuren moeten we misschien nog wat spelen
    color1 = QColor(255, 50, 50)
    color2 = QColor(50, 255, 50)
    main = GradientColorTest(color1=color1, color2=color2)
    main.show()
    sys.exit(app.exec_())
