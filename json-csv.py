
SELECT 
    CASE WHEN vf.added < '2025-04-20' THEN 'Before 04/20' ELSE 'From 04/20' END AS period,
    COUNT(*) AS finding_count
FROM 
    cloudplatform_vulnerabilityfindingworkload vf
JOIN 
    cloudplatform_workload wl ON vf.workload_id = wl.id
JOIN 
    cloudplatform_resource r ON wl.resource_id = r.id
WHERE 
    r.provider = 'OP'
GROUP BY 
    period;



SELECT 
    CASE 
        WHEN wl.first_seen >= '2025-04-20' THEN 'New Workloads'
        ELSE 'Old Workloads'
    END AS workload_type,
    COUNT(*) AS finding_count
FROM 
    cloudplatform_vulnerabilityfindingworkload vf
JOIN 
    cloudplatform_workload wl ON vf.workload_id = wl.id
JOIN 
    cloudplatform_resource r ON wl.resource_id = r.id
WHERE 
    r.provider = 'OP'
    AND vf.added >= '2025-04-20'
GROUP BY 
    workload_type;
