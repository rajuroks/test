
WITH clusters_before_0420 AS (
    SELECT DISTINCT r.id
    FROM cloudplatform_resource r
    WHERE r.provider = 'OP'
      AND r.type = 'CL'
      AND r.first_seen < '2025-04-20'
),
clusters_after_0420 AS (
    SELECT 
        r.id,
        r.name AS cluster_name,
        r.first_seen,
        r.added
    FROM cloudplatform_resource r
    WHERE r.provider = 'OP'
      AND r.type = 'CL'
      AND r.first_seen >= '2025-04-20'
)

SELECT 
    a.cluster_name,
    a.first_seen AS cluster_first_seen,
    a.added AS cluster_added
FROM 
    clusters_after_0420 a
LEFT JOIN 
    clusters_before_0420 b ON a.id = b.id
WHERE 
    b.id IS NULL  -- ✅ Only clusters not existing before 04/20
ORDER BY 
    a.first_seen;
