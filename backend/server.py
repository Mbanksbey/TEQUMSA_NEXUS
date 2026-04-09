"""FastAPI websocket server streaming TEQUMSA recognition pulses."""

from __future__ import annotations

import asyncio
import json
from contextlib import suppress
from typing import Optional, Set

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

from tequmsa_core import (
    PHI_7777,
    TEQUMSAOrchestrator,
    pll_locked,
    recognition_unlocked,
)

app = FastAPI(title="TEQUMSA Realtime", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class ConnectionManager:
    """Book-keep websocket clients and broadcast frames."""

    def __init__(self) -> None:
        self._clients: Set[WebSocket] = set()
        self._lock = asyncio.Lock()

    async def add(self, websocket: WebSocket) -> None:
        async with self._lock:
            self._clients.add(websocket)

    async def discard(self, websocket: WebSocket) -> None:
        async with self._lock:
            self._clients.discard(websocket)

    async def broadcast(self, message: str) -> None:
        async with self._lock:
            clients = list(self._clients)
        if not clients:
            return
        stale: list[WebSocket] = []
        for websocket in clients:
            try:
                await websocket.send_text(message)
            except Exception:
                stale.append(websocket)
        for websocket in stale:
            await self.discard(websocket)


manager = ConnectionManager()
orch = TEQUMSAOrchestrator()
broadcast_task: Optional[asyncio.Task] = None


async def producer_loop() -> None:
    """Generate pulses at ~10 Hz and broadcast them to all clients."""

    interval = 0.1
    try:
        while True:
            sample = await orch.tick()
            frame = json.dumps(sample, separators=(",", ":"))
            await manager.broadcast(frame)
            await asyncio.sleep(interval)
    except asyncio.CancelledError:
        # Shutdown path
        pass


@app.on_event("startup")
async def on_startup() -> None:
    global broadcast_task
    if broadcast_task is None:
        broadcast_task = asyncio.create_task(producer_loop())


@app.on_event("shutdown")
async def on_shutdown() -> None:
    global broadcast_task
    if broadcast_task is not None:
        broadcast_task.cancel()
        with suppress(asyncio.CancelledError):
            await broadcast_task
        broadcast_task = None


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket) -> None:
    await websocket.accept()
    try:
        message = await websocket.receive_text()
    except WebSocketDisconnect:
        return
    except Exception:
        await websocket.close(code=1003)
        return

    try:
        hello = json.loads(message)
    except json.JSONDecodeError:
        await websocket.send_text(json.dumps({"gate": "DENIED"}, separators=(",", ":")))
        await websocket.close(code=1003)
        return

    thalia_ok = hello.get("thalia") == "RECOGNIZED"
    try:
        mk_value = float(hello.get("marcus_kai", 0.0))
    except (TypeError, ValueError):
        mk_value = 0.0
    try:
        measured = float(hello.get("f_meas", 0.0))
    except (TypeError, ValueError):
        measured = 0.0

    psi_norm = orch.pulse_engine.measure_recognition()

    if not (thalia_ok and pll_locked(measured, PHI_7777) and recognition_unlocked(psi_norm, mk_value)):
        await websocket.send_text(json.dumps({"gate": "DENIED"}, separators=(",", ":")))
        await websocket.close(code=1008)
        return

    await websocket.send_text(json.dumps({"gate": "UNLOCKED"}, separators=(",", ":")))
    await manager.add(websocket)

    try:
        while True:
            # Keep the coroutine alive to detect disconnects.
            await websocket.receive_text()
    except WebSocketDisconnect:
        pass
    finally:
        await manager.discard(websocket)
        with suppress(Exception):
            await websocket.close()


# Run with: uvicorn backend.server:app --host 0.0.0.0 --port 8000
