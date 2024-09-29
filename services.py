import ollama
from mtranslate import translate
import mysql.connector
import json
import random
import string


conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="mysql",
    database="sih_chatbot"
)
dbcursor=conn.cursor()

def check_id_exist(chat_id:str):
  query = "SELECT COUNT(*) FROM chats WHERE id = %s"
  dbcursor.execute(query, (chat_id,))
  result = dbcursor.fetchone()
  
  return result[0] > 0

def random_id_genrator(length:int=15):
  characters = string.ascii_letters + string.digits
  chat_id=''
  while True:
    chat_id=''.join(random.choice(characters) for _ in range(length))
    if check_id_exist(chat_id=chat_id):
      continue
    else:
      break
  return chat_id
  

def create_new_chat():
  chat_history=[{'role':'user','content':'hi'}]
  chat_history.append(generate_response(context=chat_history,stream=True,hindi=False))
  chat_history_json=json.dumps(chat_history)
  chat_id=random_id_genrator()
  query='insert into chats(id,chat_history) values(%s,%s)'
  dbcursor.execute(query, (chat_id,chat_history_json,))
  conn.commit()
  
  return chat_id
  

def get_chat_history(chat_id: str):
  if not check_id_exist(chat_id=chat_id):
    return []
  chat_id = chat_id.replace(".", "").replace("=", "").replace(" ", "")
  query = "SELECT chat_history FROM chats WHERE id = %s"
  dbcursor.execute(query, (chat_id,))
  result = dbcursor.fetchone()
  
  if result:
      return json.loads(result[0])
  else:
      return None

def update_chat_history(chat_id:str,new_chat_history:list):
  if not check_id_exist(chat_id=chat_id):
    return []
  chat_id = chat_id.replace(".", "").replace("=", "").replace(" ", "")
  new_chat_history_json = json.dumps(new_chat_history)
  query = "UPDATE chats SET chat_history=%s WHERE id = %s"
  dbcursor.execute(query, (new_chat_history_json, chat_id))
  conn.commit()
  

def english_to_hindi(english_input):
    return translate(english_input, "hi")

def generate_response(context,stream,hindi):
  stream = ollama.chat(
        model='gemma2:2b',
        messages=context,
        stream=stream,
    )
  bot_message=""
  print("Bot: ",end='',flush=True)
  for chunk in stream:
    bot_message+=chunk['message']['content']
    if hindi:
      print(english_to_hindi(chunk['message']['content']), end='', flush=True)
    else:
      print(chunk['message']['content'], end='', flush=True)
  print()
  return {'role':'assistant','content':bot_message.replace("\n"," ")}
  

def respond(chat_id:str,question:str):
  context=get_chat_history(chat_id=chat_id)
  hindi=False
  exit_commands=["/exit","/bye","/goodbye","/quit"]
  clear_context=["/clear","/clean","/clr","/cln"]
  if question in exit_commands:
    return
  if question in clear_context:
    update_chat_history(chat_id=chat_id,new_chat_history=context)
  context.append({'role': 'user','content': question,})
  context.append(generate_response(context=context,stream=True,hindi=hindi))
  update_chat_history(chat_id=chat_id,new_chat_history=context)

