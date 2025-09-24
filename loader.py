import os
from dotenv import load_dotenv
from pathlib import Path

# абсолютный путь к .env
dotenv_path = Path(r"C:\Users\Madiyar\Downloads\Madi code\petproject\.env")
print(f"Используем .env из: {dotenv_path}")
load_dotenv(dotenv_path)

# проверка
print("DB_NAME:", os.getenv("DB_NAME"))
print("DB_USER:", os.getenv("DB_USER"))
print("DB_PASSWORD:", os.getenv("DB_PASSWORD"))
print("DB_HOST:", os.getenv("DB_HOST"))
print("DB_PORT:", os.getenv("DB_PORT"))




import requests
import psycopg2


conn = psycopg2.connect(
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT")
)
cur = conn.cursor()


cur.execute("TRUNCATE character_episode, characters, episodes, locations RESTART IDENTITY CASCADE;")


def fetch_all(url):
    while url:
        try:
            res = requests.get(url)
            res.raise_for_status()
            data = res.json()
            yield from data["results"]
            url = data["info"]["next"]
        except Exception as e:
            print(f"❌ Ошибка при запросе {url}: {e}")
            break


for loc in fetch_all("https://rickandmortyapi.com/api/location"):
    cur.execute("""
        INSERT INTO locations (id, name, type, dimension)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (id) DO NOTHING;
    """, (loc["id"], loc["name"], loc["type"], loc["dimension"]))


for ep in fetch_all("https://rickandmortyapi.com/api/episode"):
    cur.execute("""
        INSERT INTO episodes (id, name, air_date, episode_code)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (id) DO NOTHING;
    """, (ep["id"], ep["name"], ep["air_date"], ep["episode"]))


for ch in fetch_all("https://rickandmortyapi.com/api/character"):
    loc_id = int(ch["location"]["url"].split("/")[-1]) if ch["location"]["url"] else None

    cur.execute("""
        INSERT INTO characters (id, name, species, gender, status, location_id)
        VALUES (%s, %s, %s, %s, %s, %s)
        ON CONFLICT (id) DO NOTHING;
    """, (ch["id"], ch["name"], ch["species"], ch["gender"], ch["status"], loc_id))

    for ep_url in ch["episode"]:
        ep_id = int(ep_url.split("/")[-1])
        cur.execute("""
            INSERT INTO character_episode (character_id, episode_id)
            VALUES (%s, %s)
            ON CONFLICT DO NOTHING;
        """, (ch["id"], ep_id))


conn.commit()
cur.close()
conn.close()

print("✅ Данные успешно загружены из Rick and Morty API в PostgreSQL!")
