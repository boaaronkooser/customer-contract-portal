from fastapi import FastAPI

app = FastAPI(title="Customer Contract Management Portal API")

@app.get("/")
def root():
    return {"status": "ok"}
