from flask import Flask, request
import telebot
import os
from datetime import datetime
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get the Bot Token and Admin User ID from environment variables
BOT_TOKEN = os.getenv('BOT_TOKEN')
ADMIN_USER_ID = os.getenv('ADMIN_USER_ID')  # Add the Admin User ID here or in your environment variables

# Ensure the bot token and admin ID are available
if not BOT_TOKEN or not ADMIN_USER_ID:
    raise ValueError("BOT_TOKEN or ADMIN_USER_ID is missing!")

bot = telebot.TeleBot(BOT_TOKEN)

# Flask App
app = Flask(__name__)

# Route for the root page to check if the server is running
@app.route('/')
def home():
    return "Bot is running!", 200

# Route for Telegram Webhook
@app.route(f"/{BOT_TOKEN}", methods=['POST'])
def telegram_webhook():
    json_update = request.get_json()
    update = telebot.types.Update.de_json(json_update)
    bot.process_new_updates([update])
    return "OK", 200

# Function to fetch Bikram Samwat date
def get_bikram_samwat_date():
    """Fetch the current Bikram Samwat date using an API."""
    try:
        response = requests.get("https://api.nepalitoday.com/api/dateconverter", timeout=10)
        if response.status_code == 200:
            data = response.json()
            return data.get('bs', "Unknown Date")
    except:
        return "Error fetching Bikram Samwat date"
    return "Unknown Date"

# Bot Logic: Handle forwarded messages and notify the sender and admin
@bot.message_handler(content_types=['text', 'photo', 'video', 'document'])
def handle_message(message):
    if message.forward_date:  # Check if the message is forwarded
        sender_id = message.from_user.id
        sender_name = f"{message.from_user.first_name} {message.from_user.last_name or ''}".strip()
        sender_username = f"@{message.from_user.username}" if message.from_user.username else "No username"

        # Delete the original forwarded message
        try:
            bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
        except:
            pass

        # Resend the forwarded content
        bikram_samwat_date = get_bikram_samwat_date()
        if message.text:
            content = f"{bikram_samwat_date}\nIs it Useful?:\n{message.text}"
            bot.send_message(message.chat.id, content)
        elif message.photo:
            content = f"{bikram_samwat_date}\nCopyright Photo!"
            bot.send_photo(message.chat.id, message.photo[-1].file_id, caption=content)
        elif message.document:
            content = f"{bikram_samwat_date}\nCopyright Document!"
            bot.send_document(message.chat.id, message.document.file_id, caption=content)
        elif message.video:
            content = f"{bikram_samwat_date}\nCopyright Video!"
            bot.send_video(message.chat.id, message.video.file_id, caption=content)

        # Notify the sender
        try:
            bot.send_message(
                sender_id,
                f"Dear {sender_name},\n\nThank you for forwarding content to the group. "
                f"We've processed your message. If you need assistance, feel free to reach out!"
            )
        except:
            pass

        # Notify the admin
        try:
            bot.send_message(
                ADMIN_USER_ID,
                f"**Forwarded Content Alert:**\n"
                f"- Sender: {sender_name} ({sender_username})\n"
                f"- Content Type: {'Text' if message.text else 'Media'}\n"
                f"- Bikram Samwat Date: {bikram_samwat_date}"
            )
        except:
            pass

# Run Flask App Locally or on Render
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv('PORT', 5000)))
