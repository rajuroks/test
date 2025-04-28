WITH workload_data AS (
    SELECT 
        wl.id AS workload_id,
        r.name AS namespace_name,
        cl.name AS cluster_name,
        i.name AS image_name,
        wl.first_seen
    FROM 
        cloudplatform_workload wl
    JOIN 
        cloudplatform_resource r ON wl.resource_id = r.id   -- r is namespace (CN)
    LEFT JOIN 
        cloudplatform_resource cl ON r.parent_id = cl.id AND cl.type = 'CL' -- cl is cluster (CL)
    JOIN 
        cloudplatform_image i ON wl.image_id = i.id          -- 🔥 image linked to workload
    WHERE 
        r.provider = 'OP'
        AND r.type = 'CN'
)

SELECT 
    namespace_name,
    cluster_name,
    image_name,
    SUM(CASE WHEN first_seen < '2025-04-20' THEN 1 ELSE 0 END) AS workloads_before_0420,
    SUM(CASE WHEN first_seen >= '2025-04-20' THEN 1 ELSE 0 END) AS workloads_from_0420
FROM 
    workload_data
GROUP BY 
    namespace_name,
    cluster_name,
    image_name
ORDER BY 
    workloads_from_0420 DESC;
