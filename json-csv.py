
WITH recent_notifications AS (
  SELECT *
  FROM vm_data.cloudplatform_notification
  WHERE added >= DATE '2024-06-01'
    AND added < DATE '2025-04-23'
),
all_findings AS (
  SELECT 
    vf.id AS finding_id,
    vfw.workload_id,
    rwlo.eonid,
    CASE 
      WHEN n.remediation_due_date < CURRENT_DATE THEN 'Yes'
      ELSE 'No'
    END AS is_overdue,
    vf.last_seen,
    DATE_PART('day', vf.last_seen - n.remediation_due_date) AS days_overdue,
    n.notification_id,
    n.added AS notified_date,
    n.remediation_due_date,
    r.type AS resource_type,
    r.provider AS resource_provider,
    cve.name AS cve_id,
    stix.vm_severity,
    stix.vm_exploitability
  FROM vm_data.cloudplatform_vulnerabilityfinding AS vf
  JOIN vm_data.cloudplatform_vulnerability AS v
    ON vf.vulnerability_id = v.id
  JOIN vm_data.cloudplatform_vulnerabilitynotification AS vn
    ON vf.id = vn.vulnerability_finding_id
  JOIN recent_notifications AS n
    ON vn.notification_id = n.id
  JOIN vm_data.cloudplatform_vulnerabilityfindingworkload AS vfw
    ON vf.id = vfw.vulnerability_finding_id
  JOIN vm_data.cloudplatform_workload AS w
    ON vfw.workload_id = w.id
  JOIN vm_data.cloudplatform_resource AS r
    ON w.resource_id = r.id
  JOIN vm_data.cloudplatform_ownership AS rwlo
    ON r.ownership_id = rwlo.id
  LEFT JOIN vm_data.cloudplatform_vulnerabilitysource AS vs
    ON v.source_id = vs.id
  LEFT JOIN vm_data.cloudplatform_vulnerabilitysourcecve AS vsc
    ON vs.id = vsc.vulnerability_source_id
  LEFT JOIN vm_data.cloudplatform_cve AS cve
    ON vsc.cve_id = cve.id
  LEFT JOIN vm_data.acti_stix_vulns AS stix
    ON cve.name = stix.name
  WHERE 
    DATE(vf.last_seen) = CURRENT_DATE - INTERVAL '1 day'
)

SELECT 
  notification_id,
  cve_id,
  MAX(notified_date) AS notified_date,
  MAX(remediation_due_date) AS remediation_due_date,
  STRING_AGG(DISTINCT eonid::text, ', ') AS eonid,
  MAX(resource_type) AS resource_type,
  MAX(resource_provider) AS resource_provider,
  MAX(vm_severity) AS vm_severity,
  MAX(vm_exploitability) AS vm_exploitability,
  MAX(last_seen) AS last_seen,
  MAX(days_overdue) AS max_days_overdue,
  MAX(is_overdue) AS is_overdue,
  COUNT(DISTINCT workload_id) AS resource_count

FROM all_findings
GROUP BY notification_id, cve_id
ORDER BY notification_id;
