from sage.all import *
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from random import randint
import hashlib
import os

p = 57896044618658103051097247842201434560310253892815534401457040244646854264811

# y^2 = x^3 + 57896044618658103051097247842201434560310253892815534336455328262589759096811*x + 6378745995050415640528904257536000
a = 57896044618658103051097247842201434560310253892815534336455328262589759096811
b = 6378745995050415640528904257536000
E = EllipticCurve(GF(p), [a, b])

# ECDH
G = E(46876917648549268272641716936114495226812126512396931121066067980475334056759, 29018161638760518123770904309639572979634020954930188106398864033161780615057)

dA = randint(2, G.order())
dB = randint(2, G.order())

PA = E(41794565872898552028378254333448511042514164360566217446125286680794907163222, 28501067479064047326107608780246105661757692260405498327414296914217192089882)
PB = E(832923623940209904267388169663314834051489004894067103155141367420578675552, 7382962163953851721569729505742450736497607615866914193411926051803583826592)



s = int((dB * PA).x())
key = hashlib.sha256(int(s).to_bytes((s.bit_length() + 7) // 8, 'big')).digest()
iv = bytes.fromhex("478876e42be078dceb3aee3a6a8f260f")
encrypted = bytes.fromhex("e31e0e638110d1e5c39764af90ac6194c1f9eaabd396703371dc2e6bb2932a18d824d86175ab071943cba7c093ccc6c6")

print(E.order() == p)
n_a = PA.log(G)
S = (n_a * PB).xy()[0]

key = hashlib.sha256(int(S).to_bytes((s.bit_length() + 7) // 8, 'big')).digest()

cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
decryptor = cipher.decryptor()
padded = decryptor.update(encrypted) + decryptor.finalize()

unpadder = padding.PKCS7(128).unpadder()
flag = unpadder.update(padded) + unpadder.finalize()
print(flag.decode())

#gigem{an0ma1ou5_curv3_ss5a_d41z8GaFF3kZ8}