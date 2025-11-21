
import pytest
import sys
from unittest.mock import MagicMock

# Mock PyQt5 before importing util
from tests.mock_pyqt5 import mock_qt_modules
mock_qt_modules()

from util import join_utxo, split_utxo, make_prefill, make_transfer

def test_join_utxo():
    assert join_utxo("txid123", 0) == "txid123-0"
    assert join_utxo("abc", 10) == "abc-10"

def test_split_utxo():
    assert split_utxo("txid123-0") == ("txid123", 0)
    assert split_utxo("abc-10") == ("abc", 10)

def test_make_prefill():
    asset = {"name": "MY_ASSET"}
    prefill = make_prefill(asset, 10, 5)
    assert prefill == {"asset": "MY_ASSET", "quantity": 10, "unit_price": 5}

    # Test defaults
    prefill_default = make_prefill(asset)
    assert prefill_default == {"asset": "MY_ASSET", "quantity": 1, "unit_price": 1}

def test_make_transfer():
    transfer = make_transfer("MY_ASSET", 50)
    assert transfer == {"transfer": {"MY_ASSET": 50.0}}

    transfer_str = make_transfer("MY_ASSET", "50.5")
    assert transfer_str == {"transfer": {"MY_ASSET": 50.5}}
