from fastapi import FastAPI

from app.controllers.wellness_profile_routes import wellness_profile
from app.controllers.wellness_profile_ws_routes import ws_routes


def ws_controller(app: FastAPI):
    app.include_router(ws_routes, prefix='/ws', tags=['Websocket Endpoints'])
    app.include_router(wellness_profile, prefix='/profile', tags=['Wellness REST Profile'])
