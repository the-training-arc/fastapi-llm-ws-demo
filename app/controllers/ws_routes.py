from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.usecases.llm_usecase import LLMUsecase
from app.models.wellness_profile import WellnessProfileIn

ws_routes = APIRouter()


class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)


manager = ConnectionManager()


@ws_routes.websocket('/wellness_profile')
async def wellness_profile(websocket: WebSocket):
    llm_usecase = LLMUsecase()

    await manager.connect(websocket)

    try:
        while True:
            data = await websocket.receive_text()
            if not data:
                continue

            result = llm_usecase.generate_questions_from_llm(data, WellnessProfileIn)
            result_str = result.model_dump_json()
            await manager.send_personal_message(result_str, websocket)

    except WebSocketDisconnect:
        manager.disconnect(websocket)
