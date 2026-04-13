import os
import telebot
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GROK_API_KEY = os.getenv("GROK_API_KEY")

bot = telebot.TeleBot(TELEGRAM_TOKEN)

client = OpenAI(
    api_key=GROK_API_KEY,
    base_url="https://api.x.ai/v1"
)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Hello! I'm Hermes Telegram Dashboard powered by Grok.\nSend me any message and I'll help you.")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        response = client.chat.completions.create(
            model="grok-beta",
            messages=[{"role": "user", "content": message.text}],
            temperature=0.7
        )
        reply = response.choices[0].message.content
        bot.reply_to(message, reply)
    except Exception as e:
        bot.reply_to(message, f"Error: {str(e)}")

if __name__ == "__main__":
    print("Hermes Telegram Dashboard is running...")
    bot.infinity_polling()
