import time
import requests
from typing import List, Dict, Optional, Any

BASE_URL: str = "https://dodecacrypt-949351df.challenges.bsidessf.net/" 
KEY: str = "BYLOGRAPHICS"

VIS: List[int] = [3, 5, 6, 7, 10, 11]

flag: List[Dict[int, str]] = [
    {3:"#ffd8b1",5:"#e6194b",6:"#000075",7:"#aaffc3",10:"#800000",11:"#ffe119"},
    {3:"#000075",5:"#f032e6",6:"#e6beff",7:"#bcf60c",10:"#e6194b",11:"#aa00ff"},
    {3:"#46f0f0",5:"#f032e6",6:"#bcf60c",7:"#e6beff",10:"#3cb44b",11:"#aa00ff"},
    {3:"#e6194b",5:"#ffd8b1",6:"#3cb44b",7:"#aa00ff",10:"#bcf60c",11:"#e6beff"},
    {3:"#f032e6",5:"#e6beff",6:"#3cb44b",7:"#46f0f0",10:"#ffe119",11:"#800000"},
    {3:"#e6194b",5:"#ffd8b1",6:"#3cb44b",7:"#aa00ff",10:"#bcf60c",11:"#e6beff"},
    {3:"#000075",5:"#f032e6",6:"#46f0f0",7:"#ffe119",10:"#aaffc3",11:"#800000"},
    {3:"#46f0f0",5:"#f032e6",6:"#000075",7:"#ffe119",10:"#800000",11:"#aaffc3"},
    {3:"#bcf60c",5:"#e6194b",6:"#ffd8b1",7:"#aa00ff",10:"#e6beff",11:"#3cb44b"},
    {3:"#e6beff",5:"#3cb44b",6:"#ffd8b1",7:"#aa00ff",10:"#bcf60c",11:"#e6194b"},
    {3:"#e6194b",5:"#aa00ff",6:"#3cb44b",7:"#ffd8b1",10:"#aaffc3",11:"#800000"},
    {3:"#e6beff",5:"#46f0f0",6:"#ffe119",7:"#f032e6",10:"#bcf60c",11:"#000075"},
    {3:"#ffe119",5:"#800000",6:"#3cb44b",7:"#46f0f0",10:"#f032e6",11:"#e6beff"},
    {3:"#800000",5:"#ffe119",6:"#f032e6",7:"#46f0f0",10:"#3cb44b",11:"#e6beff"},
    {3:"#ffd8b1",5:"#3cb44b",6:"#46f0f0",7:"#800000",10:"#aaffc3",11:"#ffe119"},
    {3:"#bcf60c",5:"#f032e6",6:"#46f0f0",7:"#e6beff",10:"#aa00ff",11:"#3cb44b"},
    {3:"#800000",5:"#ffe119",6:"#000075",7:"#aaffc3",10:"#ffd8b1",11:"#e6194b"},
    {3:"#800000",5:"#46f0f0",6:"#f032e6",7:"#ffe119",10:"#aaffc3",11:"#000075"},
    {3:"#ffd8b1",5:"#aaffc3",6:"#000075",7:"#e6194b",10:"#aa00ff",11:"#bcf60c"},
    {3:"#e6beff",5:"#aa00ff",6:"#e6194b",7:"#bcf60c",10:"#f032e6",11:"#000075"},
    {3:"#e6194b",5:"#000075",6:"#f032e6",7:"#bcf60c",10:"#aa00ff",11:"#e6beff"},
    {3:"#46f0f0",5:"#e6beff",6:"#bcf60c",7:"#f032e6",10:"#ffe119",11:"#000075"},
    {3:"#800000",5:"#ffd8b1",6:"#e6194b",7:"#aaffc3",10:"#ffe119",11:"#000075"},
    {3:"#46f0f0",5:"#3cb44b",6:"#ffd8b1",7:"#800000",10:"#ffe119",11:"#aaffc3"},
    {3:"#ffe119",5:"#000075",6:"#e6194b",7:"#aaffc3",10:"#800000",11:"#ffd8b1"},
    {3:"#e6beff",5:"#3cb44b",6:"#ffd8b1",7:"#aa00ff",10:"#bcf60c",11:"#e6194b"},
]

session: requests.Session = requests.Session()

def enc(m: str) -> Optional[Dict[str, Any]]:
    for _ in range(5):
        try:
            r: requests.Response = session.post(
                f"{BASE_URL}/api/encrypt",
                json = {"key": KEY, "message": m},
            )
            r.raise_for_status()
            return r.json()
        except Exception as e:
            print(f"Retry... ({e})")
            time.sleep(2)
    return None

def dsig(dd: List[Dict[str, str]], i: int) -> str:
    return ",".join(dd[i][f] for f in VIS)

