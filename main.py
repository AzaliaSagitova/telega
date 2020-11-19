# -*- coding: utf-8 -*-
import telebot
import mysql.connector

bot = telebot.TeleBot("1467292575:AAFc0ffFrW06Z8S7KV4cPYxNWwsgVopf4Lo", parse_mode=None) # You can set parse_mode by default. HTML or MARKDOWN

db = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="payment"
)

cursor = db.cursor()

# sql = "INSERT INTO order_status (order_id, status) VALUES (%s, %s)"
# val = ("78", "Заказ формируется, дата доставки: 05.11.2020")
# cursor.execute(sql, val)

# db.commit()

# print(cursor.rowcount, "запись добавлена.")

user_data = {}

class User:
    def __init__(self, zakaz):
        self.zakaz = zakaz
        self.status = ""

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    msg = bot.send_message(message.chat.id, "Введите номер заказа?")
    bot.register_next_step_handler(msg, process_zakaz_step)

def process_zakaz_step(message):
    try:
        user_id = message.from_user.id
        user_data[user_id] = User(message.text)

        msg = bot.send_message(message.chat.id, "Введите статус заказа:")
        bot.register_next_step_handler(msg, process_status_step)
    except Exception as e:
        bot.reply_to(message, 'Ошибка или заказ уже выполнен')

def process_status_step(message):
    try:
        user_id = message.from_user.id
        user = user_data[user_id]
        user.status = message.text

        #sql = "INSERT INTO order_status (order_id, status) VALUES (%s, %s)"
        #val = (user.zakaz, user.status)
        #cursor.execute(sql, val)
        sql = "INSERT INTO order_status (order_id, status) VALUES (%s, %s)"
        val = (user.zakaz, user.status)
        cursor.execute(sql, val)
        db.commit()

    except Exception as e:
        bot.reply_to(message, 'Ошибка или заказ уже выполнен')

    try:
        user_id = message.from_user.id
        user = user_data[user_id]
        user.status = message.text

        #sql = "INSERT INTO order_status (order_id, status) VALUES (%s, %s)"
        #val = (user.zakaz, user.status)
        #cursor.execute(sql, val)
        sql = "UPDATE Orders SET status = %s WHERE id = %s"
        val = (user.status, int(user.zakaz))
        cursor.execute(sql, val)
        db.commit()
        bot.send_message(message.chat.id, "Статус заказа сохранен!")

    except Exception as e:
        bot.reply_to(message, 'Ошибка или заказ уже выполнен')

# Enable saving next step handlers to file "./.handlers-saves/step.save".
# Delay=2 means that after any change in next step handlers (e.g. calling register_next_step_handler())
# saving will hapen after delay 2 seconds.
bot.enable_save_next_step_handlers(delay=2)

# Load next_step_handlers from save file (default "./.handlers-saves/step.save")
# WARNING It will work only if enable_save_next_step_handlers was called!
bot.load_next_step_handlers()

if __name__ == '__main__':
    bot.polling(none_stop=True)