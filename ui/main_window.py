"""
main_window.py — Ventana principal de Gauss-Jordan Master Pro
"""
import qtawesome as qta
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QMessageBox, QCheckBox,
    QGroupBox, QLineEdit, QFrame, QDialog,
    QTextBrowser, QTabWidget, QScrollArea, QSizePolicy
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

from ui.widgets.matrix_grid import MatrixGrid
from ui.widgets.step_viewer import StepViewer
from ui.widgets.graph_3d import Graph3DWidget
from logic.solver import GaussJordanSolver
from ui.styles import MAIN_STYLE

# ── Ejemplos predefinidos ────────────────────────────────────────────────────
EXAMPLES = [
    {
        "label": "Ejemplo 1",
        "color": "#a6e3a1", "dark": "#1a2a1a",
        "tooltip": "Solución única: x=2, y=3, z=-1",
        "eqs": ["2x + y - z = 8", "-3x - y + 2z = -11", "-2x + y + 2z = -3"],
    },
    {
        "label": "Ejemplo 2",
        "color": "#a6e3a1", "dark": "#1a2a1a",
        "tooltip": "Solución única: x=1, y=-1, z=2",
        "eqs": ["x - 2y + 3z = 9", "-x + 3y = -4", "2x - 5y + 5z = 17"],
    },
    {
        "label": "Sin Solución",
        "color": "#f38ba8", "dark": "#2a1a1a",
        "tooltip": "Sistema inconsistente (sin solución)",
        "eqs": ["x + y + z = 6", "2x + 2y + 2z = 14", "3x + 3y + 3z = 20"],
    },
    {
        "label": "∞ Soluciones",
        "color": "#f9e2af", "dark": "#2a2a10",
        "tooltip": "Sistema indeterminado (infinitas soluciones)",
        "eqs": ["x + 2y + 3z = 6", "2x + 4y + 6z = 12", "3x + 6y + 9z = 18"],
    },
]

