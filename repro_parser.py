from logic.parser import parse_equation

def test_parse(eq_str):
    print(f"Testing: '{eq_str}'")
    try:
        res = parse_equation(eq_str)
        print(f"  Success! Result: {res}")
    except Exception as e:
        print(f"  FAILED: {e}")

test_parse("-x + 2y - 3z = -4")
test_parse("2x - y + z = 5")
test_parse("3x + 4y - 2z = 6")
test_parse("x+y+z=0")
test_parse("-x-y-z=-1")
test_parse("1/2x + 0.5y = 10")
test_parse("x = 5")
test_parse("10 = x + y")
