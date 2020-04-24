import sys
import math
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class NeuronGui(QWidget):
    def __init__(self, input, parent=None):
        #de input wordt hardgecodeert meegegeven.
        super(NeuronGui, self).__init__(parent)            
        self.input=input
        self.bias=0
        self.weight0=0
        self.weight1=0
        self.weight2=0
        self.activation=0

        self.__initGui()
        self.paintEvent(self.repaint())
        self.setWindowTitle("NeuronGui")
        self.showMaximized()

    def __initGui(self):
        layout = QHBoxLayout(self)
        self.activationL=QLabel()
        layout.addWidget(self.createSliderGroup())
        layout.addWidget(self.createLabelGroup())

        self.setLayout(layout)
    
    def createLabelGroup(self):
        groupBox = QWidget()
        vert=QVBoxLayout()
        self.activationL = QLabel(str(self.activation))
        self.activationL.setAlignment(Qt.AlignCenter)
        self.activationL.setFont(QFont("Calibir", 20, QFont.Bold))

        explanation = QLabel()
        explanation.setText("Lorem ipsum dolor sit amet, consectetur adipiscing elit.\n"
                            " Sed semper neque vel erat efficitur, non interdum ipsum blandit.\n"
                            " Nulla id suscipit elit, nec congue risus.\n"
                            " Etiam posuere libero quis accumsan egestas.\n"
                            " Curabitur vitae risus at nisl mollis tincidunt.\n"
                            " Sed rhoncus et ligula et tincidunt.\n\n"
                            "hier komt uitleg over de variabelen")
        explanation.setAlignment(Qt.AlignCenter)

        vert.addStretch(3)
        vert.addWidget(self.activationL)
        vert.addStretch(1)
        vert.addWidget(explanation)
        vert.addStretch(1)
        groupBox.setLayout(vert)

        return groupBox
    
    def paintEvent(self,event):
        """
        Deze methode tekent de Neuron, deze wordt elke keer getekend als er een slider van waarde veranderd.
        Dit zorgt voor een goede visualisatie wat er precies veranderd bij de neuron.
        """
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        d=250
        x=self.width()*3/4-(d/2)
        y=self.height()/4-(d/2)
        painter.setPen(QPen(Qt.black,3))
        painter.drawLine(x-d, y, x-d/3+d, y+d/2)
        painter.drawLine(x-d-d/15, y+d/2, x+2*d , y+d/2)
        painter.drawLine(x-d, y+d, x-d/3+d, y+d/2)
        painter.setBrush(QBrush(QColor(169,169,169)))
        painter.drawEllipse( x, y, d, d)

        font = QFont("Calibir", 20, QFont.Bold)
        painter.setFont(font)
        painter.drawText(x-d-d/6, y,"{}".format(3))
        painter.drawText(x-d-d/3, y+d/2,"{}".format(-2))
        painter.drawText(x-d-d/6, y+d+d/15,"{}".format(1))

        painter.setPen(QPen(QColor(105,105,105)))
        painter.drawText(x-d/2, y+d/15,"{}".format('w0: '+str(self.weight0)))
        painter.drawText(x-d/2-d/6, y+d/2-d/15,"{}".format('w1: '+ str(self.weight1)))
        painter.drawText(x-d/2-d/8, y+d ,"{}".format('w2: '+ str(self.weight2)))
        painter.drawText(x+d/3, y-d/15,"{}".format('b: '+ str(self.bias)))
        painter.drawText(x+2*d-d/8, y+d/2-d/15 ,"{}".format('a'))

    def createSliderGroup(self):    
        #Het linker deel van de Gui wordt hier gemaakt, alle initialisaties van de vier sliders.
    
        sliderWidget = QWidget()
        layoutS = QGridLayout() 

        label1=QLabel("weight1 (w1):")
        label2=QLabel("weight2 (w2):")
        label0=QLabel("weight0 (w0):")
        labelb=QLabel("Bias (b):")

        self.labelS0 = QLabel("0")
        self.labelS1 = QLabel("0")
        self.labelS2 = QLabel("0")
        self.labelb = QLabel("0")

        labelSliderMin0 = QLabel("-2.50")
        labelSliderMax0 = QLabel("2.50")

        labelSliderMin1 = QLabel("-2.50")
        labelSliderMax1 = QLabel("2.50")

        labelSliderMin2 = QLabel("-2.50")
        labelSliderMax2 = QLabel("2.50")
    
        labelSliderMinb = QLabel("-2.50")
        labelSliderMaxb = QLabel("2.50")

        self.slider0=self.makeSlider()
        self.slider1=self.makeSlider()
        self.slider2=self.makeSlider()
        self.sliderb=self.makeSlider()

        self.slider0.valueChanged.connect(lambda: self.sliderChange(0))         #door een int mee te geven juiste weight/bias veranderen
        self.slider1.valueChanged.connect(lambda: self.sliderChange(1))
        self.slider2.valueChanged.connect(lambda: self.sliderChange(2))
        self.sliderb.valueChanged.connect(lambda: self.sliderChange(3))
                                  
        layoutS.addWidget(label0,0,0)                          
        layoutS.addWidget(self.labelS0,0,2,Qt.AlignRight)
        layoutS.addWidget(self.slider0,1,0,1,3)
        layoutS.addWidget(labelSliderMin0, 2, 0)
        layoutS.addWidget(labelSliderMax0, 2, 2, Qt.AlignRight)

        layoutS.addWidget(label1,3,0)
        layoutS.addWidget(self.labelS1,3,2,Qt.AlignRight)
        layoutS.addWidget(self.slider1,4,0,1,3)
        layoutS.addWidget(labelSliderMin1, 5, 0)
        layoutS.addWidget(labelSliderMax1, 5, 2, Qt.AlignRight)

        layoutS.addWidget(label2,6,0)
        layoutS.addWidget(self.labelS2,6,2,Qt.AlignRight)
        layoutS.addWidget(self.slider2,7,0,1,3)
        layoutS.addWidget(labelSliderMin2, 8, 0)
        layoutS.addWidget(labelSliderMax2, 8, 2, Qt.AlignRight)

        layoutS.addWidget(labelb,9,0)
        layoutS.addWidget(self.labelb,9,2,Qt.AlignRight)
        layoutS.addWidget(self.sliderb,10,0,1,3)
        layoutS.addWidget(labelSliderMinb, 11, 0)
        layoutS.addWidget(labelSliderMaxb, 11, 2, Qt.AlignRight)

        layoutS.setRowMinimumHeight(9,20)

        buttonBack = QPushButton("Back")
        buttonBack.setFixedWidth(100)
        buttonActivation = QPushButton("Activation")
        buttonActivation.setFixedWidth(100)
        layoutS.setRowStretch(17,20)
        layoutS.addWidget(buttonBack,17,0)
        layoutS.addWidget(buttonActivation,17,2,Qt.AlignRight)

        buttonActivation.clicked.connect(lambda: self.changeActivation(self.activationL))


        sliderWidget.setFixedHeight(1000)
        sliderWidget.setFixedWidth(900)
        sliderWidget.setLayout(layoutS)

        return sliderWidget

    def makeSlider(self):
        slider1 = QSlider(Qt.Horizontal)
        slider1.setFocusPolicy(Qt.StrongFocus)
        slider1.setTickPosition(QSlider.TicksBelow)
        slider1.setTickInterval(10)
        slider1.setSingleStep(0.1)
        slider1.setMinimum(-250)
        slider1.setMaximum(250)

        return slider1

    def sliderChange(self,i):
        if i==0:
            string = str(self.slider0.value()/100)
            self.labelS0.setText(string)
            self.weight0=self.slider0.value()/100
        elif i==1:
            string = str(self.slider1.value()/100)
            self.labelS1.setText(string)
            self.weight1=self.slider1.value()/100
        elif i==2:
            string = str(self.slider2.value()/100)
            self.labelS2.setText(string)
            self.weight2=self.slider2.value()/100
        elif i==3:
            string = str(self.sliderb.value()/100)
            self.labelb.setText(string)
            self.bias=self.sliderb.value()/100.0                
        self.paintEvent(self.repaint())
   
    #activatie van neuron berekenen
    def changeActivation(self,label):
        x=0
        self.weights = (self.weight0,self.weight1,self.weight2)
        for i in range(3):
            x+=self.weights[i]*self.input[i]
        x+=self.bias
        z=1/(1+math.exp(-1*x))
        self.activation = z
        label.setText(str(z))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    input=(3,-2,1)                      #input wordt hier hardgecodeert meegegeven
    clock = NeuronGui(input)
    sys.exit(app.exec_())