def fsig(i: int) -> str:
    return ",".join(flag[i][f] for f in VIS)

def lead_match(dd: List[Dict[str, str]]) -> int:
    n: int = 0
    for i in range(26):
        if dsig(dd, i) == fsig(i):
            n += 1
        else:
            break
    return n

AL: str = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
A2: str = "_" + AL

def msg_to_num(s: str) -> int:
    if len(s) == 1:
        return AL.index(s[0])
    
    n: int = 27**(len(s) - 1)
    n += AL.index(s[0]) * (27**(len(s) - 1))
    
    for i in range(1, len(s)):
        c: int = 0 if s[i] == '_' else AL.index(s[i])
        n += c * (27**(len(s) - 1 - i))
    return n

def num_to_msg(n: int) -> str:
    if n < 26:
        return AL[n]
    
    length: int = 2
    while (27**length) - 1 <= n:
        length += 1
        
    rem: int = n - (27**(length - 1))
    chars: List[str] = []
    div: int = 27**(length - 1)
    
    chars.append(AL[rem // div])
    rem = rem % div
    
    for i in range(length - 2, -1, -1):
        div = 27**i
        chars.append(A2[rem // div])
        rem = rem % div
        
    return "".join(chars)

def confirmed(lo: int, hi: int) -> str:
    a: str = num_to_msg(lo)
    b: str = num_to_msg(hi)
    s: str = ""
    for i in range(min(len(a), len(b))):
        if a[i] == b[i]:
            s += a[i]
        else:
            s += "?" * (max(len(a), len(b)) - i)
            break
    return s

q_count: int = 0

def try_msg(n: int) -> int:
    global q_count
    msg: str = num_to_msg(n)
    if len(msg) not in [37, 38]:
        return -1
    
    r: Optional[Dict[str, Any]] = enc(msg)
    q_count += 1
    
    if not r or r.get("count") != 26:
        return -1
        
    return lead_match(r.get("dodecahedra", []))

def main() -> None:
    global q_count
    # Initial bounds from a prior run — empirical approximation of the
    # message space. The exact values don't matter as long as the true
    # answer lies within [lo, hi].
    lo: int = msg_to_num(f"BVDQXLAVADG{'A' * 26}")
    hi: int = msg_to_num(f"LNNSOQQAZCYCZUPMQOLTUIIWJAKMZH{'_' * 8}")
    
    print("Finding seed...")
    good: int = -1
    for i in range(500):
        test: int = lo + (hi - lo) * i // 500
        m: int = try_msg(test)
        if m >= 1:
            good = test
            print(f"Seed i={i} lm={m} \"{num_to_msg(test)[:20]}...\"")
            break
        if i % 50 == 0:
            print(f"  {i}/500")
            
    if good == -1:
        print("No seed found!")
        return

    for d in range(26):
        m: int = try_msg(good)
        if m < d + 1:
            print(f"Die {d}: scanning...")
            found: bool = False
            for i in range(200):
                test: int = lo + (hi - lo) * i // 200
                m = try_msg(test)
                if m >= d + 1:
                    good = test
                    found = True
                    print(f"Die {d}: found good, lm={m}")
                    break
            
            if not found:
                step: int = (hi - lo) // 50000
                if step == 0:
                    step = 1
                
                n: int = lo
                while n < hi:
                    m = try_msg(n)
                    if m >= d + 1:
                        good = n
                        found = True
                        print(f"Die {d}: dense scan found, lm={m}")
                        break
                    n += step
                    
            if not found:
                print(f"Die {d}: FAILED")
                break
            
        left: int = lo
        right: int = good
        while right - left > 1:
            mid: int = (left + right) // 2
            m = try_msg(mid)
            if m >= d + 1:
                right = mid
            else:
                left = mid
        lo = right
        
        left = good
        right = hi
        while right - left > 1:
            mid = (left + right) // 2
            m = try_msg(mid)
            if m >= d + 1:
                left = mid
            else:
                right = mid
        hi = left
        good = (lo + hi) // 2
        
        print(f"Die {d}: q={q_count} locked=\"{confirmed(lo, hi)}\" lo={lo} hi={hi}")
        
        if lo == hi:
            final_msg: str = num_to_msg(lo)
            m = try_msg(lo)
            print(f"\n*** CONVERGED: \"{final_msg}\" lm={m}/26 ***")
            if m == 26:
                print(f"FLAG: CTF{{{final_msg}}}")
            return

    print(f"\nFINAL: \"{num_to_msg(lo)}\"")
    print(f"FLAG: CTF{{{num_to_msg(lo)}}}")
    print(f"Queries: {q_count}")

if __name__ == "__main__":
    main()