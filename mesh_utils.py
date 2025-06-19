import trimesh
import numpy as np
import subprocess
import os

class STLMeshHandler:
    def __init__(self):
        self.mesh = None
        self.last_file = None
        self.nonmanifold_edges = None

    def load_mesh(self, filename):
        self.mesh = trimesh.load_mesh(filename, process=True)
        self.last_file = filename
        print(f"Loaded mesh with {len(self.mesh.faces)} faces, {len(self.mesh.vertices)} vertices, {len(self.mesh.edges_unique)} unique edges")

    def check_manifold(self):
        if self.mesh.is_watertight:
            self.nonmanifold_edges = np.array([])
            return ("STL is manifold (watertight). No repair needed.", True)
        # Find all edges
        all_edges = self.mesh.edges_sorted
        unique_edges, edge_counts = np.unique(all_edges, axis=0,         return_counts=True)
        # Non-manifold: edges used by != 2 faces (boundary or overconnected)
        nonmanifold_mask = edge_counts != 2
        self.nonmanifold_edges = unique_edges[nonmanifold_mask]
        count = len(self.nonmanifold_edges)
        return (f"Found {count} non-manifold edges. Model is NOT manifold.", False)


def open_in_blender(stl_path):
    try:
        subprocess.Popen(['blender', stl_path])
    except FileNotFoundError:
        try:
            from PyQt5.QtWidgets import QFileDialog, QMessageBox
            exe, _ = QFileDialog.getOpenFileName(None, "Select Blender Executable", "", "Executable Files (*.exe)")
            if exe:
                subprocess.Popen([exe, stl_path])
            else:
                QMessageBox.warning(None, "Blender Not Found", "Could not open Blender. Make sure it's installed and try again.")
        except Exception:
            print("Could not open Blender.")
