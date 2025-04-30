
WITH recent_notifications AS (
  SELECT *
  FROM vm_data.cloudplatform_notification
  WHERE added >= DATE '2024-06-01'
    AND added < DATE '2025-04-23'
),
notification_counts AS (
  SELECT 
    n.id AS notification_id,
    COUNT(DISTINCT vfw.workload_id) AS workload_count
  FROM vm_data.cloudplatform_vulnerabilityfinding vf
  JOIN vm_data.cloudplatform_vulnerabilityfindingworkload vfw
    ON vf.id = vfw.vulnerability_finding_id
  JOIN vm_data.cloudplatform_vulnerabilitynotification vn
    ON vf.id = vn.vulnerability_finding_id
  JOIN recent_notifications n
    ON vn.notification_id = n.id
  WHERE DATE(vf.last_seen) = CURRENT_DATE - INTERVAL '1 day'
  GROUP BY n.id
)

SELECT 
  vf.id AS finding_id,
  vfw.workload_id,
  rwlo.eonid AS workload_eonid,
  CASE 
    WHEN n.remediation_due_date < CURRENT_DATE THEN 'Yes'
    ELSE 'No'
  END AS is_overdue,
  DATE_PART('day', vf.last_seen - n.remediation_due_date) AS days_overdue,
  n.notification_id,
  n.added AS notified_date,
  nc.workload_count,
  stix.name AS cve_id,
  stix.vm_severity,
  stix.vm_exploitability,
  r.type AS resource_type,
  r.provider AS resource_provider,
  vf.last_seen,
  n.remediation_due_date

FROM vm_data.cloudplatform_vulnerabilityfinding AS vf
JOIN vm_data.cloudplatform_vulnerability AS v
  ON vf.vulnerability_id = v.id
JOIN vm_data.cloudplatform_vulnerabilitynotification AS vn
  ON vf.id = vn.vulnerability_finding_id
JOIN recent_notifications AS n
  ON vn.notification_id = n.id
JOIN notification_counts AS nc
  ON n.id = nc.notification_id

JOIN vm_data.cloudplatform_vulnerabilityfindingworkload AS vfw
  ON vf.id = vfw.vulnerability_finding_id
JOIN vm_data.cloudplatform_workload AS w
  ON vfw.workload_id = w.id
JOIN vm_data.cloudplatform_resource AS r
  ON w.resource_id = r.id
JOIN vm_data.cloudplatform_ownership AS rwlo
  ON r.ownership_id = rwlo.id

-- CVE join remains optional
LEFT JOIN vm_data.cloudplatform_vulnerabilitysource AS vs
  ON v.source_id = vs.id
LEFT JOIN vm_data.acti_stix_vulns AS stix
  ON vs.notes = stix.name

WHERE 
  DATE(vf.last_seen) = CURRENT_DATE - INTERVAL '1 day'

ORDER BY n.notification_id;
