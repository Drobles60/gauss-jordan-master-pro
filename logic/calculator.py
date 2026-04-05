"""
calculator.py — Utilidades de cálculo numérico
===============================================
Proporciona dos componentes:

  1. SafeEvaluator: evalúa expresiones matemáticas en texto sin usar eval(),
     evitando vulnerabilidades de seguridad.  Soporta +, -, *, /, paréntesis.

  2. parse_fraction(text): convierte una cadena como "1/2" o "-3.5" a
     fractions.Fraction para mantener precisión aritmética exacta.

Entrada:  Cadena de texto con expresión o número (str)
Salida:   Valor numérico (int, float, o Fraction)
"""
import ast
import operator as op
from fractions import Fraction


class SafeEvaluator:
    """
    Evaluador seguro de expresiones matemáticas simples.

    Usa el árbol de sintaxis abstracta (AST) de Python para interpretar
    la expresión sin ejecutar código arbitrario (alternativa segura a eval()).

    Operadores soportados: +  -  *  /  y negación unaria (-)
    """

    # Tabla de operadores permitidos: tipo de nodo AST → función Python
    operators = {
        ast.Add:  op.add,    # a + b
        ast.Sub:  op.sub,    # a - b
        ast.Mult: op.mul,    # a * b
        ast.Div:  op.truediv, # a / b
        ast.USub: op.neg     # -a
    }

    def evaluate(self, expression):
        """
        Evalúa una expresión matemática dada como cadena de texto.

        Args:
            expression (str): Expresión, ej: "3 + 2*5", "(1+2)/3"

        Returns:
            int | float: Resultado de la evaluación.

        Raises:
            ValueError: Si la expresión contiene operadores o construcciones no permitidas.
        """
        if not expression:
            return 0
        try:
            # Parsear la cadena como árbol AST de Python (modo expresión)
            node = ast.parse(expression, mode='eval').body
            return self._eval_node(node)
        except Exception as e:
            raise ValueError(f"Expresión inválida: {e}")

    def _eval_node(self, node):
        """
        Recorre recursivamente el árbol AST y calcula el valor de cada nodo.

        Args:
            node: Nodo del árbol AST de Python.

        Returns:
            Valor numérico del sub-árbol.

        Raises:
            TypeError: Si el nodo contiene una construcción no permitida.
        """
        if isinstance(node, ast.Num):        # Literal numérico (Python < 3.8)
            return node.n
        elif isinstance(node, ast.Constant):  # Literal numérico (Python 3.8+)
            return node.value
        elif isinstance(node, ast.BinOp):     # Operación binaria: a OP b
            left  = self._eval_node(node.left)
            right = self._eval_node(node.right)
            return self.operators[type(node.op)](left, right)
        elif isinstance(node, ast.UnaryOp):   # Operación unaria: -a
            return self.operators[type(node.op)](self._eval_node(node.operand))
        else:
            raise TypeError(f"Operación no permitida: {type(node)}")


# ---------------------------------------------------------------------------
# Función auxiliar de parseo
# ---------------------------------------------------------------------------

def parse_fraction(text):
    """
    Convierte una cadena de texto a fractions.Fraction con precisión exacta.

    Acepta:
      - Enteros:    "3"  → Fraction(3, 1)
      - Decimales:  "1.5"  → Fraction(3, 2)
      - Fracciones: "1/2"  → Fraction(1, 2)
      - Negativos:  "-3/4" → Fraction(-3, 4)
      - Vacío:      ""     → Fraction(0)

    Args:
        text (str): Representación textual del número.

    Returns:
        Fraction: Valor exacto.

    Raises:
        ValueError: Si el formato no es reconocible.
    """
    try:
        text = text.strip().replace(' ', '')   # eliminar espacios residuales
        if not text:
            return Fraction(0)
        return Fraction(text)
    except Exception:
        raise ValueError(f"Formato numérico inválido: '{text}'")
