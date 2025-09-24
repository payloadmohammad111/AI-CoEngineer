from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"msg": "Hello AI Co-Engineer"}
