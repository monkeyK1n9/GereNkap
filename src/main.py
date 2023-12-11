import os
import requests
from dotenv import load_dotenv
from bardapi import Bard
import sqlite3
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes, CallbackContext
from telegram import InlineKeyboardMarkup, InlineKeyboardButton

load_dotenv()  # This line brings all environment variables from .env into os.environ
BARD_API_KEY = os.environ.get("BARD_API_KEY");
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN");
BOT_USERNAME = os.environ.get("BOT_USERNAME");

# Connect to database
connection = sqlite3.connect("GereNkapDB.db");
cursor = connection.cursor();

# Create a table to store user's information
cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_preferences (
        user_id INTEGER PRIMARY KEY,
        language TEXT
    )
''')

connection.commit();


session = requests.Session()
session.headers = {
            "Host": "bard.google.com",
            "X-Same-Domain": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
            "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
            "Origin": "https://bard.google.com",
            "Referer": "https://bard.google.com/",
        }
session.cookies.set("__Secure-1PSID", BARD_API_KEY) 

print(BARD_API_KEY)

# Function to get and set the language preference of the user
def get_set_language_choice(user_id, language=None):
    if language is not None:
        # Update or insert the language preference
        cursor.execute(
            'INSERT OR REPLACE INTO user_preferences (user_id, language) VALUES (?, ?)',
            (user_id, language)
        );

        connection.commit();
    

    # Get user's language preference if it exists
    cursor.execute(
        'SELECT language FROM user_preferences WHERE user_id = ?',
        (user_id,)
    );
    result = cursor.fetchone();
    print("result:", result)
    return result[0] if result else "English"; # English is our default if not is provided by user

def get_language_keyboard():
    # Create inline keyboard with language options
    keyboard = [
        [InlineKeyboardButton("English", callback_data='English'),
         InlineKeyboardButton("Français", callback_data='Français')]
    ]
    return InlineKeyboardMarkup(keyboard)

async def language_choice(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    user_id = query.from_user.id
    chosen_language = query.data
    await query.answer()
    print("chosen language: ", chosen_language)

    stored_language = get_set_language_choice(user_id, chosen_language);

    # Handle the chosen language (you can save it, use it, etc.)
    if stored_language == "English":
        await update.callback_query.message.edit_text(f"You selected: {chosen_language} \n\nGive me you prompt, what do you want to save or a debt or budget?\n\nExample: Today I spent 2000FCFA on transport.__");
    elif stored_language == "Français":
        await update.callback_query.message.edit_text(f"Vous avez choisi le: {chosen_language} \n\nDonnez-moi une idée de ce que vous voulez économiser ou une dette ou un budget.\n\nExemple : Aujourd'hui, j'ai dépensé 2000FCFA pour le transport.")



# COMMANDS
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello, thanks for taking your finances in hand. Select your preferred language: \n\nSalut, merci de prendre vos finances en main. Sélectionnez votre langue préférée :", reply_markup=get_language_keyboard());


async def language_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Select your preferred language: \n\nSélectionnez votre langue préférée :", reply_markup=get_language_keyboard());


# RESPONSES
BARD_INTRO = "Respond to the prompt as if your name is GereNkap created by monkeyK1n9, you are an expert in finances. You only generate SQL queries. Don't give explanation, just give the SQL query. Here is the prompt: ";

BARD_OUTRO = "Read this for a non-technical person: "

def handle_response(text: str, language: str) -> str:
    if text == '/start' or text == '/language':
        return None;

    # bard = Bard(token=BARD_API_KEY, session=session, timeout=60);
    bard = Bard(token=BARD_API_KEY, language=language);

    request_query = BARD_INTRO + text;

    language = get_set_language_choice(1);
    response_query = bard.get_answer(request_query)['content'];

    try:
        # executing the query
        cursor.execute(f"{response_query}")

        connection.commit();
    except Exception as e:
        print(f"Error executing query: {e}")

    request_user = BARD_OUTRO + response_query;

    response_user = bard.get_answer(request_user);
    return response_user;


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type;
    text: str = update.message.text;
    user_id = update.message.from_user.id;

    stored_language = get_set_language_choice(user_id);

    print(f"User in ({update.message.chat.id}) in {message_type}: {text}");

    if message_type == 'group':
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, '').strip();
            response: str = handle_response(new_text, stored_language);
        else:
            return;
    else:
        response: str = handle_response(text, stored_language);

    print("Bot: ", response);
    await update.message.reply_text(response);


async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"Update ({update}) caused an error: {context.error}");




if __name__ == "__main__":
    print("Starting bot...")
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build();
    
    # Commands
    app.add_handler(CommandHandler('start', start_command));
    app.add_handler(CallbackQueryHandler(language_choice))
    app.add_handler(CommandHandler('language', language_command));

    # Messages responses
    app.add_handler(MessageHandler(filters.TEXT, handle_message));

    # Errors
    app.add_error_handler(error);

    print("Polling...")
    # Polls the bot
    app.run_polling(poll_interval=5)
