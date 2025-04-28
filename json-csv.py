
SELECT 
    vf.id AS finding_id,
    vf.added AS finding_added_date,
    wl.first_seen AS workload_first_seen_date,
    DATE_PART('day', vf.added - wl.first_seen) AS days_old
FROM 
    cloudplatform_vulnerabilityfindingworkload vf
JOIN 
    cloudplatform_workload wl ON vf.workload_id = wl.id
WHERE 
    vf.added >= CURRENT_DATE - INTERVAL '4 days'
    AND wl.first_seen < CURRENT_DATE - INTERVAL '4 days'
ORDER BY 
    days_old DESC;
