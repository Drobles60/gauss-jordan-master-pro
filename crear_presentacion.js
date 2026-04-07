const pptxgen = require("pptxgenjs");
const pres = new pptxgen();
pres.layout = "LAYOUT_16x9";
pres.title = "Gauss-Jordan Master Pro";

// ── Paleta de colores (basada en la plantilla) ──────────────────────────
const C = {
  negro:    "000000",
  blanco:   "FFFFFF",
  gris_bg:  "F5F5F5",
  gris_med: "DDDDDD",
  gris_osc: "444444",
  acento:   "1A1A2E",   // azul oscuro casi negro
  acento2:  "2E4057",
  verde:    "2C7A4B",
  rojo:     "B71C1C",
};

const FONT_TITULO = "Montserrat";
const FONT_CUERPO = "Open Sans";

// ── Helpers ──────────────────────────────────────────────────────────────
function barraLateral(slide) {
  slide.addShape(pres.ShapeType.rect, {
    x: 0, y: 0, w: 0.12, h: 5.625,
    fill: { color: C.acento },
    line: { color: C.acento },
  });
}

function barraInferior(slide, texto) {
  slide.addShape(pres.ShapeType.rect, {
    x: 0, y: 5.2, w: 10, h: 0.425,
    fill: { color: C.acento },
    line: { color: C.acento },
  });
  slide.addText(texto, {
    x: 0.3, y: 5.2, w: 9.4, h: 0.425,
    fontSize: 11, color: C.blanco,
    fontFace: FONT_CUERPO, valign: "middle",
  });
}

function tituloSlide(slide, texto) {
  slide.addText(texto, {
    x: 0.3, y: 0.18, w: 9.4, h: 0.7,
    fontSize: 28, bold: true,
    fontFace: FONT_TITULO, color: C.acento,
    valign: "middle", margin: 0,
  });
  slide.addShape(pres.ShapeType.rect, {
    x: 0.3, y: 0.88, w: 9.4, h: 0.04,
    fill: { color: C.gris_med }, line: { color: C.gris_med },
  });
}

function tarjeta(slide, x, y, w, h, titulo, cuerpo, colorTitulo) {
  slide.addShape(pres.ShapeType.rect, {
    x, y, w, h,
    fill: { color: C.gris_bg },
    line: { color: C.gris_med, pt: 1 },
  });
  slide.addText(titulo, {
    x: x + 0.15, y: y + 0.1, w: w - 0.3, h: 0.4,
    fontSize: 14, bold: true,
    fontFace: FONT_TITULO, color: colorTitulo || C.acento,
    margin: 0,
  });
  slide.addText(cuerpo, {
    x: x + 0.15, y: y + 0.5, w: w - 0.3, h: h - 0.6,
    fontSize: 12, fontFace: FONT_CUERPO, color: C.gris_osc,
    valign: "top", wrap: true, margin: 0,
  });
}

// ════════════════════════════════════════════════════════════
// DIAPOSITIVA 1 — PORTADA
// ════════════════════════════════════════════════════════════
{
  const s = pres.addSlide();
  // Fondo dividido
  s.addShape(pres.ShapeType.rect, { x:0, y:0, w:10, h:5.625, fill:{ color: C.acento }, line:{ color: C.acento } });
  s.addShape(pres.ShapeType.rect, { x:5.2, y:0, w:4.8, h:5.625, fill:{ color: C.blanco }, line:{ color: C.blanco } });

  // Linea vertical decorativa
  s.addShape(pres.ShapeType.rect, { x:5.1, y:0.4, w:0.06, h:4.8, fill:{ color: C.gris_med }, line:{ color: C.gris_med } });

  // Texto izquierdo (blanco sobre oscuro)
  s.addText("GAUSS-JORDAN\nMASTER PRO", {
    x: 0.4, y: 0.8, w: 4.5, h: 2.2,
    fontSize: 38, bold: true, fontFace: FONT_TITULO,
    color: C.blanco, valign: "middle",
  });
  s.addText("Resolucion de sistemas de ecuaciones\nlineales 3x3 paso a paso", {
    x: 0.4, y: 3.0, w: 4.5, h: 0.9,
    fontSize: 14, fontFace: FONT_CUERPO,
    color: "AAAACC", valign: "top",
  });
  s.addText("Analisis Numerico", {
    x: 0.4, y: 3.95, w: 4.5, h: 0.4,
    fontSize: 13, fontFace: FONT_CUERPO,
    color: "888888", bold: true,
  });

  // Texto derecho (negro sobre blanco)
  s.addText("Universidad Francisco de Paula\nSantander Ocana", {
    x: 5.4, y: 0.6, w: 4.3, h: 0.9,
    fontSize: 13, fontFace: FONT_CUERPO,
    color: C.gris_osc, valign: "top",
  });
  s.addText("Ingenieria de Sistemas", {
    x: 5.4, y: 1.55, w: 4.3, h: 0.4,
    fontSize: 12, fontFace: FONT_CUERPO, color: C.gris_osc,
  });
  s.addShape(pres.ShapeType.rect, { x:5.4, y:2.05, w:4.0, h:0.04, fill:{color:C.gris_med}, line:{color:C.gris_med} });
  s.addText("Estudiante:", {
    x: 5.4, y: 2.2, w: 4.3, h: 0.35,
    fontSize: 11, fontFace: FONT_CUERPO, color: "888888", bold: true,
  });
  s.addText("Maicol Robles\nCodigo: 192125", {
    x: 5.4, y: 2.55, w: 4.3, h: 0.7,
    fontSize: 13, fontFace: FONT_CUERPO, color: C.negro, bold: true,
  });
  s.addText("Docente:", {
    x: 5.4, y: 3.35, w: 4.3, h: 0.35,
    fontSize: 11, fontFace: FONT_CUERPO, color: "888888", bold: true,
  });
  s.addText("Ing. ______________________", {
    x: 5.4, y: 3.7, w: 4.3, h: 0.4,
    fontSize: 13, fontFace: FONT_CUERPO, color: C.negro,
  });
  s.addText("Ocana, 2026", {
    x: 5.4, y: 4.9, w: 4.3, h: 0.4,
    fontSize: 11, fontFace: FONT_CUERPO, color: "888888",
  });
}

