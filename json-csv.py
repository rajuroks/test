
SELECT 
  r.name,
  r.first_seen,
  r.last_seen,
  vf.added,
  DATE_PART('day', vf.added - r.first_seen) AS days_old,
  COUNT(*) OVER (PARTITION BY DATE_PART('day', vf.added - r.first_seen)) AS findings_count
FROM 
  cloudplatform_vulnerabilityfindingresource vf
JOIN 
  cloudplatform_resource r ON vf.resource_id = r.id
WHERE 
  vf.added BETWEEN '2025-04-01' AND '2025-04-23'
  AND r.first_seen < vf.added
  AND DATE_PART('day', vf.added - r.first_seen) >= 6
  AND r.provider = 'OP'
  AND r.type = 'CN'
ORDER BY 
  days_old;
