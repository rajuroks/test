
WITH recent_notifications AS (
  SELECT *
  FROM vm_data.cloudplatform_notification
  WHERE added >= DATE '2024-06-01'
    AND added < DATE '2025-04-23'
)

SELECT 
  vf.id AS finding_id,
  vfw.workload_id,
  rwlo.eonid AS workload_eonid,
  CASE 
    WHEN vf.last_seen >= n.remediation_due_date THEN 'Yes'
    ELSE 'No'
  END AS is_overdue,
  DATE_PART('day', vf.last_seen - n.remediation_due_date) AS days_overdue,
  n.notification_id,
  r.type AS resource_type,
  r.provider AS resource_provider,
  vf.last_seen,
  n.remediation_due_date

FROM vm_data.cloudplatform_vulnerabilityfinding AS vf
JOIN vm_data.cloudplatform_vulnerability AS v
  ON vf.vulnerability_id = v.id

LEFT JOIN vm_data.cloudplatform_vulnerabilityfindingworkload AS vfw
  ON vf.id = vfw.vulnerability_finding_id
LEFT JOIN vm_data.cloudplatform_workload AS w
  ON vfw.workload_id = w.id
LEFT JOIN vm_data.cloudplatform_resource AS r
  ON w.resource_id = r.id
LEFT JOIN vm_data.cloudplatform_ownership AS rwlo
  ON r.ownership_id = rwlo.id

LEFT JOIN vm_data.cloudplatform_vulnerabilitynotification AS vn
  ON vf.id = vn.vulnerability_finding_id
LEFT JOIN recent_notifications AS n
  ON vn.notification_id = n.id

WHERE 
  vfw.workload_id IS NOT NULL
  AND n.id IS NOT NULL
  AND vf.last_seen IS NOT NULL
  AND n.remediation_due_date IS NOT NULL

ORDER BY n.notification_id;