// ════════════════════════════════════════════════════════════
// DIAPOSITIVA 2 — QUE ES EL METODO
// ════════════════════════════════════════════════════════════
{
  const s = pres.addSlide();
  barraLateral(s);
  tituloSlide(s, "¿Que es el Metodo de Gauss-Jordan?");
  barraInferior(s, "Analisis Numerico  |  Gauss-Jordan Master Pro");

  s.addText(
    "Es un algoritmo del algebra lineal que resuelve sistemas de ecuaciones lineales " +
    "transformando la matriz aumentada del sistema en su forma escalonada reducida por filas (RREF).",
    { x:0.3, y:1.05, w:9.4, h:0.75, fontSize:14, fontFace:FONT_CUERPO, color:C.gris_osc, wrap:true }
  );

  // 3 columnas
  const cols = [
    { x:0.3, titulo:"Matriz Aumentada", icono:"[A|b]", texto:"Se representa el sistema ax+by+cz=d como una matriz de 3 filas y 4 columnas con los coeficientes y terminos independientes." },
    { x:3.55, titulo:"Operaciones Elementales", icono:"Ri <-> Rj", texto:"Intercambio de filas, multiplicar una fila por escalar no nulo, y sumar el multiplo de una fila a otra." },
    { x:6.8, titulo:"Resultado Final", icono:"RREF", texto:"Si la submatriz izquierda se convierte en la identidad, los valores de x, y, z quedan en la ultima columna." },
  ];
  cols.forEach(c => {
    s.addShape(pres.ShapeType.rect, { x:c.x, y:1.9, w:3.0, h:2.9, fill:{color:C.gris_bg}, line:{color:C.gris_med, pt:1} });
    s.addText(c.icono, { x:c.x, y:2.0, w:3.0, h:0.5, fontSize:20, bold:true, fontFace:FONT_TITULO, color:C.acento, align:"center" });
    s.addText(c.titulo, { x:c.x+0.1, y:2.55, w:2.8, h:0.45, fontSize:13, bold:true, fontFace:FONT_TITULO, color:C.negro });
    s.addText(c.texto, { x:c.x+0.1, y:3.05, w:2.8, h:1.6, fontSize:11.5, fontFace:FONT_CUERPO, color:C.gris_osc, wrap:true, valign:"top" });
  });
}

