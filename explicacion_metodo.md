# Explicación del Método de Gauss-Jordan

## 1. Definición del Método Numérico

El método de **Gauss-Jordan** es un algoritmo del álgebra lineal para determinar las soluciones de un sistema de ecuaciones lineales y para encontrar matrices inversas. Es una extensión del método de eliminación gaussiana que lleva la matriz a su **forma escalonada reducida por filas** (RREF).

---

## 2. Análisis: Datos de Entrada y Salida

### Datos de Entrada
- Un sistema de **3 ecuaciones lineales** con **3 incógnitas** (x, y, z).
- Cada ecuación de la forma: `ax + by + cz = d`
- El usuario puede ingresar:
  - Las ecuaciones en texto libre (ej: `2x + y - z = 8`)
  - Directamente los coeficientes en la matriz aumentada `[A|b]`

### Información Producida (Salida)
- **Tipo de solución**: Solución única / Sin solución / Infinitas soluciones.
- Si hay solución única: los valores de `x`, `y`, `z`.
- **Procedimiento paso a paso**: cada operación elemental aplicada con explicación.
- Los valores pueden mostrarse en fracciones exactas o en decimales (4 cifras).

---

## 3. Resumen Teórico

Consiste en aplicar una serie de **operaciones elementales de fila** a la matriz aumentada del sistema hasta transformarla en la **identidad** (si hay solución única).

### Matriz Aumentada
Dado un sistema 3×3:
```
a1·x + b1·y + c1·z = d1
a2·x + b2·y + c2·z = d2
a3·x + b3·y + c3·z = d3
```
Su matriz aumentada es:
```
[ a1  b1  c1 | d1 ]
[ a2  b2  c2 | d2 ]
[ a3  b3  c3 | d3 ]
```

### Operaciones Elementales
1. **Intercambio**: `Ri ↔ Rj` — Intercambiar dos filas entre sí.
2. **Escalamiento**: `Ri ← k · Ri` — Multiplicar una fila por un escalar no nulo.
3. **Sustitución**: `Ri ← Ri + k · Rj` — Sumar a una fila el múltiplo de otra.

### Tipos de Soluciones
- **Solución Única**: La submatriz izquierda se convierte en la identidad `[I|x]`.
- **Sin Solución**: Aparece una fila `[ 0  0  0 | c ]` con `c ≠ 0` (contradicción).
- **Infinitas Soluciones**: Una o más filas de ceros completos `[ 0  0  0 | 0 ]`.

---

## 4. Pseudocódigo

```
INICIO
  LEER matriz_aumentada[3][4]   // 3 filas, 4 columnas (a, b, c | d)

  PARA h = 0 HASTA 2 HACER      // h = índice del pivote

    // Paso 1: Pivoteo parcial
    max_fila = fila con mayor |valor| en columna h, desde fila h hasta 2

    SI matriz[max_fila][h] == 0 ENTONCES
      CONTINUAR  // columna singular, saltar
    FIN SI

    SI max_fila != h ENTONCES
      INTERCAMBIAR filas h y max_fila
      REGISTRAR paso: "R(h+1) ↔ R(max_fila+1)"
    FIN SI

    // Paso 2: Normalizar fila pivote
    pivote = matriz[h][h]
    SI pivote != 1 ENTONCES
      PARA j = 0 HASTA 3 HACER
        matriz[h][j] = matriz[h][j] / pivote
      FIN PARA
      REGISTRAR paso: "R(h+1) ← R(h+1) / pivote"
    FIN SI

    // Paso 3: Eliminación en todas las demás filas
    PARA i = 0 HASTA 2 HACER
      SI i != h ENTONCES
        factor = matriz[i][h]
        SI factor != 0 ENTONCES
          PARA j = 0 HASTA 3 HACER
            matriz[i][j] = matriz[i][j] - factor * matriz[h][j]
          FIN PARA
          REGISTRAR paso: "R(i+1) ← R(i+1) - factor * R(h+1)"
        FIN SI
      FIN SI
    FIN PARA

  FIN PARA

  // Analizar resultado
  PARA cada fila i HACER
    SI todos los coeficientes de i son 0 ENTONCES
      SI termino_independiente[i] != 0 ENTONCES
        RETORNAR "Sin solución"
      SINO
        RETORNAR "Infinitas soluciones"
      FIN SI
    FIN SI
  FIN PARA

  RETORNAR "Solución única", [x = matriz[0][3], y = matriz[1][3], z = matriz[2][3]]
FIN
```

---

## 5. Diagrama de Flujo (ASCII)

```
         ┌─────────────────────────┐
         │         INICIO          │
         └────────────┬────────────┘
                      │
         ┌────────────▼────────────┐
         │  Leer matriz aumentada  │
         │       [3 x 4]           │
         └────────────┬────────────┘
                      │
              h = 0, 1, 2
         ┌────────────▼────────────┐
         │  Buscar fila max en     │
         │  columna h (pivoteo)    │
         └────────────┬────────────┘
                      │
         ┌────────────▼────────────┐
         │  ¿pivote = 0?           │──── SI ──► Continuar con h+1
         └────────────┬────────────┘
                      │ NO
         ┌────────────▼────────────┐
         │  Intercambiar filas     │
         │  si max_fila != h       │
         └────────────┬────────────┘
                      │
         ┌────────────▼────────────┐
         │  Normalizar fila h:     │
         │  Rh ← Rh / pivote       │
         └────────────┬────────────┘
                      │
         ┌────────────▼────────────┐
         │  Eliminar en filas      │
         │  i ≠ h:                 │
         │  Ri ← Ri - factor*Rh   │
         └────────────┬────────────┘
                      │
         ┌────────────▼────────────┐
         │  ¿h < 2?                │──── SI ──► h = h + 1 (volver)
         └────────────┬────────────┘
                      │ NO
         ┌────────────▼────────────┐
         │  Analizar resultado     │
         └────────────┬────────────┘
              ┌───────┴──────────┐
              │                  │
   ┌──────────▼──────┐  ┌───────▼────────────┐
   │ Fila [0,0,0|c≠0]│  │ Identidad formada  │
   │  = Sin solución  │  │ x=m[0][3]          │
   └─────────────────┘  │ y=m[1][3]          │
                        │ z=m[2][3]          │
                        └────────────────────┘
```

---

## 6. Bibliografía

- Chapra, S. C., & Canale, R. P. (2010). *Numerical Methods for Engineers* (6th ed.). McGraw-Hill.
- Burden, R. L., & Faires, J. D. (2010). *Numerical Analysis* (9th ed.). Brooks/Cole.
- Nakamura, S. (1992). *Métodos Numéricos Aplicados con Software*. Prentice-Hall.
