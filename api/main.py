import uvicorn
from fastapi import FastAPI
from fastapi.responses import JSONResponse, Response

from config import API_PORT
from db.db_manager import get_user_by_login

app = FastAPI()


def user_log(tag, msg):
    print(f"############-- {tag}:{msg} --############ ")


@app.get("/api/auth/{login}&{passwd}")
async def auth(login, passwd):
    user = get_user_by_login(login)
    if user.password == passwd:
        user_log(tag="Вход", msg=f"Login={login}, Passwd={passwd}")
        return Response(status_code=200)
    else:
        user_log(tag="Неудачная попытка входа", msg=f"Login={login}, Passwd={passwd}")
        return Response(status_code=401)


@app.get("/api/user/check/{login}")
async def check_admin(login):
    user = get_user_by_login(login)
    if user.type.is_admin:
        return JSONResponse(status_code=200, content={"admin": True})
    else:
        return JSONResponse(status_code=200, content={"admin": False})


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
    uvicorn.run(app, host="127.0.0.1", port=API_PORT, log_level="info")
