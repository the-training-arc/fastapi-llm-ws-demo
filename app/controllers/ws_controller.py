from fastapi import FastAPI

from app.controllers.ws_routes import ws_routes


def ws_controller(app: FastAPI):
    app.include_router(ws_routes, prefix='/ws', tags=['Websocket Endpoints'])
