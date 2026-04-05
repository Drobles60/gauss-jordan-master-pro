"""
solver.py — Motor de resolución Gauss-Jordan
=============================================
Implementa el algoritmo de Gauss-Jordan con pivoteo parcial para resolver
sistemas de 3 ecuaciones lineales con 3 incógnitas.

Entrada:  matrix (list[list[Fraction]]) — Matriz aumentada 3x4 [A|b]
Salida:   (status: str, resultado: list | str) — Tipo de solución y valores x,y,z
"""
from fractions import Fraction
import copy


class GaussJordanSolver:
    """
    Resuelve sistemas de ecuaciones lineales 3×3 usando el método de Gauss-Jordan.

    Usa fractions.Fraction internamente para mantener precisión aritmética exacta
    (sin errores de punto flotante en la representación de fracciones).

    Atributos:
        matrix (list[list[Fraction]]): Copia profunda de la matriz aumentada [A|b].
        steps (list[dict]):  Historial de pasos con estado de la matriz,
                             operación realizada y explicación didáctica.
    """

    def __init__(self, matrix):
        """
        Inicializa el solver con la matriz aumentada.

        Args:
            matrix: list[list[Fraction]] de dimensión 3×4.
                    Columnas 0-2 son los coeficientes; columna 3 es el término independiente.
        """
        # Copiamos profundamente para no modificar la matriz original del llamador
        self.matrix = copy.deepcopy(matrix)
        self.steps = []  # Cada elemento: {matrix, operation, explanation, highlight_rows}
        self._record_step("Inicio", "Se construye la matriz aumentada [A|b] con los valores ingresados.")

    # ------------------------------------------------------------------
    # Métodos internos
    # ------------------------------------------------------------------

    def _record_step(self, operation, explanation, highlight_rows=None):
        """
        Guarda un snapshot del estado actual de la matriz junto con la descripción del paso.

        Args:
            operation (str):       Nombre corto de la operación (ej: "R1 ← R1 / 2").
            explanation (str):     Descripción didáctica en español.
            highlight_rows (dict): Mapeo {índice_fila: rol} para colorear en la UI.
                                   Roles válidos: 'pivot' (verde), 'target' (rojo), 'swap' (amarillo).
        """
        self.steps.append({
            "matrix": copy.deepcopy(self.matrix),   # snapshot inmutable
            "operation": operation,
            "explanation": explanation,
            "highlight_rows": highlight_rows or {}
        })

    # ------------------------------------------------------------------
    # Algoritmo principal
    # ------------------------------------------------------------------

    def solve(self):
        """
        Ejecuta el algoritmo de Gauss-Jordan completo con pivoteo parcial.

        El proceso tiene 3 sub-pasos por cada columna pivote h:
          1. Pivoteo parcial: elegir la fila con el mayor valor absoluto en la columna h.
          2. Normalización: dividir la fila pivote para que matrix[h][h] = 1.
          3. Eliminación: anular el valor en la columna h para todas las filas i ≠ h.

        Returns:
            tuple: ("Solución única",    [x, y, z])       si el sistema tiene solución única.
                   ("No tiene solución", str_mensaje)     si hay contradicción.
                   ("Infinitas soluciones", str_mensaje)  si el sistema es indeterminado.
        """
        rows = 3
        cols = 3  # La parte A es 3×3; la matriz aumentada es 3×4

        for h in range(rows):  # h = índice de la columna/fila pivote actual

            # ── Paso 1: Pivoteo parcial ──────────────────────────────────────
            # Busca la fila de índice >= h que tenga el mayor valor absoluto
            # en la columna h. Esto mejora la estabilidad numérica.
            max_row = max(range(h, rows), key=lambda i: abs(self.matrix[i][h]))

            if self.matrix[max_row][h] == 0:
                # Toda la columna h (desde la fila h) es cero → columna singular.
                # No podemos crear un pivote aquí; continuamos con la siguiente columna.
                continue

            if max_row != h:
                # Intercambiamos para llevar el mejor pivote a la fila h
                self.matrix[h], self.matrix[max_row] = self.matrix[max_row], self.matrix[h]
                self._record_step(
                    f"R{h+1} ↔ R{max_row+1}",
                    f"Intercambiamos la fila {h+1} con la {max_row+1} para usar el valor más grande como pivote.",
                    {h: 'swap', max_row: 'swap'}
                )

            # ── Paso 2: Normalización del pivote ─────────────────────────────
            # Dividimos todos los elementos de la fila h por matrix[h][h],
            # de modo que el elemento pivote quede igual a 1.
            pivot = self.matrix[h][h]
            if pivot != 1:
                self.matrix[h] = [x / pivot for x in self.matrix[h]]
                self._record_step(
                    f"R{h+1} ← R{h+1} / ({pivot})",
                    f"Dividimos la fila {h+1} por el pivote {pivot} para normalizar a 1.",
                    {h: 'pivot'}
                )
            else:
                # El pivote ya es 1; solo registramos el paso informativo
                self._record_step(
                    "Pivote listo",
                    f"El elemento en R{h+1},C{h+1} ya es 1. Usamos esta fila como base.",
                    {h: 'pivot'}
                )

            # ── Paso 3: Eliminación en todas las demás filas ─────────────────
            # Para cada fila i ≠ h, restamos el múltiplo adecuado de la fila h
            # de modo que la columna h quede con 0 en las filas i.
            for i in range(rows):
                if i != h:
                    factor = self.matrix[i][h]   # valor a eliminar
                    if factor != 0:
                        # Ri ← Ri - factor * Rh
                        self.matrix[i] = [
                            self.matrix[i][j] - factor * self.matrix[h][j]
                            for j in range(cols + 1)
                        ]
                        self._record_step(
                            f"R{i+1} ← R{i+1} - ({factor}) * R{h+1}",
                            f"Hacemos cero la posición C{h+1} en la fila {i+1} usando la fila pivote R{h+1}.",
                            {h: 'pivot', i: 'target'}
                        )

        return self._analyze_result()

    # ------------------------------------------------------------------
    # Análisis del resultado
    # ------------------------------------------------------------------

    def _analyze_result(self):
        """
        Determina el tipo de solución después de aplicar Gauss-Jordan.

        Casos posibles:
          • Fila [ 0  0  0 | c≠0 ] → Sin solución (sistema inconsistente).
          • Fila [ 0  0  0 |  0  ] → Infinitas soluciones (filas dependientes).
          • Ninguno de los anteriores → Solución única; lee x,y,z de la columna 3.

        Returns:
            tuple: (tipo_solución: str, resultado)
        """
        rows = 3
        cols = 3
        has_infinite = False

        for i in range(rows):
            # Verifica si todos los coeficientes de la fila son cero
            all_zeros_a = all(self.matrix[i][j] == 0 for j in range(cols))
            if all_zeros_a:
                if self.matrix[i][cols] != 0:
                    # Contradicción: 0 = constante no nula → sin solución
                    return "No tiene solución", "Se detectó una contradicción (0 = constante no nula)."
                else:
                    # Fila de ceros completa → sistema indeterminado
                    has_infinite = True

        if has_infinite:
            return "Infinitas soluciones", "El sistema es compatible indeterminado (filas dependientes)."

        # Si llegamos aquí la submatriz izquierda es la identidad
        # La solución está en la columna de términos independientes
        unique_results = [self.matrix[i][cols] for i in range(rows)]  # [x, y, z]
        return "Solución única", unique_results
