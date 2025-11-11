from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()

@app.get("/")
def read_root():
    return JSONResponse(content={"message": "Hello from regular FastAPI!"})

@app.get("/ping")
def ping():
    return JSONResponse(content={"status": "ok"})
