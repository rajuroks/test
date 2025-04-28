
SELECT 
    wl.id AS workload_id,
    wl.added AS workload_added_date,
    wl.first_seen AS workload_first_seen_date,
    r.name AS namespace_name,
    cl.name AS cluster_name,
    i.name AS image_name
FROM 
    cloudplatform_workload wl
JOIN 
    cloudplatform_resource r ON wl.resource_id = r.id
LEFT JOIN 
    cloudplatform_resource cl ON r.parent_id = cl.id AND cl.type = 'CL'
JOIN 
    cloudplatform_image i ON wl.image_id = i.id
WHERE 
    r.provider = 'OP'
    AND r.type = 'CN'
    AND wl.added >= '2025-04-20'
ORDER BY 
    wl.added;