// ════════════════════════════════════════════════════════════
// DIAPOSITIVA 3 — TIPOS DE SOLUCION
// ════════════════════════════════════════════════════════════
{
  const s = pres.addSlide();
  barraLateral(s);
  tituloSlide(s, "Tipos de Solucion del Sistema");
  barraInferior(s, "Analisis Numerico  |  Gauss-Jordan Master Pro");

  const tipos = [
    { y:1.1, color:C.verde,  titulo:"SOLUCION UNICA", cond:"La submatriz A se convierte en la identidad", res:"x, y, z determinados. Los tres planos se cruzan en un punto." },
    { y:2.65, color:"B8860B", titulo:"INFINITAS SOLUCIONES", cond:"Aparece una fila de ceros completa [0  0  0 | 0]", res:"Sistema indeterminado. Los planos se intersectan en una recta o coinciden." },
    { y:4.2,  color:C.rojo,   titulo:"SIN SOLUCION", cond:"Aparece fila [0  0  0 | c] con c diferente de 0", res:"Sistema inconsistente. Hay una contradiccion matematica." },
  ];

  tipos.forEach(t => {
    s.addShape(pres.ShapeType.rect, { x:0.3, y:t.y, w:0.35, h:1.2, fill:{color:t.color}, line:{color:t.color} });
    s.addShape(pres.ShapeType.rect, { x:0.65, y:t.y, w:9.05, h:1.2, fill:{color:C.gris_bg}, line:{color:C.gris_med, pt:1} });
    s.addText(t.titulo, { x:0.8, y:t.y+0.08, w:8.7, h:0.38, fontSize:14, bold:true, fontFace:FONT_TITULO, color:t.color, margin:0 });
    s.addText("Condicion: " + t.cond, { x:0.8, y:t.y+0.45, w:8.7, h:0.3, fontSize:11.5, fontFace:FONT_CUERPO, color:C.gris_osc, margin:0 });
    s.addText("Resultado: " + t.res, { x:0.8, y:t.y+0.76, w:8.7, h:0.35, fontSize:11.5, fontFace:FONT_CUERPO, color:C.gris_osc, margin:0 });
  });
}

// ════════════════════════════════════════════════════════════
// DIAPOSITIVA 4 — ALGORITMO (PASOS)
// ════════════════════════════════════════════════════════════
{
  const s = pres.addSlide();
  barraLateral(s);
  tituloSlide(s, "Algoritmo de Gauss-Jordan con Pivoteo Parcial");
  barraInferior(s, "Analisis Numerico  |  Gauss-Jordan Master Pro");

  const pasos = [
    { n:"1", titulo:"Pivoteo Parcial", desc:"En la columna h, buscar la fila con el mayor valor absoluto desde la fila h hasta la 3. Intercambiar esa fila con la fila h para mejorar la estabilidad numerica." },
    { n:"2", titulo:"Normalizacion", desc:"Dividir todos los elementos de la fila h entre el valor del pivote para que el elemento en la posicion [h][h] quede igual a 1." },
    { n:"3", titulo:"Eliminacion", desc:"Para cada fila i diferente de h, restar el multiplo adecuado de la fila h para hacer cero el elemento en la columna h." },
    { n:"4", titulo:"Analisis del Resultado", desc:"Revisar si hay contradiccion (sin solucion), filas de ceros (infinitas soluciones), o la identidad (solucion unica x, y, z)." },
  ];

  pasos.forEach((p, i) => {
    const x = i < 2 ? 0.3 : 0.3;
    const y = i < 2 ? 1.05 + i * 1.85 : 1.05 + i * 1.85;
    const col = i % 2 === 0 ? 0.3 : 5.2;
    const row = i < 2 ? 1.05 : 1.05;
    const yi = i < 2 ? 1.05 + i * 1.9 : 3.0 + (i-2) * 1.9;
    const xi = 0.3;

    // Dos columnas
    const cx = i % 2 === 0 ? 0.3 : 5.2;
    const cy = i < 2 ? 1.05 : 1.05 + Math.floor(i/2) * 1.9;

    s.addShape(pres.ShapeType.rect, { x:cx, y:cy, w:0.6, h:1.65, fill:{color:C.acento}, line:{color:C.acento} });
    s.addText(p.n, { x:cx, y:cy+0.5, w:0.6, h:0.6, fontSize:22, bold:true, fontFace:FONT_TITULO, color:C.blanco, align:"center", margin:0 });
    s.addShape(pres.ShapeType.rect, { x:cx+0.6, y:cy, w:4.0, h:1.65, fill:{color:C.gris_bg}, line:{color:C.gris_med, pt:1} });
    s.addText(p.titulo, { x:cx+0.7, y:cy+0.1, w:3.8, h:0.4, fontSize:13, bold:true, fontFace:FONT_TITULO, color:C.negro, margin:0 });
    s.addText(p.desc, { x:cx+0.7, y:cy+0.55, w:3.8, h:1.0, fontSize:11, fontFace:FONT_CUERPO, color:C.gris_osc, wrap:true, valign:"top", margin:0 });
  });
}

