const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  HeadingLevel, AlignmentType, BorderStyle, WidthType, ShadingType,
  PageNumber, Header, Footer, LevelFormat, PageBreak, UnderlineType
} = require("docx");
const fs = require("fs");

// ── Colores ──────────────────────────────────────────────────────────
const AZUL    = "000000";   // negro para titulos
const AZUL_L  = "000000";   // negro para subtitulos
const GRIS_H  = "EEEEEE";
const GRIS_F  = "F5F5F5";
const NEGRO   = "000000";
const BLANCO  = "FFFFFF";

// ── Helpers ────────────────────────────────────────────────────────────
const B  = (border) => ({ style: BorderStyle.SINGLE, size: 1, color: border });
const BORDERS_BLUE = { top: B("888888"), bottom: B("888888"), left: B("888888"), right: B("888888") };
const BORDERS_GRAY = { top: B("AAAAAA"), bottom: B("AAAAAA"), left: B("AAAAAA"), right: B("AAAAAA") };
const CELL_MARGIN  = { top: 100, bottom: 100, left: 140, right: 140 };

const title = (text) => new Paragraph({
  heading: HeadingLevel.HEADING_1,
  pageBreakBefore: true,
  spacing: { before: 0, after: 200 },
  children: [new TextRun({ text, bold: true, color: AZUL, font: "Arial", size: 32 })],
});

const h2 = (text) => new Paragraph({
  heading: HeadingLevel.HEADING_2,
  spacing: { before: 240, after: 120 },
  children: [new TextRun({ text, bold: true, color: AZUL_L, font: "Arial", size: 26 })],
});

const p = (text, opts = {}) => new Paragraph({
  spacing: { after: 160 },
  alignment: opts.center ? AlignmentType.CENTER : AlignmentType.JUSTIFIED,
  children: [new TextRun({ text, font: "Arial", size: 24, ...opts })],
});

const code = (text) => new Paragraph({
  spacing: { after: 0 },
  shading: { fill: "F0F4F8", type: ShadingType.CLEAR },
  indent: { left: 360 },
  children: [new TextRun({ text, font: "Courier New", size: 19, color: "1a1a6e" })],
});

const bullet = (text, bold_prefix = "") => new Paragraph({
  numbering: { reference: "bullets", level: 0 },
  spacing: { after: 80 },
  children: [
    ...(bold_prefix ? [new TextRun({ text: bold_prefix + " ", bold: true, font: "Arial", size: 24 })] : []),
    new TextRun({ text, font: "Arial", size: 24 }),
  ],
});

const numbered = (text) => new Paragraph({
  numbering: { reference: "numbers", level: 0 },
  spacing: { after: 80 },
  children: [new TextRun({ text, font: "Arial", size: 24 })],
});

const divider = () => new Paragraph({
  spacing: { after: 100 },
  border: { bottom: { style: BorderStyle.SINGLE, size: 4, color: AZUL_L, space: 1 } },
  children: [],
});

// Celda de tabla header
const thCell = (text, w) => new TableCell({
  width: { size: w, type: WidthType.DXA },
  shading: { fill: "DDDDDD", type: ShadingType.CLEAR },
  borders: BORDERS_GRAY,
  margins: CELL_MARGIN,
  children: [new Paragraph({ alignment: AlignmentType.CENTER,
    children: [new TextRun({ text, bold: true, color: NEGRO, font: "Arial", size: 22 })] }) ],
});

// Celda de tabla normal
const tdCell = (text, w, shade = BLANCO) => new TableCell({
  width: { size: w, type: WidthType.DXA },
  shading: { fill: shade, type: ShadingType.CLEAR },
  borders: BORDERS_GRAY,
  margins: CELL_MARGIN,
  children: [new Paragraph({ children: [new TextRun({ text, font: "Arial", size: 22 })] }) ],
});

