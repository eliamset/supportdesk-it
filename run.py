import pymysql
from config import Config

def ensure_database_exists():
    """Crea la base de datos MySQL si todavía no existe."""
    uri = Config.SQLALCHEMY_DATABASE_URI  # mysql+pymysql://user:pass@host/dbname
    # Extraer partes de la URI
    parts = uri.replace('mysql+pymysql://', '')
    credentials, rest = parts.split('@')
    host_and_db = rest.split('/', 1)
    host = host_and_db[0]
    db_name = host_and_db[1]

    if ':' in credentials:
        user, password = credentials.split(':', 1)
    else:
        user, password = credentials, ''

    try:
        conn = pymysql.connect(host=host, user=user, password=password)
        with conn.cursor() as cursor:
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{db_name}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
        conn.close()
        print(f"✅ Base de datos '{db_name}' lista.")
    except Exception as e:
        print(f"⚠️  No se pudo crear la base de datos automáticamente: {e}")
        print("   Crea la BD manualmente en phpMyAdmin y vuelve a intentar.")
        raise SystemExit(1)

# 1. Asegurar que la base de datos exista antes de conectar Flask
ensure_database_exists()

from app import create_app, db

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print("✅ Tablas creadas/verificadas correctamente.")
    app.run(debug=True)

