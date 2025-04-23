WITH recent_notifications AS (
    SELECT *
    FROM vm_data.cloudplatform_notification
    WHERE added >= DATE '2024-01-01'
      AND added <  DATE '2024-03-02'
)

SELECT
    vn.notification_id,
    rwo.eonid    AS direct_resource_eonid,
    rro.eonid    AS vuln_id_resource_eonid,    -- ADDED
    img_o.eonid  AS image_resource_eonid,
    rw1o.eonid   AS workload_resource_eonid,
    n.remediation_due_date,
    (
      COUNT(DISTINCT vfr.resource_id)
    + COUNT(DISTINCT vfi.resource_id)
    + COUNT(DISTINCT rw1.id)
    + COUNT(DISTINCT rr.id)                  -- ADDED to include rr resources
    )              AS total_resource_count,
    n.added,
    r.type        AS direct_resource_type,
    rimg.type     AS image_resource_type,
    vf.last_seen
FROM vm_data.cloudplatform_vulnerabilityfinding AS vf
  JOIN vm_data.cloudplatform_vulnerability          AS v   ON vf.vulnerability_id = v.id

  -- 1) direct finding → resource
  LEFT JOIN vm_data.cloudplatform_vulnerabilityfindingresource AS vfr
    ON vf.id = vfr.vulnerabilityfinding_id
  LEFT JOIN vm_data.cloudplatform_resource              AS r
    ON vfr.resource_id = r.id

  -- 2) finding → image → resource
  LEFT JOIN vm_data.cloudplatform_vulnerabilityfindingimage AS vfi
    ON vf.id = vfi.vulnerabilityfinding_id
  LEFT JOIN vm_data.cloudplatform_resource              AS rimg
    ON vfi.resource_id = rimg.id

  -- 3) finding → workload → resource
  LEFT JOIN vm_data.cloudplatform_vulnerabilityfindingworkload AS vfw
    ON vf.id = vfw.vulnerabilityfinding_id
  LEFT JOIN vm_data.cloudplatform_workload                 AS w
    ON vfw.workload_id = w.id
  LEFT JOIN vm_data.cloudplatform_resource                 AS rw1
    ON w.resource_id = rw1.id

  -- 4) vulnerability-id → resource (rr) → ownership (rro)
  LEFT JOIN vm_data.cloudplatform_resource              AS rr
    ON vf.vulnerability_id = rr.id                     -- ADDED
  LEFT JOIN vm_data.cloudplatform_ownership            AS rro
    ON rr.ownership_id = rro.id                        -- ADDED

  -- ownership for each context
  LEFT JOIN vm_data.cloudplatform_ownership AS rwo   ON r.ownership_id    = rwo.id
  LEFT JOIN vm_data.cloudplatform_ownership AS img_o ON rimg.ownership_id = img_o.id
  LEFT JOIN vm_data.cloudplatform_ownership AS rw1o  ON rw1.ownership_id  = rw1o.id

  -- notifications
  LEFT JOIN vm_data.cloudplatform_vulnerabilitynotification AS vn
    ON vf.id = vn.vulnerability_finding_id
  LEFT JOIN recent_notifications                        AS n
    ON vn.notification_id = n.id

WHERE
    n.id IS NOT NULL
    AND vf.last_seen > n.remediation_due_date
    AND (
         rwo.eonid  IN ('123456','123456')
      OR rro.eonid  IN ('123456','123456')        -- ADDED
      OR img_o.eonid IN ('123456','123456')
      OR rw1o.eonid IN ('123456','123456')
    )
GROUP BY
    vn.notification_id,
    rwo.eonid,
    rro.eonid,                                    -- ADDED
    img_o.eonid,
    rw1o.eonid,
    n.remediation_due_date,
    n.added,
    r.type,
    rimg.type,
    vf.last_seen
ORDER BY
    vn.notification_id;
