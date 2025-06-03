import json
from typing import Dict, List

from fastapi import WebSocket


class ConnectionManager:
    def __init__(self, session_messages: Dict[str, List[dict]]):
        self.session_messages = session_messages
        self.active_connections: list[WebSocket] = []
        self.connection_sessions: Dict[WebSocket, str] = {}

    async def connect(self, websocket: WebSocket, session_id: str):
        await websocket.accept()
        self.active_connections.append(websocket)
        self.connection_sessions[websocket] = session_id

        # Initialize message list for this session
        if session_id not in self.session_messages:
            self.session_messages[session_id] = []

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
        if websocket in self.connection_sessions:
            del self.connection_sessions[websocket]

    async def send_personal_message(self, message: str, websocket: WebSocket, persist: bool = True):
        await websocket.send_text(message)

        if persist and websocket in self.connection_sessions:
            session_id = self.connection_sessions[websocket]
            try:
                message_data = json.loads(message)
                self.session_messages[session_id].append(message_data)

            except json.JSONDecodeError:
                self.session_messages[session_id].append(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

    def get_session_messages(self, session_id: str) -> List[dict]:
        """Get all messages for a specific session"""
        return self.session_messages.get(session_id, [])

    def clear_session_messages(self, session_id: str):
        """Clear messages for a specific session"""
        if session_id in self.session_messages:
            del self.session_messages[session_id]

    def store_message(self, session_id: str, message: dict):
        self.session_messages[session_id].append(message)
