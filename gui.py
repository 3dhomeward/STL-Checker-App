from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QFileDialog, QMessageBox, QApplication
)
from PyQt5.QtGui import QColor, QPalette
from PyQt5.QtCore import Qt
from viewer import MeshViewer
from mesh_utils import STLMeshHandler

class STLCheckerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('STL Manifold Checker')
        self.setGeometry(100, 100, 1100, 600)

        self.mesh_handler = STLMeshHandler()
        self.viewer = MeshViewer()
        self.info_label = QLabel('Open an STL file to start.')
        self.info_label.setAlignment(Qt.AlignCenter)
        self.info_label.setStyleSheet("font-size: 18px; padding: 8px;")

        self.open_btn = QPushButton('Open STL File')
        self.open_btn.clicked.connect(self.open_file)

        # Instructions label (now on the right panel)
        self.instructions_label = QLabel(
            "3D View Controls:\n"
            "  • Rotate: Left mouse drag\n"
            "  • Pan: Right mouse drag or Ctrl+Left mouse drag\n"
            "  • Zoom: Mouse wheel"
        )
        self.instructions_label.setAlignment(Qt.AlignLeft)
        self.instructions_label.setStyleSheet("font-size: 12px; color: #444; margin-top: 10px;")

        # Layouts
        vbox = QVBoxLayout()
        hbox = QHBoxLayout()
        controls = QVBoxLayout()
        controls.addWidget(self.info_label)
        controls.addWidget(self.open_btn)
        controls.addWidget(self.instructions_label)
        controls.addStretch(1)
        hbox.addWidget(self.viewer, 6)
        hbox.addLayout(controls, 2)
        vbox.addLayout(hbox)
        self.setLayout(vbox)

    def set_status(self, msg, is_good):
        self.info_label.setText(msg)
        palette = self.info_label.palette()
        if is_good:
            # Green background
            palette.setColor(QPalette.Window, QColor(170, 255, 170))
            self.info_label.setAutoFillBackground(True)
        else:
            # Red background
            palette.setColor(QPalette.Window, QColor(255, 200, 200))
            self.info_label.setAutoFillBackground(True)
        self.info_label.setPalette(palette)

    def open_file(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Open STL File", "", "STL Files (*.stl)")
        if filename:
            self.info_label.setText("Loading file...")
            QApplication.processEvents()
            self.mesh_handler.load_mesh(filename)
            self.info_label.setText("Checking manifold status...")
            QApplication.processEvents()
            msg, is_good = self.mesh_handler.check_manifold()
            self.set_status(msg, is_good)
            self.viewer.display_mesh(self.mesh_handler.mesh, self.mesh_handler.nonmanifold_edges)