# ── Diálogo de Ayuda ─────────────────────────────────────────────────────────
class HelpDialog(QDialog):
    MANUAL_HTML = """
    <h2 style="color:#89b4fa;">Manual de Usuario — Gauss-Jordan Master Pro</h2>
    <hr style="border-color:#2a2a40;"/>
    <h3 style="color:#89dceb;">¿Qué hace esta aplicación?</h3>
    <p>Resuelve sistemas de <b>3 ecuaciones lineales con 3 incógnitas</b> (x, y, z)
    usando el método de <b>Gauss-Jordan con pivoteo parcial</b>.</p>

    <h3 style="color:#89dceb;">Ingreso de datos</h3>
    <p><b>Por ecuaciones (texto libre):</b></p>
    <ul>
      <li><code>2x + y - z = 8</code> — enteros</li>
      <li><code>(1/2)x + y - z = 1</code> — fracción con paréntesis</li>
      <li><code>0.5x - y + z = 3</code> — decimal</li>
      <li><code>-x + 3y = -4</code> — coeficiente implícito</li>
    </ul>
    <p><b>Por la matriz [A|b]:</b> llena las celdas directamente (columna dorada = término independiente).</p>
    <p><b>Ejemplos rápidos:</b> carga sistemas predefinidos con un clic.</p>

    <h3 style="color:#89dceb;">Interpretar resultados</h3>
    <ul>
      <li><span style="color:#a6e3a1;">Verde</span> = Solución única (x, y, z)</li>
      <li><span style="color:#f38ba8;">Rojo</span> = Sin solución (sistema inconsistente)</li>
      <li><span style="color:#f9e2af;">Amarillo</span> = Infinitas soluciones</li>
    </ul>
    <p><b>Pasos:</b> Verde = fila pivote · Rojo = fila modificada · Amarillo = filas intercambiadas.</p>
    <p><b>Gráfica 3D:</b> punto rojo = solución. Azul/Verde/Amarillo = Planos E1/E2/E3.</p>

    <h3 style="color:#89dceb;">Ejemplo</h3>
    <pre style="background:#1a1a2e;padding:10px;border-radius:8px;color:#cdd6f4;">
E1:  2x + y  - z  =  8
E2: -3x - y  + 2z = -11
E3: -2x + y  + 2z = -3
→  x = 2,  y = 3,  z = -1</pre>
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Manual de Usuario")
        self.resize(620, 580)
        self.setStyleSheet("background:#12121f; color:#cdd6f4;")
        lay = QVBoxLayout(self)
        lay.setContentsMargins(18, 18, 18, 18)
        lay.setSpacing(10)
        browser = QTextBrowser()
        browser.setHtml(self.MANUAL_HTML)
        browser.setStyleSheet(
            "QTextBrowser{background:#1a1a2e;border:1px solid #2a2a40;"
            "border-radius:10px;padding:14px;font-size:13px;color:#cdd6f4;}"
        )
        lay.addWidget(browser)
        btn = QPushButton("  Cerrar")
        btn.setIcon(qta.icon("fa5s.times", color="#0d0d1a"))
        btn.setFixedHeight(40)
        btn.setStyleSheet(
            "QPushButton{background:qlineargradient(x1:0,y1:0,x2:1,y2:0,"
            "stop:0 #7c6ff2,stop:1 #89b4fa);color:#0d0d1a;border:none;"
            "border-radius:8px;font-weight:700;font-size:13px;}"
            "QPushButton:hover{background:#b4d0ff;}"
        )
        btn.clicked.connect(self.accept)
        lay.addWidget(btn)


# ── Ventana Principal ────────────────────────────────────────────────────────
class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gauss-Jordan Master Pro")
        self.resize(1220, 860)
        self.setMinimumSize(1000, 700)
        self.setStyleSheet(MAIN_STYLE)

        self._last_matrix   = None
        self._last_solution = None

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
        s = QLabel("ANÁLISIS NUMÉRICO  ·  ÁLGEBRA LINEAL  ·  ING. SISTEMAS")
        s.setObjectName("subtitle")
        title_col.addWidget(t)
        title_col.addWidget(s)
        hdr.addLayout(title_col)
        hdr.addStretch()

        for icon_name, tooltip, slot, color in [
            ("fa5s.trash-alt",       "Limpiar campos",    self._clear_all,  "#f38ba8"),
            ("fa5s.question-circle", "Manual de usuario", self._show_help,  "#89b4fa"),
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

        # ════════════════════════════════════════════════
        # COLUMNA IZQUIERDA
        # ════════════════════════════════════════════════
        left = QVBoxLayout()
        left.setSpacing(14)
        left.setAlignment(Qt.AlignTop)
        body.addLayout(left, 16)

        # ── Grupo Ecuaciones ─────────────────────────────
        eq_group = QGroupBox("INGRESA LAS ECUACIONES")
        eq_lay   = QVBoxLayout(eq_group)
        eq_lay.setContentsMargins(16, 34, 16, 14)
        eq_lay.setSpacing(10)

        self.eq_inputs = []
        hints = [
            "Ej: 2x + y - z = 8",
            "Ej: -3x - y + 2z = -11",
            "Ej: -2x + y + 2z = -3",
        ]
        for i in range(3):
            row = QHBoxLayout()
            lbl = QLabel(f"<b style='color:#89dceb; font-size:15px;'>E{i+1}</b>")
            lbl.setFixedWidth(24)
            le = QLineEdit()
            le.setPlaceholderText(hints[i])
            le.setObjectName(f"eq_{i}")
            le.setMinimumHeight(38)
            self.eq_inputs.append(le)
            row.addWidget(lbl)
            row.addWidget(le)
            eq_lay.addLayout(row)
        left.addWidget(eq_group)

        # ── Grupo Ejemplos Rápidos ───────────────────────
        ex_group = QGroupBox("EJEMPLOS RÁPIDOS")
        ex_lay   = QVBoxLayout(ex_group)
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
                f"QPushButton:hover{{background:{c}25;border:1px solid {c};}}"
                f"QPushButton:pressed{{background:{c}50;}}"
            )
            btn.clicked.connect(lambda _, e=ex: self._load_example(e))
            (row1 if idx < 2 else row2).addWidget(btn)

        ex_lay.addLayout(row1)
        ex_lay.addLayout(row2)
        left.addWidget(ex_group)

        # ── Grupo Matriz [A|b] ───────────────────────────
        mat_group = QGroupBox("REPRESENTACIÓN MATRICIAL  [A | b]")
        mat_lay   = QVBoxLayout(mat_group)
        mat_lay.setContentsMargins(14, 32, 14, 14)
        mat_lay.setSpacing(12)

        self.matrix_grid = MatrixGrid()
        mat_lay.addWidget(self.matrix_grid, alignment=Qt.AlignCenter)

        self.check_fraction = QCheckBox("  Modo Fracciones (resultados exactos)")
        self.check_fraction.setChecked(True)
        self.check_fraction.stateChanged.connect(self._toggle_output_format)
        mat_lay.addWidget(self.check_fraction)
        left.addWidget(mat_group)

        # ── Botón principal ──────────────────────────────
        self.action_btn = QPushButton("   INTERPRETAR Y RESOLVER")
        self.action_btn.setIcon(qta.icon("fa5s.magic", color="#0d0d1a"))
        self.action_btn.setObjectName("actionButton")
        self.action_btn.setCursor(Qt.PointingHandCursor)
        self.action_btn.setFixedHeight(60)
        self.action_btn.clicked.connect(self._handle_main_action)
        left.addWidget(self.action_btn)
        left.addStretch()

        # ════════════════════════════════════════════════
        # COLUMNA DERECHA
        # ════════════════════════════════════════════════
        right = QVBoxLayout()
        right.setSpacing(12)
        body.addLayout(right, 32)

        # Pestañas
        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        self.tabs.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Pestaña 1: Procedimiento paso a paso
        tab_steps = QWidget()
        tsl = QVBoxLayout(tab_steps)
        tsl.setContentsMargins(0, 8, 0, 0)
        self.step_viewer = StepViewer()
        tsl.addWidget(self.step_viewer)
        self.tabs.addTab(tab_steps,
                         qta.icon("fa5s.list-ol", color="#89b4fa"),
                         "  Procedimiento Paso a Paso")

        # Pestaña 2: Gráfica 3D
        tab_graph = QWidget()
        tgl = QVBoxLayout(tab_graph)
        tgl.setContentsMargins(0, 8, 0, 0)
        self.graph_3d = Graph3DWidget()
        tgl.addWidget(self.graph_3d)

        lbl_legend = QLabel(
            "<span style='color:#89b4fa;'>■</span> Plano E1 &nbsp;&nbsp;"
            "<span style='color:#a6e3a1;'>■</span> Plano E2 &nbsp;&nbsp;"
            "<span style='color:#f9e2af;'>■</span> Plano E3 &nbsp;&nbsp;"
            "<span style='color:#f38ba8;'>●</span> Solución"
        )
        lbl_legend.setAlignment(Qt.AlignCenter)
        lbl_legend.setStyleSheet("font-size:12px; color:#a6adc8; padding:4px 0;")
        tgl.addWidget(lbl_legend)

        self.tabs.addTab(tab_graph,
                         qta.icon("fa5s.cube", color="#a6e3a1"),
                         "  Gráfica 3D")

        right.addWidget(self.tabs)

        # Banner resultado
        self.result_frame = QFrame()
        self.result_frame.setFixedHeight(58)
        self._set_banner_style("idle")
        res_lay = QHBoxLayout(self.result_frame)
        res_lay.setContentsMargins(18, 0, 18, 0)
        self.result_label = QLabel("Ingresa las ecuaciones y presiona  RESOLVER")
        self.result_label.setAlignment(Qt.AlignCenter)
        self._set_result_label_style("idle")
        res_lay.addWidget(self.result_label)
        right.addWidget(self.result_frame)

    # ──────────────────────────────────────────────────────────────────────────
    # Helpers de estilo
    # ──────────────────────────────────────────────────────────────────────────
    def _set_banner_style(self, mode):
        colors = {
            "idle":    ("stop:0 #1a1a30,stop:1 #1e2030", "#f9ab6e"),
            "ok":      ("stop:0 #1a2a1a,stop:1 #1a301a", "#a6e3a1"),
            "error":   ("stop:0 #2a1a1a,stop:1 #2a1a1a", "#f38ba8"),
            "inf":     ("stop:0 #2a2a10,stop:1 #1a2a10", "#f9e2af"),
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

    # ──────────────────────────────────────────────────────────────────────────
    # Lógica
    # ──────────────────────────────────────────────────────────────────────────
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
                QMessageBox.warning(self, "Ecuación incompleta",
                    f"La ecuación E{i+1} está vacía.\n"
                    f"Completa las 3, o déjalas todas vacías para usar la matriz.")
                le.setFocus()
                return False

        try:
            for i, le in enumerate(self.eq_inputs):
                row = parse_equation(le.text().strip())
                for j, val in enumerate(row):
                    self.matrix_grid.cells[i][j].setText(str(val))
        except Exception as e:
            QMessageBox.warning(self, "Error de interpretación",
                f"No pude interpretar una ecuación:\n\n{e}\n\n"
                f"Formatos válidos: '2x + y - z = 8'  |  '(1/2)x - y = 3'  |  '0.5x + y = 1'")
            return False
        return True

    def _validate_matrix(self):
        from logic.calculator import parse_fraction
        from fractions import Fraction
        for r in range(3):
            for c in range(4):
                txt = self.matrix_grid.cells[r][c].text().strip()
                if not txt:
                    QMessageBox.warning(self, "Celda vacía",
                        f"Fila {r+1}, columna {c+1} está vacía.\nIngresa 0 si el coeficiente es cero.")
                    self.matrix_grid.cells[r][c].setFocus()
                    return False
                try:
                    parse_fraction(txt)
                except ValueError:
                    QMessageBox.warning(self, "Valor inválido",
                        f"'{txt}' (fila {r+1}, col {c+1}) no es un número válido.\n"
                        f"Usa entero, decimal (1.5) o fracción (1/2).")
                    self.matrix_grid.cells[r][c].setFocus()
                    return False
        for r in range(3):
            from logic.calculator import parse_fraction
            from fractions import Fraction
            if all(parse_fraction(self.matrix_grid.cells[r][c].text().strip()) == Fraction(0)
                   for c in range(3)):
                QMessageBox.warning(self, "Fila de ceros",
                    f"La fila {r+1} tiene todos los coeficientes en cero.\n"
                    f"El sistema no está bien planteado.")
                return False
        return True

    def _solve_system(self):
        if not self._validate_matrix():
            return
        try:
            data   = self.matrix_grid.get_matrix_data()
            solver = GaussJordanSolver(data)
            status, res = solver.solve()

            self.step_viewer.set_steps(solver.steps)
            self._last_matrix = data

            if status == "Solución única":
                self._last_solution = res
                fmt = lambda v: str(v) if self.check_fraction.isChecked() else f"{float(v):.4f}"
                x, y, z = res
                self.result_label.setText(f"✓  SOLUCIÓN ÚNICA:  x = {fmt(x)}   |   y = {fmt(y)}   |   z = {fmt(z)}")
                self._set_banner_style("ok");  self._set_result_label_style("ok")
            elif status == "No tiene solución":
                self._last_solution = None
                self.result_label.setText("✗  SIN SOLUCIÓN — Sistema inconsistente (0 = c ≠ 0)")
                self._set_banner_style("error"); self._set_result_label_style("error")
            else:
                self._last_solution = None
                self.result_label.setText("∞  INFINITAS SOLUCIONES — Sistema indeterminado")
                self._set_banner_style("inf"); self._set_result_label_style("inf")

            # Gráfica en hilo separado (sin lag)
            self.graph_3d.plot(data, self._last_solution)
            self.tabs.setCurrentIndex(0)   # mantener en Procedimiento

        except Exception as e:
            QMessageBox.critical(self, "Error de cálculo", str(e))

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
        self.graph_3d._placeholder()
        self.result_label.setText("Ingresa las ecuaciones y presiona  RESOLVER")
        self._set_banner_style("idle"); self._set_result_label_style("idle")
        self.tabs.setCurrentIndex(0)

    def _show_help(self):
        HelpDialog(self).exec()
