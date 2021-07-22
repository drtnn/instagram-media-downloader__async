from environs import Env
import os

env = Env()
env.read_env()

ADMINS = [int(user_id) for user_id in env.list('ADMINS')]
BOT_TOKEN = env.str('BOT_TOKEN')
PROVIDER_TOKEN = env.str('PROVIDER_TOKEN')
BOT_NAME = env.str('BOT_NAME')
COOKIE = env.list('COOKIE')

DATABASE_URL = env.str('DATABASE_URL')
DB_NAME = env.str('DB_NAME')
DB_HOST = env.str('DB_HOST')
DB_USER = env.str('DB_USER')
DB_PASSWORD = env.str('DB_PASSWORD')
DB_PORT = env.int('DB_PORT')

CURRENT_DIR = env.str('CURRENT_DIR') if env.str('CURRENT_DIR') else f'{os.getcwd()}/'
SESSION_DIR = CURRENT_DIR + 'sessions/'
DOWNLOAD_DIR = CURRENT_DIR + 'downloads/'
LOGFILE = CURRENT_DIR + 'instagram-bot.log'

TELETHON_API_ID = env.int('API_ID')
TELETHON_API_HASH = env.str('API_HASH')
TELETHON_SESSION = env.str('SESSION')
