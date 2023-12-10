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

    if stored_language == "English":
        await update.message.reply_text("Give me you prompt, what do you want to save?\n\nExample: Today I spent 2000FCFA on transport.");
    else:
        await update.message.reply_text("Donnez-moi une idée de ce que vous voulez économiser.\n\nExemple : Aujourd'hui, j'ai dépensé 2000FCFA pour le transport.")


async def language_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Select your preferred language: \n\nSélectionnez votre langue préférée :");

    # prompt to ask to select language
    selected_language = get_language_keyboard();

    while selected_language is not "English" or selected_language is not "French":
        selected_language = get_language_keyboard();
    
    stored_language = get_set_language_choice(1);

    if stored_language == "English":
        await update.message.reply_text("Give me you prompt, what do you want to save?\n\nExample: Today I spent 2000FCFA on transport.");
    else:
        await update.message.reply_text("Donnez-moi une idée de ce que vous voulez économiser.\n\nExemple : Aujourd'hui, j'ai dépensé 2000FCFA pour le transport.")