// ── Portada ─────────────────────────────────────────────────────────────
const coverPage = [
  new Paragraph({ spacing: { before: 1440 }, children: [] }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { after: 200 },
    children: [new TextRun({ text: "UNIVERSIDAD FRANCISCO DE PAULA SANTANDER OCANA", bold: true, color: NEGRO, font: "Arial", size: 26 })],
  }),
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 80 },
    children: [new TextRun({ text: "Facultad de Ingenierias - Ingenieria de Sistemas", font: "Arial", size: 24, color: "444444" })] }),
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 400 },
    children: [new TextRun({ text: "Analisis Numerico", font: "Arial", size: 24, color: "444444" })] }),
  divider(),
  new Paragraph({ spacing: { before: 400, after: 160 }, alignment: AlignmentType.CENTER,
    children: [new TextRun({ text: "GAUSS-JORDAN MASTER PRO", bold: true, font: "Arial", size: 48, color: AZUL })] }),
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 400 },
    children: [new TextRun({ text: "Software para la resolucion de sistemas de ecuaciones lineales 3x3", font: "Arial", size: 28, italics: true, color: AZUL_L })] }),
  divider(),
  new Paragraph({ spacing: { before: 480, after: 120 }, alignment: AlignmentType.CENTER,
    children: [new TextRun({ text: "Docente:", bold: true, font: "Arial", size: 24 })] }),
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 240 },
    children: [new TextRun({ text: "Ing. Nombre del Profesor", font: "Arial", size: 24 })] }),
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 120 },
    children: [new TextRun({ text: "Estudiante(s):", bold: true, font: "Arial", size: 24 })] }),
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 80 },
    children: [new TextRun({ text: "Nombre del Estudiante", font: "Arial", size: 24 })] }),
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 480 },
    children: [new TextRun({ text: "Ocana, Norte de Santander - 2026", font: "Arial", size: 24 })] }),
  new Paragraph({ children: [new PageBreak()] }),
];

// ── 1. Objetivo ──────────────────────────────────────────────────────────
const secObjetivo = [
  title("1. Objetivo"),
  h2("Objetivo General"),
  p("Crear un programa en Python con interfaz grafica que resuelva sistemas de ecuaciones lineales de 3x3 usando el metodo de Gauss-Jordan, mostrando cada paso del proceso y una grafica 3D de los planos que representa el sistema."),
  h2("Objetivos Especificos"),
  bullet("Programar el metodo de Gauss-Jordan con pivoteo parcial en Python, usando fracciones exactas para evitar errores de redondeo."),
  bullet("Hacer una interfaz grafica con PySide6 donde el usuario pueda escribir las ecuaciones o los coeficientes directamente en la matriz."),
  bullet("Mostrar cada operacion que se le hace a la matriz, paso a paso, con colores que ayuden a entender el proceso."),
  bullet("Agregar una grafica 3D con matplotlib que muestre los tres planos del sistema y el punto donde se intersectan."),
  bullet("Detectar cuando el sistema no tiene solucion o tiene infinitas soluciones y avisar al usuario con un mensaje claro."),
];

// ── 2. Justificacion ─────────────────────────────────────────────────────
const secJustificacion = [
  title("2. Justificacion"),
  p("En la asignatura de Analisis Numerico se estudian distintos metodos para resolver problemas matematicos de forma computacional. Uno de esos temas son los sistemas de ecuaciones lineales, que aparecen en muchas areas de la ingenieria como circuitos, estructuras y redes."),
  p("El metodo de Gauss-Jordan es uno de los mas conocidos para resolver estos sistemas, pero a veces cuesta entenderlo solo viendo la teoria. Por eso se decidio hacer un programa que muestre como funciona por dentro, paso a paso, para que cualquier estudiante pueda seguirlo sin perderse."),
  p("Ademas, resolver estos sistemas a mano con numeros grandes o fracciones puede generar errores facilmente. Con este programa el calculo es exacto porque se usan fracciones reales en lugar de decimales con redondeo. La grafica 3D que se agrego tambien ayuda a entender geometricamente que significa la solucion: el punto donde se cruzan los tres planos."),
];

