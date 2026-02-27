from PySide6.QtWidgets import QWidget, QGridLayout, QLineEdit, QToolTip
from PySide6.QtCore import Qt, Signal
from logic.calculator import parse_fraction

class MatrixGrid(QWidget):
    """
    Grid interactivo de 3x4 para ingresar la matriz aumentada.
    """
    cellChanged = Signal(int, int, str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QGridLayout(self)
        self.layout.setSpacing(10)
        self.cells = []
        self._init_grid()
        
    def _init_grid(self):
        for row in range(3):
            row_cells = []
            for col in range(4):
                edit = QLineEdit()
                edit.setAlignment(Qt.AlignCenter)
                edit.setPlaceholderText("0")
                edit.setFocusPolicy(Qt.StrongFocus)
                edit.textChanged.connect(lambda text, r=row, c=col, e=edit: self._validate_cell(e, r, c, text))
                
                # Rastrear foco
                p = self.parent()
                if p:
                    edit.installEventFilter(p)
                
                # Diseño premium para las celdas
                style = "min-width: 50px; min-height: 35px; font-weight: bold; font-size: 13px;"
                if col == 3:
                     # Color diferente para la columna de resultados (b)
                    edit.setStyleSheet(style + "background-color: #3e3b2e; border-color: #f9e2af; color: #f9e2af;")
                else:
                    edit.setStyleSheet(style)
                    
                self.layout.addWidget(edit, row, col)
                row_cells.append(edit)
            self.cells.append(row_cells)
        
        self.layout.setContentsMargins(5, 5, 5, 5)
        self.layout.setSpacing(6)

    def _validate_cell(self, widget, row, col, text):
        """Valida que el contenido sea una fracción o número válido."""
        try:
            if text.strip():
                parse_fraction(text)
            widget.setProperty("invalid", "false")
        except ValueError:
            widget.setProperty("invalid", "true")
        
        widget.style().unpolish(widget)
        widget.style().polish(widget)
        self.cellChanged.emit(row, col, text)

    def get_matrix_data(self):
        """Retorna la matriz como una lista de listas de Fractions."""
        data = []
        for row in range(3):
            row_data = []
            for col in range(4):
                text = self.cells[row][col].text()
                try:
                    row_data.append(parse_fraction(text))
                except ValueError:
                    raise ValueError(f"Error en fila {row+1}, columna {col+1}")
            data.append(row_data)
        return data

    def get_focused_cell(self):
        """Retorna el widget de la celda que tiene el foco actual."""
        for row in self.cells:
            for cell in row:
                if cell.hasFocus():
                    return cell
        return None
