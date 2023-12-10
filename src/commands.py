from user_preferences import get_language_keyboard, get_set_language_choice
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, CallbackQueryHandler, ContextTypes
from telegram import InlineKeyboardMarkup, InlineKeyboardButton

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello, thanks for taking your finances in hand. Select your preferred language: \n\nSalut, merci de prendre vos finances en main. Sélectionnez votre langue préférée :");

    # prompt to ask to select language
    selected_language = get_language_keyboard();

    while selected_language is not "English" or selected_language is not "French":
        selected_language = get_language_keyboard();
    
    stored_language = get_set_language_choice(1);



