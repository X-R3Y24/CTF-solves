import requests
import time

BASE_URL = "https://dodecacrypt-949351df.challenges.bsidessf.net/"
KEY = "BYLOGRAPHICS"

AL = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
A2 = "_" + AL  # _ = 0, A = 1, ..., Z = 26

session = requests.Session()

def enc(msg, key=KEY):
    for _ in range(5):
        try:
            r = session.post(
                f"{BASE_URL}/api/encrypt",
                json = {"key": key, "message": msg}
            )
            return r.json()
        except Exception as e:
            print(f"Connection error ({e}), retrying...")
            time.sleep(1)
    return None

def num_to_msg(n):
    if n < 26:
        return AL[n]
    
    length = 2
    while (27**length) - 1 <= n:
        length += 1
        
    rem = n - 27**(length - 1)
    chars = []
    
    div = 27**(length - 1)
    chars.append(AL[rem // div])
    rem %= div
    
    for i in range(length - 2, -1, -1):
        div = 27**i
        chars.append(A2[rem // div])
        rem %= div
        
    return "".join(chars)

def main():

    for k in range(1, 27):
        boundary = 120**k
        last_k = boundary - 1
        
        msg_last = num_to_msg(last_k)
        msg_first = num_to_msg(boundary)
        
        res_last = enc(msg_last)
        res_first = enc(msg_first)
        
        if not res_last or not res_first:
            print(f"k ={k}: API Error")
            break
            
        count_last = res_last.get("count", 0)
        count_first = res_first.get("count", 0)
        
        print(f"k = {k:2}: last = {last_k} \"{msg_last}\" -> {count_last} die | "
              f"first = {boundary} \"{msg_first}\" -> {count_first} die")
if __name__ == "__main__":
    main()