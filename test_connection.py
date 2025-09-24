import os
from pathlib import Path
from dotenv import load_dotenv
import psycopg2


dotenv_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path)

# Проверка, что переменные загружены
print("DB_NAME:", os.getenv("DB_NAME"))
print("DB_USER:", os.getenv("DB_USER"))
print("DB_PASSWORD:", os.getenv("DB_PASSWORD"))
print("DB_HOST:", os.getenv("DB_HOST"))
print("DB_PORT:", os.getenv("DB_PORT"))

try:
    conn = psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
    )

    cur = conn.cursor()
    print("✅ Подключение к базе прошло успешно!")
    cur.execute("SELECT version();")
    print("PostgreSQL версия:", cur.fetchone())
    cur.close()
    conn.close()

except Exception as e:
    print("❌ Ошибка подключения:", e)
