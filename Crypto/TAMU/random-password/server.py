from functools import partial
import re
import random

random.seed(121728)

def random_sleep(timeout: float) -> None:
  time_elapsed = 0
  while time_elapsed < timeout:
    time_elapsed += random.random()

handle_zero = partial(random_sleep, 5)
handle_one = partial(random_sleep, 17)

def verify(password: str, correct_value: float) -> bool:
  if len(password) != 64: return False

  bit_str = bin(int(password, 16))[2:].zfill(256)

  for bit in bit_str:
    match bit:
      case '0':
        handle_zero()
      case '1':
        handle_one()

  return random.random() == correct_value

password = input('Enter the password in hex: ')
if not re.match('^[0-9a-f]+$', password):
  print('Invalid nonhex input')
  exit()

if verify(password, 0.9992610559813815):
  with open('flag.txt', 'r') as outfile:
    print("Here's the flag", outfile.readline().strip())
    exit()
else:
  print('Incorrect password')
  exit()
