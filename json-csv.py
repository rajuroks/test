
SELECT 
    r.id AS container_id,
    r.name AS container_name,
    cl.id AS cluster_id,
    cl.name AS cluster_name
FROM 
    cloudplatform_resource r
LEFT JOIN 
    cloudplatform_resource cl ON r.parent_id = cl.id AND cl.type = 'CL'
WHERE 
    r.type = 'CN'
    AND r.provider = 'OP'
LIMIT 20;
