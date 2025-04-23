SELECT
    vf.id AS notification_id,
    rwlo.eonid AS eonid,
    vf.remediation_due_date,
    COUNT(DISTINCT rr.id) AS resource_count,
    vf.added
FROM
    vm_data.cloudplatform_notification AS vf
    LEFT OUTER JOIN vm_data.cloudplatform_vulnerabilityfindingresource AS vfr ON vfr.notification_id = vf.id
    LEFT OUTER JOIN vm_data.cloudplatform_resource AS rr ON rr.id = vfr.resource_id
    LEFT OUTER JOIN vm_data.cloudplatform_ownership AS rwlo ON rwlo.resource_id = rr.id
WHERE
    vf.added IS NOT NULL
    AND vf.added > CURRENT_DATE - INTERVAL '60 days'
    AND (rwlo.eonid NOT IN ('123456') OR rwlo.eonid IS NULL)
    AND vf.remediation_due_date IS NOT NULL
    AND vfr.last_seen > vf.remediation_due_date
GROUP BY
    vf.id,
    rwlo.eonid,
    vf.remediation_due_date,
    vf.added
