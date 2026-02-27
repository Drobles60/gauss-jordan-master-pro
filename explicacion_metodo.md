# Explicación del Método de Gauss-Jordan

El método de **Gauss-Jordan** es un algoritmo del álgebra lineal para determinar las soluciones de un sistema de ecuaciones lineales y para encontrar matrices inversas.

## Resumen Teórico
Consiste en aplicar una serie de **operaciones elementales de fila** a la matriz aumentada del sistema hasta transformarla en una **matriz escalonada reducida por filas** (la identidad en el mejor de los casos).

### Matriz Aumentada
Dado un sistema 3x3:
```
a1x + b1y + c1z = d1
a2x + b2y + c2z = d2
a3x + b3y + c3z = d3
```
Su matriz aumentada es:
```
[ a1  b1  c1 | d1 ]
[ a2  b2  c2 | d2 ]
[ a3  b3  c3 | d3 ]
```

## Operaciones Elementales
Existen tres tipos de operaciones permitidas que no alteran el conjunto de soluciones:
1. **Intercambio**: Intercambiar dos filas entre sí ($R_i \leftrightarrow R_j$).
2. **Escalamiento**: Multiplicar una fila por un escalar no nulo ($R_i \leftarrow k \cdot R_i$).
3. **Sustitución**: Sumar a una fila el múltiplo de otra ($R_i \leftarrow R_i + k \cdot R_j$).

## Tipos de Soluciones
Tras el proceso, podemos encontrarnos con:
- **Solución Única**: La matriz izquierda se convierte en la identidad.
- **Sin Solución**: Aparece una fila del tipo `[ 0  0  0 | c ]` donde $c \neq 0$.
- **Infinitas Soluciones**: Hay una o más filas de ceros completos `[ 0  0  0 | 0 ]` y no hay contradicciones.
