"""
DodecaCrypt Step 1: Key Recovery via Constraint Satisfaction

Given: flag.png with 26 colored dodecahedra, each showing 6 visible faces.
Goal: Find a 12-letter key whose color palette matches the flag's 12 colors.

Method:
1. Build the 120-element icosahedral symmetry group from known character permutations
2. For each die × each possible die value (0-119), compute constraints on the key
3. Backtracking search across all 26 dice to find a consistent key assignment

This recovers ONE valid key out of 120 equivalent keys (all related by dodecahedron symmetries).
"""

import math
from itertools import combinations

# =====================================================
# PART 1: Build dodecahedron geometry → face structure
# =====================================================
phi = (1 + math.sqrt(5)) / 2
ip = 1 / phi
V = [[-1,-1,-1],[-1,-1,1],[-1,1,-1],[-1,1,1],[1,-1,-1],[1,-1,1],[1,1,-1],[1,1,1],
     [0,-ip,-phi],[0,-ip,phi],[0,ip,-phi],[0,ip,phi],
     [-ip,-phi,0],[-ip,phi,0],[ip,-phi,0],[ip,phi,0],
     [-phi,0,-ip],[phi,0,-ip],[-phi,0,ip],[phi,0,ip]]

def d3(a, b): 
    return math.sqrt(sum((a[i] - b[i])**2 for i in range(3)))
def dot3(a, b): 
    return sum(a[i] * b[i] for i in range(3))
def cross3(a, b):
    return [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]]
def sub3(a, b): 
    return [a[i] - b[i] for i in range(3)]
def mag3(v): 
    return math.sqrt(dot3(v, v))
def sc3(v, s): 
    return [v[i] * s for i in range(3)]
def cen3(pts): 
    n=len(pts); 
    return [sum(p[i] for p in pts) / n for i in range(3)]

# Build edge set
ES = set()
for i in range(20):
    for j in range(i + 1, 20):
        if d3(V[i], V[j]) < 1.24:
            ES.add(f"{i} - {j}")

def ek(a, b): 
    return f"{min(a, b)} - {max(a, b)}"

# Find 12 pentagonal faces
faces = []
for combo in combinations(range(20), 5):
    ids = list(combo)
    p0, p1, p2 = V[ids[0]], V[ids[1]], V[ids[2]]
    nn = cross3(sub3(p1,p0), sub3(p2,p0))
    nnm = mag3(nn)
    if nnm < 1e-8: 
        continue
    u = sc3(nn, 1 / nnm)
    if any(abs(dot3(sub3(V[ids[i]],p0), u)) > 1e-6 for i in range(3,5)): 
        continue
    if any(sum(1 for x in ids if x!=v and ek(v,x) in ES) != 2 for v in ids):
        continue
    s = set(ids)
    stk = [ids[0]] 
    seen = set()
    while stk:
        v = stk.pop()
        if v in seen: 
            continue
        seen.add(v)
        for x in s:
            if x != v and ek(x,v) in ES and x not in seen: 
                stk.append(x)
    if len(seen) != 5: 
        continue
    pos = neg = 0 
    fs = set(ids)
    ok = True
    for i in range(20):
        if i in fs: 
            continue
        dd = dot3(sub3(V[i],p0), u)
        if dd > 1e-6: 
            pos += 1
        if dd < -1e-6: 
            neg += 1
        if pos > 0 and neg > 0: 
            ok = False 
            break
    if not ok: 
        continue
    pts = [V[i] for i in ids]
    ce = cen3(pts)
    fn = cross3(sub3(pts[1], pts[0]), sub3(pts[2], pts[0]))
    fn = sc3(fn, 1 / mag3(fn))
    axU = sub3(pts[0], ce)
    axU = sc3(axU, 1 / mag3(axU))
    axV = cross3(fn, axU)
    axV = sc3(axV, 1/mag3(axV))
    angs = sorted([(math.atan2(dot3(sub3(V[idx], ce), axV), dot3(sub3(V[idx], ce), axU)), idx) for idx in ids])
    faces.append([a[1] for a in angs])

