WITH recent_findings AS (
    SELECT 
        vf.id,
        vf.added,
        wl.first_seen,
        c.name AS cve_id,
        i.name AS image_name,
        r.name AS resource_name,
        r.provider,
        r.type
    FROM 
        cloudplatform_vulnerabilityfindingworkload vf
    JOIN cloudplatform_workload wl ON vf.workload_id = wl.id
    JOIN cloudplatform_resource r ON wl.resource_id = r.id
    JOIN cloudplatform_image i ON wl.image_id = i.id
    JOIN cloudplatform_vulnerabilityfinding vfind ON vf.vulnerability_finding_id = vfind.id
    JOIN cloudplatform_vulnerability v ON vfind.vulnerability_id = v.id
    JOIN cloudplatform_vulnerabilitysource vs ON vs.id = v.source_id
    JOIN cloudplatform_vulnerabilitysourcecve vsc ON vsc.vulnerability_source_id = vs.id
    JOIN cloudplatform_cve c ON c.id = vsc.cve_id
    WHERE 
        vf.added >= CURRENT_DATE - INTERVAL '4 days'
        AND r.provider = 'OP'
        AND r.type = 'CN'
),
previous_findings AS (
    SELECT DISTINCT 
        c.name AS cve_id,
        i.name AS image_name
    FROM 
        cloudplatform_vulnerabilityfindingworkload vf
    JOIN cloudplatform_workload wl ON vf.workload_id = wl.id
    JOIN cloudplatform_resource r ON wl.resource_id = r.id
    JOIN cloudplatform_image i ON wl.image_id = i.id
    JOIN cloudplatform_vulnerabilityfinding vfind ON vf.vulnerability_finding_id = vfind.id
    JOIN cloudplatform_vulnerability v ON vfind.vulnerability_id = v.id
    JOIN cloudplatform_vulnerabilitysource vs ON vs.id = v.source_id
    JOIN cloudplatform_vulnerabilitysourcecve vsc ON vsc.vulnerability_source_id = vs.id
    JOIN cloudplatform_cve c ON c.id = vsc.cve_id
    WHERE 
        vf.added < CURRENT_DATE - INTERVAL '4 days'
        AND r.provider = 'OP'
        AND r.type = 'CN'
)
SELECT *
FROM recent_findings rf
WHERE NOT EXISTS (
    SELECT 1 
    FROM previous_findings pf
    WHERE rf.cve_id = pf.cve_id
      AND rf.image_name = pf.image_name
)
ORDER BY rf.added DESC;
