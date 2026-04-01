import requests
from typing import List, Dict, Tuple, Optional, Any, Union

URL: str = "https://dodecacrypt-949351df.challenges.bsidessf.net/api/encrypt"
KEY: str = "YILRBASPGHOC"
VIS: List[int] = [3, 5, 6, 7, 10, 11]
NUM_ORIENTS: int = 120
BASE27: int = 27

flag_vis: List[Tuple[str, ...]] = [
    ("#ffd8b1","#e6194b","#000075","#aaffc3","#800000","#ffe119"),
    ("#000075","#f032e6","#e6beff","#bcf60c","#e6194b","#aa00ff"),
    ("#46f0f0","#f032e6","#bcf60c","#e6beff","#3cb44b","#aa00ff"),
    ("#e6194b","#ffd8b1","#3cb44b","#aa00ff","#bcf60c","#e6beff"),
    ("#f032e6","#e6beff","#3cb44b","#46f0f0","#ffe119","#800000"),
    ("#e6194b","#ffd8b1","#3cb44b","#aa00ff","#bcf60c","#e6beff"),
    ("#000075","#f032e6","#46f0f0","#ffe119","#aaffc3","#800000"),
    ("#46f0f0","#f032e6","#000075","#ffe119","#800000","#aaffc3"),
    ("#bcf60c","#e6194b","#ffd8b1","#aa00ff","#e6beff","#3cb44b"),
    ("#e6beff","#3cb44b","#ffd8b1","#aa00ff","#bcf60c","#e6194b"),
    ("#e6194b","#aa00ff","#3cb44b","#ffd8b1","#aaffc3","#800000"),
    ("#e6beff","#46f0f0","#ffe119","#f032e6","#bcf60c","#000075"),
    ("#ffe119","#800000","#3cb44b","#46f0f0","#f032e6","#e6beff"),
    ("#800000","#ffe119","#f032e6","#46f0f0","#3cb44b","#e6beff"),
    ("#ffd8b1","#3cb44b","#46f0f0","#800000","#aaffc3","#ffe119"),
    ("#bcf60c","#f032e6","#46f0f0","#e6beff","#aa00ff","#3cb44b"),
    ("#800000","#ffe119","#000075","#aaffc3","#ffd8b1","#e6194b"),
    ("#800000","#46f0f0","#f032e6","#ffe119","#aaffc3","#000075"),
    ("#ffd8b1","#aaffc3","#000075","#e6194b","#aa00ff","#bcf60c"),
    ("#e6beff","#aa00ff","#e6194b","#bcf60c","#f032e6","#000075"),
    ("#e6194b","#000075","#f032e6","#bcf60c","#aa00ff","#e6beff"),
    ("#46f0f0","#e6beff","#bcf60c","#f032e6","#ffe119","#000075"),
    ("#800000","#ffd8b1","#e6194b","#aaffc3","#ffe119","#000075"),
    ("#46f0f0","#3cb44b","#ffd8b1","#800000","#ffe119","#aaffc3"),
    ("#ffe119","#000075","#e6194b","#aaffc3","#800000","#ffd8b1"),
    ("#e6beff","#3cb44b","#ffd8b1","#aa00ff","#bcf60c","#e6194b"),
]

