SELECT 
    wl.id AS workload_id,
    wl.first_seen AS workload_first_seen_date,
    r.name AS container_resource_name,
    i.name AS image_name,
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
    vf.added >= CURRENT_DATE - INTERVAL '4 days'   -- Finding inserted recently (to detect new bump)
    AND wl.first_seen < CURRENT_DATE - INTERVAL '4 days'  -- Workload is old
ORDER BY 
    wl.first_seen;
