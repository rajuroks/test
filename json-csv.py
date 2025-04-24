SELECT 
    img.id AS image_id,
    img.name AS image_name,
    img.release,
    img.registry,
    wl.id AS workload_id,
    wl.first_seen AS workload_first_seen,
    res.name AS resource_name,
    res.provider AS platform_provider,
    res.type AS platform_type
FROM 
    cloudplatform_image img
JOIN 
    cloudplatform_workload wl ON img.id = wl.image_id
JOIN 
    cloudplatform_resource res ON wl.resource_id = res.id
WHERE 
    res.type = 'CN'   -- filter for containers
LIMIT 10;
