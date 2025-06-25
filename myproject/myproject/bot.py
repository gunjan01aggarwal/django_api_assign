
import os
import django
import sys
import time
from dotenv import load_dotenv



sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE","myproject.settings")
django.setup()

from telebot import TeleBot
from webapp.models import Telegram

load_dotenv()

Token=os.getenv("Token")
bot=TeleBot(Token)
current_time=time.ctime().split(' ')[3]
print(current_time)


@bot.message_handler(['start'])
def start(message):
    bot.reply_to(message,"Welcome to bot!!")
    if current_time>="00:00:01" and current_time<="12:00:00":
        bot.reply_to(message,"Good Morning!!")
    elif "12:00:01"<=current_time <="07:00:00":
        bot.reply_to(message,"Good Afternoon!!")
    else:
        bot.reply_to(message,"Good Evening")       
    
    
@bot.message_handler(['talk'])
def talk(message):
    bot.reply_to(message,"May I know your good name?")
    bot.register_next_step_handler(message, save_name)


def save_name(message):
    
    name = message.text

    # Save to database
    obj, created = Telegram.objects.update_or_create(
        
        defaults={'username': name}
    )

    bot.reply_to(message, f"Nice to meet you, {name}!")



bot.polling()