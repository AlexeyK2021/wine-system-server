from fastapi import FastAPI
from fastapi.responses import JSONResponse, Response

app = FastAPI()


def server_log(tag, msg):
    print(f"############-- {tag}:{msg} --############ ")


@app.get("/api/auth/{login}&{passwd}")
async def auth(login, passwd):
    server_log(tag="Login", msg=f"Login={login}, Passwd={passwd}")
    if login == "admin" and passwd == "admin":
        return JSONResponse(
            status_code=200,
            content={"admin": 1}
        )
    elif login == "alexey" and passwd == "alexey":
        return JSONResponse(
            status_code=200,
            content={"admin": 0}
        )
    else:
        return Response(
            status_code=403
        )


@app.get("/")
async def main():
    return False
