WITH recent_notifications AS (
    SELECT *
    FROM vm_data.cloudplatform_notification
    WHERE added IS NOT NULL
      AND added BETWEEN DATE '2024-01-01' AND DATE '2024-03-01'
)

SELECT 
    n.notification_id,
    rwo.eonid,
    n.remediation_due_date,
    COUNT(DISTINCT vfr.resource_id) AS resource_count,
    n.added
FROM 
    vm_data.cloudplatform_vulnerabilityfinding AS vf
JOIN vm_data.cloudplatform_vulnerability AS v ON vf.vulnerability_id = v.id
LEFT JOIN vm_data.cloudplatform_vulnerabilityfindingworkload AS vfw ON vf.id = vfw.vulnerabilityfinding_id
LEFT JOIN vm_data.cloudplatform_vulnerabilityfindingresource AS vfr ON vf.id = vfr.vulnerabilityfinding_id
LEFT JOIN vm_data.cloudplatform_resource AS r ON vfr.resource_id = r.id
LEFT JOIN vm_data.cloudplatform_workload AS w ON vfw.workload_id = w.id
LEFT JOIN vm_data.cloudplatform_ownership AS rwo ON r.id = rwo.id
LEFT JOIN vm_data.cloudplatform_vulnerabilitynotification AS vn ON vn.vulnerability_finding_id = vf.id
LEFT JOIN recent_notifications AS n ON vn.notification_id = n.id
WHERE 
    vf.last_seen > n.remediation_due_date
    AND ('123456' = '123456' OR rwo.eonid NOT IN ('123456'))  -- Modify as needed
GROUP BY 
    n.notification_id,
    rwo.eonid,
    n.remediation_due_date,
    n.added;
