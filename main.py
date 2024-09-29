from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import controllers
import models as Models

app = FastAPI()

# Configure CORS
origins = [
    "http://localhost",
    "http://localhost:3000",  # Assuming your frontend runs on port 3000
    "http://127.0.0.1",
    "http://127.0.0.1:3000",
    # Add any other origins (frontend URLs) you want to allow
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.get("/api/chatbot/create_new")
def create_new():
    newid = controllers.create_new_chat()
    return {'id': newid}

@app.post("/api/chatbot/get_response")
def get_response(data: Models.Chatbot_generate):
    response = controllers.generate_answer(data)  # Assuming this is the correct function call
    return {"data": response}

@app.post("/api/chatbot/get_chat_history")
def get_chat_history(data: Models.Chatbot_history):
    chat_history = controllers.get_history(data.id)
    return {'chat_history': chat_history}