// ── 3. Marco Teorico ─────────────────────────────────────────────────────
const secMarco = [
  title("3. Marco Teorico"),
  h2("3.1 Sistemas de Ecuaciones Lineales"),
  p("Un sistema de m ecuaciones lineales con n incognitas es un conjunto de ecuaciones de la forma:"),
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 120 },
    shading: { fill: GRIS_F, type: ShadingType.CLEAR },
    children: [new TextRun({ text: "a1x + b1y + c1z = d1  |  a2x + b2y + c2z = d2  |  a3x + b3y + c3z = d3",
      font: "Courier New", size: 22, bold: true })] }),
  p("La representacion matricial de este sistema es la matriz aumentada [A|b]:"),

  h2("3.2 Metodo de Gauss-Jordan"),
  p("El metodo de Gauss-Jordan es una extension del metodo de eliminacion gaussiana. Su objetivo es transformar la matriz aumentada del sistema en la forma escalonada reducida por filas (RREF), aplicando operaciones elementales de fila:"),
  bullet("Intercambio de dos filas: Ri <-> Rj"),
  bullet("Multiplicacion de una fila por un escalar no nulo: Ri <- k * Ri"),
  bullet("Sustitucion: sumar a una fila el multiplo de otra: Ri <- Ri + k * Rj"),

  h2("3.3 Pivoteo Parcial"),
  p("Para mejorar la estabilidad numerica del algoritmo, se utiliza pivoteo parcial: en cada paso se selecciona como pivote el elemento de mayor valor absoluto en la columna actual (desde la fila del pivote hasta la ultima fila), intercambiando filas si es necesario. Esto reduce los errores de redondeo en implementaciones con punto flotante."),

  h2("3.4 Tipos de Solucion"),
  new Table({
    width: { size: 9360, type: WidthType.DXA },
    columnWidths: [3120, 3120, 3120],
    rows: [
      new TableRow({ children: [thCell("Tipo", 3120), thCell("Condicion", 3120), thCell("Resultado", 3120)] }),
      new TableRow({ children: [tdCell("Solucion unica", 3120, GRIS_F), tdCell("La submatriz A se convierte en la identidad", 3120), tdCell("x, y, z determinados", 3120, GRIS_F)] }),
      new TableRow({ children: [tdCell("Sin solucion", 3120, GRIS_F), tdCell("Aparece fila [0 0 0 | c] con c != 0", 3120), tdCell("Sistema inconsistente", 3120, GRIS_F)] }),
      new TableRow({ children: [tdCell("Infinitas soluciones", 3120, GRIS_F), tdCell("Fila de ceros completa [0 0 0 | 0]", 3120), tdCell("Sistema indeterminado", 3120, GRIS_F)] }),
    ],
  }),
  new Paragraph({ spacing: { after: 160 }, children: [] }),

  h2("3.5 Interpretacion Geometrica"),
  p("Cada ecuacion lineal de 3 variables representa un plano en el espacio R3. La solucion del sistema corresponde a la interseccion de los tres planos. Segun el tipo de solucion: tres planos se intersectan en un punto (solucion unica), dos planos son paralelos (sin solucion), o los tres planos se intersectan en una recta o coinciden (infinitas soluciones)."),
];

