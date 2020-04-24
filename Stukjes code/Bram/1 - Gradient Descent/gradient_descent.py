import graphics as g
import tkinter as tk
import numpy as np

win = g.GraphWin(title="Testing Gradient Descent", width=600, height=450)
set_of_x = list()
set_of_y = list()
i = 0
A = None

def ray(a=0.0, b=0.0):
    """
    Return graphics.Polygon with given function: y = ax+b
    """
    first = g.Point(0.0, b)
    second = g.Point(win.getWidth(), a * win.getWidth() + b)
    p = g.Polygon(first, second)
    p.setOutline("green")
    return p



def gradient_descent():
    sum = 0.0
    # het doel is om lineaire regressie toe te passen op een verzameling
    # van punten, de functie is dus y = ax + b met a en b variabelen
    # die at random werden ingesteld, gebruik makend van gradient descent
    # zullen a en b berekend woren
    # de learning rate stellen we in op 0.4
    _m = np.random.rand() * 10 # random variabele tussen 0 en 10 (double)
    _c = np.random.rand() * 10 #
    A = np.vstack([set_of_x, np.ones(len(set_of_x))]).T
    eta = 0.4
    m, c = np.linalg.lstsq(A, set_of_y, rcond=None)[0]
    #print("Verwachtte functie is: y = {0}x + {1}".format(m, c))
    yPolygon = ray(m, c).draw(win)
    # lijst met verwachte waarden door lineaire regressie toe te passen
    y = [m * x + c for x in range(win.getWidth())]
    # lijst die we met huidige coefficienten _m en _c hebben
    a = [_m * x + c for x in range(win.getWidth())]
    # error
    

    """for (x, y) in zip(set_of_x, set_of_y):
        print("({0},{1})".format(x, y))"""

try:
    while True:
        new = win.getMouse()
        c = g.Circle(new, 5)
        c.setFill("black")
        set_of_x.append(new.getX())
        A = np.vstack([set_of_x, np.ones(len(set_of_x))]).T
        set_of_y.append(new.getY())
        i += 1
        if i == 5:
            gradient_descent()
            i = 0
        c.draw(win)
except g.GraphicsError:
    print("Ended well")