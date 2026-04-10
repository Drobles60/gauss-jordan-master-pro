"""
main_window.py — Ventana principal de Gauss-Jordan Master Pro
"""
import qtawesome as qta
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QMessageBox, QCheckBox,
    QGroupBox, QLineEdit, QFrame, QDialog,
    QTextBrowser, QSizePolicy
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

from ui.widgets.matrix_grid import MatrixGrid
from ui.widgets.step_viewer import StepViewer
from logic.solver import GaussJordanSolver
from ui.styles import MAIN_STYLE

# ── Ejemplos predefinidos ────────────────────────────────────────────────────
EXAMPLES = [
    {
        "label": "Ejemplo 1",
        "color": "#a6e3a1", "dark": "#1a2a1a",
        "tooltip": "Solucion unica: x=2, y=3, z=-1",
        "eqs": ["2x + y - z = 8", "-3x - y + 2z = -11", "-2x + y + 2z = -3"],
    },
    {
        "label": "Ejemplo 2",
        "color": "#a6e3a1", "dark": "#1a2a1a",
        "tooltip": "Solucion unica: x=1, y=-1, z=2",
        "eqs": ["x - 2y + 3z = 9", "-x + 3y = -4", "2x - 5y + 5z = 17"],
    },
    {
        "label": "Sin Solucion",
        "color": "#f38ba8", "dark": "#2a1a1a",
        "tooltip": "Sistema inconsistente",
        "eqs": ["x + y + z = 6", "2x + 2y + 2z = 14", "3x + 3y + 3z = 20"],
    },
    {
        "label": "Infinitas",
        "color": "#f9e2af", "dark": "#2a2a10",
        "tooltip": "Sistema indeterminado",
        "eqs": ["x + 2y + 3z = 6", "2x + 4y + 6z = 12", "3x + 6y + 9z = 18"],
    },
]