// ── 4. Datos de Entrada y Salida ────────────────────────────────────────
const secDatos = [
  title("4. Definicion del Metodo: Entradas y Salidas"),
  h2("4.1 Datos de Entrada"),
  p("La aplicacion acepta un sistema de 3 ecuaciones lineales con 3 incognitas (x, y, z). El usuario puede ingresar los datos mediante dos modalidades:"),
  new Table({
    width: { size: 9360, type: WidthType.DXA },
    columnWidths: [2340, 3510, 3510],
    rows: [
      new TableRow({ children: [thCell("Modalidad", 2340), thCell("Descripcion", 3510), thCell("Ejemplo", 3510)] }),
      new TableRow({ children: [tdCell("Texto libre", 2340, GRIS_F), tdCell("Ecuacion escrita en lenguaje natural", 3510), tdCell("2x + y - z = 8", 3510, GRIS_F)] }),
      new TableRow({ children: [tdCell("Fraccion parentesis", 2340, GRIS_F), tdCell("Coeficiente fraccionario", 3510), tdCell("(1/2)x + y - z = 1", 3510, GRIS_F)] }),
      new TableRow({ children: [tdCell("Decimal", 2340, GRIS_F), tdCell("Coeficiente decimal", 3510), tdCell("0.5x - y + z = 3", 3510, GRIS_F)] }),
      new TableRow({ children: [tdCell("Matriz directa", 2340, GRIS_F), tdCell("Coeficientes en la cuadricula [A|b]", 3510), tdCell("Celdas de la interfaz grafica", 3510, GRIS_F)] }),
    ],
  }),
  new Paragraph({ spacing: { after: 160 }, children: [] }),
  h2("4.2 Datos de Salida"),
  bullet("Tipo de solucion del sistema: unica, sin solucion, o infinitas soluciones."),
  bullet("Valores de las incognitas x, y, z (si hay solucion unica), en formato fraccion exacta o decimal de 4 cifras."),
  bullet("Procedimiento completo: cada operacion elemental aplicada a la matriz con su descripcion textual."),
  bullet("Visualizacion 3D: los tres planos del sistema y el punto de interseccion (solucion unica)."),
];

// ── 5. Metodologia ──────────────────────────────────────────────────────
const secMetodologia = [
  title("5. Metodologia"),
  h2("5.1 Fases de Desarrollo"),
  numbered("Contextualizacion: estudio del metodo de Gauss-Jordan, operaciones elementales de fila y tipos de solucion de sistemas lineales."),
  numbered("Requerimientos: definicion de entradas (ecuaciones en texto libre y matriz directa), salidas (pasos, resultado y grafica 3D) y restricciones (precision exacta con fracciones)."),
  numbered("Analisis: identificacion de los modulos del sistema: parser de ecuaciones, motor de calculo, visualizador de pasos y grafica 3D."),
  numbered("Diseno: elaboracion del diagrama de flujo, pseudocodigo del algoritmo y arquitectura de modulos."),
  numbered("Implementacion: desarrollo en Python 3.13 con PySide6 (GUI), fractions.Fraction (precision), matplotlib (graficas 3D) y QtAwesome (iconos)."),
  numbered("Prueba: verificacion con sistemas de solucion unica, sin solucion, infinitas soluciones, coeficientes fraccionarios y entradas invalidas."),

  h2("5.2 Arquitectura del Software"),
  new Table({
    width: { size: 9360, type: WidthType.DXA },
    columnWidths: [2340, 2340, 4680],
    rows: [
      new TableRow({ children: [thCell("Modulo", 2340), thCell("Archivo", 2340), thCell("Funcion", 4680)] }),
      new TableRow({ children: [tdCell("Motor de calculo", 2340, GRIS_F), tdCell("logic/solver.py", 2340), tdCell("Implementa el algoritmo Gauss-Jordan con pivoteo parcial", 4680, GRIS_F)] }),
      new TableRow({ children: [tdCell("Parser", 2340, GRIS_F), tdCell("logic/parser.py", 2340), tdCell("Interpreta ecuaciones en texto libre a coeficientes Fraction", 4680, GRIS_F)] }),
      new TableRow({ children: [tdCell("Calculadora", 2340, GRIS_F), tdCell("logic/calculator.py", 2340), tdCell("Evaluador seguro de expresiones y conversor de fracciones", 4680, GRIS_F)] }),
      new TableRow({ children: [tdCell("Ventana principal", 2340, GRIS_F), tdCell("ui/main_window.py", 2340), tdCell("Orquesta la interfaz grafica y la logica de negocio", 4680, GRIS_F)] }),
      new TableRow({ children: [tdCell("Visor de pasos", 2340, GRIS_F), tdCell("ui/widgets/step_viewer.py", 2340), tdCell("Muestra cada operacion elemental con colores", 4680, GRIS_F)] }),
      new TableRow({ children: [tdCell("Grafica 3D", 2340, GRIS_F), tdCell("ui/widgets/graph_3d.py", 2340), tdCell("Renderiza los 3 planos y el punto de solucion en hilo separado", 4680, GRIS_F)] }),
    ],
  }),
  new Paragraph({ spacing: { after: 160 }, children: [] }),
];

