from main import app
from fastapi import FastAPI, Request


@app.middleware("http")
async def check_auth(request: Request, call_next):
    print("MIDDLEWARE")
    print(request.dir)
    response = await call_next(request)
    return response