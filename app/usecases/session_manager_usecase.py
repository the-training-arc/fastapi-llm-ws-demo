import json
from typing import Dict, List

from fastapi import WebSocket


class ConnectionManager:
    _instance = None
    _initialized = False

    def __new__(cls, session_messages: Dict[str, List[dict]] = None):
        if cls._instance is None:
            cls._instance = super(ConnectionManager, cls).__new__(cls)
        return cls._instance

    def __init__(self, session_messages: Dict[str, List[dict]] = None):
        if not self._initialized:
            self.session_messages = session_messages
            self.active_connections: list[WebSocket] = []
            self.connection_sessions: Dict[WebSocket, str] = {}
            self._initialized = True

    async def connect(self, websocket: WebSocket, session_id: str):
        """Connect a connection to a session

        :param WebSocket websocket: The connection to connect
        :param str session_id: The ID of the session to connect to
        """
        await websocket.accept()
        self.active_connections.append(websocket)
        self.connection_sessions[websocket] = session_id

        # Initialize message list for this session
        if session_id not in self.session_messages:
            self.session_messages[session_id] = []

    def disconnect(self, websocket: WebSocket):
        """Disconnect a connection

        :param WebSocket websocket: The connection to disconnect
        """
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
        if websocket in self.connection_sessions:
            del self.connection_sessions[websocket]

    async def send_personal_message(self, message: str, websocket: WebSocket, persist: bool = True):
        """Send a message to a specific connection

        :param str message: The message to send
        :param WebSocket websocket: The connection to send the message to
        :param bool persist: Whether to persist the message in the session messages
        """
        await websocket.send_text(message)

        if persist and websocket in self.connection_sessions:
            session_id = self.connection_sessions[websocket]
            try:
                message_data = json.loads(message)
                self.session_messages[session_id].append(message_data)

            except json.JSONDecodeError:
                self.session_messages[session_id].append(message)

    async def broadcast(self, message: str):
        """Broadcast a message to all connections

        :param str message: The message to broadcast
        """
        for connection in self.active_connections:
            await connection.send_text(message)

    def get_session_messages(self, session_id: str) -> List[dict]:
        """Get all messages for a specific session

        :param str session_id: The ID of the session to get the messages for
        :return List[dict]: The list of messages for the session
        """
        return self.session_messages.get(session_id, [])

    def clear_session_messages(self, session_id: str):
        """Clear messages for a specific session

        :param str session_id: The ID of the session to clear the messages for
        """
        if session_id in self.session_messages:
            del self.session_messages[session_id]

    def store_message(self, session_id: str, message: dict):
        """Store a message in the session messages

        :param str session_id: The ID of the session to store the message in
        :param dict message: The message to store
        """
        self.session_messages[session_id].append(message)

    def get_connections_with_session_id(self, session_id: str) -> List[WebSocket]:
        """Get all connections for a specific session

        :param str session_id: The ID of the session to get the connections for
        :return List[WebSocket]: The list of connections for the session
        """
        return [
            connection
            for connection in self.active_connections
            if self.connection_sessions[connection] == session_id
        ]

    async def send_message_to_all_connections_with_session_id(
        self, session_id: str, message: str, persist: bool = True
    ):
        """Send a message to all connections with a specific session ID

        :param str session_id: The ID of the session to send the message to
        :param str message: The message to send
        :param bool persist: Whether to persist the message in the session messages
        """
        for connection in self.get_connections_with_session_id(session_id):
            await self.send_personal_message(message, connection, persist)
