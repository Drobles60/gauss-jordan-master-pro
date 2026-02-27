import ast
import operator as op
from fractions import Fraction

class SafeEvaluator:
    """
    Evaluador seguro de expresiones matemáticas simples para evitar el uso de eval().
    Soporta sumas, restas, multiplicaciones, divisiones y paréntesis.
    """
    
    # Operadores permitidos
    operators = {
        ast.Add: op.add, 
        ast.Sub: op.sub, 
        ast.Mult: op.mul,
        ast.Div: op.truediv, 
        ast.USub: op.neg
    }

    def evaluate(self, expression):
        """Evalúa una expresión string y retorna el valor como Fraction o float."""
        if not expression:
            return 0
        try:
            # Reemplazar '/' por divisiones de fracciones si es necesario para precisión?
            # Por ahora evaluamos normalmente y devolvemos Fraction
            node = ast.parse(expression, mode='eval').body
            result = self._eval_node(node)
            return result
        except Exception as e:
            raise ValueError(f"Expresión inválida: {e}")

    def _eval_node(self, node):
        if isinstance(node, ast.Num):  # < Python 3.8
            return node.n
        elif isinstance(node, ast.Constant):  # Python 3.8+
            return node.value
        elif isinstance(node, ast.BinOp):
            return self.operators[type(node.op)](self._eval_node(node.left), self._eval_node(node.right))
        elif isinstance(node, ast.UnaryOp):
            return self.operators[type(node.op)](self._eval_node(node.operand))
        else:
            raise TypeError(f"Nodo no soportado: {type(node)}")

def parse_fraction(text):
    """Convierte un string tipo '1/2' o '-3.5' a Fraction."""
    try:
        text = text.strip().replace(' ', '')
        if not text:
            return Fraction(0)
        return Fraction(text)
    except Exception:
        raise ValueError(f"Formato numérico inválido: '{text}'")
