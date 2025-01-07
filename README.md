# Forward-Blocker
It blocks the forwarded content, saves and resend.
# Telegram Bot with Flask for Real-Time Forward Detection

This is a simple Telegram bot deployed using Flask. It detects forwarded messages in real time and resends them using the bot.

## Features
- Detects forwarded messages.
- Supports text, photos, documents, and videos.
- Resends the forwarded content instantly.

## Deployment on Render
1. Fork this repository.
2. Add your `BOT_TOKEN` in Render's environment variables.
3. Deploy the app using Render's web service with the following settings:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python app.py`
4. Set up the Telegram webhook:
   ```bash
   curl -F "url=https://<YOUR-RENDER-URL>/<BOT_TOKEN>" https://api.telegram.org/bot<BOT_TOKEN>/setWebhook
   
