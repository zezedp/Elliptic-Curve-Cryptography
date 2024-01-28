import math
class EllipticCurve:
    def __init__(self, a, b, p, order=""):
        """
        y^2 = x^3 + ax + b (mod p)
        """
        self.a = a
        self.b = b
        self.p = p
        if order == "":
            self.order = self.hasse_theorem()
        else:
            self.order = order

    def add_PQ(self, P, Q):
        """
        P -> (x0,y0)
        Q -> (x1,y1)

        a -> Coeficiente da Equação Cartesiana da Curva Elíptica

        p -> módulo primo
        """
        O = (0,0) # Elemento Neutro
        if P == (0, 0):
            return Q
        if Q == (0, 0):
            return P
        
        x1, y1 = P
        x2, y2 = Q

        if x1 == x2 and y2 == -y1:
            return O
        
        if P != Q:
            m = ((y2 - y1) * pow(x2 - x1, -1, self.p)) % self.p
        else:
            m = ((3 * x1**2 + self.a) * pow(2 * y1,-1, self.p)) % self.p
        
        x3 = (m**2 - x1 - x2) % self.p
        y3 = (m * (x1 - x3) - y1) % self.p
        return x3, y3

    def encontra_nP(self, k, P):
        """
        Double-and-Add : Algoritmo eficiente para computar multiplicação escalar de Curvas Elípticas
        """
        result = (0, 0)
        addend = P
        while k > 0:
            if k % 2 == 1:
                result = self.add_PQ(result, addend)
            addend = self.add_PQ(addend, addend)
            k //= 2
        return result
    

    def scaling_part1(self, P, Q, a, p):
        if P == (0, 0):
            return Q
        if Q == (0, 0):
            return P
        x1, y1 = P
        x2, y2 = Q
        if P != Q:
            m = ((y2 - y1) * pow(x2 - x1, -1, p)) % p
        else:
            m = ((3 * x1**2 + a) * pow(2 * y1,-1, p)) % p
        x3 = (m**2 - x1 - x2) % p
        y3 = (m * (x1 - x3) - y1) % p
        return x3, y3

    def scaling_part2(self,k, P, p):
        result = (0, 0)
        addend = P
        while k > 0:
            if k % 2 == 1:
                result = self.scaling_part1(result, addend, self.a, p)
            addend = self.scaling_part1(addend, addend, self.a, p)
            k //= 2
        return result

    def scaling(self, k, P):
        """
        Double-and-Add : Algoritmo eficiente para computar multiplicação escalar de Curvas Elípticas
        """
        result = (0, 0)
        addend = P
        while k > 0:
            if k % 2 == 1:
                result = self.add_PQ(result, addend, )
            addend = self.add_PQ(addend, addend)
            k //= 2
        return result

    def hasse_theorem(self):
        return (self.p+1) + 2*math.sqrt(self.p)
    
    def on_curve(self, P):
        x,y = P[0], P[1]
        return (y**2 - x**3 - self.a*x - self.b) % self.p == 0
