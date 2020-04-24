# ======================================================================================================================
# ============================================   API VAN DE KLASSE HumanCanvas   =======================================
# ======================================================================================================================
# + paintEvent                              Tekent alle figuren, met onder andere 4 kadertjes, het cijfer 7 als
#                                           voorbeeld en het cijfer 7 opgesplitst in zijn sub delen en lijnen die alles
#                                           aan elkaar verbinden.

import sys

from PyQt5.QtGui import QPainter, QFont
from PyQt5.QtWidgets import QWidget


class HumanCanvas(QWidget):
    def __init__(self,parent=None):
        super().__init__(parent=parent)

    def paintEvent(self, event):
        """
        Hier tekenen we een simpele vorm van een netwerk die de tekening van een cijfer opsplitst in
        verschillende stukken om dan het cijfer te bepalen.
        """
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        #enkele punten berekenen
        width = self.width()
        height = self.height()

        xvalues = [width * 0, width * (1/12), width * (2/12), width * (3/12), width * (4/12), width * (5/12)
                   , width * (6/12), width * (7/12), width * (8/12), width * (9/12), width * (10/12)
                   , width * (11/12), width * (12/12)]
        yvalues = [height * (0), height * (1/10), height * (2/10), height * (3/10), height * (4/10)
                   , height * (5/10), height * (6/10), height * (7/10), height * (8/10), height * (9/10)
                   , height * (10/10)]
        widthRect = xvalues[3] - xvalues[1]
        heightRect = yvalues[3] - yvalues[1]

        #tekenen van de rechthoeken
        painter.drawRect(xvalues[1], yvalues[4], widthRect, heightRect)
        painter.drawRect(xvalues[5], yvalues[1], widthRect, heightRect)
        painter.drawRect(xvalues[5], yvalues[4], widthRect, heightRect)
        painter.drawRect(xvalues[5], yvalues[7], widthRect, heightRect)

        #tekstvak eindresultaat
        font = QFont("Calibir", 20, QFont.Bold)
        painter.setFont(font)
        painter.drawText(xvalues[9] + (width/20),yvalues[5] + (height/50),"ZEVEN")
        painter.drawLine(xvalues[9], yvalues[5] - (height/30), xvalues[11] + (width/18), yvalues[5] - (height/30))
        painter.drawLine(xvalues[9], yvalues[5] + (height/30), xvalues[11] + (width/18), yvalues[5] + (height/30))
        painter.drawLine(xvalues[9], yvalues[5] - (height/30), xvalues[9], yvalues[5] + (height / 30))
        painter.drawLine(xvalues[11] + (width/18), yvalues[5] - (height / 30), xvalues[11] + (width/18), yvalues[5] + (height / 30))

        #verbindingslijnen tekenen
        painter.drawLine(xvalues[3], yvalues[5], xvalues[5], yvalues[2])
        painter.drawLine(xvalues[3], yvalues[5], xvalues[5], yvalues[5])
        painter.drawLine(xvalues[3], yvalues[5], xvalues[5], yvalues[8])

        painter.drawLine(xvalues[7], yvalues[2], xvalues[9], yvalues[5])
        painter.drawLine(xvalues[7], yvalues[5], xvalues[9], yvalues[5])
        painter.drawLine(xvalues[7], yvalues[8], xvalues[9], yvalues[5])

        #cijfer 7 tekenen in het eerste kader
        painter.drawLine(xvalues[1] + (widthRect/4), yvalues[4] + (heightRect/4), xvalues[1] + (widthRect/4*3),
                         yvalues[4] + (heightRect/4))
        painter.drawLine(xvalues[1] + (widthRect/4*3), yvalues[4] + (heightRect/4), xvalues[1] + (widthRect/2),
                         yvalues[4] + (heightRect/8*7))
        painter.drawLine(xvalues[1] + (widthRect/2), yvalues[5], xvalues[1] + (widthRect/4*3), yvalues[5])

        #cijfer 7 opdelen in 3 stukken
        painter.drawLine(xvalues[5] + (widthRect/4), yvalues[1] + (heightRect/4), xvalues[5] + (widthRect/4*3),
                         yvalues[1] + (heightRect/4))
        painter.drawLine(xvalues[5] + (widthRect / 4 * 3), yvalues[4] + (heightRect / 4), xvalues[5] + (widthRect / 2),
                         yvalues[4] + (heightRect / 8 * 7))
        painter.drawLine(xvalues[5] + (widthRect / 2), yvalues[8], xvalues[5] + (widthRect / 4 * 3), yvalues[8])
