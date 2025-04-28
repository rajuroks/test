
SELECT 
    vf.id AS finding_id,
    vf.added AS finding_added_date,
    wl.first_seen AS workload_first_seen_date,
    DATE_PART('day', vf.added - wl.first_seen) AS days_old,
    i.name AS image_name,
    r.name AS container_resource_name,
    cl.name AS cluster_name
FROM 
    cloudplatform_vulnerabilityfindingworkload vf
JOIN 
    cloudplatform_workload wl ON vf.workload_id = wl.id
JOIN 
    cloudplatform_resource r ON wl.resource_id = r.id
LEFT JOIN 
    cloudplatform_resource cl ON r.parent_id = cl.id AND cl.type = 'CL'
JOIN 
    cloudplatform_image i ON wl.image_id = i.id
WHERE 
    vf.added >= CURRENT_DATE - INTERVAL '4 days'
    AND wl.first_seen < CURRENT_DATE - INTERVAL '4 days'
ORDER BY 
    days_old DESC;
