SELECT 
  DATE_PART('day', added - first_seen) AS days_old,
  COUNT(*) AS finding_count
FROM 
  cloudplatform_vulnerabilityfinding
WHERE 
  added BETWEEN '2025-04-01' AND '2025-04-23'
  AND firstseen < added
  AND DATE_PART('day', added - firstseen) >= 6
GROUP BY 
  days_old
ORDER BY 
  days_old;