AL27: str = "_ABCDEFGHIJKLMNOPQRSTUVWXYZ"
# all_keys are the result of the key_recovery group + symmetry group permutation
all_keys: List[str] = ["YILRBASPGHOC","BYLOGRAPHICS","RYBPOAISGLCH","ORBCGPASLYHI","GOBHLCPSYRIA","LGBIYHCSROAP","YLBARIHSOGPC","OBGPCRYAHLSI","COGSHPRALBIY","HCGILSPABOYR","LHGYBISAOCRP","BLGROYIACHPS","GLHOCBYRSIPA","CGHPSOBRILAY","SCHAIPORLGYB","ISHYLAPRGCBO","LIHBGYARCSOP","LYIGHBROSACP","HLICSGBOAYPR","SHIPACGOYLRB","ASIRYPCOLHBG","YAIBLRPOHSGC","RAYOBPSCLIGH","BRYGLOPCIAHS","ILYSAHGCRBPO","AIYPRSHCBLOG","COPHSGBLARIY","GBLCHORPIYSA","LBYHIGOCARSP","RAPBOYILCSGH","SCPIAHGLROYB","PROSCAYIGBHL","AYRSPILHOBCG","POCASRBYHGIL","RBOAPYLICGSH","OGCRPBLYSHAI","PCSRAOGBIHYL","CHSOPGLBAIRY","PSAORCHGYIBL","SIACPHLGRYOB","PARCOSIHBYGL","HCSLIGOBAPYR","CPOHGSAIBRLY","SPCIHARYGOLB","APSYIROBHCLG","RPABYOCGISLH","OPRGBCSHYALI","IHSYALGBPCRO","GCOLBHSIRPYA","HSCLGIAYOPBR","IASLHYRBCPGO","YRALIBOGSPHC","BORLYGCHAPIS","AISRPYLBCHOG","BGOYRLHIPCAS","GHCBOLIYPSRA","HISGCLYBPAOR","IYAHSLBGPRCO","YBRIALGHPOSC","PASOCRYBHIGL","CPSGHORBIALY","ISALYHCGRPBO","YIABRLHGPSOC","RYAOPBLGSICH","PRACSOBGIYHL","SPAHICOGYRLB","APRIYSCHBOLG","YARLBISHOPGC","BYRGOLIHPACS","OBRCPGLHAYSI","PORSACGHYBIL","PCOARSHIBGYL","RPOYBASIGCLH","BROLGYAICPHS","GBOHCLYIPRSA","CGOSPHLIRBAY","HGCISLBYPOAR","SHCAPILYOGRB","OPCBGRAYHSLI","GOCLHBRYSPIA","ASPYRIHLOCBG","PSCROAIYGHBL","SAPHCIYLORGB","ARPISYBLCOHG","ROPYABGLSCIH","OCPBRGHLASYI","CSPGOHILRABY","LHIBYGCOASRP","GCHBLOPRISYA","LIYGBHSCRAOP","HSIGLCPOYABR","IAYHLSPCBRGO","LYBHGIASORCP","YRBILAPSGOHC","LBGIHYRACOSP","BOGYLRPAHCIS","LGHYIBORSCAP","YLIRABGOSHPC","BLYORGHCAIPS","GLBCOHISRYPA","HLGSCIYAOBPR","ILHASYBRCGPO","AYIPSRBOHLCG","RBYPAOGCILSH","OGBPRCHSYLAI","CHGPOSIABLRY","SIHPCAYRGLOB","SAICHPROLYGB","ARYSIPOCLBHG","ROBAYPCSLGIH","OCGRBPSALHYI","CSHOGPARLIBY","BGLRYOCPIHAS","GHLOBCSPYIRA","HILCGSAPBYOR","IYLSHARPGBCO","YBLAIROPHGSC","HGLSICOPYBAR","IHLAYSCPBGRO"]

sess: requests.Session = requests.Session()

def base27_to_msg(n: int) -> str:
    if n == 0: return "_"
    chars: List[str] = []
    while n > 0:
        chars.append(AL27[n % BASE27])
        n //= BASE27
    chars.reverse()
    return ''.join(chars)

def encode_base27_message(n: int) -> str:
    alphabet: str = "_ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    out: List[str] = []
    while n > 0:
        n, rem = divmod(n, BASE27)
        out.append(alphabet[rem])
    return "".join(reversed(out))

def compose(a: Tuple[int, ...], b: Tuple[int, ...]) -> Tuple[int, ...]:
    return tuple(a[b[i]] for i in range(12))

def invert(p: Tuple[int, ...]) -> Tuple[int, ...]:
    inv: List[int] = [0] * 12
    for i in range(12): 
        inv[p[i]] = i
    return tuple(inv)

# Step 1: Fetch 120 orientations
print("Fetching 120 orientations...")
service_orients: List[Optional[Tuple[str, ...]]] = [None] * NUM_ORIENTS
for idx in range(1, NUM_ORIENTS):
    msg: str = encode_base27_message(idx)
    r: Dict[str, Any] = sess.post(URL, json={"key": KEY, "message": msg}).json()
    service_orients[idx] = tuple(c.lower() for c in r["dodecahedra"][0])
    if idx % 20 == 0: 
        print(f"  {idx}/{NUM_ORIENTS}")

