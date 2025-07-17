from fastapi import FastAPI
from file_tools import list_files, create_directory

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/files/")
def get_files(path: str = "."):
    return {"files": list_files(path)}

@app.post("/directories")
def create_new_directory(path: str):
    return create_directory(path)
