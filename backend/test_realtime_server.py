import pytest
from fastapi.testclient import TestClient
from starlette.websockets import WebSocketDisconnect

from server import app
from tequmsa_core import PHI_7777, pll_locked, recognition_unlocked


@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client


def test_pll_locked_thresholds():
    assert pll_locked(PHI_7777)
    assert pll_locked(PHI_7777 * 1.004)
    assert not pll_locked(PHI_7777 * 1.01)


def test_recognition_gate():
    assert recognition_unlocked(0.9, 1.0)
    assert not recognition_unlocked(0.5, 1.0)
    assert not recognition_unlocked(0.9, 0.5)


def test_websocket_handshake_unlocks(client):
    with client.websocket_connect("/ws") as websocket:
        websocket.send_json(
            {
                "thalia": "RECOGNIZED",
                "marcus_kai": 10930.81,
                "f_meas": 12583.45,
            }
        )
        message = websocket.receive_json()
        assert message["gate"] == "UNLOCKED"
        frame = websocket.receive_json()
        assert "pulse" in frame
        assert "synergy" in frame


def test_websocket_handshake_denied(client):
    with client.websocket_connect("/ws") as websocket:
        websocket.send_json(
            {
                "thalia": "RECOGNIZED",
                "marcus_kai": 0.1,
                "f_meas": 14000.0,
            }
        )
        message = websocket.receive_json()
        assert message["gate"] == "DENIED"
        with pytest.raises(WebSocketDisconnect):
            websocket.receive_text()