# ── Dialogo de Ayuda ─────────────────────────────────────────────────────────
class HelpDialog(QDialog):
    MANUAL_HTML = """
<body style="font-family:Segoe UI,Arial,sans-serif; color:#cdd6f4; background:#1a1a2e; margin:0; padding:4px;">

<!-- ===== TITULO ===== -->
<h2 style="color:#89b4fa; margin-bottom:2px;">&#128218; Manual de Usuario</h2>
<p style="color:#6c7086; font-size:11px; margin-top:0;">Gauss-Jordan Master Pro &mdash; Gu&iacute;a completa de uso</p>
<hr style="border:none; border-top:1px solid #2a2a40; margin:8px 0;"/>

<!-- ===== 1. QUE ES ===== -->
<h3 style="color:#89dceb; margin-bottom:4px;">&#128269; &iquest;Qu&eacute; es esta aplicaci&oacute;n?</h3>
<p style="margin:4px 0 10px 0;">
  <b>Gauss-Jordan Master Pro</b> resuelve sistemas de <b>3 ecuaciones lineales con 3 inc&oacute;gnitas</b>
  (x, y, z) usando el m&eacute;todo de eliminaci&oacute;n de Gauss-Jordan con pivoteo parcial.
  Muestra cada operaci&oacute;n de fila paso a paso para que puedas aprender el procedimiento completo.
</p>

<!-- ===== 2. PASOS DE USO ===== -->
<h3 style="color:#89dceb; margin-bottom:6px;">&#9654; C&oacute;mo usar la aplicaci&oacute;n (paso a paso)</h3>
<table width="100%" cellspacing="0" cellpadding="0">
  <tr>
    <td style="vertical-align:top; padding:4px 0;">
      <div style="background:#12122a; border-left:3px solid #89b4fa; border-radius:6px; padding:8px 12px; margin-bottom:6px;">
        <b style="color:#89b4fa;">PASO 1 &mdash; Ingresa las ecuaciones</b><br/>
        Escribe cada ecuaci&oacute;n en los campos <b>E1, E2, E3</b> de la columna izquierda.
        Puedes usar texto libre con x, y, z (ver formatos abajo).
        <br/><br/>
        <i style="color:#6c7086;">Alternativa:</i> si ya tienes los coeficientes num&eacute;ricos, llena
        directamente las celdas de la <b>Matriz [A|b]</b> (columna dorada = t&eacute;rmino independiente).
      </div>
      <div style="background:#12122a; border-left:3px solid #a6e3a1; border-radius:6px; padding:8px 12px; margin-bottom:6px;">
        <b style="color:#a6e3a1;">PASO 2 &mdash; Usa un ejemplo r&aacute;pido (opcional)</b><br/>
        Haz clic en <b>Ejemplo 1</b> o <b>Ejemplo 2</b> para cargar un sistema con soluci&oacute;n &uacute;nica,
        en <b>Sin Soluci&oacute;n</b> para ver un sistema inconsistente, o en <b>Infinitas</b> para
        ver un sistema indeterminado.
      </div>
      <div style="background:#12122a; border-left:3px solid #f9e2af; border-radius:6px; padding:8px 12px; margin-bottom:6px;">
        <b style="color:#f9e2af;">PASO 3 &mdash; Presiona RESOLVER</b><br/>
        Haz clic en el bot&oacute;n grande <b>&ldquo;INTERPRETAR Y RESOLVER&rdquo;</b>.
        La aplicaci&oacute;n convierte las ecuaciones a la matriz, ejecuta Gauss-Jordan y
        muestra el procedimiento completo en la columna derecha.
      </div>
      <div style="background:#12122a; border-left:3px solid #cba6f7; border-radius:6px; padding:8px 12px; margin-bottom:6px;">
        <b style="color:#cba6f7;">PASO 4 &mdash; Navega los pasos</b><br/>
        Usa los botones <b>&laquo; Anterior</b> y <b>Siguiente &raquo;</b> en el panel derecho para
        avanzar o retroceder en el procedimiento.  Cada paso muestra la operaci&oacute;n realizada,
        una explicaci&oacute;n en espa&ntilde;ol y la matriz coloreada.
      </div>
      <div style="background:#12122a; border-left:3px solid #fab387; border-radius:6px; padding:8px 12px; margin-bottom:6px;">
        <b style="color:#fab387;">PASO 5 &mdash; Lee el resultado</b><br/>
        El <b>banner inferior</b> muestra el tipo de soluci&oacute;n y los valores de x, y, z.
        Activa o desactiva <b>&ldquo;Modo Fracciones&rdquo;</b> para ver resultados exactos (1/3)
        o decimales (0.3333).
      </div>
    </td>
  </tr>
</table>

<!-- ===== 3. FORMATOS DE ECUACION ===== -->
<h3 style="color:#89dceb; margin-top:10px; margin-bottom:6px;">&#9998; Formatos de ecuaci&oacute;n aceptados</h3>
<p style="margin:0 0 6px 0; color:#a6adc8;">Puedes combinar cualquiera de estos formatos en la misma ecuaci&oacute;n:</p>
<table width="100%" cellspacing="4" cellpadding="6" style="border-collapse:separate; font-size:12px;">
  <tr style="background:#0d0d1a;">
    <th align="left" style="color:#89b4fa; padding:6px 10px; border-radius:4px 0 0 4px;">Formato</th>
    <th align="left" style="color:#89b4fa; padding:6px 10px;">Ejemplo</th>
    <th align="left" style="color:#89b4fa; padding:6px 10px; border-radius:0 4px 4px 0;">Descripci&oacute;n</th>
  </tr>
  <tr style="background:#12122a;">
    <td style="padding:5px 10px;"><code style="color:#a6e3a1;">2x</code></td>
    <td style="padding:5px 10px;"><code>2x + y - z = 8</code></td>
    <td style="padding:5px 10px; color:#a6adc8;">Coeficiente entero</td>
  </tr>
  <tr style="background:#0d0d1a;">
    <td style="padding:5px 10px;"><code style="color:#a6e3a1;">-3x</code></td>
    <td style="padding:5px 10px;"><code>-3x + 2y = 0</code></td>
    <td style="padding:5px 10px; color:#a6adc8;">Coeficiente entero negativo</td>
  </tr>
  <tr style="background:#12122a;">
    <td style="padding:5px 10px;"><code style="color:#a6e3a1;">x</code> &nbsp;o&nbsp; <code style="color:#a6e3a1;">-x</code></td>
    <td style="padding:5px 10px;"><code>x - y + z = 1</code></td>
    <td style="padding:5px 10px; color:#a6adc8;">Coeficiente impl&iacute;cito +1 o &minus;1</td>
  </tr>
  <tr style="background:#0d0d1a;">
    <td style="padding:5px 10px;"><code style="color:#a6e3a1;">1/2 x</code></td>
    <td style="padding:5px 10px;"><code>1/2 x + y = 3</code></td>
    <td style="padding:5px 10px; color:#a6adc8;">Fracci&oacute;n separada por espacio</td>
  </tr>
  <tr style="background:#12122a;">
    <td style="padding:5px 10px;"><code style="color:#a6e3a1;">(1/2)x</code></td>
    <td style="padding:5px 10px;"><code>(1/2)x - (3/4)y = 5</code></td>
    <td style="padding:5px 10px; color:#a6adc8;">Fracci&oacute;n entre par&eacute;ntesis</td>
  </tr>
  <tr style="background:#0d0d1a;">
    <td style="padding:5px 10px;"><code style="color:#a6e3a1;">0.5x</code></td>
    <td style="padding:5px 10px;"><code>0.5x - 1.25y = 2.0</code></td>
    <td style="padding:5px 10px; color:#a6adc8;">Coeficiente decimal</td>
  </tr>
  <tr style="background:#12122a;">
    <td style="padding:5px 10px;"><code style="color:#a6e3a1;">2*x</code></td>
    <td style="padding:5px 10px;"><code>2*x + 3*y - z = 6</code></td>
    <td style="padding:5px 10px; color:#a6adc8;">Con asterisco (se ignora el *)</td>
  </tr>
  <tr style="background:#0d0d1a;">
    <td style="padding:5px 10px; color:#a6adc8;" colspan="3">
      <b>RHS (lado derecho):</b> entero (<code>= 5</code>), negativo (<code>= -3</code>),
      decimal (<code>= 1.5</code>), fracci&oacute;n (<code>= 1/2</code>) o cero (<code>= 0</code>)
    </td>
  </tr>
</table>

<!-- ===== 4. ELEMENTOS DE LA INTERFAZ ===== -->
<h3 style="color:#89dceb; margin-top:14px; margin-bottom:6px;">&#128421; Elementos de la interfaz</h3>
<table width="100%" cellspacing="0" cellpadding="0" style="font-size:12px;">
  <tr>
    <td width="50%" style="vertical-align:top; padding-right:8px;">
      <p style="color:#89b4fa; margin:0 0 4px 0;"><b>Columna izquierda</b></p>
      <ul style="margin:0; padding-left:18px; line-height:1.8;">
        <li><b>E1, E2, E3</b> &mdash; campos de texto para las ecuaciones</li>
        <li><b>Ejemplos R&aacute;pidos</b> &mdash; carga sistemas predefinidos</li>
        <li><b>Matriz [A|b]</b> &mdash; tabla 3&times;4 editable directamente</li>
        <li><b>Columna dorada</b> &mdash; t&eacute;rminos independientes (b)</li>
        <li><b>Modo Fracciones</b> &mdash; alterna entre fracci&oacute;n y decimal</li>
        <li><b>Bot&oacute;n RESOLVER</b> &mdash; inicia el c&aacute;lculo completo</li>
      </ul>
    </td>
    <td width="50%" style="vertical-align:top; padding-left:8px;">
      <p style="color:#89b4fa; margin:0 0 4px 0;"><b>Columna derecha</b></p>
      <ul style="margin:0; padding-left:18px; line-height:1.8;">
        <li><b>Panel de pasos</b> &mdash; muestra cada operaci&oacute;n de fila</li>
        <li><b>N&uacute;mero de paso</b> &mdash; ej. &ldquo;Paso 3 de 9&rdquo;</li>
        <li><b>Operaci&oacute;n</b> &mdash; notaci&oacute;n matricial (ej. R2 &larr; R2 &minus; 3R1)</li>
        <li><b>Explicaci&oacute;n</b> &mdash; descripci&oacute;n en espa&ntilde;ol del paso</li>
        <li><b>Matriz coloreada</b> &mdash; resalta filas involucradas</li>
        <li><b>Banner resultado</b> &mdash; tipo y valores de la soluci&oacute;n</li>
      </ul>
    </td>
  </tr>
</table>
<p style="margin:8px 0 4px 0; font-size:12px; color:#a6adc8;">
  <b style="color:#cdd6f4;">Bot&oacute;n &#128465;</b> (papelera, esquina superior derecha) &mdash; limpia todos los campos y reinicia la aplicaci&oacute;n.<br/>
  <b style="color:#cdd6f4;">Bot&oacute;n &#10067;</b> (interrogaci&oacute;n, esquina superior derecha) &mdash; abre este manual.
</p>

<!-- ===== 5. COLORES EN LA MATRIZ ===== -->
<h3 style="color:#89dceb; margin-top:14px; margin-bottom:6px;">&#127912; C&oacute;digo de colores en el panel de pasos</h3>
<table width="100%" cellspacing="4" cellpadding="6" style="border-collapse:separate; font-size:13px;">
  <tr style="background:#1a2a1a;">
    <td width="20" style="border-radius:4px 0 0 4px;">&#9632;</td>
    <td><b style="color:#a6e3a1;">Verde &mdash; Fila Pivote</b></td>
    <td style="color:#a6adc8;">Fila que se usa como referencia para eliminar las dem&aacute;s.
    Su pivote ya fue normalizado a 1.</td>
  </tr>
  <tr style="background:#2a1a1a;">
    <td style="border-radius:4px 0 0 4px;">&#9632;</td>
    <td><b style="color:#f38ba8;">Rojo &mdash; Fila Modificada</b></td>
    <td style="color:#a6adc8;">Fila que est&aacute; siendo alterada en este paso.
    Se le rest&oacute; un m&uacute;ltiplo de la fila pivote para hacer cero su columna.</td>
  </tr>
  <tr style="background:#2a2a10;">
    <td style="border-radius:4px 0 0 4px;">&#9632;</td>
    <td><b style="color:#f9e2af;">Amarillo &mdash; Intercambio</b></td>
    <td style="color:#a6adc8;">Dos filas intercambiadas (pivoteo parcial).
    Se elige la fila con el mayor valor absoluto para mejorar la estabilidad.</td>
  </tr>
</table>

<!-- ===== 6. TIPOS DE RESULTADO ===== -->
<h3 style="color:#89dceb; margin-top:14px; margin-bottom:6px;">&#127919; Tipos de resultado</h3>

<div style="background:#1a2a1a; border:1px solid #a6e3a1; border-radius:8px; padding:10px 14px; margin-bottom:8px;">
  <b style="color:#a6e3a1; font-size:13px;">&#10003; SOLUCI&Oacute;N &Uacute;NICA</b>
  <span style="color:#6c7086; font-size:11px;"> &mdash; banner verde</span><br/>
  <p style="margin:4px 0;">El sistema tiene exactamente una respuesta. La submatriz izquierda
  se redujo a la identidad. Los valores x, y, z se muestran en el banner inferior.</p>
  <pre style="background:#0d0d1a; padding:8px; border-radius:6px; color:#cdd6f4; margin:4px 0; font-size:11px;">E1:  2x +  y -  z =  8
E2: -3x -  y + 2z = -11
E3: -2x +  y + 2z = -3
Resultado: x = 2,  y = 3,  z = -1</pre>
</div>

<div style="background:#2a1a1a; border:1px solid #f38ba8; border-radius:8px; padding:10px 14px; margin-bottom:8px;">
  <b style="color:#f38ba8; font-size:13px;">&#10007; SIN SOLUCI&Oacute;N</b>
  <span style="color:#6c7086; font-size:11px;"> &mdash; banner rojo</span><br/>
  <p style="margin:4px 0;">El sistema es <b>inconsistente</b>: aparece una fila del tipo
  <code>[0  0  0 | c &ne; 0]</code>, que representa la contradicci&oacute;n <i>0 = constante</i>.
  No existe ning&uacute;n valor de x, y, z que satisfaga las tres ecuaciones simult&aacute;neamente.</p>
  <pre style="background:#0d0d1a; padding:8px; border-radius:6px; color:#cdd6f4; margin:4px 0; font-size:11px;">E1:  x +  y +  z =  6
E2: 2x + 2y + 2z = 14   &larr; inconsistente con E1
E3: 3x + 3y + 3z = 20
Resultado: Sin solucion</pre>
</div>

<div style="background:#2a2a10; border:1px solid #f9e2af; border-radius:8px; padding:10px 14px; margin-bottom:8px;">
  <b style="color:#f9e2af; font-size:13px;">&#8734; INFINITAS SOLUCIONES</b>
  <span style="color:#6c7086; font-size:11px;"> &mdash; banner amarillo</span><br/>
  <p style="margin:4px 0;">El sistema es <b>compatible indeterminado</b>: al menos una fila queda
  <code>[0  0  0 | 0]</code>. Hay m&aacute;s inc&oacute;gnitas que ecuaciones independientes,
  por lo que existen infinitas combinaciones (x, y, z) v&aacute;lidas.</p>
  <pre style="background:#0d0d1a; padding:8px; border-radius:6px; color:#cdd6f4; margin:4px 0; font-size:11px;">E1:  x + 2y + 3z =  6
E2: 2x + 4y + 6z = 12   &larr; m&uacute;ltiplo de E1
E3: 3x + 6y + 9z = 18   &larr; m&uacute;ltiplo de E1
Resultado: Infinitas soluciones</pre>
</div>

<!-- ===== 7. CONSEJOS ===== -->
<h3 style="color:#89dceb; margin-top:14px; margin-bottom:6px;">&#128161; Consejos y errores comunes</h3>
<table width="100%" cellspacing="0" cellpadding="0" style="font-size:12px;">
  <tr>
    <td style="vertical-align:top; width:50%; padding-right:8px;">
      <p style="color:#a6e3a1; margin:0 0 4px 0;"><b>&#10003; Buenas pr&aacute;cticas</b></p>
      <ul style="margin:0; padding-left:16px; line-height:1.9; color:#a6adc8;">
        <li>Escribe siempre las 3 ecuaciones o deja las 3 vac&iacute;as.</li>
        <li>Usa <code>= 0</code> cuando el t&eacute;rmino independiente es cero.</li>
        <li>Si una inc&oacute;gnita no aparece, puedes omitirla (su coeficiente ser&aacute; 0).</li>
        <li>Activa <b>Modo Fracciones</b> para ver resultados exactos sin redondeo.</li>
        <li>Prueba los ejemplos r&aacute;pidos para entender cada tipo de resultado.</li>
        <li>Usa la papelera &#128465; para reiniciar antes de ingresar un nuevo sistema.</li>
      </ul>
    </td>
    <td style="vertical-align:top; width:50%; padding-left:8px;">
      <p style="color:#f38ba8; margin:0 0 4px 0;"><b>&#10007; Errores frecuentes</b></p>
      <ul style="margin:0; padding-left:16px; line-height:1.9; color:#a6adc8;">
        <li>Olvidar el signo <code>=</code> en la ecuaci&oacute;n.</li>
        <li>Escribir variables distintas a x, y, z (p.ej. <code>a</code> o <code>n</code>).</li>
        <li>Dejar una celda de la matriz vac&iacute;a en lugar de poner 0.</li>
        <li>Poner una fila completa de ceros en los coeficientes.</li>
        <li>Usar coma decimal en lugar de punto (<code>1,5</code> en vez de <code>1.5</code>).</li>
        <li>Mezclar letras may&uacute;sculas: usa solo <b>x, y, z</b> (min&uacute;sculas).</li>
      </ul>
    </td>
  </tr>
</table>

<!-- ===== 8. MODO FRACCIONES ===== -->
<h3 style="color:#89dceb; margin-top:14px; margin-bottom:4px;">&#128290; Modo Fracciones vs. Decimal</h3>
<p style="margin:4px 0; color:#a6adc8; font-size:12px;">
  La casilla <b>&ldquo;Modo Fracciones (resultados exactos)&rdquo;</b> controla c&oacute;mo se muestran
  los valores en la soluci&oacute;n y en la matriz de cada paso:
</p>
<ul style="font-size:12px; color:#a6adc8; margin:4px 0 0 0; padding-left:18px; line-height:1.8;">
  <li><b style="color:#cdd6f4;">Activado</b> &mdash; muestra fracciones exactas: <code>x = 1/3</code>, <code>y = 7/4</code></li>
  <li><b style="color:#cdd6f4;">Desactivado</b> &mdash; muestra decimales con 4 cifras: <code>x = 0.3333</code>, <code>y = 1.7500</code></li>
</ul>
<p style="font-size:12px; color:#a6adc8; margin:4px 0 0 0;">
  El c&aacute;lculo interno siempre usa fracciones exactas; el modo s&oacute;lo cambia la presentaci&oacute;n.
</p>

<!-- ===== EJEMPLO COMPLETO ===== -->
<h3 style="color:#89dceb; margin-top:14px; margin-bottom:4px;">&#128196; Ejemplo completo resuelto</h3>
<pre style="background:#0d0d1a; padding:12px 16px; border-radius:8px; color:#cdd6f4; font-size:12px; line-height:1.7; margin:0;">
Sistema:
  E1:  2x +  y -  z =  8
  E2: -3x -  y + 2z = -11
  E3: -2x +  y + 2z = -3

Matriz aumentada inicial:
  [  2   1  -1 |  8  ]
  [ -3  -1   2 | -11 ]
  [ -2   1   2 |  -3 ]

Gauss-Jordan aplica 9 pasos:
  1. Inicio (snapshot)
  2. R1 &harr; R2  (pivoteo: -3 tiene mayor valor absoluto en col 1)
  3. R1 &larr; R1 / (-3)    (normalizar pivote a 1)
  4. R2 &larr; R2 - 2*R1   (eliminar col 1 en fila 2)
  5. R3 &larr; R3 - (-2)*R1 (eliminar col 1 en fila 3)
  6. Pivote col 2 ya es 1
  7. R1 &larr; R1 - (1/3)*R2 (eliminar col 2 en fila 1)
  8. R3 &larr; R3 - (5/3)*R2 (eliminar col 2 en fila 3)
  9. Pivote col 3 ...

Resultado:  x = 2,  y = 3,  z = -1</pre>

<br/>
<p style="color:#6c7086; font-size:10px; text-align:center; margin:8px 0 0 0;">
  Gauss-Jordan Master Pro &mdash; Desarrollado con Python 3 + PySide6 &mdash; Aritm&eacute;tica exacta con fractions.Fraction
</p>
</body>
"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Manual de Usuario")
        self.resize(720, 680)
        self.setStyleSheet("background:#12121f; color:#cdd6f4;")
        lay = QVBoxLayout(self)
        lay.setContentsMargins(16, 16, 16, 16)
        lay.setSpacing(10)
        browser = QTextBrowser()
        browser.setHtml(self.MANUAL_HTML)
        browser.setStyleSheet(
            "QTextBrowser{background:#1a1a2e;border:1px solid #2a2a40;"
            "border-radius:10px;padding:12px;font-size:13px;color:#cdd6f4;}"
        )
        lay.addWidget(browser)
        btn = QPushButton("  Cerrar")
        btn.setIcon(qta.icon("fa5s.times", color="#0d0d1a"))
        btn.setFixedHeight(38)
        btn.setStyleSheet(
            "QPushButton{background:qlineargradient(x1:0,y1:0,x2:1,y2:0,"
            "stop:0 #7c6ff2,stop:1 #89b4fa);color:#0d0d1a;border:none;"
            "border-radius:8px;font-weight:700;}"
            "QPushButton:hover{background:#b4d0ff;}"
        )
        btn.clicked.connect(self.accept)
        lay.addWidget(btn)


# ── Ventana Principal ────────────────────────────────────────────────────────
class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gauss-Jordan Master Pro")
        self.resize(1100, 820)
        self.setMinimumSize(900, 650)
        self.setStyleSheet(MAIN_STYLE)

        central = QWidget()
        self.setCentralWidget(central)
        root = QVBoxLayout(central)
        root.setContentsMargins(26, 18, 26, 18)
        root.setSpacing(16)

        # ── Encabezado ───────────────────────────────────────────────────────
        hdr = QHBoxLayout()
        hdr.setSpacing(8)
        title_col = QVBoxLayout()
        title_col.setSpacing(1)
        t = QLabel("Gauss-Jordan Master Pro")
        t.setObjectName("title")
        s = QLabel("ANALISIS NUMERICO  ·  ALGEBRA LINEAL  ·  ING. SISTEMAS")
        s.setObjectName("subtitle")
        title_col.addWidget(t)
        title_col.addWidget(s)
        hdr.addLayout(title_col)
        hdr.addStretch()
        for icon_name, tooltip, slot, color in [
            ("fa5s.trash-alt",       "Limpiar campos",    self._clear_all, "#f38ba8"),
            ("fa5s.question-circle", "Manual de usuario", self._show_help, "#89b4fa"),
        ]:
            b = QPushButton()
            b.setIcon(qta.icon(icon_name, color=color))
            b.setToolTip(tooltip)
            b.setFixedSize(44, 44)
            b.setCursor(Qt.PointingHandCursor)
            b.clicked.connect(slot)
            hdr.addWidget(b)
        root.addLayout(hdr)

        # ── Cuerpo 2 columnas ────────────────────────────────────────────────
        body = QHBoxLayout()
        body.setSpacing(26)
        root.addLayout(body)

        # ════════ COLUMNA IZQUIERDA ════════
        left = QVBoxLayout()
        left.setSpacing(14)
        left.setAlignment(Qt.AlignTop)
        body.addLayout(left, 16)

        # Ecuaciones
        eq_group = QGroupBox("INGRESA LAS ECUACIONES")
        eq_lay = QVBoxLayout(eq_group)
        eq_lay.setContentsMargins(16, 34, 16, 14)
        eq_lay.setSpacing(10)
        self.eq_inputs = []
        hints = ["Ej: 2x + y - z = 8", "Ej: -3x - y + 2z = -11", "Ej: -2x + y + 2z = -3"]
        for i in range(3):
            row = QHBoxLayout()
            lbl = QLabel(f"<b style='color:#89dceb;font-size:15px;'>E{i+1}</b>")
            lbl.setFixedWidth(24)
            le = QLineEdit()
            le.setPlaceholderText(hints[i])
            le.setMinimumHeight(38)
            self.eq_inputs.append(le)
            row.addWidget(lbl)
            row.addWidget(le)
            eq_lay.addLayout(row)
        left.addWidget(eq_group)

        # Ejemplos rapidos
        ex_group = QGroupBox("EJEMPLOS RAPIDOS")
        ex_lay = QVBoxLayout(ex_group)
        ex_lay.setContentsMargins(12, 30, 12, 12)
        ex_lay.setSpacing(6)
        row1, row2 = QHBoxLayout(), QHBoxLayout()
        for idx, ex in enumerate(EXAMPLES):
            btn = QPushButton(ex["label"])
            btn.setToolTip(ex["tooltip"])
            btn.setCursor(Qt.PointingHandCursor)
            btn.setFixedHeight(32)
            c, d = ex["color"], ex["dark"]
            btn.setStyleSheet(
                f"QPushButton{{background:{d};border:1px solid {c};"
                f"border-radius:8px;color:{c};font-size:12px;font-weight:600;padding:0 8px;}}"
                f"QPushButton:hover{{background:{c}25;}}"
                f"QPushButton:pressed{{background:{c}50;}}"
            )
            btn.clicked.connect(lambda _, e=ex: self._load_example(e))
            (row1 if idx < 2 else row2).addWidget(btn)
        ex_lay.addLayout(row1)
        ex_lay.addLayout(row2)
        left.addWidget(ex_group)

        # Matriz
        mat_group = QGroupBox("REPRESENTACION MATRICIAL  [A | b]")
        mat_lay = QVBoxLayout(mat_group)
        mat_lay.setContentsMargins(14, 32, 14, 14)
        mat_lay.setSpacing(12)
        self.matrix_grid = MatrixGrid()
        mat_lay.addWidget(self.matrix_grid, alignment=Qt.AlignCenter)
        self.check_fraction = QCheckBox("  Modo Fracciones (resultados exactos)")
        self.check_fraction.setChecked(True)
        self.check_fraction.stateChanged.connect(self._toggle_output_format)
        mat_lay.addWidget(self.check_fraction)
        left.addWidget(mat_group)

        # Boton principal
        self.action_btn = QPushButton("   INTERPRETAR Y RESOLVER")
        self.action_btn.setIcon(qta.icon("fa5s.magic", color="#0d0d1a"))
        self.action_btn.setObjectName("actionButton")
        self.action_btn.setCursor(Qt.PointingHandCursor)
        self.action_btn.setFixedHeight(60)
        self.action_btn.clicked.connect(self._handle_main_action)
        left.addWidget(self.action_btn)
        left.addStretch()

        # ════════ COLUMNA DERECHA ════════
        right = QVBoxLayout()
        right.setSpacing(12)
        body.addLayout(right, 32)

        right.addWidget(QLabel("<b>PROCEDIMIENTO PASO A PASO:</b>"))
        self.step_viewer = StepViewer()
        right.addWidget(self.step_viewer)

        # Banner resultado
        self.result_frame = QFrame()
        self.result_frame.setFixedHeight(58)
        self._set_banner_style("idle")
        res_lay = QHBoxLayout(self.result_frame)
        res_lay.setContentsMargins(16, 0, 16, 0)
        self.result_label = QLabel("Ingresa las ecuaciones y presiona  RESOLVER")
        self.result_label.setAlignment(Qt.AlignCenter)
        self._set_result_label_style("idle")
        res_lay.addWidget(self.result_label)
        right.addWidget(self.result_frame)

    # ── Helpers de estilo ────────────────────────────────────────────────────
    def _set_banner_style(self, mode):
        colors = {
            "idle":  ("stop:0 #1a1a30,stop:1 #1e2030", "#f9ab6e"),
            "ok":    ("stop:0 #1a2a1a,stop:1 #1a301a", "#a6e3a1"),
            "error": ("stop:0 #2a1a1a,stop:1 #2a1a1a", "#f38ba8"),
            "inf":   ("stop:0 #2a2a10,stop:1 #1a2a10", "#f9e2af"),
        }
        grad, border = colors[mode]
        self.result_frame.setStyleSheet(
            f"QFrame{{background:qlineargradient(x1:0,y1:0,x2:1,y2:0,{grad});"
            f"border:2px solid {border};border-radius:12px;}}"
        )

    def _set_result_label_style(self, mode):
        colors = {"idle": "#fab387", "ok": "#a6e3a1", "error": "#f38ba8", "inf": "#f9e2af"}
        self.result_label.setStyleSheet(
            f"color:{colors[mode]};font-weight:800;font-size:15px;border:none;"
        )

    # ── Logica ───────────────────────────────────────────────────────────────
    def _handle_main_action(self):
        if self._parse_equations_silent():
            self._solve_system()

    def _load_example(self, ex):
        for i, eq in enumerate(ex["eqs"]):
            self.eq_inputs[i].setText(eq)
        self._parse_equations_silent()

    def _parse_equations_silent(self):
        from logic.parser import parse_equation
        any_filled = any(le.text().strip() for le in self.eq_inputs)
        if not any_filled:
            return True
        for i, le in enumerate(self.eq_inputs):
            if not le.text().strip():
                QMessageBox.warning(self, "Ecuacion incompleta",
                    f"La ecuacion E{i+1} esta vacia.\n"
                    f"Completa las 3, o dejalas todas vacias para usar la matriz.")
                le.setFocus()
                return False
        try:
            for i, le in enumerate(self.eq_inputs):
                row = parse_equation(le.text().strip())
                for j, val in enumerate(row):
                    self.matrix_grid.cells[i][j].setText(str(val))
        except Exception as e:
            QMessageBox.warning(self, "Error de interpretacion",
                f"No pude interpretar una ecuacion:\n\n{e}\n\n"
                f"Formatos validos: '2x + y - z = 8'  |  '(1/2)x - y = 3'")
            return False
        return True

    def _validate_matrix(self):
        from logic.calculator import parse_fraction
        from fractions import Fraction
        for r in range(3):
            for c in range(4):
                txt = self.matrix_grid.cells[r][c].text().strip()
                if not txt:
                    QMessageBox.warning(self, "Celda vacia",
                        f"Fila {r+1}, columna {c+1} esta vacia.\nIngresa 0 si el coeficiente es cero.")
                    self.matrix_grid.cells[r][c].setFocus()
                    return False
                try:
                    parse_fraction(txt)
                except ValueError:
                    QMessageBox.warning(self, "Valor invalido",
                        f"'{txt}' (fila {r+1}, col {c+1}) no es un numero valido.\n"
                        f"Usa entero, decimal (1.5) o fraccion (1/2).")
                    self.matrix_grid.cells[r][c].setFocus()
                    return False
        for r in range(3):
            from logic.calculator import parse_fraction
            from fractions import Fraction
            if all(parse_fraction(self.matrix_grid.cells[r][c].text().strip()) == Fraction(0)
                   for c in range(3)):
                QMessageBox.warning(self, "Fila de ceros",
                    f"La fila {r+1} tiene todos los coeficientes en cero.")
                return False
        return True

    def _solve_system(self):
        if not self._validate_matrix():
            return
        try:
            data = self.matrix_grid.get_matrix_data()
            solver = GaussJordanSolver(data)
            status, res = solver.solve()
            self.step_viewer.set_steps(solver.steps)

            if status == "Solucion unica":
                x, y, z = res
                fmt = lambda v: str(v) if self.check_fraction.isChecked() else f"{float(v):.4f}"
                self.result_label.setText(
                    f"SOLUCION UNICA:  x = {fmt(x)}   |   y = {fmt(y)}   |   z = {fmt(z)}")
                self._set_banner_style("ok"); self._set_result_label_style("ok")
            elif status == "No tiene solucion":
                self.result_label.setText("SIN SOLUCION — Sistema inconsistente (0 = c != 0)")
                self._set_banner_style("error"); self._set_result_label_style("error")
            else:
                self.result_label.setText("INFINITAS SOLUCIONES — Sistema indeterminado")
                self._set_banner_style("inf"); self._set_result_label_style("inf")
        except Exception as e:
            QMessageBox.critical(self, "Error de calculo", str(e))

    def _toggle_output_format(self):
        self.step_viewer.toggle_format(self.check_fraction.isChecked())
        if self.step_viewer.steps:
            self._solve_system()

    def _clear_all(self):
        for le in self.eq_inputs:
            le.clear()
        for row in self.matrix_grid.cells:
            for cell in row:
                cell.clear()
        self.step_viewer.set_steps([])
        self.result_label.setText("Ingresa las ecuaciones y presiona  RESOLVER")
        self._set_banner_style("idle"); self._set_result_label_style("idle")

    def _show_help(self):
        HelpDialog(self).exec()