// ════════════════════════════════════════════════════════════
// DIAPOSITIVA 5 — PSEUDOCODIGO
// ════════════════════════════════════════════════════════════
{
  const s = pres.addSlide();
  barraLateral(s);
  tituloSlide(s, "Pseudocodigo del Algoritmo");
  barraInferior(s, "Analisis Numerico  |  Gauss-Jordan Master Pro");

  s.addShape(pres.ShapeType.rect, { x:0.3, y:1.05, w:9.4, h:3.85, fill:{color:"F0F4F8"}, line:{color:C.gris_med, pt:1} });

  const lineas = [
    "INICIO",
    "  LEER matriz_aumentada[3][4]",
    "  PARA h = 0 HASTA 2:",
    "    max_fila = fila con mayor |valor| en columna h",
    "    SI pivote = 0: CONTINUAR",
    "    SI max_fila != h: INTERCAMBIAR filas h y max_fila",
    "    Rh = Rh / pivote              // normalizar",
    "    PARA i = 0 HASTA 2:",
    "      SI i != h:",
    "        Ri = Ri - factor * Rh     // eliminar",
    "  ANALIZAR resultado:",
    "    Fila [0,0,0|c!=0] -> Sin solucion",
    "    Fila [0,0,0|0]    -> Infinitas soluciones",
    "    Identidad          -> x=m[0][3], y=m[1][3], z=m[2][3]",
    "FIN",
  ];

  lineas.forEach((l, i) => {
    const esComentario = l.includes("//");
    const esLabel = l.startsWith("INICIO") || l.startsWith("FIN") || l.startsWith("  PARA") || l.startsWith("  LEER") || l.startsWith("  ANALIZAR");
    s.addText(l, {
      x: 0.45, y: 1.12 + i * 0.24, w: 9.1, h: 0.25,
      fontSize: 11,
      fontFace: "Courier New",
      color: esComentario ? "2C7A4B" : esLabel ? C.acento : C.negro,
      bold: esLabel,
      margin: 0,
    });
  });
}

