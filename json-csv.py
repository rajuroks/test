
WITH recent_notifications AS (
  SELECT *
  FROM vm_data.cloudplatform_notification
  WHERE added >= DATE '2024-06-01'
    AND added < DATE '2025-04-23'
)

SELECT
  COALESCE(rwo.eonid, rro.eonid, rio.eonid) AS eonid,
  n.id AS notification_id,
  n.added AS notified_date,
  n.remediation_due_date,
  vf.last_seen,
  CASE 
    WHEN n.remediation_due_date < CURRENT_DATE THEN 'Yes'
    ELSE 'No'
  END AS is_overdue

FROM vm_data.cloudplatform_vulnerabilityfinding vf
LEFT JOIN vm_data.cloudplatform_vulnerabilitynotification vn
  ON vf.id = vn.vulnerability_finding_id
LEFT JOIN recent_notifications n
  ON vn.notification_id = n.id

-- Join workload (CN)
LEFT JOIN vm_data.cloudplatform_vulnerabilityfindingworkload vfw
  ON vf.id = vfw.vulnerability_finding_id
LEFT JOIN vm_data.cloudplatform_workload w
  ON vfw.workload_id = w.id
LEFT JOIN vm_data.cloudplatform_resource rw
  ON w.resource_id = rw.id
LEFT JOIN vm_data.cloudplatform_ownership rwo
  ON rw.ownership_id = rwo.id

-- Join resource (VM, SC)
LEFT JOIN vm_data.cloudplatform_vulnerabilityfindingresource vfr
  ON vf.id = vfr.vulnerability_finding_id
LEFT JOIN vm_data.cloudplatform_resource rr
  ON vfr.resource_id = rr.id
LEFT JOIN vm_data.cloudplatform_ownership rro
  ON rr.ownership_id = rro.id

-- Join image
LEFT JOIN vm_data.cloudplatform_vulnerabilityfindingimage vfi
  ON vf.id = vfi.vulnerability_finding_id
LEFT JOIN vm_data.cloudplatform_image i
  ON vfi.image_id = i.id
LEFT JOIN vm_data.cloudplatform_ownership rio
  ON i.ownership_id = rio.id

WHERE 
  DATE(vf.last_seen) = CURRENT_DATE - INTERVAL '1 day'
  AND n.id IS NOT NULL
  AND COALESCE(rwo.eonid, rro.eonid, rio.eonid) IS NOT NULL

ORDER BY notification_id;
