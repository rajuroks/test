SELECT 
    n.notification_id,
    rw0.eonid,
    n.remediation_due_date,
    COUNT(DISTINCT vfr.resource_id) AS resource_count,
    n.added
FROM 
    vm_data.cloudplatform_vulnerabilityfinding AS vf
JOIN vm_data.cloudplatform_vulnerability AS v ON vf.vulnerability_id = v.id
LEFT OUTER JOIN vm_data.cloudplatform_vulnerabilityfindingworkload AS vfw ON vf.vulnerabilityfinding_id = vfw.id
LEFT OUTER JOIN vm_data.cloudplatform_vulnerabilityfindingresource AS vfr ON vf.vulnerability_finding_id = vfr.id
LEFT OUTER JOIN vm_data.cloudplatform_resource AS r ON vfr.resource_id = r.id
LEFT OUTER JOIN vm_data.cloudplatform_workload AS w ON vfw.workload_id = w.id
LEFT OUTER JOIN vm_data.cloudplatform_ownership AS rwo ON r.id = rwo.resource_id
LEFT OUTER JOIN vm_data.cloudplatform_vulnerabilitynotification AS vn ON vn.vulnerability_finding_id = vf.id
LEFT OUTER JOIN vm_data.cloudplatform_notification AS n ON vn.notification_id = n.id
WHERE 
    n.added IS NOT NULL 
    AND vf.last_seen > n.remediation_due_date
    AND n.added > CURRENT_DATE - INTERVAL '60 days'
    AND ('123456' = '123456' OR rwo.eonid NOT IN ('123456'))  -- Modify logic if needed
GROUP BY 
    n.notification_id,
    rw0.eonid,
    n.remediation_due_date,
    n.added;