// ════════════════════════════════════════════════════════════
// DIAPOSITIVA 6 — DIAGRAMA DE FLUJO
// ════════════════════════════════════════════════════════════
{
  const s = pres.addSlide();
  barraLateral(s);
  tituloSlide(s, "Diagrama de Flujo del Algoritmo");
  barraInferior(s, "Analisis Numerico  |  Gauss-Jordan Master Pro");

  // Columna izquierda: flujo principal
  const cajas = [
    { y:1.1,  texto:"INICIO", tipo:"oval" },
    { y:1.75, texto:"Leer matriz\naumantada [3x4]", tipo:"rect" },
    { y:2.55, texto:"Buscar max |val|\nen columna h\n(pivoteo parcial)", tipo:"rect" },
    { y:3.5,  texto:"¿pivote = 0?", tipo:"diamond" },
    { y:4.3,  texto:"Normalizar fila h\nRh = Rh / pivote", tipo:"rect" },
  ];

  // Dibujar cajas izquierda
  cajas.forEach((c, i) => {
    const w = 2.2, x = 0.4, h = c.tipo === "diamond" ? 0.55 : (c.tipo === "oval" ? 0.45 : 0.62);
    if (c.tipo === "oval") {
      s.addShape(pres.ShapeType.ellipse, { x, y:c.y, w, h, fill:{color:C.acento}, line:{color:C.acento} });
      s.addText(c.texto, { x, y:c.y, w, h, fontSize:12, bold:true, fontFace:FONT_TITULO, color:C.blanco, align:"center", valign:"middle", margin:0 });
    } else if (c.tipo === "diamond") {
      s.addShape(pres.ShapeType.rect, { x, y:c.y, w, h:0.55, fill:{color:"E8E8E8"}, line:{color:C.gris_med} });
      s.addText(c.texto, { x, y:c.y, w, h:0.55, fontSize:12, fontFace:FONT_TITULO, color:C.negro, align:"center", valign:"middle", margin:0 });
    } else {
      s.addShape(pres.ShapeType.rect, { x, y:c.y, w, h, fill:{color:C.gris_bg}, line:{color:C.gris_med} });
      s.addText(c.texto, { x, y:c.y, w, h, fontSize:11, fontFace:FONT_CUERPO, color:C.negro, align:"center", valign:"middle", margin:0 });
    }
    // Flecha hacia abajo (excepto el ultimo)
    if (i < cajas.length - 1) {
      s.addShape(pres.ShapeType.line, { x:x+w/2, y:c.y+h, w:0.01, h:0.15, line:{color:C.gris_osc, pt:1.5} });
    }
  });

  // Columna derecha: eliminacion + resultado
  const cajas2 = [
    { y:1.1, texto:"Eliminar col h\nen filas i != h\nRi = Ri - f*Rh", tipo:"rect" },
    { y:2.0, texto:"¿h < 2?", tipo:"diamond" },
    { y:2.8, texto:"Analizar\nresultado", tipo:"rect" },
    { y:3.6, texto:"FIN", tipo:"oval" },
  ];

  cajas2.forEach((c, i) => {
    const w = 2.2, x = 7.1, h = c.tipo === "diamond" ? 0.55 : (c.tipo === "oval" ? 0.45 : 0.7);
    if (c.tipo === "oval") {
      s.addShape(pres.ShapeType.ellipse, { x, y:c.y, w, h, fill:{color:C.acento}, line:{color:C.acento} });
      s.addText(c.texto, { x, y:c.y, w, h, fontSize:12, bold:true, fontFace:FONT_TITULO, color:C.blanco, align:"center", valign:"middle", margin:0 });
    } else if (c.tipo === "diamond") {
      s.addShape(pres.ShapeType.rect, { x, y:c.y, w, h:0.55, fill:{color:"E8E8E8"}, line:{color:C.gris_med} });
      s.addText(c.texto, { x, y:c.y, w, h:0.55, fontSize:12, fontFace:FONT_TITULO, color:C.negro, align:"center", valign:"middle", margin:0 });
    } else {
      s.addShape(pres.ShapeType.rect, { x, y:c.y, w, h, fill:{color:C.gris_bg}, line:{color:C.gris_med} });
      s.addText(c.texto, { x, y:c.y, w, h, fontSize:11, fontFace:FONT_CUERPO, color:C.negro, align:"center", valign:"middle", margin:0 });
    }
    if (i < cajas2.length - 1) {
      s.addShape(pres.ShapeType.line, { x:x+w/2, y:c.y+h, w:0.01, h:0.15, line:{color:C.gris_osc, pt:1.5} });
    }
  });

  // Etiquetas de decision
  s.addText("SI -> h+1", { x:2.7, y:3.6, w:1.4, h:0.35, fontSize:10, fontFace:FONT_CUERPO, color:"888888" });
  s.addText("NO", { x:1.5, y:3.95, w:0.8, h:0.3, fontSize:10, fontFace:FONT_CUERPO, color:"888888" });
  s.addText("SI -> h+1", { x:9.4, y:2.18, w:0.55, h:0.3, fontSize:9, fontFace:FONT_CUERPO, color:"888888" });

  // Descripcion central
  s.addShape(pres.ShapeType.rect, { x:2.85, y:1.1, w:3.9, h:3.75, fill:{color:"FAFAFA"}, line:{color:C.gris_med, pt:1} });
  s.addText("Flujo del Algoritmo", { x:2.95, y:1.15, w:3.7, h:0.35, fontSize:12, bold:true, fontFace:FONT_TITULO, color:C.acento });
  const desc = [
    "El bucle principal recorre las 3",
    "columnas (h = 0, 1, 2).",
    "",
    "Para cada columna:",
    "  1. Pivoteo parcial",
    "  2. Normalizacion",
    "  3. Eliminacion",
    "",
    "Al final se analiza si la",
    "solucion es unica, sin",
    "solucion o infinitas.",
  ];
  desc.forEach((l, i) => {
    s.addText(l, { x:3.0, y:1.55+i*0.28, w:3.6, h:0.28, fontSize:11, fontFace:FONT_CUERPO, color:C.gris_osc, margin:0 });
  });
}

// ════════════════════════════════════════════════════════════
// DIAPOSITIVA 7 — ESTRUCTURA DEL PROGRAMA
// ════════════════════════════════════════════════════════════
{
  const s = pres.addSlide();
  barraLateral(s);
  tituloSlide(s, "Estructura del Programa en Python");
  barraInferior(s, "Analisis Numerico  |  Gauss-Jordan Master Pro");

  const modulos = [
    { archivo:"main.py",                  color:C.acento,  desc:"Punto de entrada. Inicia la aplicacion Qt." },
    { archivo:"logic/solver.py",          color:"1B5E20",  desc:"Motor Gauss-Jordan. Implementa el algoritmo con pivoteo parcial usando fractions.Fraction." },
    { archivo:"logic/parser.py",          color:"1B5E20",  desc:"Interpreta ecuaciones en texto: '2x+y-z=8', '(1/2)x-y=3', '0.5x+z=1'." },
    { archivo:"logic/calculator.py",      color:"1B5E20",  desc:"Convierte texto a Fraction. Evaluador seguro de expresiones." },
    { archivo:"ui/main_window.py",        color:"4A148C",  desc:"Ventana principal. Orquesta la interfaz, botones de ejemplo y validacion." },
    { archivo:"ui/widgets/matrix_grid.py",color:"4A148C",  desc:"Cuadricula 3x4 para ingresar la matriz aumentada [A|b]." },
    { archivo:"ui/widgets/step_viewer.py",color:"4A148C",  desc:"Muestra los pasos del algoritmo con codigo de colores." },
    { archivo:"ui/styles.py",             color:"4A148C",  desc:"Estilos CSS de la interfaz (tema oscuro)." },
  ];

  modulos.forEach((m, i) => {
    const col = i < 4 ? 0.3 : 5.2;
    const y   = 1.1 + (i % 4) * 1.05;
    s.addShape(pres.ShapeType.rect, { x:col, y, w:4.65, h:0.9, fill:{color:C.gris_bg}, line:{color:C.gris_med, pt:1} });
    s.addShape(pres.ShapeType.rect, { x:col, y, w:0.18, h:0.9, fill:{color:m.color}, line:{color:m.color} });
    s.addText(m.archivo, { x:col+0.25, y:y+0.05, w:4.2, h:0.32, fontSize:12, bold:true, fontFace:"Courier New", color:m.color, margin:0 });
    s.addText(m.desc,    { x:col+0.25, y:y+0.42, w:4.2, h:0.42, fontSize:10.5, fontFace:FONT_CUERPO, color:C.gris_osc, wrap:true, margin:0 });
  });
}

