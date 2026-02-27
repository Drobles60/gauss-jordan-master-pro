MAIN_STYLE = """
QMainWindow {
    background-color: #11111b;
}

QWidget {
    font-family: 'Inter', 'Segoe UI', sans-serif;
    color: #cdd6f4;
}

QTabWidget::pane {
    border: 1px solid #313244;
    background: #181825;
    border-radius: 12px;
}

QTabBar::tab {
    background: #1e1e2e;
    padding: 12px 24px;
    margin-right: 4px;
    border-top-left-radius: 8px;
    border-top-right-radius: 8px;
    color: #a6adc8;
}

QTabBar::tab:selected {
    background: #89b4fa;
    color: #11111b;
    font-weight: bold;
}

QLineEdit {
    background-color: #313244;
    border: 2px solid #45475a;
    border-radius: 8px;
    padding: 8px;
    font-size: 15px;
    color: #f5e0dc;
    selection-background-color: #89b4fa;
}

QLineEdit:focus {
    border: 2px solid #89b4fa;
}

QLineEdit[invalid="true"] {
    border: 2px solid #f38ba8;
}

QPushButton {
    background-color: #313244;
    border: 1px solid #45475a;
    border-radius: 8px;
    padding: 10px 20px;
    font-weight: 600;
    color: #cdd6f4;
}

QPushButton:hover {
    background-color: #45475a;
    border: 1px solid #585b70;
}

QPushButton#actionButton {
    background-color: #89b4fa;
    color: #11111b;
    border: none;
    font-size: 16px;
}

QPushButton#actionButton:hover {
    background-color: #b4befe;
}

QGroupBox {
    border: 1px solid #313244;
    border-radius: 12px;
    margin-top: 25px;
    background-color: #181825;
}

QGroupBox::title {
    subcontrol-origin: margin;
    left: 20px;
    padding: 5px 15px;
    color: #89dceb;
    font-weight: bold;
    font-size: 13px;
    background-color: #1e1e2e;
    border: 1px solid #313244;
    border-radius: 6px;
}

QTextBrowser {
    background-color: #1e1e2e;
    border: 1px solid #313244;
    border-radius: 12px;
    padding: 15px;
    font-size: 14px;
    selection-background-color: #89b4fa;
}

QLabel#title {
    font-size: 32px;
    font-weight: 800;
    color: #89b4fa;
    margin: 10px 0;
}
"""
