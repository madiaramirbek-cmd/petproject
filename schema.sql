CREATE TABLE IF NOT EXISTS locations (
  id INT PRIMARY KEY,
  name TEXT NOT NULL,
  type TEXT,
  dimension TEXT
);

CREATE TABLE IF NOT EXISTS episodes (
  id INT PRIMARY KEY,
  name TEXT NOT NULL,
  air_date TEXT,
  episode_code TEXT UNIQUE
);

CREATE TABLE IF NOT EXISTS characters (
  id INT PRIMARY KEY,
  name TEXT NOT NULL,
  species TEXT,
  gender TEXT,
  status TEXT,
  location_id INT REFERENCES locations(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS character_episode (
  character_id INT REFERENCES characters(id) ON DELETE CASCADE,
  episode_id INT REFERENCES episodes(id) ON DELETE CASCADE,
  PRIMARY KEY (character_id, episode_id)
);
