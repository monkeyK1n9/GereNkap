import os
from dotenv import load_dotenv
from bardapi import Bard
import sqlite3
from telegram import Update
from telegram.ext import Application, Updater, CommandHandler, MessageHandler, filters, CallbackContext, CallbackQueryHandler, ContextTypes
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from commands import start_command, language_command
from responses import handle_message, handle_response, error

load_dotenv()  # This line brings all environment variables from .env into os.environ
BARD_API_KEY = os.environ.get("BARD_API_KEY");
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN");
BOT_USERNAME = os.environ.get("BOT_USERNAME");

# Connect to database
connection = sqlite3.connect("GereNkapDB.db");
cursor = connection.cursor();

# Create a table to store user's information
cursor.execute('''
    CREATE IF NOT EXISTS user_preferences (
        user_id INTEGER PRIMARY KEY
        language TEXT
    )
''')

connection.commit();


bard = Bard(token=BARD_API_KEY, language = "English")

if __name__ == "__main__":
    print("Starting bot...")
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build();

    # Commands
    app.add_handler(CommandHandler('start', start_command));
    app.add_handler(CommandHandler('language', language_command));

    # Messages responses
    app.add_handler(MessageHandler(filters.TEXT, handle_message));

    # Errors
    app.add_error_handler(error);

    print("Polling...")
    # Polls the bot
    app.run_polling(poll_interval=3)
