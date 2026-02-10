import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('TELEGRAM_API_TOKEN')
WEBHOOK_URL = os.getenv('WEBHOOK_URL')
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
ADMIN_CHAT_ID = os.getenv('ADMIN_CHAT_ID')
