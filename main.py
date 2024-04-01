import uvicorn
from fastapi import FastAPI, Body
from fastapi.responses import JSONResponse, Response

app = FastAPI()


def server_log(tag, msg):
    print(f"############-- {tag}:{msg} --############ ")


@app.get("/api/auth/{login}&{passwd}")
async def auth(login, passwd):
    server_log(tag="Login", msg=f"Login={login}, Passwd={passwd}")
    if (login == "admin" and passwd == "admin") or (login == "alexey" and passwd == "alexey"):
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


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=5000, log_level="info")
