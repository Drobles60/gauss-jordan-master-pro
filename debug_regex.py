import re
from fractions import Fraction
import sys

def parse_fraction(text):
    text = text.strip().replace(' ', '')
    if not text: return Fraction(0)
    return Fraction(text)

def parse_equation_v2(eq_str):
    print(f"DEBUG: Input: '{eq_str}'")
    eq_str = re.sub(r'\s+', '', eq_str.lower())
    print(f"DEBUG: Normalized: '{eq_str}'")
    
    if "=" not in eq_str: raise ValueError("=")
    left_str, right_str = eq_str.split("=", 1)
    
    pattern = re.compile(r'([+-]?)([\d\./]+)?([xyz]?)')
    pos = 0
    while pos < len(left_str):
        match = pattern.match(left_str, pos)
        print(f"DEBUG: pos={pos}, match='{match.group(0)}', groups={match.groups()}")
        if not match or match.group(0) == "":
            print(f"DEBUG: FAILURE at pos {pos}")
            return None
        pos += len(match.group(0))
    return True

print("--- Test 1 ---")
parse_equation_v2("-x + 2y - 3z = -4")
print("--- Test 2 (Manual match) ---")
p = re.compile(r'([+-]?)([\d\./]+)?([xyz]?)')
s = "-x+2y-3z"
m = p.match(s, 0)
print(f"Match at 0: '{m.group(0)}'")
m = p.match(s, 2)
print(f"Match at 2: '{m.group(0)}'")
