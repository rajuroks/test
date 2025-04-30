
WITH recent_notifications AS (
  SELECT *
  FROM vm_data.cloudplatform_notification
  WHERE added >= DATE '2024-06-01'
    AND added < DATE '2025-04-23'
),

all_findings AS (
  -- Workload-based findings (CN)
  SELECT 
    n.notification_id,
    rwlo.eonid,
    vf.last_seen,
    n.remediation_due_date,
    CASE 
      WHEN n.remediation_due_date < CURRENT_DATE THEN 'Yes'
      ELSE 'No'
    END AS is_overdue
  FROM vm_data.cloudplatform_vulnerabilityfinding vf
  LEFT JOIN vm_data.cloudplatform_vulnerabilitynotification vn
    ON vf.id = vn.vulnerability_finding_id
  LEFT JOIN recent_notifications n
    ON vn.notification_id = n.id
  LEFT JOIN vm_data.cloudplatform_vulnerabilityfindingworkload vfw
    ON vf.id = vfw.vulnerability_finding_id
  LEFT JOIN vm_data.cloudplatform_workload w
    ON vfw.workload_id = w.id
  LEFT JOIN vm_data.cloudplatform_resource r
    ON w.resource_id = r.id
  LEFT JOIN vm_data.cloudplatform_ownership rwlo
    ON r.ownership_id = rwlo.id
  WHERE DATE(vf.last_seen) = CURRENT_DATE - INTERVAL '1 day'

  UNION ALL

  -- Resource-based findings (VM, SC, etc.)
  SELECT 
    n.notification_id,
    rwlo.eonid,
    vf.last_seen,
    n.remediation_due_date,
    CASE 
      WHEN n.remediation_due_date < CURRENT_DATE THEN 'Yes'
      ELSE 'No'
    END AS is_overdue
  FROM vm_data.cloudplatform_vulnerabilityfinding vf
  LEFT JOIN vm_data.cloudplatform_vulnerabilitynotification vn
    ON vf.id = vn.vulnerability_finding_id
  LEFT JOIN recent_notifications n
    ON vn.notification_id = n.id
  LEFT JOIN vm_data.cloudplatform_vulnerabilityfindingresource vfr
    ON vf.id = vfr.vulnerability_finding_id
  LEFT JOIN vm_data.cloudplatform_resource r
    ON vfr.resource_id = r.id
  LEFT JOIN vm_data.cloudplatform_ownership rwlo
    ON r.ownership_id = rwlo.id
  WHERE DATE(vf.last_seen) = CURRENT_DATE - INTERVAL '1 day'

  UNION ALL

  -- Image-based findings
  SELECT 
    n.notification_id,
    rwlo.eonid,
    vf.last_seen,
    n.remediation_due_date,
    CASE 
      WHEN n.remediation_due_date < CURRENT_DATE THEN 'Yes'
      ELSE 'No'
    END AS is_overdue
  FROM vm_data.cloudplatform_vulnerabilityfinding vf
  LEFT JOIN vm_data.cloudplatform_vulnerabilitynotification vn
    ON vf.id = vn.vulnerability_finding_id
  LEFT JOIN recent_notifications n
    ON vn.notification_id = n.id
  LEFT JOIN vm_data.cloudplatform_vulnerabilityfindingimage vfi
    ON vf.id = vfi.vulnerability_finding_id
  LEFT JOIN vm_data.cloudplatform_image img
    ON vfi.image_id = img.id
  LEFT JOIN vm_data.cloudplatform_resource r
    ON vfi.resource_id = r.id
  LEFT JOIN vm_data.cloudplatform_ownership rwlo
    ON r.ownership_id = rwlo.id
  WHERE DATE(vf.last_seen) = CURRENT_DATE - INTERVAL '1 day'
)

SELECT *
FROM all_findings
WHERE 
  notification_id IS NOT NULL
  AND remediation_due_date IS NOT NULL
  AND eonid IS NOT NULL
ORDER BY notification_id;
