"""
STARK INDUSTRIES SQL — WebSocket Attack Monitor
Real-time event stream for the attack monitor dashboard panel.
"""
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import List, Dict
import asyncio
import json
from datetime import datetime, timezone

router = APIRouter(prefix="/ws", tags=["monitor"])

# Store active WebSocket connections per challenge
connections: Dict[str, List[WebSocket]] = {}


async def broadcast_event(challenge_id: int, event: dict):
    """Broadcast an event to all connected clients watching this challenge."""
    key = str(challenge_id)
    if key not in connections:
        return
    dead = []
    for ws in connections[key]:
        try:
            await ws.send_json(event)
        except Exception:
            dead.append(ws)
    for ws in dead:
        connections[key].remove(ws)


async def broadcast_global(event: dict):
    """Broadcast to all connected clients."""
    for key in list(connections.keys()):
        dead = []
        for ws in connections[key]:
            try:
                await ws.send_json(event)
            except Exception:
                dead.append(ws)
        for ws in dead:
            connections[key].remove(ws)


@router.websocket("/monitor/{challenge_id}")
async def monitor_websocket(websocket: WebSocket, challenge_id: int):
    """WebSocket endpoint for live attack monitor."""
    await websocket.accept()
    key = str(challenge_id)
    if key not in connections:
        connections[key] = []
    connections[key].append(websocket)

    # Send connection established event
    await websocket.send_json({
        "type": "CONNECTED",
        "challenge_id": challenge_id,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "message": f"Connected to challenge {challenge_id} monitor",
    })

    try:
        while True:
            # Keep connection alive — ping every 30s
            await asyncio.sleep(30)
            await websocket.send_json({
                "type": "PING",
                "timestamp": datetime.now(timezone.utc).isoformat(),
            })
    except WebSocketDisconnect:
        if key in connections and websocket in connections[key]:
            connections[key].remove(websocket)


@router.websocket("/monitor/global/stream")
async def global_monitor(websocket: WebSocket):
    """Global monitor WebSocket — all events."""
    await websocket.accept()
    key = "global"
    if key not in connections:
        connections[key] = []
    connections[key].append(websocket)

    await websocket.send_json({
        "type": "CONNECTED",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "message": "Connected to global attack monitor",
    })

    try:
        while True:
            await asyncio.sleep(30)
            await websocket.send_json({
                "type": "PING",
                "timestamp": datetime.now(timezone.utc).isoformat(),
            })
    except WebSocketDisconnect:
        if key in connections and websocket in connections[key]:
            connections[key].remove(websocket)
