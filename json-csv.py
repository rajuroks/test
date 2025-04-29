
SELECT 
    CASE 
        WHEN wl.added BETWEEN '2025-04-13' AND '2025-04-19' THEN 'Week Before 04/20'
        WHEN wl.added BETWEEN '2025-04-20' AND '2025-04-26' THEN 'Week After 04/20'
    END AS period,
    COUNT(DISTINCT wl.id) AS workload_count
FROM 
    cloudplatform_workload wl
JOIN 
    cloudplatform_resource r ON wl.resource_id = r.id
WHERE 
    r.provider = 'OP'
    AND r.type = 'CN'
    AND wl.added BETWEEN '2025-04-13' AND '2025-04-26'
GROUP BY 
    period;




SELECT 
    CASE 
        WHEN vf.added BETWEEN '2025-04-13' AND '2025-04-19' THEN 'Week Before 04/20'
        WHEN vf.added BETWEEN '2025-04-20' AND '2025-04-26' THEN 'Week After 04/20'
    END AS period,
    COUNT(*) AS finding_count
FROM 
    cloudplatform_vulnerabilityfindingworkload vf
JOIN 
    cloudplatform_workload wl ON vf.workload_id = wl.id
JOIN 
    cloudplatform_resource r ON wl.resource_id = r.id
WHERE 
    r.provider = 'OP'
    AND r.type = 'CN'
    AND vf.added BETWEEN '2025-04-13' AND '2025-04-26'
GROUP BY 
    period;




SELECT 
    wl.id AS workload_id,
    wl.added AS workload_added_date,
    MIN(vf.added) AS first_finding_added_date,
    DATE_PART('day', MIN(vf.added) - wl.added) AS days_delay
FROM 
    cloudplatform_workload wl
JOIN 
    cloudplatform_vulnerabilityfindingworkload vf ON vf.workload_id = wl.id
JOIN 
    cloudplatform_resource r ON wl.resource_id = r.id
WHERE 
    r.provider = 'OP'
    AND r.type = 'CN'
    AND wl.added BETWEEN '2025-04-13' AND '2025-04-26'
GROUP BY 
    wl.id, wl.added
ORDER BY 
    workload_added_date;



