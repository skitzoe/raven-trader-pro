
import pytest
import sys
from unittest.mock import MagicMock, patch

# Mock PyQt5 before importing rvn_rpc
from tests.mock_pyqt5 import mock_qt_modules
mock_qt_modules()

# We need to mock AppInstance and its settings before importing rvn_rpc
# because rvn_rpc might access them or importing them might trigger things.
# However, rvn_rpc imports AppInstance at the END of the file.
# But `do_rpc` uses `AppInstance.settings.rpc_url()`.

# Let's mock AppInstance in sys.modules to avoid importing the real one which does logging setup etc.
mock_app_instance = MagicMock()
sys.modules["app_instance"] = mock_app_instance

from rvn_rpc import do_rpc, test_rpc_status

def test_do_rpc_success(mocker):
    # Mock post request
    mock_post = mocker.patch("rvn_rpc.post")
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.text = '{"result": "success", "error": null, "id": 1}'
    mock_post.return_value = mock_response

    # Mock AppInstance.settings.rpc_url()
    mock_app_instance.AppInstance.settings.rpc_url.return_value = "http://user:pass@localhost:8766"

    result = do_rpc("getinfo")
    assert result == "success"
    mock_post.assert_called_once()

def test_do_rpc_failure(mocker):
    # Mock post request returning error
    mock_post = mocker.patch("rvn_rpc.post")
    mock_response = MagicMock()
    mock_response.status_code = 500
    mock_response.text = '{"error": {"code": -1, "message": "Error"}, "result": null, "id": 1}'
    mock_post.return_value = mock_response

    # Mock AppInstance.settings.rpc_url()
    mock_app_instance.AppInstance.settings.rpc_url.return_value = "http://user:pass@localhost:8766"

    # do_rpc returns None on error (based on current implementation) or maybe the error object?
    # Looking at rvn_rpc.py:
    # if resp.status_code != 200: try: return json.loads(resp.text)

    result = do_rpc("getinfo")
    assert result == {"error": {"code": -1, "message": "Error"}, "result": None, "id": 1}

def test_do_rpc_timeout(mocker):
    # Mock timeout
    mock_post = mocker.patch("rvn_rpc.post")
    mock_post.side_effect = TimeoutError()

    mock_app_instance.AppInstance.settings.rpc_url.return_value = "http://user:pass@localhost:8766"

    # It calls AppInstance.on_exit() and exit(-1) on timeout
    # We need to mock exit to prevent test runner from exiting
    mock_exit = mocker.patch("rvn_rpc.exit")
    mock_show_error = mocker.patch("rvn_rpc.show_error")

    result = do_rpc("getinfo")

    assert result is None
    mock_app_instance.AppInstance.on_exit.assert_not_called()
    mock_exit.assert_not_called()
    mock_show_error.assert_called_once()
