import uvicorn
from fastapi import FastAPI, Body, WebSocket
from fastapi.responses import JSONResponse, Response

from config import API_PORT

app = FastAPI()


def server_log(tag, msg):
    print(f"############-- {tag}:{msg} --############ ")


@app.get("/api/auth/{login}&{passwd}")
async def auth(login, passwd):
    server_log(tag="Login", msg=f"Login={login}, Passwd={passwd}")
    if (login == "admin" and passwd == "8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918") or (
            login == "alexey" and passwd == "d217e1716cb7b36f8be65117f625a1e39d22fd585528632391bb74310a4f255d"):
        return Response(status_code=200)
    else:
        return Response(status_code=403)


@app.get("/api/user/check/{login}")
async def check_admin(login):
    if login == "admin":
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
