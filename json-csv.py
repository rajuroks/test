SELECT 
    owner,
    cve,
    COUNT(DISTINCT notification_id) AS notification_count
FROM cloudplatform_vmarc_vulnerability_details
WHERE cve IN ('CVE-2024-1111', 'CVE-2024-2222', 'CVE-2024-3333') -- Your CVEs
  AND notification_date >= DATE '2024-01-01'
  AND notification_date <= CURRENT_DATE
GROUP BY owner, cve
ORDER BY owner, cve;
