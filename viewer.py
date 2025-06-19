import pyqtgraph.opengl as gl
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
import numpy as np

class MeshViewer(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.view = gl.GLViewWidget()
        self.layout.addWidget(self.view)

        self.setLayout(self.layout)
        self.mesh_item = None
        self.error_items = []

    def clear(self):
        self.view.clear()
        self.mesh_item = None
        self.error_items = []

    def display_mesh(self, mesh, highlight_edges=None):
        self.clear()
        faces = np.array(mesh.faces)
        vertices = np.array(mesh.vertices)
        colors = np.ones((faces.shape[0], 4)) * [0.6, 0.8, 1.0, 0.7]
        self.mesh_item = gl.GLMeshItem(vertexes=vertices, faces=faces, faceColors=colors, smooth=False, drawEdges=True)
        self.view.addItem(self.mesh_item)

        if highlight_edges is not None and len(highlight_edges) > 0:
            max_edges = 100  # Safety: never draw too many lines at once
            for edge in highlight_edges[:max_edges]:
                v = mesh.vertices[np.array(edge)]
                edge_line = gl.GLLinePlotItem(pos=v, color=(1,0,0,1), width=3, antialias=True)
                self.view.addItem(edge_line)
