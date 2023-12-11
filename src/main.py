import os
from dotenv import load_dotenv
from langchain.llms import GooglePalm
from langchain_experimental.sql import SQLDatabaseChain
from langchain.utilities import SQLDatabase
from langchain.agents import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit

# from langchain.agents import AgentExecutor
from langchain.agents.agent_types import AgentType
import sqlite3
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes, CallbackContext
from telegram import InlineKeyboardMarkup, InlineKeyboardButton

load_dotenv()  # This line brings all environment variables from .env into os.environ
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY");
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN");
BOT_USERNAME = os.environ.get("BOT_USERNAME");
db_path = "sqlite:///GereNkapDB.db";


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

# Create a table to store user's information
cursor.execute('''
    CREATE TABLE IF NOT EXISTS expenses (
        user_id INTEGER PRIMARY KEY
    )
''')

# Create a table to store user's information
cursor.execute('''
    CREATE TABLE IF NOT EXISTS debts (
        user_id INTEGER PRIMARY KEY
    )
''')

# Create a table to store user's information
cursor.execute('''
    CREATE TABLE IF NOT EXISTS budget (
        user_id INTEGER PRIMARY KEY
    )
''')

connection.commit();


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
        await update.callback_query.message.edit_text(f"You selected: {chosen_language} \n\nGive me you prompt, what do you want to save or a debt or budget?\n\nExample: Store this: today I spent 2000FCFA on transport.");
    elif stored_language == "Français":
        await update.callback_query.message.edit_text(f"Vous avez choisi le: {chosen_language} \n\nDonnez-moi une idée de ce que vous voulez économiser ou une dette ou un budget.\n\nExemple : Enregistre ceci: aujourd'hui, j'ai dépensé 2000FCFA pour le transport.")



# COMMANDS
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello, thanks for taking your finances in hand. Select your preferred language: \n\nSalut, merci de prendre vos finances en main. Sélectionnez votre langue préférée :", reply_markup=get_language_keyboard());


async def language_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Select your preferred language: \n\nSélectionnez votre langue préférée :", reply_markup=get_language_keyboard());



async def handle_response(text: str, language: str, user_id) -> str:
    if text == '/start' or text == '/language':
        return None;

    # reading database
    db = SQLDatabase.from_uri(db_path);
    llm = GooglePalm(google_api_key=GOOGLE_API_KEY);
    db_chain = SQLDatabaseChain.from_llm(llm, db, verbose=True)

    agent_executor = create_sql_agent(
        llm=llm,
        toolkit=SQLDatabaseToolkit(db=db, llm=llm),
        verbose=True,
        agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    )

    if language == "English":
        result = agent_executor.run(f"Execute for user_id {user_id}: {text}")
        print(result)

        return result;
    else:
        result = agent_executor.run(f"Execute for user_id {user_id}: {text}")
        print(result)

        return result;

        return result;


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type;
    text: str = update.message.text;
    user_id = update.message.from_user.id;

    stored_language = get_set_language_choice(user_id);

    print(f"User in ({update.message.chat.id}) in {message_type}: {text}");

    if message_type == 'group':
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, '').strip();
            response: str = await handle_response(new_text, stored_language, user_id);
        else:
            return;
    else:
        response: str = await handle_response(text, stored_language, user_id);

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