// ── 6. Diagrama de Flujo ─────────────────────────────────────────────────
const secFlujo = [
  title("6. Diagrama de Flujo del Algoritmo"),
  p("El siguiente diagrama representa el flujo del algoritmo de Gauss-Jordan implementado en el modulo logic/solver.py:"),
  new Paragraph({ spacing: { after: 80 }, shading: { fill: "F0F4F8", type: ShadingType.CLEAR },
    children: [] }),
  ...[
    "         +---------------------------+",
    "         |          INICIO           |",
    "         +-------------+-------------+",
    "                       |",
    "         +-------------v-------------+",
    "         |  Leer matriz aumentada    |",
    "         |  [3 x 4] con Fraction     |",
    "         +-------------+-------------+",
    "                       |",
    "              h = 0, 1, 2 (bucle)",
    "         +-------------v-------------+",
    "         |  Buscar fila de max |val|  |",
    "         |  en columna h (pivoteo)   |",
    "         +-------------+-------------+",
    "                       |",
    "         +-------------v-------------+",
    "         |    pivote en col h = 0?   |--SI--> siguiente h",
    "         +-------------+-------------+",
    "                       | NO",
    "         +-------------v-------------+",
    "         |  Intercambiar filas si    |",
    "         |  max_fila != h            |",
    "         +-------------+-------------+",
    "                       |",
    "         +-------------v-------------+",
    "         |  Normalizar fila h:       |",
    "         |  Rh <- Rh / pivote        |",
    "         +-------------+-------------+",
    "                       |",
    "         +-------------v-------------+",
    "         |  Eliminar columna h en    |",
    "         |  filas i != h:            |",
    "         |  Ri <- Ri - factor * Rh   |",
    "         +-------------+-------------+",
    "                       |",
    "         +-------------v-------------+",
    "         |  h < 2? --SI--> volver    |",
    "         +-------------+-------------+",
    "                       | NO",
    "         +-------------v-------------+",
    "         |     Analizar resultado    |",
    "         +------+----------+---------+",
    "                |          |",
    "    Fila [0,0,0|c!=0]   Identidad",
    "    Sin solucion        Solucion unica",
    "                        x,y,z = col.4",
  ].map(line => code(line)),
  new Paragraph({ spacing: { after: 160 }, children: [] }),
];

// ── 7. Pseudocodigo ─────────────────────────────────────────────────────
const secPseudo = [
  title("7. Pseudocodigo"),
  ...[
    "INICIO",
    "  LEER matriz_aumentada[3][4]   // coeficientes como Fraction",
    "",
    "  PARA h = 0 HASTA 2 HACER     // h = indice del pivote",
    "",
    "    // Paso 1: Pivoteo parcial",
    "    max_fila = fila con mayor |valor| en columna h (desde fila h)",
    "",
    "    SI matriz[max_fila][h] == 0 ENTONCES",
    "      CONTINUAR  // columna singular",
    "    FIN SI",
    "",
    "    SI max_fila != h ENTONCES",
    "      INTERCAMBIAR filas h y max_fila",
    "      REGISTRAR paso de intercambio",
    "    FIN SI",
    "",
    "    // Paso 2: Normalizar la fila pivote",
    "    pivote = matriz[h][h]",
    "    SI pivote != 1 ENTONCES",
    "      PARA j = 0 HASTA 3:",
    "        matriz[h][j] = matriz[h][j] / pivote",
    "      REGISTRAR paso de normalizacion",
    "    FIN SI",
    "",
    "    // Paso 3: Eliminar en todas las demas filas",
    "    PARA i = 0 HASTA 2 HACER",
    "      SI i != h ENTONCES",
    "        factor = matriz[i][h]",
    "        SI factor != 0 ENTONCES",
    "          PARA j = 0 HASTA 3:",
    "            matriz[i][j] = matriz[i][j] - factor * matriz[h][j]",
    "          REGISTRAR paso de eliminacion",
    "        FIN SI",
    "      FIN SI",
    "    FIN PARA",
    "",
    "  FIN PARA",
    "",
    "  // Analizar resultado",
    "  PARA cada fila i HACER",
    "    SI todos coeficientes de i son 0 ENTONCES",
    "      SI termino_independiente[i] != 0 ENTONCES",
    "        RETORNAR 'Sin solucion'",
    "      SINO",
    "        RETORNAR 'Infinitas soluciones'",
    "      FIN SI",
    "    FIN SI",
    "  FIN PARA",
    "",
    "  RETORNAR 'Solucion unica', [x=m[0][3], y=m[1][3], z=m[2][3]]",
    "FIN",
  ].map(line => code(line)),
  new Paragraph({ spacing: { after: 160 }, children: [] }),
];

