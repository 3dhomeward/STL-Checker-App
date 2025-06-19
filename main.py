from gui import STLCheckerApp
from PyQt5.QtWidgets import QApplication
import sys

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = STLCheckerApp()
    window.show()
    app.exec_()
