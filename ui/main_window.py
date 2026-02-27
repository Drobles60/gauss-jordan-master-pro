import qtawesome as qta
from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QLabel, QMessageBox, QCheckBox,
                             QGroupBox, QLineEdit, QGridLayout, QApplication, QFrame, QScrollArea)
from PySide6.QtCore import Qt, QEvent
from ui.widgets.matrix_grid import MatrixGrid
from ui.widgets.step_viewer import StepViewer
from logic.solver import GaussJordanSolver
from ui.styles import MAIN_STYLE

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gauss-Jordan Master Pro")
        self.resize(1150, 800)
        self.setStyleSheet(MAIN_STYLE)
        
        # Central widget
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(20)
        
        # Header
        header_layout = QHBoxLayout()
        title = QLabel("Gauss-Jordan Master Pro")
        title.setObjectName("title")
        header_layout.addWidget(title)
        header_layout.addStretch()
        main_layout.addLayout(header_layout)
        
        # Main Body: 2 Columns
        body_layout = QHBoxLayout()
        body_layout.setSpacing(40)
        main_layout.addLayout(body_layout)
        
        # --- COLUMNA IZQUIERDA: ENTRADA DE DATOS (CENTRADITA) ---
        left_panel = QVBoxLayout()
        left_panel.setSpacing(20)
        left_panel.setAlignment(Qt.AlignTop)
        body_layout.addLayout(left_panel, 18) # Stretch 1.8
        
        # 1. Grupo de Ecuaciones
        eq_group = QGroupBox("CONFIGURACIÓN DEL SISTEMA")
        eq_layout = QVBoxLayout(eq_group)
        eq_layout.setContentsMargins(20, 35, 20, 20)
        eq_layout.setSpacing(15)
        
        self.eq_inputs = []
        for i in range(3):
            row = QHBoxLayout()
            lbl = QLabel(f"<b>E{i+1}:</b>")
            lbl.setFixedWidth(30)
            le = QLineEdit()
            le.setPlaceholderText(f"Escribe aquí (ej: 2x + y = 5)")
            le.setObjectName(f"eq_{i}")
            self.eq_inputs.append(le)
            row.addWidget(lbl)
            row.addWidget(le)
            eq_layout.addLayout(row)
        left_panel.addWidget(eq_group)
        
        # 2. Matriz (Solo visual/edición directa si se desea)
        input_group = QGroupBox("REPRESENTACIÓN MATRICIAL")
        input_layout = QVBoxLayout(input_group)
        input_layout.setContentsMargins(15, 30, 15, 20)
        input_layout.setSpacing(15)
        
        self.matrix_grid = MatrixGrid()
        input_layout.addWidget(self.matrix_grid, alignment=Qt.AlignCenter)
        
        # Modo fracciones
        self.check_fraction = QCheckBox("Modo Fracciones (Resultados Exactos)")
        self.check_fraction.setChecked(True)
        self.check_fraction.stateChanged.connect(self._toggle_output_format)
        input_layout.addWidget(self.check_fraction)
        left_panel.addWidget(input_group)
        
        # BOTÓN ÚNICO DE ACCIÓN (MAGIA)
        self.action_btn = QPushButton(" INTERPRETAR Y RESOLVER")
        self.action_btn.setIcon(qta.icon("fa5s.magic", color="#11111b"))
        self.action_btn.setObjectName("actionButton")
        self.action_btn.setCursor(Qt.PointingHandCursor)
        self.action_btn.setFixedHeight(65)
        self.action_btn.clicked.connect(self._handle_main_action)
        left_panel.addWidget(self.action_btn)
        
        left_panel.addStretch()
        
        # --- COLUMNA DERECHA: RESULTADOS Y PASOS ---
        right_panel = QVBoxLayout()
        right_panel.setSpacing(15)
        body_layout.addLayout(right_panel, 30) # Stretch 3.0
        
        right_panel.addWidget(QLabel("<b>PROCEDIMIENTO PASO A PASO:</b>"))
        self.step_viewer = StepViewer()
        right_panel.addWidget(self.step_viewer)
        
        # Banner de Resultado final
        self.result_container = QFrame()
        self.result_container.setStyleSheet("background-color: #1e1e2e; border: 2px solid #fab387; border-radius: 12px;")
        res_layout = QVBoxLayout(self.result_container)
        self.result_label = QLabel("Ingresa las ecuaciones para ver la solución")
        self.result_label.setAlignment(Qt.AlignCenter)
        self.result_label.setStyleSheet("color: #fab387; font-weight: 900; font-size: 18px; border: none;")
        res_layout.addWidget(self.result_label)
        right_panel.addWidget(self.result_container)

    def _handle_main_action(self):
        """Orquestador: Parsea y entonces Resuelve."""
        # 1. Intentar parsear ecuaciones primero
        if self._parse_equations_silent():
            # 2. Si hay datos, resolver
            self._solve_system()

    def _parse_equations_silent(self):
        """Parsea las ecuaciones sin mostrar warnings a menos que todas estén vacías."""
        from logic.parser import parse_equation
        any_data = False
        try:
            for i, le in enumerate(self.eq_inputs):
                text = le.text().strip()
                if not text: continue
                any_data = True
                row_data = parse_equation(text)
                for j, val in enumerate(row_data):
                    self.matrix_grid.cells[i][j].setText(str(val))
            
            if not any_data:
                # Si no hay ecuaciones, intentar resolver lo que ya esté en la matriz
                return True 
            return True
        except Exception as e:
            QMessageBox.warning(self, "Error de Interpretación", f"No pude entender una de las ecuaciones:\n{e}")
            return False

    def _solve_system(self):
        try:
            data = self.matrix_grid.get_matrix_data()
            solver = GaussJordanSolver(data)
            status, res = solver.solve()
            
            self.step_viewer.set_steps(solver.steps)
            
            if status == "Solución única":
                x, y, z = res
                fmt = lambda v: str(v) if self.check_fraction.isChecked() else f"{float(v):.4f}"
                self.result_label.setText(f"SOLUCIÓN FINAL: x = {fmt(x)},  y = {fmt(y)},  z = {fmt(z)}")
            else:
                self.result_label.setText(f"ESTADO: {status}\n{res}")
                
        except Exception as e:
            QMessageBox.critical(self, "Error de Cálculo", str(e))

    def _toggle_output_format(self):
        self.step_viewer.toggle_format(self.check_fraction.isChecked())
        if self.step_viewer.steps:
            self._solve_system()
