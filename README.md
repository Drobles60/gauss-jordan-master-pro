# Gauss-Jordan 3x3 - Herramienta Didáctica

Este proyecto es una aplicación de escritorio moderna desarrollada en Python con **PySide6** para resolver sistemas de ecuaciones lineales 3x3 utilizando el método de **Gauss-Jordan**.

## Características
- **Interfaz Moderna**: Diseño limpio y profesional con soporte para fracciones y decimales.
- **Modo Paso a Paso**: Visualiza cada operación elemental aplicada a la matriz.
- **Panel Didáctico**: Explicaciones detalladas en español sobre el proceso matemático.
- **Calculadora Integrada**: Evalúa expresiones matemáticas simples.
- **Precisión Total**: Uso interno de la clase `fractions.Fraction` para evitar errores de redondeo.

## Instalación

1. Asegúrate de tener Python 3.9 o superior instalado.
2. Clona o descarga este repositorio.
3. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

## Ejecución

Para iniciar la aplicación, ejecuta:
```bash
python main.py
```

## Estructura del Proyecto
- `main.py`: Punto de entrada de la aplicación.
- `logic/`: Motores de cálculo (Gauss-Jordan y calculadora).
- `ui/`: Componentes de la interfaz gráfica y estilos.
- `explicacion_metodo.md`: Documentación teórica del método.
