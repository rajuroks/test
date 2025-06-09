
SELECT 
    owner,
    COUNT(DISTINCT vulnerability_finding_id) AS finding_count
FROM vm_data.cloudplatform_vmarc_vulnerability_details
WHERE 
    provider = 'OP'
    AND false_positive = FALSE
    AND resource_lifespan > INTERVAL '24' HOUR
    AND notification_date IS NOT NULL
    AND vulnerability_first_seen >= CURRENT_DATE - INTERVAL '4' DAY
GROUP BY owner
ORDER BY finding_count DESC
FETCH FIRST 5 ROWS ONLY;
