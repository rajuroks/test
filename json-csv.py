
WITH namespaces_before_0420 AS (
    SELECT DISTINCT r.id
    FROM cloudplatform_resource r
    WHERE r.provider = 'OP'
      AND r.type = 'CN'
      AND r.first_seen < '2025-04-20'
),
namespaces_after_0420 AS (
    SELECT 
        r.id,
        r.name AS namespace_name,
        r.first_seen,
        r.added,
        cl.name AS cluster_name
    FROM 
        cloudplatform_resource r
    LEFT JOIN 
        cloudplatform_resource cl ON r.parent_id = cl.id AND cl.type = 'CL'
    WHERE 
        r.provider = 'OP'
        AND r.type = 'CN'
        AND r.first_seen >= '2025-04-20'
)

SELECT 
    a.namespace_name,
    a.cluster_name,
    a.first_seen AS namespace_first_seen,
    a.added AS namespace_added
FROM 
    namespaces_after_0420 a
LEFT JOIN 
    namespaces_before_0420 b ON a.id = b.id
WHERE 
    b.id IS NULL  -- ✅ Only namespaces not existing before 04/20
ORDER BY 
    a.first_seen;
