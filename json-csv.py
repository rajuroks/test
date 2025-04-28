
SELECT 
    r.name AS container_resource_name,
    i.name AS image_name,
    cl.name AS cluster_name,
    wl.first_seen AS workload_first_seen_date,
    MIN(vf.added) AS oldest_finding_added_date,
    DATE_PART('day', MIN(vf.added) - wl.first_seen) AS days_old
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
    vf.added >= CURRENT_DATE - INTERVAL '4 days'   -- findings inserted recently
    AND wl.first_seen < CURRENT_DATE - INTERVAL '4 days' -- workloads seen earlier
    AND r.provider = 'OP'                          -- ✅ only new data source
    AND r.type = 'CN'                              -- ✅ only containers
GROUP BY 
    r.name, i.name, cl.name, wl.first_seen
ORDER BY 
    days_old DESC;
