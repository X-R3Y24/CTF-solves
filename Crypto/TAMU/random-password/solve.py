import random
from pwn import *

random.seed(int(121728))

target = 0.9992610559813815
target_ix = 5719

states = []
fives = [0] * target_ix
seventeens = [0] * target_ix

r = random.random()

while r != target:
    states.append(r)
    r = random.random()

def check_right(i, x):
    j = i + 1
    next_i = 0
    while j < target_ix:
        sum_i = 0
        while j < target_ix and sum_i < x:
            sum_i += states[j]
            j += 1
        if sum_i >= x:
            next_i += 1
    return next_i

for i in range(0, target_ix):
    fives[i] = check_right(i, 5)
    seventeens[i] = check_right(i, 17)

memo = set()

def consume(i, timeout):
    t = 0
    while t < timeout:
        if i >= len(states):
            return None
        t += states[i]
        i += 1
    return i

def can_reach(i, remaining_bits):
    if i >= target_ix or remaining_bits <= 0:
        return True
    return seventeens[i] <= remaining_bits <= fives[i]

def solve(pos, i, bits):
    if pos == 256:
        if i == target_ix:
            return bits
        return None
    if (pos, i) in memo or not can_reach(i, 256 - pos):
        memo.add((pos, i))
        return None
    for bit in ['0', '1']:
        timeout = 5 if bit == '0' else 17
        new_i = consume(i, timeout)
        if new_i is None:
            continue
        if not can_reach(new_i, 255 - pos):
            continue
        result = solve(pos + 1, new_i, bits + bit)
        if result:
            return result
    memo.add((pos, i))
    return None

bits = solve(0, 0, "")
password = hex(int(bits, 2))[2:].zfill(64)
io = remote("streams.tamuctf.com", 443, ssl=True, sni="random-password")
io.recvuntil(b"Enter the password in hex: ")
io.sendline(password.encode())
print(io.recvline().decode())

#Here's the flag gigem{h3rd1ng_rand0m_sh3ep_LiNBpqRTk}