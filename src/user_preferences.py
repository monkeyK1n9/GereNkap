from main import cursor, connection;
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, CallbackQueryHandler, ContextTypes
from telegram import InlineKeyboardMarkup, InlineKeyboardButton

# Function to get and set the language preference of the user
def get_set_language_choice(user_id, language=None):
    if language is None:
        # Update or insert the language preference
        cursor.execute(
            'INSERT OR REPLACE INTO user_preferences (user_id, language) VALUES (?, ?)',
            (user_id, language)
        );

        connection.commit();
    else:
        # Get user's language preference if it exists
        cursor.execute(
            'SELECT language FROM user_preferences WHERE user_id = ?',
            (user_id,)
        );
        result = cursor.fetchone();

        return result[0] if result else "English"; # English is our default if not is provided by user

def get_language_keyboard():
    # Create inline keyboard with language options
    keyboard = [
        [InlineKeyboardButton("English", callback_data='English'),
         InlineKeyboardButton("Français", callback_data='French')]
    ]
    return InlineKeyboardMarkup(keyboard)