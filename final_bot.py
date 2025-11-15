import logging
import re
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Get from Railway environment variables
BOT_TOKEN = os.environ["BOT_TOKEN"]
CHANNEL_ID = os.environ["CHANNEL_ID"]

def is_valid_device_id(text):
    if len(text) != 12:
        return False
    return bool(re.match('^[a-zA-Z0-9]+$', text))

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message:
        await update.message.reply_text("WELCOME, IM BOSS FRANKS BOT\nSEND YOUR DEVICE ID")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return
    
    user = update.message.from_user
    user_message = update.message.text.strip()
    
    if is_valid_device_id(user_message):
        try:
            user_info = f"👤 {user.first_name}"
            if user.last_name:
                user_info += f" {user.last_name}"
            if user.username:
                user_info += f" (@{user.username})"
            user_info += f"\n🆔 User ID: {user.id}"
            
            await context.bot.send_message(
                chat_id=CHANNEL_ID,
                text=f"{user_info}\n\n📱 Device ID:\n{user_message}"
            )
            
            await update.message.reply_text("DONT FORGET TO FEEDBACK 😉")
            
            print(f"✅ Valid Device ID: {user_message}")
            
        except Exception as e:
            print(f"❌ Error: {e}")
            
    else:
        await update.message.reply_text("✅DEVICE ID ONLY")
        print(f"❌ Invalid: {user_message}")

def main():
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("🤖 BOSS FRANK'S BOT STARTED")
    print("📍 Only 12-character Device IDs")
    print("🔄 Running forever on Railway...")
    print("✅ Bot is LIVE 24/7!")
    
    application.run_polling()

if __name__ == "__main__":
    main()