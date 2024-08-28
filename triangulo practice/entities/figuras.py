import math


class triangulo:
    def __init__(self, base : float, altura : float):
        self.base = base
        self.altura = altura
        self.area = 0

    def Calcular (self):
        self.area = (self.base * self.altura)/2
    
    def getArea(self) -> float:
        return self.area
    

class cuadrado:
    def __init__(self, lado : float):
        self.lado = lado
        self.area = 0

    def Calcular(self) -> None:
        self.area = self.lado * self.lado

    def getArea(self) -> float:
        return self.area
    
class rectangulo:
    def __init__(self, base : float, altura : float):
        self.base = base
        self.altura = altura
        self.area = 0

    def Calcular(self) -> None:
        self.area = self.base * self.altura

    def getArea(self) -> float:
        return self.area

class poligono:
    def __init__(self, lado: float, n: float):
        self.lado = lado
        self.n = 5 #5 by default
        self.area = 0
        self.apotema = 0
    
    def Calcular(self) -> None:
        self.apotema = self.lado / (2 * math.tan(math.pi / self.n))

        self.area = (self.n * self.lado * self.apotema) / 2

    def getArea(self) -> float:
        return self.area