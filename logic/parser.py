"""
parser.py — Intérprete robusto de ecuaciones lineales
======================================================
Convierte una ecuación lineal escrita en texto libre a [a, b, c, d] como Fraction.
Soporta todos los formatos de entrada comunes:

  Formatos de coeficiente aceptados:
    2x          coeficiente entero
    -3x         coeficiente negativo
    1/2 x       fracción separada
    (1/2)x      fracción entre paréntesis
    0.5x        decimal
    x           coeficiente implícito 1
    -x          coeficiente implícito -1
    2*x         con asterisco multiplicador

  Formatos de constante:
    = 5         entero
    = -3.5      decimal negativo
    = 1/2       fracción
    = 0         cero

Entrada:  str  — ecuación como texto (ej: "(1/2)x + y - z = 8")
Salida:   list[Fraction] — [coef_x, coef_y, coef_z, rhs]
"""
import re
from fractions import Fraction
from logic.calculator import parse_fraction


def _preprocess(eq_str):
    """
    Normaliza la cadena antes del parseo principal:
      1. Elimina todos los espacios.
      2. Convierte a minúsculas.
      3. Reemplaza (a/b) → a/b  (fracciones entre paréntesis).
      4. Reemplaza * entre número y variable → vacío (2*x → 2x).
      5. Convierte decimales como coeficientes (0.5x → fracción internamente aceptada).
    """
    s = "".join(eq_str.lower().split())

    # (a/b) o (a) → quitar paréntesis cuando el contenido es numérico
    # Ej: (1/2)x → 1/2 x,   (-3)x → -3x
    s = re.sub(r'\(([+-]?[\d\.]+(?:/[\d\.]+)?)\)', r'\1', s)

    # Eliminar asterisco multiplicador: 2*x → 2x
    s = s.replace('*', '')

    # Simplificar dobles signos: --y → +y, +-y → -y, -+y → -y, ++y → +y
    s = s.replace('--', '+').replace('++', '+').replace('+-', '-').replace('-+', '-')

    return s


def parse_equation(eq_str):
    """
    Parsea una ecuación lineal de 3 variables (x, y, z).

    Soporta:
      - Coeficientes enteros, decimales, fracciones simples y entre paréntesis.
      - Coeficiente implícito 1 o -1 (solo la variable).
      - Constantes en el lado izquierdo (se mueven al lado derecho).
      - Espacios libres y mezcla de formatos.

    Args:
        eq_str (str): Ecuación en texto. Debe contener '='.

    Returns:
        list[Fraction]: [coef_x, coef_y, coef_z, rhs]

    Raises:
        ValueError: Si el formato es irreconocible.
    """
    if "=" not in eq_str:
        raise ValueError("La ecuación debe contener el signo '='")

    # Separar antes de normalizar para no perder el '='
    raw_left, raw_right = eq_str.split("=", 1)

    # Normalizar cada lado por separado
    left_side = _preprocess(raw_left)
    right_side = _preprocess(raw_right)

    # BUG 2: ecuación completamente vacía (solo "=" o "  =  ")
    if not left_side and not right_side:
        raise ValueError("La ecuación está vacía.")

    # Parsear el RHS (término independiente)
    try:
        rhs = parse_fraction(right_side) if right_side else Fraction(0)
    except Exception:
        raise ValueError(f"El lado derecho '{raw_right.strip()}' no es un número válido.")

    # Diccionario de coeficientes
    coeffs = {'x': Fraction(0), 'y': Fraction(0), 'z': Fraction(0)}
    found_variable = False  # para detectar ecuaciones sin variables (BUG 1)

    # Patrón ampliado:
    #   Grupo 1: signo opcional  [+-]
    #   Alternativa A: número (entero, decimal o fracción a/b) seguido de variable opcional
    #   Alternativa B: variable sola (coeficiente implícito 1)
    #
    # Número: dígitos con punto decimal y/o barra de fracción
    NUM = r'[\d]+(?:\.[\d]+)?(?:/[\d]+(?:\.[\d]+)?)?'
    pattern = re.compile(
        rf'([+-]?)(?:({NUM})([xyz]?)|([xyz]))'
    )

    pos = 0
    while pos < len(left_side):
        match = pattern.match(left_side, pos)
        if not match:
            bad_char = left_side[pos]
            # BUG 4: signo seguido de variable no soportada (ej: "+w")
            if bad_char in '+-' and pos + 1 < len(left_side) and left_side[pos + 1].isalpha():
                unknown_var = left_side[pos + 1]
                raise ValueError(
                    f"Variable '{unknown_var}' no reconocida. "
                    f"Solo se aceptan las variables x, y, z."
                )
            # BUG 4: variable no soportada directa (ej: "w")
            if bad_char.isalpha():
                raise ValueError(
                    f"Variable '{bad_char}' no reconocida. "
                    f"Solo se aceptan las variables x, y, z."
                )
            raise ValueError(
                f"No se puede interpretar el carácter '{bad_char}' "
                f"en la posición {pos} de '{left_side}'.\n"
                f"Formatos válidos: '2x', '-y', '1/2 z', '(1/2)x', '0.5x'"
            )

        full_term      = match.group(0)
        sign           = match.group(1)         # '+', '-', o ''
        num_str        = match.group(2)         # parte numérica
        var_after_num  = match.group(3)         # variable tras número
        var_standalone = match.group(4)         # variable sola (sin número)

        if var_standalone:
            # Caso: solo la variable → coef implícito 1
            val = Fraction(1)
            var = var_standalone
        else:
            try:
                val = parse_fraction(num_str)
                var = var_after_num if var_after_num else None
            except Exception:
                raise ValueError(f"Coeficiente numérico inválido: '{num_str}'")

        # Aplicar signo
        if sign == '-':
            val = -val

        # BUG 3: detectar "2xy" — variable pegada a otra variable sin operador
        if var and (pos + len(full_term)) < len(left_side):
            next_char = left_side[pos + len(full_term)]
            if next_char in 'xyz':
                raise ValueError(
                    f"Formato inválido '{full_term}{next_char}': dos variables pegadas. "
                    f"Use un operador entre ellas, por ejemplo: '{full_term} + {next_char}'"
                )

        if var:
            found_variable = True
            coeffs[var] += val
        else:
            # Constante en el LHS → pasar al RHS con signo contrario
            rhs -= val

        pos += len(full_term)

    # BUG 1: ecuación sin ninguna variable (ej: "3 + 5 = 8" o "= 5")
    if not found_variable and left_side:
        raise ValueError(
            "La ecuación no contiene variables (x, y, z). "
            "Ingrese una ecuación lineal válida, por ejemplo: '2x + y - z = 5'"
        )

    return [coeffs['x'], coeffs['y'], coeffs['z'], rhs]
