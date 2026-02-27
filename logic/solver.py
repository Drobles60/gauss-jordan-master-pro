from fractions import Fraction
import copy

class GaussJordanSolver:
    """
    Clase encargada de resolver sistemas de ecuaciones 3x3 paso a paso.
    Utiliza fractions.Fraction para mantener precisión exacta.
    """

    def __init__(self, matrix):
        """
        matrix: list of list of fractions.Fraction (mapeada a 3x4)
        """
        self.matrix = copy.deepcopy(matrix)
        self.steps = []  # Lista de dicts con {matrix: list, operation: str, explanation: str}
        self._record_step("Inicio", "Se construye la matriz aumentada [A|b] con los valores ingresados.")

    def _record_step(self, operation, explanation, highlight_rows=None):
        """
        Guarda el estado actual de la matriz y la explicación del paso.
        highlight_rows: dict con {row_index: color_role} 
        roles: 'pivot' (green), 'target' (red), 'swap' (yellow)
        """
        # Convertimos las fracciones a string para facilitar la visualización o guardamos el objeto
        # Guardaremos el objeto Fraction para que la UI decida cómo mostrarlo (exacto/decimal)
        self.steps.append({
            "matrix": copy.deepcopy(self.matrix),
            "operation": operation,
            "explanation": explanation,
            "highlight_rows": highlight_rows or {}
        })

    def solve(self):
        """Ejecuta el algoritmo de Gauss-Jordan con pivoteo parcial."""
        rows = 3
        cols = 3  # A es 3x3, matriz aumentada es 3x4

        for h in range(rows):  # h es la fila del pivote
            # 1. Pivoteo parcial: buscar la fila con el valor absoluto más grande en la columna actual
            max_row = max(range(h, rows), key=lambda i: abs(self.matrix[i][h]))
            
            if self.matrix[max_row][h] == 0:
                # Si el máximo es 0, la columna es singular, pasamos a la siguiente o el sistema es especial
                continue

            if max_row != h:
                self.matrix[h], self.matrix[max_row] = self.matrix[max_row], self.matrix[h]
                self._record_step(
                    f"R{h+1} ↔ R{max_row+1}",
                    f"Intercambiamos la fila {h+1} con la {max_row+1} para usar el valor más grande como pivote.",
                    {h: 'swap', max_row: 'swap'}
                )

            # 2. Normalizar la fila del pivote (hacer que matrix[h][h] sea 1)
            pivot = self.matrix[h][h]
            if pivot != 1:
                self.matrix[h] = [x / pivot for x in self.matrix[h]]
                self._record_step(
                    f"R{h+1} ← R{h+1} / ({pivot})",
                    f"Dividimos la fila {h+1} por el pivote {pivot} para normalizar a 1.",
                    {h: 'pivot'}
                )
            else:
                self._record_step(
                    "Pivote listo",
                    f"El elemento en R{h+1},C{h+1} ya es 1. Usamos esta fila como base.",
                    {h: 'pivot'}
                )

            # 3. Eliminación de las demás filas
            for i in range(rows):
                if i != h:
                    factor = self.matrix[i][h]
                    if factor != 0:
                        self.matrix[i] = [self.matrix[i][j] - factor * self.matrix[h][j] for j in range(cols + 1)]
                        self._record_step(
                            f"R{i+1} ← R{i+1} - ({factor}) * R{h+1}",
                            f"Hacemos cero la posición C{h+1} en la fila {i+1} usando la fila pivote R{h+1}.",
                            {h: 'pivot', i: 'target'}
                        )

        return self._analyze_result()

    def _analyze_result(self):
        """Determina el tipo de solución del sistema."""
        # Verificamos si hay filas [0 0 0 | c]
        rows = 3
        cols = 3
        
        has_infinite = False
        
        for i in range(rows):
            all_zeros_a = all(self.matrix[i][j] == 0 for j in range(cols))
            if all_zeros_a:
                if self.matrix[i][cols] != 0:
                    return "No tiene solución", "Se detectó una contradicción (0 = constante no nula)."
                else:
                    has_infinite = True
        
        if has_infinite:
            return "Infinitas soluciones", "El sistema es compatible indeterminado (filas dependientes)."
        
        # Si llegamos aquí, verificamos si tenemos la identidad
        # En Gauss-Jordan completo 3x3, si no hubo singularidad, debería ser identidad.
        unique_results = [self.matrix[i][cols] for i in range(rows)]
        return "Solución única", unique_results