// ════════════════════════════════════════════════════════════
// DIAPOSITIVA 8 — INTERFAZ DEL PROGRAMA
// ════════════════════════════════════════════════════════════
{
  const s = pres.addSlide();
  barraLateral(s);
  tituloSlide(s, "Interfaz del Programa");
  barraInferior(s, "Analisis Numerico  |  Gauss-Jordan Master Pro");

  // Panel izquierdo (descripcion)
  const items = [
    { titulo:"Ingreso de Ecuaciones", desc:"3 campos de texto donde se escribe cada ecuacion. Acepta decimales, fracciones y coeficientes implicitos." },
    { titulo:"Ejemplos Rapidos", desc:"4 botones que cargan sistemas predefinidos con un clic: solucion unica, sin solucion e infinitas." },
    { titulo:"Matriz Aumentada [A|b]", desc:"Cuadricula 3x4 editable. La columna dorada es el termino independiente." },
    { titulo:"Procedimiento Paso a Paso", desc:"Cada operacion elemental se muestra en una tarjeta con colores: verde=pivote, rojo=modificada." },
    { titulo:"Resultado Final", desc:"Banner inferior que cambia de color: verde (solucion), rojo (sin sol), amarillo (infinitas)." },
  ];

  items.forEach((it, i) => {
    s.addShape(pres.ShapeType.rect, { x:0.3, y:1.05+i*0.85, w:0.12, h:0.7, fill:{color:C.acento}, line:{color:C.acento} });
    s.addText(it.titulo, { x:0.55, y:1.05+i*0.85, w:4.2, h:0.32, fontSize:12, bold:true, fontFace:FONT_TITULO, color:C.acento, margin:0 });
    s.addText(it.desc,   { x:0.55, y:1.38+i*0.85, w:4.2, h:0.4,  fontSize:11, fontFace:FONT_CUERPO, color:C.gris_osc, wrap:true, margin:0 });
  });

  // Panel derecho (esquema visual de la app)
  s.addShape(pres.ShapeType.rect, { x:5.1, y:1.05, w:4.6, h:4.0, fill:{color:"1A1A2E"}, line:{color:"333355", pt:1} });
  s.addText("Gauss-Jordan Master Pro", { x:5.2, y:1.1, w:4.4, h:0.35, fontSize:11, bold:true, fontFace:FONT_TITULO, color:"89B4FA", align:"center" });
  s.addShape(pres.ShapeType.rect, { x:5.2, y:1.48, w:2.0, h:1.0, fill:{color:"12121F"}, line:{color:"2A2A40"} });
  s.addText("INGRESA LAS\nECUACIONES", { x:5.2, y:1.5, w:2.0, h:0.4, fontSize:7, bold:true, fontFace:FONT_TITULO, color:"89DCEB", align:"center" });
  s.addShape(pres.ShapeType.rect, { x:5.25, y:1.92, w:1.9, h:0.15, fill:{color:"313244"}, line:{color:"45475A"} });
  s.addShape(pres.ShapeType.rect, { x:5.25, y:2.1,  w:1.9, h:0.15, fill:{color:"313244"}, line:{color:"45475A"} });
  s.addShape(pres.ShapeType.rect, { x:5.25, y:2.28, w:1.9, h:0.15, fill:{color:"313244"}, line:{color:"45475A"} });

  s.addShape(pres.ShapeType.rect, { x:7.3, y:1.48, w:2.3, h:2.6, fill:{color:"12121F"}, line:{color:"2A2A40"} });
  s.addText("PROCEDIMIENTO\nPASO A PASO", { x:7.3, y:1.52, w:2.3, h:0.4, fontSize:7, bold:true, fontFace:FONT_TITULO, color:"89B4FA", align:"center" });
  const pasoColors = ["2E3B3E","3E2E2E","2E3B3E","3E2E2E"];
  pasoColors.forEach((c, i) => {
    s.addShape(pres.ShapeType.rect, { x:7.35, y:1.98+i*0.46, w:2.2, h:0.38, fill:{color:c}, line:{color:"313244"} });
    s.addText(`PASO ${i+1}`, { x:7.4, y:2.0+i*0.46, w:2.1, h:0.2, fontSize:8, fontFace:FONT_TITULO, color:"89B4FA" });
  });

  s.addShape(pres.ShapeType.rect, { x:5.2, y:3.55, w:4.4, h:0.45, fill:{color:"1A2A1A"}, line:{color:"A6E3A1", pt:1} });
  s.addText("SOLUCION UNICA:  x = 2   y = 3   z = -1", { x:5.2, y:3.55, w:4.4, h:0.45, fontSize:10, bold:true, fontFace:FONT_TITULO, color:"A6E3A1", align:"center", valign:"middle" });

  s.addShape(pres.ShapeType.rect, { x:5.1, y:4.05, w:4.6, h:1.0, fill:{color:"12121F"}, line:{color:"333355"} });
  const btnColors = ["1A2A1A","1A2A1A","2A1A1A","2A2A10"];
  const btnTxt = ["Ejemplo 1","Ejemplo 2","Sin Sol.","Infinitas"];
  btnColors.forEach((c, i) => {
    s.addShape(pres.ShapeType.rect, { x:5.15+i*1.13, y:4.12, w:1.05, h:0.35, fill:{color:c}, line:{color:"888888"} });
    s.addText(btnTxt[i], { x:5.15+i*1.13, y:4.12, w:1.05, h:0.35, fontSize:8, fontFace:FONT_CUERPO, color:"AAAAAA", align:"center", valign:"middle" });
  });
}

