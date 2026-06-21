import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'supportdesk-secret-key-12345'
    # Configuración de base de datos MySQL
    # Formato: mysql+pymysql://user:password@host/dbname
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'mysql+pymysql://root:@localhost/supportdesk_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
