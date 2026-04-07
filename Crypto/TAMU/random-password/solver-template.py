from pwn import *

context.log_level = "debug"
io = remote("streams.tamuctf.com", 443, ssl=True, sni="random-password")
io.interactive(prompt="00000000000000000000000000000000ffffffffefffffffffffffffffffff7f\n")
io.close()