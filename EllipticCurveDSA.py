from EllipticCurve import *
from hashes import *
from random import randint
class ECDSA:
    def __init__(self, a, b, p, P, order="", h="SHA-1", dA=1):
        self.EC = EllipticCurve(a,b,p,order)
        self.P = P
        self.hash = dict_hashes.get(h)
        self.QA=(1,1)
        if dA == 1:
            self.dA = self.rand_dA_k(order)
        else:
            self.dA = dA
    
    def hash_message(self, message):
        self.hash.update(message.encode('utf-8'))
        return self.hash.hexdigest()

    def rand_dA_k(self, n):
        return randint(1, n-1)

    def get_curve_params(self):
        print(f"y²≡x³+{self.EC.a}x + {self.EC.b} (mod {self.p})")
        print(f"P = {self.P}")
        return (self.EC.a, self.EC.b, self.EC.p)

    def get_pubkey(self):
        return self.QA

    def sign_message(self, message):

        self.QA = self.EC.encontra_nP(self.dA, self.P)

        enc = self.hash_message(message)

        Ln = len(bin(int(enc, 16))) - 2
        z = int(enc[:Ln], 16)

        r = 0
        s = 0
        while r == 0 or s == 0:
            k = self.rand_dA_k(self.EC.order)

            x1, y1 = self.EC.encontra_nP(k, self.QA)

            r = x1 % self.EC.p

            s = (pow(k, -1, self.EC.p) * (z + r * self.dA)) % self.EC.p

        return r, s
    
    def verify_signature(self, message, r,s):
        if not 1 <= r <= (self.EC.order -1) and 1 <= r <= (self.EC.order -1):
            return "Not Valid Signature"
            
        enc = self.hash_message(message)

        Ln = len(bin(int(enc, 16))) - 2
        z = int(enc[:Ln], 16)

        w = pow(s,-1,self.EC.order)

        u1 = self.EC.scaling_part2(z,w,self.EC.order)
        u2 = self.EC.scaling_part2(r,w,self.EC.order)

        C = self.EC.add_PQ(self.EC.scaling(u1,self.P,self.EC.order), self.EC.scaling(u2,self.QA,self.EC.order))
        if C == (0,0):
            return "Not Valid Signature"
        
        if (r % self.EC.order) != C[0]:
            return "Not Valid Signature"
        
        return "Valid Signature!"
    
digitalSignature = ECDSA(1,1, 6846869858332693264879382366866797734569, (0,1), order=6846869858332693264898511507613378704826)
r,s=digitalSignature.sign_message("Elliptic Curves are Awesome!")
