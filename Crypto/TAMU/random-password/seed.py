import random
from functools import partial

random.seed(121728)

bits = "0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000011111111111111111111111111111111111011111111111111111111111111111111111111111111111111111111111111111111111111111111111101111111"
i = 0
for bit in bits:
    t = 0
    timeout = 5 if bit == '0' else 17
    while t < timeout:
        i += 1
        t += random.random()

result = random.random()
i += 1
print(i)
print(f"Result: {result}")
print(f"Target: 0.9992610559813815")
print(f"Match: {result == 0.9992610559813815}")
print(f"Hex: {hex(int(bits, 2))[2:].zfill(64)}")