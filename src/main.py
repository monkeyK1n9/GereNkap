import os
from dotenv import load_dotenv
from bardapi import Bard
import sqlite3

load_dotenv()  # This line brings all environment variables from .env into os.environ
BARD_API_KEY = os.environ.get("BARD_API_KEY");
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