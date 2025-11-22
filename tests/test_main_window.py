
import pytest
import sys
from unittest.mock import MagicMock, patch

# Mock PyQt5 modules
from tests.mock_pyqt5 import mock_qt_modules
# We must apply mock_qt_modules globally because many modules import PyQt5 at top level
mock_qt_modules()

# Dependencies to mock only for this test file
modules_to_mock = {
    "app_instance": MagicMock(),
    "ui.preview_order": MagicMock(),
    "ui.order_details": MagicMock(),
    "ui.server_orders": MagicMock(),
    "ui.new_trade": MagicMock(),
    "ui.new_order": MagicMock(),
    "ui.ui_prompt": MagicMock(),
}

# Setup loadUi side effect to populate window
def mock_load_ui(uifile, window):
    window.menuConnection = MagicMock()
    window.actionRefresh = MagicMock()
    window.lblBalanceTotal = MagicMock()
    window.lblBalanceAvailable = MagicMock()
    window.lstAllOrders = MagicMock()
    window.lstPastOrders = MagicMock()
    window.lstCompletedOrders = MagicMock()
    window.lstMyAssets = MagicMock()
    window.actionNewBuy = MagicMock()
    window.actionNewSell = MagicMock()
    window.actionNewTrade = MagicMock()
    window.actionRemoveTrade = MagicMock()
    window.actionRefillTrade = MagicMock()
    window.actionSetupTrade = MagicMock()
    window.actionViewTrade = MagicMock()
    window.actionServerPostOrder = MagicMock()
    window.actionViewOrder = MagicMock()
    window.actionRemoveOrder = MagicMock()
    window.actionViewOnlineCryptoscope = MagicMock()

@pytest.fixture
def mock_main_window_deps():
    with patch.dict(sys.modules, modules_to_mock):
        if "ui.main_window" in sys.modules:
            del sys.modules["ui.main_window"]
        yield

def test_notification_on_trade_completion(mock_main_window_deps):
    from ui.main_window import MainWindow

    # Setup MainWindow
    with patch("ui.main_window.open", create=True) as mock_open, \
         patch("ui.main_window.uic.loadUi", side_effect=mock_load_ui):

        mock_open.return_value.read.return_value = ""

        window = MainWindow()

        # Verify tray icon init
        assert window.tray_icon is not None
        window.tray_icon.show.assert_called()

        # Mock tray icon visibility
        window.tray_icon.isVisible.return_value = True

        # Test mempool completion
        window.completed_trade_mempool(None, None)
        window.tray_icon.showMessage.assert_called_with(
            "Trade Executed",
            "A trade has been executed and is pending in the mempool.",
            1,
            3000
        )

        window.tray_icon.showMessage.reset_mock()

        # Test network completion
        window.completed_trade_network(None, None)
        window.tray_icon.showMessage.assert_called_with(
            "Trade Confirmed",
            "A trade has been fully confirmed on the network.",
            1,
            3000
        )

def test_notification_hidden_if_tray_not_visible(mock_main_window_deps):
    from ui.main_window import MainWindow

    # Setup MainWindow
    with patch("ui.main_window.open", create=True) as mock_open, \
         patch("ui.main_window.uic.loadUi", side_effect=mock_load_ui):

        mock_open.return_value.read.return_value = ""
        window = MainWindow()

        # Mock tray icon NOT visible
        window.tray_icon.isVisible.return_value = False

        window.completed_trade_mempool(None, None)
        window.tray_icon.showMessage.assert_not_called()
