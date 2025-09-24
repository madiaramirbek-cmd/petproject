
SELECT species, COUNT(*) AS count
FROM characters
GROUP BY species
ORDER BY count DESC;


SELECT l.name AS location, COUNT(c.id) AS character_count
FROM locations l
LEFT JOIN characters c ON c.location_id = l.id
GROUP BY l.name
ORDER BY character_count DESC
LIMIT 5;


SELECT e.name, e.episode_code, e.air_date
FROM episodes e
JOIN character_episode ce ON e.id = ce.episode_id
JOIN characters c ON ce.character_id = c.id
WHERE c.name = 'Rick Sanchez'
ORDER BY e.id;


SELECT status, COUNT(*) AS count
FROM characters
GROUP BY status;


SELECT AVG(char_count) AS avg_characters_per_episode
FROM (
    SELECT e.id, COUNT(ce.character_id) AS char_count
    FROM episodes e
    JOIN character_episode ce ON e.id = ce.episode_id
    GROUP BY e.id
) sub;
