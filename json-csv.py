SELECT COUNT(DISTINCT vulnerability_finding_id) AS recent_vulnerability_count
FROM *
WHERE 
    provider = 'OP'
    AND false_positive = FALSE
    AND resource_lifespan > INTERVAL '24' HOUR
    AND notification_date IS NOT NULL
    AND vulnerability_first_seen >= CURRENT_DATE - INTERVAL '5' DAY;
