from vpython import *
import math


class Turtle3D:

    def __init__(self):
        '''
        Constructora de la tortuga.

        Atributs:
            scnece: finestra gràfica.
            pos: posició actual de la tortuga (vector).
            alpha: angle hortizontal( radians).
            beta: angle vertical (radians).
            direction: direcció de mirada de la tortuga (vector).
            col: color dels cilindres que dibuixa (vector).
            paint: boolea que indica si hem de dibuixar o no.
        '''
        scene.height = scene.width = 1000
        scene.autocenter = True
        self.pos = vector(0, 0, 0)
        self.alpha = math.radians(0)
        self.beta = math.radians(0)
        self.direction = vector(1, 0, 0)
        self.col = vector(1.0, 0.0, 0.0)
        self.paint = True

    def show(self):
        '''
        Funcions, la qual, indica a la la tortuga que pinti els cilindres.
        '''
        self.paint = True

    def hide(self):
        '''
        Funcions, la qual, indica a la la tortuga que deixi de pintar els cilindres.
        '''
        self.paint = False

    def home(self):
        '''
        Funció que retorna la tortuga a l'origen de coordenades.
        '''
        self.pos = vector(0, 0, 0)

    def color(self, r, g, b):
        '''
        Funció que canvia el color dels cilindres de la tortuga.
        '''
        self.col = vector(r, g, b)

    def right(self, degree):
        '''
        Funcions que incrementa l'angle horitontal i actualitza la direcció de la tortuga.
        '''
        self.alpha += math.radians(degree)
        self.__updateDirection()

    def left(self, degree):
        '''
        Funcions que decrementa l'angle horitontal i actualitza la direcció de la tortuga.
        '''
        self.alpha -= math.radians(degree)
        self.__updateDirection()

    def up(self, degree):
        '''
        Funcions que incrementa l'angle vertical i actualitza la direcció de la tortuga.
        '''
        self.beta += math.radians(degree)
        self.__updateDirection()

    def down(self, degree):
        '''
        Funcions que incrementa el l'angle vertical i actualitza la direcció de la tortuga.
        '''
        self.beta -= math.radians(degree)
        self.__updateDirection()

    def forward(self, distance):
        '''
        Funcions que avança la tortuda en la direcció actual.
        '''
        self.__drawCylinder(distance)

    def backward(self, distance):
        '''
        Funcions que retrocedeix la tortuga en la direcció actual.
        '''
        self.__drawCylinder(-distance)

    def __drawCylinder(self, lenght):
        '''
        Funció que dibuixa una esfera en la posició original, avança la tortuga a la nova
        dibuixa un cilindre desde la posicio origial a la nova i torna a dibuixar un altra esfera;
        les figures es dibuixen si el bolea paint = True, la posició sempre se actualitza.
        '''
        newPos = self.pos + lenght * self.direction
        if self.paint:
            sphere(pos=self.pos, radius=0.15, color=self.col)
            cylinder(pos=self.pos, axis=lenght * self.direction,
                     radius=0.15, color=self.col)
            sphere(pos=newPos, radius=0.15, color=self.col)
        self.pos = newPos

    def __updateDirection(self):
        '''
        Funció que actualitza la direccio de la tortgua segons els angles alpha i beta,
        la direcció sempres és un vector unitari.
        '''
        self.direction = vector(math.cos(self.alpha) * math.cos(self.beta),
                                math.sin(self.beta), math.sin(self.alpha) * math.cos(self.beta))
