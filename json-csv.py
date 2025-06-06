
SELECT 
    TO_CHAR(vulnerability_first_seen, 'YYYY-MM-DD') AS date,
    COUNT(DISTINCT vulnerability_finding_id) AS vulnerability_count
FROM *
WHERE 
    provider = 'OP'
    AND false_positive = FALSE
    AND resource_lifespan > INTERVAL '24' HOUR
    AND notification_date IS NOT NULL
    AND vulnerability_first_seen >= CURRENT_DATE - INTERVAL '5' DAY
GROUP BY TO_CHAR(vulnerability_first_seen, 'YYYY-MM-DD')
ORDER BY date;
