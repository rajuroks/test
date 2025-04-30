
WITH recent_notifications AS (
  SELECT *
  FROM vm_data.cloudplatform_notification
  WHERE added >= DATE '2024-06-01'
    AND added < DATE '2025-04-23'
),

all_findings AS (
  -- 🧩 Workload-based findings (CN)
  SELECT 
    vf.id AS finding_id,
    n.notification_id,
    n.added AS notified_date,
    n.remediation_due_date,
    vf.last_seen,
    vfw.workload_id AS entity_id,
    rwlo.eonid,
    r.type AS resource_type,
    r.provider AS resource_provider,
    cve.name AS cve_id,
    stix.vm_severity,
    stix.vm_exploitability,
    CASE 
      WHEN n.remediation_due_date < CURRENT_DATE THEN 'Yes'
      ELSE 'No'
    END AS is_overdue
  FROM vm_data.cloudplatform_vulnerabilityfinding vf
  JOIN vm_data.cloudplatform_vulnerability v
    ON vf.vulnerability_id = v.id
  JOIN vm_data.cloudplatform_vulnerabilitynotification vn
    ON vf.id = vn.vulnerability_finding_id
  JOIN recent_notifications n
    ON vn.notification_id = n.id
  JOIN vm_data.cloudplatform_vulnerabilityfindingworkload vfw
    ON vf.id = vfw.vulnerability_finding_id
  JOIN vm_data.cloudplatform_workload w
    ON vfw.workload_id = w.id
  JOIN vm_data.cloudplatform_resource r
    ON w.resource_id = r.id
  JOIN vm_data.cloudplatform_ownership rwlo
    ON r.ownership_id = rwlo.id
  LEFT JOIN vm_data.cloudplatform_vulnerabilitysource vs
    ON v.source_id = vs.id
  LEFT JOIN vm_data.cloudplatform_vulnerabilitysourcecve vsc
    ON vs.id = vsc.vulnerability_source_id
  LEFT JOIN vm_data.cloudplatform_cve cve
    ON vsc.cve_id = cve.id
  LEFT JOIN vm_data.acti_stix_vulns stix
    ON cve.name = stix.name
  WHERE DATE(vf.last_seen) = CURRENT_DATE - INTERVAL '1 day'

  UNION ALL

  -- 🧩 Resource-based findings (VM, SC, etc.)
  SELECT 
    vf.id AS finding_id,
    n.notification_id,
    n.added AS notified_date,
    n.remediation_due_date,
    vf.last_seen,
    vfr.resource_id AS entity_id,
    rwlo.eonid,
    r.type AS resource_type,
    r.provider AS resource_provider,
    cve.name AS cve_id,
    stix.vm_severity,
    stix.vm_exploitability,
    CASE 
      WHEN n.remediation_due_date < CURRENT_DATE THEN 'Yes'
      ELSE 'No'
    END AS is_overdue
  FROM vm_data.cloudplatform_vulnerabilityfinding vf
  JOIN vm_data.cloudplatform_vulnerability v
    ON vf.vulnerability_id = v.id
  JOIN vm_data.cloudplatform_vulnerabilitynotification vn
    ON vf.id = vn.vulnerability_finding_id
  JOIN recent_notifications n
    ON vn.notification_id = n.id
  JOIN vm_data.cloudplatform_vulnerabilityfindingresource vfr
    ON vf.id = vfr.vulnerability_finding_id
  JOIN vm_data.cloudplatform_resource r
    ON vfr.resource_id = r.id
  JOIN vm_data.cloudplatform_ownership rwlo
    ON r.ownership_id = rwlo.id
  LEFT JOIN vm_data.cloudplatform_vulnerabilitysource vs
    ON v.source_id = vs.id
  LEFT JOIN vm_data.cloudplatform_vulnerabilitysourcecve vsc
    ON vs.id = vsc.vulnerability_source_id
  LEFT JOIN vm_data.cloudplatform_cve cve
    ON vsc.cve_id = cve.id
  LEFT JOIN vm_data.acti_stix_vulns stix
    ON cve.name = stix.name
  WHERE DATE(vf.last_seen) = CURRENT_DATE - INTERVAL '1 day'
)

SELECT 
  notification_id,
  cve_id,
  MAX(notified_date) AS notified_date,
  MAX(remediation_due_date) AS remediation_due_date,
  STRING_AGG(DISTINCT eonid::text, ', ') AS eonid,
  STRING_AGG(DISTINCT resource_type, ', ') AS resource_type,
  STRING_AGG(DISTINCT resource_provider, ', ') AS resource_provider,
  MAX(vm_severity) AS vm_severity,
  MAX(vm_exploitability) AS vm_exploitability,
  MAX(last_seen) AS last_seen,
  MAX(is_overdue) AS is_overdue,
  COUNT(DISTINCT entity_id) AS resource_count

FROM all_findings
GROUP BY notification_id, cve_id
ORDER BY notification_id;
