from data.config import LOGFILE
import logging
import os

if not os.path.exists(LOGFILE):
    file = open(LOGFILE, 'a')  # Создание файла, если он отсутствовал
    file.close()

logging.basicConfig(filename=LOGFILE,
                    format='[%(asctime)s] [%(levelname)s] => %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO)
