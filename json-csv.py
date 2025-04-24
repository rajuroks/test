
SELECT 
    DATE_PART('day', vf.added - wl.first_seen) AS days_old,
    COUNT(*) AS finding_count
FROM 
    cloudplatform_vulnerabilityfindingworkload vf
JOIN 
    cloudplatform_workload wl ON vf.workload_id = wl.id
JOIN 
    cloudplatform_resource r ON wl.resource_id = r.id
WHERE 
    vf.added >= '2025-01-01'  -- adjust your time range as needed
    AND DATE_PART('day', vf.added - wl.first_seen) > 7
    AND r.provider = 'OP'
    AND r.type = 'CN'
GROUP BY 
    days_old
ORDER BY 
    days_old;
