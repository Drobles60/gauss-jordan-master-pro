"""
styles.py — Hoja de estilos global de la aplicación
Paleta: Catppuccin Mocha mejorada con degradados y efectos premium.
"""

MAIN_STYLE = """
/* ── Ventana y widgets base ── */
QMainWindow, QDialog {
    background-color: #0d0d1a;
}

QWidget {
    font-family: 'Segoe UI', 'Inter', sans-serif;
    color: #cdd6f4;
    font-size: 14px;
}

/* ── Grupos ── */
QGroupBox {
    border: 1px solid #2a2a40;
    border-radius: 14px;
    margin-top: 28px;
    background-color: #12121f;
    padding: 5px;
}

QGroupBox::title {
    subcontrol-origin: margin;
    left: 18px;
    padding: 4px 14px;
    color: #89dceb;
    font-weight: 700;
    font-size: 11px;
    letter-spacing: 1.5px;
    background-color: #1a1a2e;
    border: 1px solid #2a2a40;
    border-radius: 6px;
}

/* ── Entradas de texto ── */
QLineEdit {
    background-color: #1e1e30;
    border: 2px solid #3a3a55;
    border-radius: 10px;
    padding: 9px 12px;
    font-size: 14px;
    color: #e0e6ff;
    selection-background-color: #585b99;
}

QLineEdit:focus {
    border: 2px solid #89b4fa;
    background-color: #22223a;
}

QLineEdit:hover {
    border: 2px solid #585b70;
}

QLineEdit[invalid="true"] {
    border: 2px solid #f38ba8;
    background-color: #2a1a20;
}

QLineEdit::placeholder {
    color: #585b70;
}

/* ── Botones generales ── */
QPushButton {
    background-color: #1e1e30;
    border: 1px solid #3a3a55;
    border-radius: 10px;
    padding: 10px 20px;
    font-weight: 600;
    color: #cdd6f4;
    font-size: 13px;
}

QPushButton:hover {
    background-color: #2a2a45;
    border: 1px solid #585b99;
    color: #e0e6ff;
}

QPushButton:pressed {
    background-color: #585b99;
    color: #ffffff;
}

/* ── Botón de acción principal ── */
QPushButton#actionButton {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #7c6ff2, stop:0.5 #89b4fa, stop:1 #74c7ec);
    color: #0d0d1a;
    border: none;
    font-size: 15px;
    font-weight: 800;
    border-radius: 14px;
    letter-spacing: 0.5px;
}

QPushButton#actionButton:hover {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #9a90ff, stop:0.5 #b4d0ff, stop:1 #94e2ff);
}

QPushButton#actionButton:pressed {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #5a52cc, stop:0.5 #6a94da, stop:1 #54a7cc);
}

/* ── Botones de ejemplos ── */
QPushButton.exampleBtn {
    background-color: #1a2a1a;
    border: 1px solid #2ea043;
    border-radius: 8px;
    color: #a6e3a1;
    font-size: 12px;
    padding: 6px 10px;
}

QPushButton.exampleBtn:hover {
    background-color: #1e3a1e;
    border-color: #3dd457;
    color: #ceffd6;
}

/* ── Etiquetas ── */
QLabel#title {
    font-size: 28px;
    font-weight: 900;
    color: #89b4fa;
    letter-spacing: 1px;
}

QLabel#subtitle {
    font-size: 12px;
    color: #585b70;
    letter-spacing: 2px;
    font-weight: 600;
}

/* ── Scroll Areas ── */
QScrollArea {
    border: none;
    background: transparent;
}

QScrollBar:vertical {
    background: #12121f;
    width: 8px;
    border-radius: 4px;
}

QScrollBar::handle:vertical {
    background: #3a3a55;
    border-radius: 4px;
    min-height: 30px;
}

QScrollBar::handle:vertical:hover {
    background: #89b4fa;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}

/* ── Checkbox ── */
QCheckBox {
    spacing: 10px;
    color: #a6adc8;
    font-size: 13px;
}

QCheckBox::indicator {
    width: 18px;
    height: 18px;
    border-radius: 5px;
    border: 2px solid #3a3a55;
    background-color: #1e1e30;
}

QCheckBox::indicator:checked {
    background-color: #89b4fa;
    border-color: #89b4fa;
    image: url(none);
}

QCheckBox::indicator:hover {
    border-color: #89b4fa;
}

/* ── Pestañas ── */
QTabWidget::pane {
    border: 1px solid #2a2a40;
    background: #12121f;
    border-radius: 12px;
}

QTabBar::tab {
    background: #1a1a2e;
    padding: 10px 22px;
    margin-right: 4px;
    border-top-left-radius: 8px;
    border-top-right-radius: 8px;
    color: #a6adc8;
    font-weight: 600;
    border: 1px solid #2a2a40;
    border-bottom: none;
}

QTabBar::tab:selected {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #89b4fa, stop:1 #74c7ec);
    color: #0d0d1a;
    font-weight: 800;
}

QTabBar::tab:hover:!selected {
    background: #22223a;
    color: #e0e6ff;
}

/* ── Text Browser ── */
QTextBrowser {
    background-color: #12121f;
    border: 1px solid #2a2a40;
    border-radius: 12px;
    padding: 15px;
    font-size: 14px;
    color: #cdd6f4;
    selection-background-color: #585b99;
}

/* ── Tooltips ── */
QToolTip {
    background-color: #1e1e30;
    color: #cdd6f4;
    border: 1px solid #89b4fa;
    border-radius: 6px;
    padding: 6px 10px;
    font-size: 13px;
}

/* ── Message Boxes ── */
QMessageBox {
    background-color: #12121f;
}

QMessageBox QLabel {
    color: #cdd6f4;
    font-size: 14px;
}
"""
