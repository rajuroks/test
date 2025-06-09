
SELECT 
  TO_CHAR(vulnerability_first_seen, 'YYYY-MM-DD') AS day,
  name AS cluster_name,
  COUNT(DISTINCT vulnerability_finding_id) AS finding_count
FROM vm_data.cloudplatform_vmarc_vulnerability_details
WHERE 
  provider = 'OP'
  AND vulnerability_first_seen >= CURRENT_DATE - INTERVAL '6' DAY
GROUP BY TO_CHAR(vulnerability_first_seen, 'YYYY-MM-DD'), name
ORDER BY day, finding_count DESC;
