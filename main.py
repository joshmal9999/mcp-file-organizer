from fastapi import FastAPI
from file_tools import list_files, create_directory
from gemini_client import get_ai_response

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

@app.get("/chat")
def chat_with_ai(query: str):
    response = get_ai_response(query)
    return {"response": response}