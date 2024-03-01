import uvicorn
from fastapi import FastAPI
from models import *
from modules.response import ResponseGPT
from modules.intent import intentGPT
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health-check")
def read_root():
    return {"Main app working": "successful"}

# AI Chatbot response
@app.post("/response")
def chat_response(message: HumanMessage):
    response = ResponseGPT()
    return response.aiRespond(message)

# AI Chatbot response
@app.post("/intent")
def chat_response(message: ForIntent):
    response = intentGPT()
    return response.aiRespond(message)

if __name__=="__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=5000, log_level="info")