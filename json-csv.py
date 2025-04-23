
SELECT DISTINCT
    n.id AS notification_id,
    rro.eonid,
    n.remediation_due_date,
    COUNT(rr.id) AS resource_count
FROM
    (
        SELECT *
        FROM vm_data.cloudplatform_notification
        WHERE
            added IS NOT NULL
            AND remediation_due_date::date <= '2025-04-22'
            AND added >= '2025-01-01 00:00:00.000 -0500'
            AND added <= '2025-04-22 23:59:59.999 -0500'
    ) n
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
    vm_data.cloudplatform_resource AS rr 
    ON vfw.vulnerability_id = rr.id 
    AND rr.last_seen > n.remediation_due_date
LEFT OUTER JOIN
    vm_data.cloudplatform_ownership AS rro ON rr.ownership_id = rro.id
WHERE
    rro.eonid IN ('')
GROUP BY
    n.id,
    rro.eonid,