// ── 8. Codigo Fuente ─────────────────────────────────────────────────────
const codeLines = (lines) => lines.map(l => code(l));

const secCodigo = [
  title("8. Codigo Fuente en Python"),
  h2("8.1 logic/solver.py — Motor de Gauss-Jordan"),
  ...codeLines([
    "from fractions import Fraction",
    "import copy",
    "",
    "class GaussJordanSolver:",
    "    def __init__(self, matrix):",
    "        self.matrix = copy.deepcopy(matrix)",
    "        self.steps = []",
    "        self._record_step('Inicio', 'Matriz aumentada [A|b] construida.')",
    "",
    "    def solve(self):",
    "        rows = cols = 3",
    "        for h in range(rows):                          # h = columna pivote",
    "            max_row = max(range(h, rows),",
    "                         key=lambda i: abs(self.matrix[i][h]))",
    "            if self.matrix[max_row][h] == 0:",
    "                continue                               # columna singular",
    "            if max_row != h:",
    "                self.matrix[h], self.matrix[max_row] = \\",
    "                    self.matrix[max_row], self.matrix[h]",
    "                self._record_step(f'R{h+1} <-> R{max_row+1}', ...)",
    "            pivot = self.matrix[h][h]",
    "            if pivot != 1:",
    "                self.matrix[h] = [x / pivot for x in self.matrix[h]]",
    "                self._record_step(f'R{h+1} <- R{h+1} / {pivot}', ...)",
    "            for i in range(rows):",
    "                if i != h:",
    "                    factor = self.matrix[i][h]",
    "                    if factor != 0:",
    "                        self.matrix[i] = [",
    "                            self.matrix[i][j] - factor * self.matrix[h][j]",
    "                            for j in range(cols + 1)]",
    "                        self._record_step(f'R{i+1} <- R{i+1} - ({factor})*R{h+1}', ...)",
    "        return self._analyze_result()",
  ]),
  new Paragraph({ spacing: { after: 160 }, children: [] }),

  h2("8.2 logic/parser.py — Interprete de Ecuaciones"),
  ...codeLines([
    "import re",
    "from fractions import Fraction",
    "",
    "def parse_equation(eq_str):",
    "    # Normalizar: quitar espacios, minusculas, quitar parentesis en (1/2)",
    "    s = re.sub(r'\\(([+-]?[\\d\\.]+(?:/[\\d\\.]+)?)\\)', r'\\1',",
    "               ''.join(eq_str.lower().split()))",
    "    left, right = s.split('=', 1)",
    "    rhs = Fraction(right)",
    "    coeffs = {'x': Fraction(0), 'y': Fraction(0), 'z': Fraction(0)}",
    "",
    "    # Patron: signo + numero + variable | variable sola",
    "    pattern = re.compile(",
    "        r'([+-]?)(?:([\\d]+(?:\\.[\\d]+)?(?:/[\\d]+)?)([xyz]?)|([xyz]))'",
    "    )",
    "    pos = 0",
    "    while pos < len(left):",
    "        m = pattern.match(left, pos)",
    "        val = Fraction(m.group(2)) if m.group(2) else Fraction(1)",
    "        var = m.group(3) or m.group(4)",
    "        if m.group(1) == '-': val = -val",
    "        if var: coeffs[var] += val",
    "        else:   rhs -= val",
    "        pos += len(m.group(0))",
    "    return [coeffs['x'], coeffs['y'], coeffs['z'], rhs]",
  ]),
  new Paragraph({ spacing: { after: 160 }, children: [] }),
];

