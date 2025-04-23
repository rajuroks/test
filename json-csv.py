SELECT DISTINCT
    n.id AS notification_id,
    rro.eonid,
    n.remediation_due_date,
    n.added as notification_sent_date,
    COUNT(rr.id) AS resource_count
FROM
    vm_data.cloudplatform_notification n
LEFT OUTER JOIN
    vm_data.cloudplatform_vulnerabilitynotification AS vn ON vn.notification_id = n.id
LEFT OUTER JOIN
    vm_data.cloudplatform_vulnerabilityfindingworkload AS vfw ON vn.vulnerability_finding_id = vfw.vulnerability_finding_id
LEFT OUTER JOIN
    vm_data.cloudplatform_workload AS w ON vfw.workload_id = w.id
LEFT OUTER JOIN
    vm_data.cloudplatform_resource AS rwl ON w.resource_id = rwl.id
LEFT OUTER JOIN
    vm_data.cloudplatform_ownership AS rwlo ON rwl.ownership_id = rwlo.id
LEFT OUTER JOIN
    vm_data.cloudplatform_resource AS rr ON vfw.vulnerability_id = rr.id
LEFT OUTER JOIN
    vm_data.cloudplatform_ownership AS rro ON rr.ownership_id = rro.id
WHERE
    n.added IS NOT NULL
    AND rro.eonid IN ('')
GROUP BY
    n.id,
    rro.eonid,
    n.remediation_due_date,
    n.added
ORDER BY
    n.id;