// ════════════════════════════════════════════════════════════
// DIAPOSITIVA 9 — CODIGO CLAVE
// ════════════════════════════════════════════════════════════
{
  const s = pres.addSlide();
  barraLateral(s);
  tituloSlide(s, "Fragmento de Codigo Clave — solver.py");
  barraInferior(s, "Analisis Numerico  |  Gauss-Jordan Master Pro");

  s.addShape(pres.ShapeType.rect, { x:0.3, y:1.05, w:9.4, h:3.85, fill:{color:"F0F4F8"}, line:{color:C.gris_med, pt:1} });

  const codigo = [
    { t:"for h in range(3):                         # h = columna pivote", c:C.acento, b:true },
    { t:"    max_row = max(range(h, 3),", c:C.negro, b:false },
    { t:"                 key=lambda i: abs(matrix[i][h]))", c:C.negro, b:false },
    { t:"    if matrix[max_row][h] == 0: continue   # columna singular", c:"2C7A4B", b:false },
    { t:"    if max_row != h:", c:C.negro, b:false },
    { t:"        matrix[h], matrix[max_row] = matrix[max_row], matrix[h]", c:C.negro, b:false },
    { t:"    pivot = matrix[h][h]", c:C.negro, b:false },
    { t:"    matrix[h] = [x / pivot for x in matrix[h]]  # normalizar", c:"2C7A4B", b:false },
    { t:"    for i in range(3):", c:C.acento, b:true },
    { t:"        if i != h:", c:C.negro, b:false },
    { t:"            factor = matrix[i][h]", c:C.negro, b:false },
    { t:"            matrix[i] = [matrix[i][j] - factor*matrix[h][j]", c:C.negro, b:false },
    { t:"                         for j in range(4)]  # eliminar", c:"2C7A4B", b:false },
    { t:"return self._analyze_result()               # analizar tipo", c:"888888", b:false },
  ];

  codigo.forEach((l, i) => {
    s.addText(l.t, {
      x:0.45, y:1.1+i*0.26, w:9.1, h:0.27,
      fontSize:10.5, fontFace:"Courier New",
      color:l.c, bold:l.b, margin:0,
    });
  });
}

