from fastapi import FastAPI

from app.api.router import api_router

app = FastAPI(title="URL Shortener")

app.include_router(api_router)


@app.get("/")
async def root():
    return {"message": "hello world"}