// ── 9. Resultados ────────────────────────────────────────────────────────
const secResultados = [
  title("9. Resultados"),
  h2("9.1 Casos de Prueba"),
  new Table({
    width: { size: 9360, type: WidthType.DXA },
    columnWidths: [3240, 2700, 3420],
    rows: [
      new TableRow({ children: [thCell("Sistema", 3240), thCell("Tipo", 2700), thCell("Resultado", 3420)] }),
      new TableRow({ children: [
        tdCell("2x+y-z=8, -3x-y+2z=-11, -2x+y+2z=-3", 3240, GRIS_F),
        tdCell("Solucion unica", 2700),
        tdCell("x=2, y=3, z=-1", 3420, GRIS_F),
      ]}),
      new TableRow({ children: [
        tdCell("x-2y+3z=9, -x+3y=-4, 2x-5y+5z=17", 3240, GRIS_F),
        tdCell("Solucion unica", 2700),
        tdCell("x=1, y=-1, z=2", 3420, GRIS_F),
      ]}),
      new TableRow({ children: [
        tdCell("x+y+z=6, 2x+2y+2z=14, 3x+3y+3z=20", 3240, GRIS_F),
        tdCell("Sin solucion", 2700),
        tdCell("Sistema inconsistente", 3420, GRIS_F),
      ]}),
      new TableRow({ children: [
        tdCell("x+2y+3z=6, 2x+4y+6z=12, 3x+6y+9z=18", 3240, GRIS_F),
        tdCell("Infinitas soluciones", 2700),
        tdCell("Sistema indeterminado", 3420, GRIS_F),
      ]}),
      new TableRow({ children: [
        tdCell("(1/2)x+y-z=1, -3x-y+2z=-11, -2x+y+2z=-3", 3240, GRIS_F),
        tdCell("Solucion unica", 2700),
        tdCell("Fracciones exactas", 3420, GRIS_F),
      ]}),
    ],
  }),
  new Paragraph({ spacing: { after: 200 }, children: [] }),
  h2("9.2 Funcionalidades Verificadas"),
  bullet("Interfaz grafica funcional con PySide6 (1200x860 px)."),
  bullet("Parser acepta: enteros, decimales, fracciones, parentesis, coeficientes implicitos."),
  bullet("Validacion de celdas vacias, valores invalidos y filas de ceros."),
  bullet("Visor de pasos con codigo de colores (verde=pivote, rojo=objetivo, amarillo=intercambio)."),
  bullet("Grafica 3D renderizada en hilo separado (QThread) para evitar bloqueo de la UI."),
  bullet("Banner de resultado con color segun tipo de solucion."),
  bullet("Modo fracciones exactas y modo decimal con 4 cifras significativas."),
];

