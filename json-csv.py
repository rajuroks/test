
SELECT
    vf.id AS notification_id,
    rwlo.eonid AS eonid,
    vf.remediation_due_date,
    COUNT(DISTINCT rr.id) AS resource_count,
    vf.added
FROM
    vm_data.cloudplatform_notification AS vf  -- Updated table name
    LEFT OUTER JOIN vn_data.cloudplatform_vulnerability_notification AS vn ON vn.notification_id = vf.id  -- Link notifications to vulnerability notifications
    LEFT OUTER JOIN vn_data.cloudplatform_vulnerabilityfindingresource AS vfr ON vfr.id = vn.vulnerabilityfinding_id  -- Link vulnerability findings to resources
    LEFT OUTER JOIN vn_data.cloudplatform_resource AS rr ON rr.id = vfr.resource_id  -- Link resources
    LEFT OUTER JOIN vn_data.cloudplatform_resource AS rwl ON rwl.id = rr.id  -- Link additional resource for ownership
    LEFT OUTER JOIN vn_data.cloudplatform_ownership AS rwlo ON rwlo.resource_id = rwl.id  -- Link ownership for eonid
WHERE
    vf.added IS NOT NULL
    AND vf.added > CURRENT_DATE - INTERVAL '60 days'
    AND rwlo.eonid NOT IN ('123456')
GROUP BY
    vf.id,
    rwlo.eonid,
    vf.remediation_due_date,
    vf.added
