import sys
from PySide6.QtWidgets import QApplication
from ui.main_window import MainWindow

def main():
    # Inicializa la aplicación Qt
    app = QApplication(sys.argv)
    
    # Crea y muestra la ventana principal
    window = MainWindow()
    window.show()
    
    # Ejecuta el bucle de eventos
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
