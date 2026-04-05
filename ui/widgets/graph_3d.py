"""
graph_3d.py — Visualización 3D sin lag (rendering en QThread)
"""
import numpy as np
from fractions import Fraction

from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Qt, QThread, Signal, QObject


class _RenderWorker(QObject):
    """Hilo de trabajo: genera los datos numpy sin tocar la UI."""
    finished = Signal(list, object)   # (planos_data, solution)

    def __init__(self, matrix, solution):
        super().__init__()
        self.matrix = matrix
        self.solution = solution

    def run(self):
        rng = 4
        grid = np.linspace(-rng, rng, 18)   # 18×18 → rápido y suficiente
        xx, yy = np.meshgrid(grid, grid)
        planes = []

        for i in range(3):
            a = float(self.matrix[i][0])
            b = float(self.matrix[i][1])
            c = float(self.matrix[i][2])
            d = float(self.matrix[i][3])
            planes.append((a, b, c, d, xx, yy, rng))

        self.finished.emit(planes, self.solution)


class Graph3DWidget(QWidget):
    """Widget 3D sin lag: el cálculo pesado ocurre en un QThread."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumHeight(360)
        self._thread = None

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.fig = Figure(figsize=(5, 4), dpi=90, facecolor='#12121f')
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setStyleSheet("background:#12121f; border-radius:12px;")
        layout.addWidget(self.canvas)

        self._placeholder()

    def _placeholder(self):
        self.fig.clear()
        ax = self.fig.add_subplot(111, facecolor='#12121f')
        ax.text(0.5, 0.5,
                "La gráfica 3D aparecerá\naquí tras resolver el sistema",
                ha='center', va='center', fontsize=13,
                color='#585b70', transform=ax.transAxes)
        ax.axis('off')
        self.canvas.draw_idle()

    def plot(self, matrix, solution=None):
        """Inicia el render en un hilo separado para no congelar la UI."""
        # Cancelar hilo anterior si aún corre
        if self._thread and self._thread.isRunning():
            self._thread.quit()
            self._thread.wait()

        self._thread = QThread()
        self._worker = _RenderWorker(matrix, solution)
        self._worker.moveToThread(self._thread)
        self._thread.started.connect(self._worker.run)
        self._worker.finished.connect(self._on_data_ready)
        self._worker.finished.connect(self._thread.quit)
        self._thread.start()

    def _on_data_ready(self, planes, solution):
        """Dibuja en el hilo principal una vez que los datos están listos."""
        self.fig.clear()
        ax = self.fig.add_subplot(111, projection='3d', facecolor='#12121f')
        self._style_axes(ax)

        colors = ['#89b4fa', '#a6e3a1', '#f9e2af']
        names  = ['Plano E1', 'Plano E2', 'Plano E3']

        for (a, b, c, d, xx, yy, rng), color, name in zip(planes, colors, names):
            try:
                if abs(c) > 1e-10:
                    zz = (d - a*xx - b*yy) / c
                    zz = np.clip(zz, -rng*2, rng*2)
                    ax.plot_surface(xx, yy, zz, alpha=0.30, color=color, edgecolor='none')
                elif abs(b) > 1e-10:
                    zz_r = np.linspace(-rng, rng, 18)
                    xx2, zz2 = np.meshgrid(np.linspace(-rng, rng, 18), zz_r)
                    yy2 = np.clip((d - a*xx2) / b, -rng*2, rng*2)
                    ax.plot_surface(xx2, yy2, zz2, alpha=0.30, color=color, edgecolor='none')
                elif abs(a) > 1e-10:
                    yy3, zz3 = np.meshgrid(np.linspace(-rng, rng, 18), np.linspace(-rng, rng, 18))
                    ax.plot_surface(np.full_like(yy3, d/a), yy3, zz3,
                                    alpha=0.30, color=color, edgecolor='none')
            except Exception:
                pass
            ax.plot([], [], [], color=color, linewidth=4, label=name)

        if solution is not None:
            sx, sy, sz = [float(v) for v in solution]
            ax.scatter([sx], [sy], [sz], color='#f38ba8', s=200,
                       edgecolors='#ffffff', linewidths=1.5, zorder=10,
                       label=f'({sx:.2g}, {sy:.2g}, {sz:.2g})')
            for axis, vals in [('x', ([sx,sx],[sy,sy],[-4,4])),
                                ('y', ([sx,sx],[-4,4],[sz,sz])),
                                ('z', ([-4,4],[sy,sy],[sz,sz]))]:
                ax.plot(*vals, color='#f38ba8', alpha=0.25, linewidth=1, linestyle='--')

        ax.legend(loc='upper left', fontsize=9, framealpha=0.25,
                  facecolor='#1e1e30', edgecolor='#3a3a55', labelcolor='#cdd6f4')
        self.canvas.draw_idle()

    def _style_axes(self, ax):
        ax.set_xlabel('x', color='#89b4fa', fontsize=10, labelpad=6)
        ax.set_ylabel('y', color='#a6e3a1', fontsize=10, labelpad=6)
        ax.set_zlabel('z', color='#f9e2af', fontsize=10, labelpad=6)
        for pane in (ax.xaxis.pane, ax.yaxis.pane, ax.zaxis.pane):
            pane.fill = False
            pane.set_edgecolor('#2a2a40')
        ax.tick_params(colors='#585b70', labelsize=7)
        for line in (ax.xaxis.line, ax.yaxis.line, ax.zaxis.line):
            line.set_color('#2a2a40')
        ax.grid(True, color='#2a2a40', linewidth=0.4, linestyle=':')
        self.fig.patch.set_facecolor('#12121f')