// ── 10. Conclusiones ──────────────────────────────────────────────────────
const secConclusiones = [
  title("10. Conclusiones"),
  bullet("Al hacer este programa se entendio mejor como funciona el metodo de Gauss-Jordan por dentro. No es lo mismo leerlo en un libro que tener que programarlo, porque hay que pensar en cada caso posible como el pivote cero o las filas dependientes."),
  bullet("Usar fracciones exactas en vez de decimales fue una decision importante. Con decimales hay errores de redondeo que hacen que el resultado no sea correcto, y con fracciones el programa siempre da el valor exacto."),
  bullet("La parte de mostrar los pasos con colores fue lo que mas ayuda a entender el metodo. Se puede ver claramente cual es la fila pivote, cual se esta modificando y que operacion se aplico en cada momento."),
  bullet("Hacer la grafica 3D fue un reto porque matplotlib puede volverse lento dentro de una ventana. Se soluciono ejecutando el render en un hilo aparte para que la interfaz no se congele mientras dibuja."),
  bullet("El parser de ecuaciones quedo bastante flexible. Acepta formatos como (1/2)x, 0.5x, -x o 2*x sin que el usuario tenga que preocuparse por el formato exacto."),
  bullet("En general el proyecto cubrio todo el proceso de desarrollo: desde entender el metodo hasta tenerlo corriendo sin errores, lo que fue muy util para aplicar lo visto en la materia de una forma practica."),
];

// ── 11. Bibliografia ──────────────────────────────────────────────────────
const secBiblio = [
  title("11. Bibliografia"),
  p("Chapra, S. C., & Canale, R. P. (2010). Numerical Methods for Engineers (6th ed.). McGraw-Hill Education."),
  p("Burden, R. L., & Faires, J. D. (2010). Numerical Analysis (9th ed.). Brooks/Cole Cengage Learning."),
  p("Nakamura, S. (1992). Metodos Numericos Aplicados con Software. Prentice-Hall Hispanoamericana."),
  p("Python Software Foundation. (2024). fractions - Rational numbers. Python 3.13 Documentation. https://docs.python.org/3/library/fractions.html"),
  p("The Qt Company. (2024). PySide6 Documentation. https://doc.qt.io/qtforpython-6/"),
  p("Hunter, J. D. (2007). Matplotlib: A 2D Graphics Environment. Computing in Science & Engineering, 9(3), 90-95."),
];

// ── Ensamblar documento ──────────────────────────────────────────────────
const doc = new Document({
  numbering: {
    config: [
      { reference: "bullets",
        levels: [{ level: 0, format: LevelFormat.BULLET, text: "\u2022",
          alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 720, hanging: 360 } } } }] },
      { reference: "numbers",
        levels: [{ level: 0, format: LevelFormat.DECIMAL, text: "%1.",
          alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 720, hanging: 360 } } } }] },
    ],
  },
  styles: {
    default: {
      document: { run: { font: "Arial", size: 24 } },
    },
    paragraphStyles: [
      { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 32, bold: true, font: "Arial", color: AZUL },
        paragraph: { spacing: { before: 200, after: 200 }, outlineLevel: 0 } },
      { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 26, bold: true, font: "Arial", color: AZUL_L },
        paragraph: { spacing: { before: 180, after: 100 }, outlineLevel: 1 } },
    ],
  },
  sections: [{
    properties: {
      page: {
        size: { width: 12240, height: 15840 },
        margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 },
      },
    },
    headers: {
      default: new Header({ children: [
        new Paragraph({
          border: { bottom: { style: BorderStyle.SINGLE, size: 4, color: "888888", space: 1 } },
          children: [
            new TextRun({ text: "Gauss-Jordan Master Pro  |  Analisis Numerico", font: "Arial", size: 18, color: "888888" }),
            new TextRun({ text: "\t", font: "Arial", size: 18 }),
            new TextRun({ children: ["Pag. ", PageNumber.CURRENT], font: "Arial", size: 18, color: "888888" }),
          ],
          tabStops: [{ type: "right", position: 9360 }],
        }),
      ]}),
    },
    children: [
      ...coverPage,
      ...secObjetivo,
      ...secJustificacion,
      ...secMarco,
      ...secDatos,
      ...secMetodologia,
      ...secFlujo,
      ...secPseudo,
      ...secCodigo,
      ...secResultados,
      ...secConclusiones,
      ...secBiblio,
    ],
  }],
});

Packer.toBuffer(doc).then(buf => {
  fs.writeFileSync("Informe_GJ_v2.docx", buf);
  console.log("OK: Informe_GJ_v2.docx generado");
}).catch(e => { console.error("ERROR:", e.message); process.exit(1); });
