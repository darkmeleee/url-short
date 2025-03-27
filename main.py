import uvicorn
from fastapi import FastAPI
from uuid import uuid4
app = FastAPI()
from fastapi.responses import RedirectResponse



dict = {}

@app.get("/")
async def root():
    return {"message": "hello world"}

@app.post("/shorten")
async def shorten(item: str):
    rand_token = uuid4()
    dict[str(rand_token)] = item
    print(dict)
    return {"message": dict[str(rand_token)], "key": rand_token}

@app.get("/link")
async def ref(link: str):
    if dict.get(link):
        return RedirectResponse(dict[link])
    else:
        return {"message": "not found :("}


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
