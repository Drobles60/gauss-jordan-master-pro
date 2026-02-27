import re
from fractions import Fraction
from logic.calculator import parse_fraction

def parse_equation(eq_str):
    """
    Parses a linear equation of 3 variables (x, y, z) into a list of 4 fractions [a, b, c, d].
    Handles implicit coefficients (x -> 1x, -y -> -1y) and moves constants to the RHS.
    """
    # Normalize: remove all whitespace characters and lowercase
    eq_str = "".join(eq_str.lower().split())
    
    if "=" not in eq_str:
        raise ValueError("La ecuación debe contener el signo '='")
    
    left_side, right_side = eq_str.split("=", 1)
    
    # Parse RHS
    try:
        # Ensure RHS is also stripped of any whitespace
        rs_clean = right_side.strip()
        rhs = parse_fraction(rs_clean) if rs_clean else Fraction(0)
    except:
        rhs = Fraction(0)
        
    coeffs = {'x': Fraction(0), 'y': Fraction(0), 'z': Fraction(0)}
    
    # Term pattern: optional sign, then either (number followed by optional var) OR (just a var)
    # Group 1: Sign ([+-]?)
    # Group 2: Coefficient ([\d\./]+)
    # Group 3: Variable after coefficient ([xyz]?)
    # Group 4: Variable without coefficient ([xyz])
    pattern = re.compile(r'([+-]?)(?:([\d\./]+)([xyz]?)|([xyz]))')
    
    pos = 0
    while pos < len(left_side):
        match = pattern.match(left_side, pos)
        if not match:
            # Show the actual char that failed for debugging
            char_info = f"'{left_side[pos]}'"
            raise ValueError(f"No se pudo interpretar el carácter {char_info} en la posición {pos} de '{left_side}'")
            
        full_term = match.group(0)
        sign = match.group(1)
        num_str = match.group(2)
        var_after_num = match.group(3)
        var_standalone = match.group(4)
        
        # Determine numeric value and variable
        if var_standalone:
            val = Fraction(1)
            var = var_standalone
        else:
            # num_str must exist because of the regex structure
            try:
                # Handle possible '*' between number and var (just in case split/join missed something)
                clean_num = num_str.replace('*', '')
                val = parse_fraction(clean_num)
                var = var_after_num if var_after_num else None
            except:
                raise ValueError(f"Formato numérico inválido: '{num_str}'")
        
        if sign == '-':
            val = -val
            
        if var:
            coeffs[var] += val
        else:
            # Constant on left side, move to right
            rhs -= val
            
        pos += len(full_term)
            
    return [coeffs['x'], coeffs['y'], coeffs['z'], rhs]
