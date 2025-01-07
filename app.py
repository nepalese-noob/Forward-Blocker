from flask import Flask, request
import telebot
import os
from dotenv import load_dotenv

# Load environment variables from a .env file (if used)
load_dotenv()

# Get the Bot Token from environment variables (or you can set it directly in the server environment)
BOT_TOKEN = os.getenv('BOT_TOKEN')

# Ensure the bot token is available
if not BOT_TOKEN:
    raise ValueError("No BOT_TOKEN provided!")

bot = telebot.TeleBot(BOT_TOKEN)

# Flask App
app = Flask(__name__)

# Route for Telegram Webhook
@app.route(f"/{BOT_TOKEN}", methods=['POST'])
def telegram_webhook():
    json_update = request.get_json()
    update = telebot.types.Update.de_json(json_update)
    bot.process_new_updates([update])
    return "OK", 200

# Bot Logic: Detect and Resend Forwarded Messages
@bot.message_handler(content_types=['text', 'photo', 'document', 'video'])
def handle_message(message):
    # Check if the message is forwarded
    if message.forward_date:
        # Resend the forwarded content in real time
        if message.text:
            bot.send_message(message.chat.id, f"Forwarded message detected:\n{message.text}")
        elif message.photo:
            file_id = message.photo[-1].file_id
            bot.send_photo(message.chat.id, file_id, caption="Forwarded photo detected!")
        elif message.document:
            file_id = message.document.file_id
            bot.send_document(message.chat.id, file_id, caption="Forwarded document detected!")
        elif message.video:
            file_id = message.video.file_id
            bot.send_video(message.chat.id, file_id, caption="Forwarded video detected!")
    else:
        # Ignore non-forwarded messages
        pass

# Run Flask App Locally (for testing)
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
  
