import telebot

import sqlite3
from sqlite3 import Error
from time import sleep, ctime

bot = telebot.TeleBot('1250456436:AAG8YLTi40rEMI7oCSur-kTJ9nDUwfuy5-Q')
@bot.message_handler(commands=['start'])
def start(message):
    register_user_data(message.from_user.id, message.message_id, message.chat.id, message.text)
    register_session_data(message.chat.id)
    bot.send_message(message.chat.id, 'Привет, как настроение? Отправь мне один смайлик! ')
    

happiness = ['😀','😃','😄','😁','😆','😂','😊','🤩','🥳']
sadness = ['😞','😔','😟','😕','😫','😩','😓','🥺']
rage = ['👿','😬','😤','😡','👺','💀','😠','🤯','🤨']

 
def post_sql_query(sql_query):
    with sqlite3.connect('test.db') as connection:
        cursor = connection.cursor()
        try:
            cursor.execute(sql_query)
        except Error:
            pass
        result = cursor.fetchall()
        return result
       
#таблица с сообщениями:
def create_user_table():
    msg_query = '''CREATE TABLE IF NOT EXISTS MSG_TABLE 
                        (user_id INTEGER,
                        text_date TEXT,
                        msg_id INTEGER PRIMARY KEY NOT NULL,
                        chat_id INTEGER,
                        msg_text TEXT);'''
    post_sql_query(msg_query)

#таблица с сессиями:
def create_ses_table():
    ses_query = '''CREATE TABLE IF NOT EXISTS SES_TABLE 
                        (session_id INTEGER,
                        start_date TEXT PRIMARY KEY NOT NULL,
                        end_date TEXT);'''
    post_sql_query(ses_query)




def register_user_data(user, message_id, chat_id, text):
    insert_to_users_db = f'INSERT INTO MSG_TABLE (user_id, text_date, msg_id, chat_id, msg_text) VALUES ({user}, "{ctime()}", "{message_id}", "{chat_id}", "{text}");'
    post_sql_query(insert_to_users_db)
        
create_user_table()

def register_session_data(chat_id):
    insert_to_ses_db = f'INSERT INTO SES_TABLE (session_id, start_date, end_date) VALUES ("{chat_id}", "{ctime()}", "{ctime()}");'
    post_sql_query(insert_to_ses_db)
        
create_ses_table()




@bot.message_handler(content_types=['text'])
def send_text(message):
    register_user_data(message.from_user.id, message.message_id, message.chat.id, message.text)
  
    if message.text in happiness:
        
        bot.send_message(message.chat.id, 'Тебя что-то рассмешило!')
    elif message.text in sadness:
        
        bot.send_message(message.chat.id, 'Что случилось? Почему ты грустишь?')
    elif message.text in rage:
        
        bot.send_message(message.chat.id, 'Не злись! Все наладится!')
    else:
        bot.send_message(message.chat.id, 'Не понимаю тебя! Отправь один смайлик!')
    
bot.polling()
