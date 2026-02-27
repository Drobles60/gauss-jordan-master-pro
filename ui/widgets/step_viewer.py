from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QScrollArea, QFrame, QGridLayout
from PySide6.QtCore import Qt

class StepViewer(QScrollArea):
    """
    Componente para visualizar los pasos de la resolución como una lista de tarjetas.
    Usa colores para resaltar filas pivote y filas objetivo.
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWidgetResizable(True)
        self.setObjectName("stepViewerArea")
        
        self.container = QWidget()
        self.layout = QVBoxLayout(self.container)
        self.layout.setAlignment(Qt.AlignTop)
        self.layout.setSpacing(15)
        self.layout.setContentsMargins(10, 10, 10, 10)
        self.setWidget(self.container)
        
        self.steps = []
        self.show_fraction = True

    def set_steps(self, steps):
        self.steps = steps
        self._update_ui()

    def toggle_format(self, show_fraction):
        self.show_fraction = show_fraction
        self._update_ui()

    def _update_ui(self):
        # Limpiar layout de forma eficiente
        while self.layout.count():
            item = self.layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
                
        if not self.steps:
            return
            
        colors = {
            'pivot': "#2e3b3e",  # Greenish dark
            'target': "#3e2e2e", # Reddish dark
            'swap': "#3e3b2e"    # Yellowish dark
        }
        
        border_colors = {
            'pivot': "#a6e3a1",
            'target': "#f38ba8",
            'swap': "#f9e2af"
        }
            
        for i, step in enumerate(self.steps):
            frame = QFrame()
            # Estilo de tarjeta premium
            frame.setStyleSheet(f"QFrame {{ background-color: #181825; border: 1px solid #313244; border-radius: 12px; }}")
            flayout = QVBoxLayout(frame)
            flayout.setContentsMargins(15, 15, 15, 15)
            
            # Encabezado del paso
            header_layout = QHBoxLayout()
            op_lbl = QLabel(f"PASO {i+1}: {step['operation']}")
            op_lbl.setStyleSheet("color: #89b4fa; font-weight: 800; font-size: 14px; border: none;")
            header_layout.addWidget(op_lbl)
            header_layout.addStretch()
            flayout.addLayout(header_layout)
            
            # Matriz con colores
            grid_container = QWidget()
            grid_container.setStyleSheet("background: transparent; border: none;")
            grid = QGridLayout(grid_container)
            grid.setSpacing(5)
            
            mat = step['matrix']
            highlights = step.get('highlight_rows', {})
            
            for r in range(3):
                row_role = highlights.get(r)
                bg_color = colors.get(row_role, "#1e1e2e")
                brd_color = border_colors.get(row_role, "#45475a")
                
                for c in range(4):
                    val = mat[r][c]
                    text = str(val) if self.show_fraction else f"{float(val):.4f}"
                    lbl = QLabel(text)
                    lbl.setAlignment(Qt.AlignCenter)
                    
                    # Estilo dinámico basado en el rol de la fila
                    lbl_style = f"""
                        padding: 8px; 
                        border: 1px solid {brd_color}; 
                        border-radius: 4px;
                        background-color: {bg_color}; 
                        color: #cdd6f4; 
                        font-weight: {'bold' if row_role else 'normal'};
                    """
                    lbl.setStyleSheet(lbl_style)
                    grid.addWidget(lbl, r, c)
            
            flayout.addWidget(grid_container)
            
            # Explicación detallada
            exp_lbl = QLabel(step['explanation'])
            exp_lbl.setWordWrap(True)
            exp_lbl.setStyleSheet("color: #a6adc8; font-size: 13px; font-style: italic; border: none; margin-top: 10px;")
            flayout.addWidget(exp_lbl)
            
            self.layout.addWidget(frame)