fc = [cen3([V[i] for i in fids]) for fids in faces]

# Antipodal map (face i → opposite face)
inv_map = tuple(min(range(12), key = lambda j: d3([-fc[i][0], -fc[i][1], -fc[i][2]], fc[j])) for i in range(12))
print(f"Antipodal map: {inv_map}")
print(f"Found {len(faces)} faces")

# =====================================================
# PART 2: Build 120-element symmetry group
# =====================================================

# Known character permutations (from API queries with default key)
# sigma[v] = permutation for die value v (C=2 is identity)
sigma_known = {
    0:[9,8,2,6,1,11,10,7,0,4,5,3], 1:[1,9,2,5,0,6,11,7,4,8,3,10],
    2:[0,1,2,3,4,5,6,7,8,9,10,11], 3:[4,0,2,10,8,3,5,7,9,1,11,6],
    4:[3,0,4,7,10,5,1,6,8,2,11,9], 5:[10,3,4,11,8,7,5,6,2,0,9,1],
    6:[8,10,4,9,2,11,7,6,0,3,1,5], 7:[2,8,4,1,0,9,11,6,3,10,5,7],
    8:[0,2,4,5,3,1,9,6,10,8,7,11], 9:[10,4,8,7,11,3,0,5,9,2,6,1],
    10:[11,10,8,6,9,7,3,5,2,4,1,0], 11:[9,11,8,1,2,6,7,5,4,10,0,3],
    12:[2,9,8,0,4,1,6,5,10,11,3,7], 13:[4,2,8,3,10,0,1,5,11,9,7,6],
    14:[8,2,9,10,11,4,0,3,6,1,7,5], 15:[11,8,9,7,6,10,4,3,1,2,5,0],
    16:[6,11,9,5,1,7,10,3,2,8,0,4], 17:[1,6,9,0,2,5,7,3,8,11,4,10],
    18:[2,1,9,4,8,0,5,3,11,6,10,7], 19:[2,0,1,8,9,4,3,10,6,5,11,7],
    20:[9,2,1,11,6,8,4,10,5,0,7,3], 21:[6,9,1,7,5,11,8,10,0,2,3,4],
    22:[5,6,1,3,0,7,11,10,2,9,4,8], 23:[0,5,1,4,2,3,7,10,9,6,8,11],
    24:[3,5,0,10,4,7,6,11,2,1,8,9], 25:[4,3,0,8,2,10,7,11,1,5,9,6],
    26:[1,2,0,6,5,9,8,11,3,4,7,10], 27:[5,1,0,7,3,6,9,11,4,2,10,8],
}

def compose(p, q):
    return [q[p[i]] for i in range(12)]

# Generate full group by closure
all_perms = set()
for v, p in sigma_known.items():
    all_perms.add(tuple(p))
all_perms.add(tuple(inv_map))

changed = True
while changed:
    changed = False
    new = set()
    for p in all_perms:
        for q in all_perms:
            r = tuple(compose(list(p), list(q)))
            if r not in all_perms and r not in new:
                new.add(r)
                changed = True
    all_perms.update(new)

print(f"Symmetry group size: {len(all_perms)}")
assert len(all_perms) == 120, "Expected 120 elements!"
APL = sorted(all_perms)

# =====================================================
# PART 3: Flag data
# =====================================================

VISIBLE = [3, 5, 6, 7, 10, 11]

# Color hex → key letter mapping (12 distinct colors in the flag)
hex_to_letter = {
    "#aa00ff": "Y", "#bcf60c": "I", "#e6beff": "L", "#ffd8b1": "R",
    "#3cb44b": "B", "#e6194b": "A", "#000075": "S", "#aaffc3": "P",
    "#46f0f0": "G", "#f032e6": "H", "#800000": "O", "#ffe119": "C"
}
KEY_LETTERS = set(hex_to_letter.values())

