from EllipticCurve import *
from random import randint
class ECC:
    def __init__(self, a, b, p, P, index,  order="", nA="", nB="", ):
        self.EC = EllipticCurve(a,b,p,order)
        self.P = P
        self.nA = self.shared_secrets(nA)
        self.nB = self.shared_secrets(nB)
        self.index = index
        self.priv_key = self.private_key()
    
    def shared_secrets(self, nX=""):
        if nX != "":
            return nX
        return randint(2**30, 2**50)

    def diffie_hellman(self):
        A = self.EC.encontra_nP(self.nA, self.P)
        B = self.EC.encontra_nP(self.nB, self.P)
        print("Diffie-Hellman Exchange:")
        print(f"A=nA*P={A}")
        print(f"B=nB*P={B}")
        return A,B
    
    def private_key(self):
        A,B= self.diffie_hellman()
        return self.EC.encontra_nP(self.nB, A)
    
    def encode(self,message):
        m = "0"
        for i in message:
            n = str(ord(i))
            if len(n) == 2:
                m += "0"
            m +=str(ord(i))
        m1 = m[:self.index]
        m2 = m[self.index:]
        return [int(m1), int(m2)]
    
    def decode(self, m1, m2, add_zero="0"):
        m = add_zero + str(m1) + str(m2)
        plaintext = ""
        for i in range(0, len(m), 3):
            plaintext += chr(int(m[i:i+3]))
        return plaintext

    def encrypt(self, message):
        T = self.priv_key
        x_T,y_T = T[0],T[1]
        m1,m2 = self.encode(message)
        x_S = (x_T * m1) % self.EC.p
        y_S = (y_T * m2) % self.EC.p
        return x_S, y_S

    def decrypt(self, S, priv_key):
        x_S, y_S = S[0], S[1]
        x_T, y_T = priv_key[0], priv_key[1]
        m1 = (x_S * pow(x_T, -1, self.EC.p)) % self.EC.p
        m2 = (y_S * pow(y_T, -1, self.EC.p)) % self.EC.p
        return [m1,m2]

    def visualize(self, message):
        x_S, y_S = curve.encrypt(message)
        print(f"\nEncrypted Message \nS={x_S, y_S}\n")
        
        m = curve.decrypt([x_S,y_S], self.priv_key)
        print(f"Encoded Decrypted Message\nM={m}\n")

        print(f"Decrypted and Decoded Message\nM= {self.decode(m[0],m[1], add_zero='0')}")
        

curve = ECC(a=1, b=1, p=6846869858332693264879382366866797734569, P=(0,1), index=30)
curve.visualize("Matemática é massa!")
