SELECT 
  DATE_PART('day', vf.added - vf.first_seen) AS days_old,
  COUNT(*) AS finding_count
FROM 
  cloudplatform_vulnerabilityfinding vf
JOIN 
  cloudplatform_vulnerabilityfindingresource vfr 
    ON vf.id = vfr.vulnerability_finding_id
JOIN 
  cloudplatform_resource r 
    ON vfr.resource_id = r.id
WHERE 
  vf.first_seen IS NOT NULL
  AND vf.added IS NOT NULL
  AND vf.first_seen < vf.added - INTERVAL '7 days'
  AND vf.added BETWEEN '2025-01-01' AND '2025-04-24'  -- adjust range as needed
  AND r.provider = 'OP'
  AND r.type = 'CN'
GROUP BY 
  days_old
ORDER BY 
  days_old;
