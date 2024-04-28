import uvicorn
from fastapi import FastAPI
from fastapi.responses import JSONResponse, Response

from config import API_PORT
import db_manager

app = FastAPI()


def user_log(login, actionId):
    # print(f"############-- {tag}:{msg} --############ ")
    db_manager.write_user_log(login, actionId)


@app.get("/api/auth/{login}&{passwd}")
async def auth(login, passwd):
    result = db_manager.get_passwd_by_login(login, passwd)
    if result is None:
        return Response(status_code=500)
    if result:
        user_log(login=login, actionId=1)
        return Response(status_code=200)
    else:
        user_log(login=login, actionId=2)
        return Response(status_code=401)


@app.get("/api/user/check/{login}")
async def check_admin(login):
    is_admin = db_manager.get_status_by_login(login)
    if is_admin:
        return JSONResponse(status_code=200, content={"admin": True})
    else:
        return JSONResponse(status_code=200, content={"admin": False})


@app.get("/api/process/temp/{tank_id}")
async def get_current_temp(tank_id):
    temp, datetime = db_manager.get_current_temp(tank_id)
    return JSONResponse(status_code=200, content={
        "datetime": datetime.isoformat(),
        "value": temp
    })


@app.get("/api/process/stop/{tank_id}&{login}")
async def emergency_stop(tank_id, login):
    db_manager.emergency_stop(tank_id, login)

@app.get("/api/process/start/{tank_id}")
async def init_tank(tank_id):
    db_manager.init_tank(tank_id)


# @app.post("/api/auth/")
# async def auth(data=Body()):
#     print(data)
#     login = data["login"]
#     passwd = data["passwd"]
#     server_log(tag="Login", msg=f"Login={login}, Passwd={passwd}")
#

# @app.websocket("/ws/time")
# async def websocket_endpoint(websocket: WebSocket):
#     await websocket.accept()
#     while True:
#         await websocket.send_text(str(datetime.datetime.now()))
#         await sleep(1)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=API_PORT, log_level="info")
    # db_manager.write_user_log("admin", 1)
