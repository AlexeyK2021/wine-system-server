import json
import uvicorn
from fastapi import FastAPI, WebSocket
from fastapi.responses import Response, JSONResponse
from starlette.websockets import WebSocketDisconnect

import db_manager
import influx_db_manager
from config import API_PORT

app = FastAPI()


@app.get("/api/auth/login={login}&passwd={passwd}")
async def auth(login, passwd):
    result = db_manager.auth_user(login, passwd)
    if result is None:
        return Response(status_code=500)
    if result:
        return Response(status_code=200)
    else:
        return Response(status_code=401)


@app.get("/api/tanks")
async def get_tanks():
    return JSONResponse(status_code=200, content=db_manager.get_tanks())


@app.get("/api/process/stop/tank={tank_id}&user={login}")
def emergency_stop(tank_id: int, login):
    db_manager.emergency_stop(tank_id, login)
    return Response(status_code=200)


@app.get("/api/process/start/tank={tank_id}&user={login}")
async def init_tank(tank_id: int, login):
    db_manager.init_tank(tank_id, login)
    return Response(status_code=200)


@app.websocket("/api/tanks/ws")
async def get_tank_info(websocket: WebSocket):
    try:
        await websocket.accept()
        while True:
            tank_id = int(await websocket.receive_text())
            eq_data = influx_db_manager.get_tank_state(tank_id)
            tank_state = db_manager.get_current_tank_state(tank_id)
            data = {"tank_id": tank_id} | tank_state | eq_data
            json_data = json.dumps(data, indent=4)
            await websocket.send_text(json_data)
    except WebSocketDisconnect:
        print(f"Websocket on {websocket.base_url.hostname} disconnected")


if __name__ == "__main__":
    try:
        uvicorn.run(app, host="0.0.0.0", port=API_PORT, log_level="info")
    except KeyboardInterrupt:
        print("Shutting down API server")
