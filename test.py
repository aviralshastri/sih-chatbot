from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import ollama

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/chatbot")
async def chatbot(message: str = Query(..., description="Message from the user")):
    response = ollama.chat(
        model='water-con-test',
        messages=[{'role': 'user', 'content': message}]
    )
    
    full_message = response['message']['content']
    
    return {"response": full_message}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
