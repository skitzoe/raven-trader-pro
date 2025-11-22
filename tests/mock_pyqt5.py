
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

    class MockQMainWindow:
        def __init__(self, *args, **kwargs): pass
        def setWindowTitle(self, title): pass
        def setStyleSheet(self, sheet): pass
        def windowIcon(self): return MagicMock()
        def statusBar(self): return MagicMock()
        def windowState(self): return 0
        def setWindowState(self, state): pass
        def activateWindow(self): pass

    class MockQTimer:
        def __init__(self, parent=None):
            self.timeout = MagicMock()
        def start(self, interval): pass
        def stop(self): pass

    class MockQSystemTrayIcon:
        Information = 1

        def __init__(self, parent=None):
            self.icon = None
            self.showMessage = MagicMock()
            self.show = MagicMock()
            self.isVisible = MagicMock(return_value=True)
            self.setIcon = MagicMock()

    # Constants
    class MockQMessageBox:
        Information = 1
        Yes = 1
        No = 0
        Cancel = 2
        Ok = 3
        Critical = 4

        def __init__(self, parent=None):
            self.exec_ = MagicMock(return_value=MockQMessageBox.Ok)

        def setText(self, text): pass
        def setIcon(self, icon): pass
        def setStandardButtons(self, buttons): pass
        def setDefaultButton(self, button): pass
        def setDetailedText(self, text): pass
        def setWindowTitle(self, title): pass
        def setInformativeText(self, text): pass

    sys.modules["PyQt5.QtWidgets"].QFrame = MockQFrame
    sys.modules["PyQt5.QtWidgets"].QMainWindow = MockQMainWindow
    sys.modules["PyQt5.QtWidgets"].QLabel = MagicMock
    sys.modules["PyQt5.QtWidgets"].QVBoxLayout = MagicMock
    sys.modules["PyQt5.QtWidgets"].QHBoxLayout = MagicMock
    sys.modules["PyQt5.QtWidgets"].QMessageBox = MockQMessageBox
    sys.modules["PyQt5.QtWidgets"].QAction = MagicMock
    sys.modules["PyQt5.QtWidgets"].QMenu = MagicMock
    sys.modules["PyQt5.QtWidgets"].QListWidgetItem = MagicMock
    sys.modules["PyQt5.QtWidgets"].QSystemTrayIcon = MockQSystemTrayIcon

    # QtCore
    sys.modules["PyQt5.QtCore"].QObject = MagicMock
    sys.modules["PyQt5.QtCore"].Qt = MagicMock()
    sys.modules["PyQt5.QtCore"].Qt.WindowFlags = int
    sys.modules["PyQt5.QtCore"].Qt.WindowMinimized = 1
    sys.modules["PyQt5.QtCore"].Qt.WindowActive = 2
    sys.modules["PyQt5.QtCore"].Qt.CustomContextMenu = 3
    sys.modules["PyQt5.QtCore"].QTimer = MockQTimer

    # QtGui
    sys.modules["PyQt5.QtGui"].QPixmap = MagicMock
