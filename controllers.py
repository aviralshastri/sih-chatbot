import services

def generate_answer(question,id=None):
    if id==None:
        newid=services.create_new_chat()
        services.respond(newid,question)
    else:
        services.respond(chat_id=id,question=question)

def create_new_chat():
    return services.create_new_chat()

def get_history(id:str):
    return services.get_chat_history(chat_id=id)