# Flag die visible face hex colors → letters
# Faces in order: F3, F5, F6, F7, F10, F11
flag_hex = [
    {7:"#aaffc3",3:"#ffd8b1",10:"#800000",5:"#e6194b",11:"#ffe119",6:"#000075"},
    {7:"#bcf60c",3:"#000075",10:"#e6194b",5:"#f032e6",11:"#aa00ff",6:"#e6beff"},
    {7:"#e6beff",3:"#46f0f0",10:"#3cb44b",5:"#f032e6",11:"#aa00ff",6:"#bcf60c"},
    {7:"#aa00ff",3:"#e6194b",10:"#bcf60c",5:"#ffd8b1",11:"#e6beff",6:"#3cb44b"},
    {7:"#46f0f0",3:"#f032e6",10:"#ffe119",5:"#e6beff",11:"#800000",6:"#3cb44b"},
    {7:"#aa00ff",3:"#e6194b",10:"#bcf60c",5:"#ffd8b1",11:"#e6beff",6:"#3cb44b"},
    {7:"#ffe119",3:"#000075",10:"#aaffc3",5:"#f032e6",11:"#800000",6:"#46f0f0"},
    {7:"#ffe119",3:"#46f0f0",10:"#800000",5:"#f032e6",11:"#aaffc3",6:"#000075"},
    {7:"#aa00ff",3:"#bcf60c",10:"#e6beff",5:"#e6194b",11:"#3cb44b",6:"#ffd8b1"},
    {7:"#aa00ff",3:"#e6beff",10:"#bcf60c",5:"#3cb44b",11:"#e6194b",6:"#ffd8b1"},
    {7:"#ffd8b1",3:"#e6194b",10:"#aaffc3",5:"#aa00ff",11:"#800000",6:"#3cb44b"},
    {7:"#f032e6",3:"#e6beff",10:"#bcf60c",5:"#46f0f0",11:"#000075",6:"#ffe119"},
    {7:"#46f0f0",3:"#ffe119",10:"#f032e6",5:"#800000",11:"#e6beff",6:"#3cb44b"},
    {7:"#46f0f0",3:"#800000",10:"#3cb44b",5:"#ffe119",11:"#e6beff",6:"#f032e6"},
    {7:"#800000",3:"#ffd8b1",10:"#aaffc3",5:"#3cb44b",11:"#ffe119",6:"#46f0f0"},
    {7:"#e6beff",3:"#bcf60c",10:"#aa00ff",5:"#f032e6",11:"#3cb44b",6:"#46f0f0"},
    {7:"#aaffc3",3:"#800000",10:"#ffd8b1",5:"#ffe119",11:"#e6194b",6:"#000075"},
    {7:"#ffe119",3:"#800000",10:"#aaffc3",5:"#46f0f0",11:"#000075",6:"#f032e6"},
    {7:"#e6194b",3:"#ffd8b1",10:"#aa00ff",5:"#aaffc3",11:"#bcf60c",6:"#000075"},
    {7:"#bcf60c",3:"#e6beff",10:"#f032e6",5:"#aa00ff",11:"#000075",6:"#e6194b"},
    {7:"#bcf60c",3:"#e6194b",10:"#aa00ff",5:"#000075",11:"#e6beff",6:"#f032e6"},
    {7:"#f032e6",3:"#46f0f0",10:"#ffe119",5:"#e6beff",11:"#000075",6:"#bcf60c"},
    {7:"#aaffc3",3:"#800000",10:"#ffe119",5:"#ffd8b1",11:"#000075",6:"#e6194b"},
    {7:"#800000",3:"#46f0f0",10:"#ffe119",5:"#3cb44b",11:"#aaffc3",6:"#ffd8b1"},
    {7:"#aaffc3",3:"#ffe119",10:"#800000",5:"#000075",11:"#ffd8b1",6:"#e6194b"},
    {7:"#aa00ff",3:"#e6beff",10:"#bcf60c",5:"#3cb44b",11:"#e6194b",6:"#ffd8b1"},
]

