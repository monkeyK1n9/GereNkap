from main import bard, BOT_USERNAME;
from user_preferences import get_set_language_choice
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, CallbackQueryHandler, ContextTypes
from telegram import InlineKeyboardMarkup, InlineKeyboardButton

BARD_INTRO = "Respond to the prompt as if your name is GereNkap created by monkeyK1n9, you are an expert in finances. You either give advices or generate SQL queries. Don't give explanation, just give the SQL query. Here is the prompt: ";

BARD_OUTRO = "Read this for a non-technical person: "

def handle_response(text: str) -> str:
    request_query = BARD_INTRO + text;

    language = get_set_language_choice(1);
    response_query = bard.get_response(request_query, language=language);
    request_user = BARD_OUTRO + response_query;

    response_user = bard.get_response(request_user, language=language);
    return response_user;


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type;
    text: str = update.message.text;

    print(f"User in ({update.message.chat.id}) in {message_type}: {text}");

    if message_type == 'group':
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, '').strip();
            response: str = handle_response(new_text);
        else:
            return;
    else:
        response: str = handle_response(text);

    print("Bot: ", response);
    await update.message.reply_text(response);


async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"Update ({update}) caused an error: {context.error}");

