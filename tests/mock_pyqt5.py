
import sys
from unittest.mock import MagicMock

def mock_qt_modules():
    modules = [
        "PyQt5",
        "PyQt5.QtCore",
        "PyQt5.QtGui",
        "PyQt5.QtWidgets",
        "PyQt5.uic"
    ]
    for mod_name in modules:
        if mod_name not in sys.modules:
            sys.modules[mod_name] = MagicMock()

    # Specifically mock QFrame and QObject if needed, but MagicMock handles it usually.
    # However, for inheritance to work in util.py: class QTwoLineRowWidget (QFrame):
    # we need QFrame to be a class.

    class MockQFrame:
        def __init__(self, parent=None): pass
        def setLayout(self, layout): pass
        def setFrameStyle(self, style): pass
        def setLineWidth(self, width): pass

    sys.modules["PyQt5.QtWidgets"].QFrame = MockQFrame
    sys.modules["PyQt5.QtWidgets"].QLabel = MagicMock
    sys.modules["PyQt5.QtWidgets"].QVBoxLayout = MagicMock
    sys.modules["PyQt5.QtWidgets"].QHBoxLayout = MagicMock
    sys.modules["PyQt5.QtWidgets"].QMessageBox = MagicMock()
    sys.modules["PyQt5.QtWidgets"].QMessageBox.Information = 1
    sys.modules["PyQt5.QtWidgets"].QMessageBox.Yes = 1
    sys.modules["PyQt5.QtWidgets"].QMessageBox.No = 0

    # QtCore
    sys.modules["PyQt5.QtCore"].QObject = MagicMock
    sys.modules["PyQt5.QtCore"].Qt = MagicMock()
    sys.modules["PyQt5.QtCore"].Qt.WindowFlags = int

    # QtGui
    sys.modules["PyQt5.QtGui"].QPixmap = MagicMock