# Convert hex to letters
flag_vis = []
for fh in flag_hex:
    flag_vis.append(tuple(hex_to_letter[fh[f]] for f in VISIBLE))

print(f"\nFlag die 0 visible letters: {flag_vis[0]}")
print(f"Flag die 1 visible letters: {flag_vis[1]}")

# =====================================================
# PART 4: Constraint Satisfaction
# =====================================================

def die_char_constraints(die_idx, perm_idx):
    """
    For a given die showing flag_vis[die_idx], assuming the die uses
    permutation APL[perm_idx], compute what key positions must hold
    which letters.
    
    Returns dict {key_position: letter} or None if invalid.
    """
    perm = APL[perm_idx]
    obs = flag_vis[die_idx]
    constraints = {}
    for i, face_idx in enumerate(VISIBLE):
        key_pos = perm[face_idx]
        letter = obs[i]
        if letter not in KEY_LETTERS:
            return None
        if key_pos in constraints:
            if constraints[key_pos] != letter:
                return None  # conflict
        constraints[key_pos] = letter
    # Check no two positions assigned same letter
    vals = list(constraints.values())
    if len(vals) != len(set(vals)):
        return None
    return constraints

def compatible(c1, c2):
    """Check if two constraint dicts can coexist in a single key."""
    pos_to_letter = {}
    letter_to_pos = {}
    for c in [c1, c2]:
        for pos, letter in c.items():
            if pos in pos_to_letter and pos_to_letter[pos] != letter:
                return False
            if letter in letter_to_pos and letter_to_pos[letter] != pos:
                return False
            pos_to_letter[pos] = letter
            letter_to_pos[letter] = pos
    return True

def merge(c1, c2):
    m = dict(c1)
    m.update(c2)
    return m

# Precompute all (perm_idx, constraints) for each die
print("\nPrecomputing constraints for all 26 dice × 120 permutations...")
die_options = []
for di in range(26):
    opts = []
    for pi in range(120):
        c = die_char_constraints(di, pi)
        if c is not None:
            opts.append((pi, c))
    die_options.append(opts)
    print(f"  Die {di:2d}: {len(opts)} valid permutations")

# Backtracking solver
print("\nSolving with backtracking...")
best_depth = [0]

def solve(dice_order, idx, key_assignment):
    if idx == len(dice_order):
        return key_assignment.copy(), {}
    
    di = dice_order[idx]
    if idx > best_depth[0]:
        best_depth[0] = idx
        print(f"  Depth {idx} / {len(dice_order)}, die {di}, key so far: {dict(sorted(key_assignment.items()))}")
    
    for pi, constraints in die_options[di]:
        if compatible(key_assignment, constraints):
            new_assignment = merge(key_assignment, constraints)
            result = solve(dice_order, idx + 1, new_assignment)
            if result is not None:
                key_result, perm_result = result
                perm_result[di] = pi
                return key_result, perm_result
    
    return None

# Sort dice by fewest options first (most constrained first)
dice_order = sorted(range(26), key=lambda d: len(die_options[d]))
print(f"Search order (most constrained first): {dice_order[:5]}...")

result = solve(dice_order, 0, {})

if result:
    key_assignment, perm_assignment = result
    key = ['?'] * 12
    for pos, letter in key_assignment.items():
        key[pos] = letter
    key_str = ''.join(key)
    
    print(f"\n{'='*60}")
    print(f"KEY FOUND: {key_str}")
    print(f"{'='*60}")
    print(f"\nKey assignment: {dict(sorted(key_assignment.items()))}")
    print(f"\nDie permutation indices:")
    for di in range(26):
        pi = perm_assignment.get(di, -1)
        print(f"  Die {di:2d}: perm #{pi}")
else:
    print("No solution found!")