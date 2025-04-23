
SELECT
    n.id AS notification_id,
    rwlo.eonid AS eonid,
    n.remediation_due_date,
    COUNT(DISTINCT rr.id) AS resource_count,
    n.added
FROM
    vn_data.cloudplatform_vulnerabilityfinding AS vf
    JOIN vn_data.cloudplatform_vulnerabilityfinding AS vfv ON vfv.id = vf.id
    LEFT OUTER JOIN vn_data.cloudplatform_vulnerabilityfindingworkload AS vfw ON vfw.vulnerabilityfinding_id = vf.id
    LEFT OUTER JOIN vn_data.cloudplatform_vulnerabilityfindingresource AS vfr ON vfr.vulnerabilityfinding_id = vf.id  -- This line
    LEFT OUTER JOIN vn_data.cloudplatform_resource AS rr ON rr.id = vfr.resource_id
    LEFT OUTER JOIN vn_data.cloudplatform_workload AS w ON w.id = vfw.workload_id
    LEFT OUTER JOIN vn_data.cloudplatform_resource AS rwl ON rwl.id = w.resource_id
    LEFT OUTER JOIN vn_data.cloudplatform_ownership AS rro ON rro.resource_id = rr.id
    LEFT OUTER JOIN vn_data.cloudplatform_ownership AS rwlo ON rwlo.resource_id = rwl.id
    LEFT OUTER JOIN vn_data.cloudplatform_vulnerability_notification AS vn ON vn.vulnerabilityfinding_id = vf.id
    LEFT OUTER JOIN vn_data.cloudplatform_notification AS n ON n.id = vn.notification_id
WHERE
    n.added IS NOT NULL
    AND n.added > CURRENT_DATE - INTERVAL '60 days'
    AND rwlo.eonid NOT IN ('123456')
GROUP BY
    n.id,
    rwlo.eonid,
    n.remediation_due_date,
    n.added
