"""
DodecaCrypt Script 6: Enumerate All 120 Valid Keys from One Known Key

The 120 valid keys are exactly the orbit of BYLOGRAPHICS under the
icosahedral symmetry group acting on key positions:
    new_key[i] = key[perm[i]]  for each perm in the group.

Requires: APL (sorted list of 120 permutations) from Script 2.
"""

# Paste APL from Script 2 here, or import it:
from key_recovery import APL

KNOWN_KEY = "BYLOGRAPHICS"  # one valid key

all_keys = []
for perm in APL:
    new_key = "".join(KNOWN_KEY[perm[i]] for i in range(12))
    all_keys.append(new_key)

all_keys = sorted(set(all_keys))
assert len(all_keys) == 120, f"Expected 120, got {len(all_keys)}"

print(f"All {len(all_keys)} valid keys:")
for i, k in enumerate(all_keys):
    print(f"  {i:3d}: {k}")

# Sanity check: BYLOGRAPHICS must be in the list
assert KNOWN_KEY in all_keys
print(f"\nBYLOGRAPHICS at index {all_keys.index(KNOWN_KEY)}")