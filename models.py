from pydantic import BaseModel

class Chatbot_generate(BaseModel):
    question: str
    id: str
    
class Chatbot_history(BaseModel):
    id: str