
SELECT 
    vf.id AS finding_id,
    vf.added,
    wl.first_seen,
    r.name AS resource_name,
    r.type AS resource_type,
    r.provider AS resource_provider
FROM 
    cloudplatform_vulnerabilityfindingworkload vf
JOIN 
    cloudplatform_workload wl ON vf.workload_id = wl.id
JOIN 
    cloudplatform_resource r ON wl.resource_id = r.id
WHERE 
    vf.added >= '2025-01-01'  -- Adjust time range as needed
    AND DATE_PART('day', vf.added - wl.first_seen) > 7
    AND r.provider = 'OP'
    AND r.type = 'CN'
ORDER BY 
    vf.added DESC
LIMIT 50;  -- Add limit to test with smaller set