// ════════════════════════════════════════════════════════════
// DIAPOSITIVA 10 — CASOS DE PRUEBA
// ════════════════════════════════════════════════════════════
{
  const s = pres.addSlide();
  barraLateral(s);
  tituloSlide(s, "Casos de Prueba y Resultados");
  barraInferior(s, "Analisis Numerico  |  Gauss-Jordan Master Pro");

  const casos = [
    { tipo:"Solucion Unica",      color:C.verde,    ecuaciones:"2x+y-z=8\n-3x-y+2z=-11\n-2x+y+2z=-3",  resultado:"x=2, y=3, z=-1" },
    { tipo:"Solucion Unica",      color:C.verde,    ecuaciones:"x-2y+3z=9\n-x+3y=-4\n2x-5y+5z=17",     resultado:"x=1, y=-1, z=2" },
    { tipo:"Sin Solucion",        color:C.rojo,     ecuaciones:"x+y+z=6\n2x+2y+2z=14\n3x+3y+3z=20",    resultado:"Sistema inconsistente" },
    { tipo:"Infinitas Soluciones",color:"B8860B",   ecuaciones:"x+2y+3z=6\n2x+4y+6z=12\n3x+6y+9z=18",  resultado:"Sistema indeterminado" },
    { tipo:"Fracciones",          color:"1565C0",   ecuaciones:"(1/2)x+y-z=1\n-3x-y+2z=-11\n-2x+y+2z=-3", resultado:"Valores exactos" },
  ];

  casos.forEach((c, i) => {
    const x = i < 3 ? 0.3 + (i % 3) * 3.2 : 0.3 + (i-3) * 3.2 + 1.6;
    const y = i < 3 ? 1.1 : 3.2;
    s.addShape(pres.ShapeType.rect, { x, y, w:3.0, h:1.85, fill:{color:C.gris_bg}, line:{color:C.gris_med, pt:1} });
    s.addShape(pres.ShapeType.rect, { x, y, w:3.0, h:0.38, fill:{color:c.color}, line:{color:c.color} });
    s.addText(c.tipo, { x:x+0.08, y, w:2.85, h:0.38, fontSize:11, bold:true, fontFace:FONT_TITULO, color:C.blanco, valign:"middle", margin:0 });
    s.addText(c.ecuaciones, { x:x+0.1, y:y+0.42, w:1.6, h:1.3, fontSize:9.5, fontFace:"Courier New", color:C.negro, valign:"top", margin:0 });
    s.addShape(pres.ShapeType.rect, { x:x+1.75, y:y+0.42, w:1.15, h:1.3, fill:{color:"FFFDE7"}, line:{color:C.gris_med} });
    s.addText(c.resultado, { x:x+1.8, y:y+0.7, w:1.05, h:0.8, fontSize:10, bold:true, fontFace:FONT_TITULO, color:c.color, align:"center", wrap:true, margin:0 });
  });
}

// ════════════════════════════════════════════════════════════
// DIAPOSITIVA 11 — CONCLUSIONES
// ════════════════════════════════════════════════════════════
{
  const s = pres.addSlide();
  barraLateral(s);
  tituloSlide(s, "Conclusiones");
  barraInferior(s, "Analisis Numerico  |  Gauss-Jordan Master Pro");

  const concl = [
    "Programar el metodo ayudo a entender mejor como funciona por dentro, porque hay que pensar en cada caso posible.",
    "Usar fracciones exactas en vez de decimales es clave: evita errores de redondeo y siempre da el resultado correcto.",
    "Mostrar los pasos con colores es lo que mas ayuda a entender el algoritmo en accion.",
    "El parser quedo flexible: acepta (1/2)x, 0.5x, -x, 2*x sin que el usuario se preocupe por el formato.",
    "El proyecto cubrio todo el ciclo: entender el metodo, disenarlo, codificarlo y probarlo con casos reales.",
  ];

  concl.forEach((c, i) => {
    s.addShape(pres.ShapeType.ellipse, { x:0.3, y:1.12+i*0.86, w:0.42, h:0.42, fill:{color:C.acento}, line:{color:C.acento} });
    s.addText(String(i+1), { x:0.3, y:1.12+i*0.86, w:0.42, h:0.42, fontSize:14, bold:true, fontFace:FONT_TITULO, color:C.blanco, align:"center", valign:"middle", margin:0 });
    s.addShape(pres.ShapeType.rect, { x:0.82, y:1.1+i*0.86, w:8.9, h:0.7, fill:{color:C.gris_bg}, line:{color:C.gris_med, pt:1} });
    s.addText(c, { x:0.97, y:1.1+i*0.86, w:8.6, h:0.7, fontSize:13, fontFace:FONT_CUERPO, color:C.gris_osc, valign:"middle", wrap:true, margin:0 });
  });
}

// ════════════════════════════════════════════════════════════
// GUARDAR
// ════════════════════════════════════════════════════════════
pres.writeFile({ fileName: "C:/Users/Administrator/gauss-jordan-master-pro/Exposicion_GaussJordan.pptx" })
  .then(() => console.log("OK: Exposicion_GaussJordan.pptx generada"))
  .catch(e => { console.error("ERROR:", e.message); process.exit(1); });