r_base: Dict[str, Any] = sess.post(URL, json={"key": KEY, "message": "DL"}).json()
service_orients[0] = tuple(c.lower() for c in r_base["dodecahedra"][1])
print("Got all 120 orientations")

# Step 2: Build group
base: Tuple[str, ...] = service_orients[0]
color_index: Dict[str, int] = {c: i for i, c in enumerate(base)}
service_group: List[Tuple[int, ...]] = []
for row_colors in service_orients:
    service_group.append(tuple(color_index[c] for c in row_colors))
perm_to_idx: Dict[Tuple[int, ...], int] = {p: i for i, p in enumerate(service_group)}

# Step 3: Match flag dice
print("\nMatching flag dice...")
vis_lookup: Dict[Tuple[str, ...], int] = {}
for oidx in range(NUM_ORIENTS):
    vis_sig: Tuple[str, ...] = tuple(service_orients[oidx][f] for f in VIS)
    vis_lookup[vis_sig] = oidx

raw_baseline: List[int] = []
for i, fvis in enumerate(flag_vis):
    fvis_lower: Tuple[str, ...] = tuple(c.lower() for c in fvis)
    if fvis_lower in vis_lookup:
        raw_baseline.append(vis_lookup[fvis_lower])
    else:
        print(f"  Die {i}: NO MATCH")
        raw_baseline.append(-1)

# Step 4: NORMALIZE — set die 0 to orientation 0
# Apply inverse of die 0's orientation to all dice
die0_perm: Tuple[int, ...] = service_group[raw_baseline[0]]
die0_inv: Tuple[int, ...] = invert(die0_perm)
baseline: List[int] = []
for idx in raw_baseline:
    new_perm: Tuple[int, ...] = compose(die0_inv, service_group[idx])
    baseline.append(perm_to_idx[new_perm])

print(f"Raw die 0 was orientation {raw_baseline[0]}, normalized to 0")
print(f"Baseline: {baseline}")

# Step 5: Compute all 120 messages
print("\nComputing 120 messages...")
messages: Dict[int, Tuple[List[int], str]] = {}
for guess in range(NUM_ORIENTS):
    pg: Tuple[int, ...] = service_group[guess]
    row: List[int] = [perm_to_idx[compose(pg, service_group[idx])] for idx in baseline]
    N: int = 0
    for d in row: N = N * NUM_ORIENTS + d
    msg_str: str = base27_to_msg(N)
    messages[guess] = (row, msg_str)

# Step 6: For each message, find matching key
print(f"\nFinding key for each message...")
print("g = 0 is identity (degenerate, 25 dice)\n")

for gi in range(NUM_ORIENTS):
    row, msg = messages[gi]
    
    keywords: List[str] = ["_IM_", "_IS_", "_AND_", "_THE_", "_YOUR_", "CRYPTO", "FLAG", "SYMMETRIC"]
    has_words: bool = any(w in msg for w in keywords)
    marker: str = "***" if has_words else "  "
    
    if gi == 0:
        # g=0 is the neutral element of the group — produces only 25 dice
        # for any message, so no valid 26-die plaintext exists for it.
        # In our normalized baseline this key is ORPGCBYLSAHI.
        # That's why it's missing from all_keys
        print(f"{marker} g={gi:3d}: key=N/A (25 dice)     msg=\"{msg}\" {marker}")
        continue
    
    found_key: Optional[str] = None
    for key_cand in all_keys:
        r_chk: Dict[str, Any] = sess.post(URL, json={"key": key_cand, "message": msg}).json()
        if r_chk.get("count") != 26: 
            continue
            
        vis0: Tuple[str, ...] = tuple(r_chk["dodecahedra"][0][f] for f in VIS)
        if vis0 != flag_vis[0]: 
            continue
            
        vis1: Tuple[str, ...] = tuple(r_chk["dodecahedra"][1][f] for f in VIS)
        if vis1 != flag_vis[1]: 
            continue
            
        found_key = key_cand
        break
    
    key_str: str = found_key if found_key else "NOT_FOUND"
    print(f"{marker} g ={gi:3d}: key = {key_str:20s} msg = \"{msg}\" {marker}")