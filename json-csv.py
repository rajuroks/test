SELECT
    n.id AS notification_id,
    rwlo.eonid AS eonid,
    n.remediation_due_date,
    COUNT(DISTINCT rr.id) AS resource_count,  -- Counting distinct resources associated with the notification
    n.added
FROM
    vn_data.cloudplatform_vulnerabilityfinding AS vf
    JOIN vn_data.cloudplatform_vulnerabilityfinding AS vfv
    LEFT OUTER JOIN vn_data.cloudplatform_vulnerabilityfindingworkload AS vfw ON
    LEFT OUTER JOIN vn_data.cloudplatform_vulnerabilityfindingresource AS vfr ON
    LEFT OUTER JOIN vn_data.cloudplatform_resource AS rr ON
    LEFT OUTER JOIN vn_data.cloudplatform_workload AS w ON
    LEFT OUTER JOIN vn_data.cloudplatform_resource AS rwl ON
    LEFT OUTER JOIN vn_data.cloudplatform_ownership AS rro ON
    LEFT OUTER JOIN vn_data.cloudplatform_ownership AS rwlo ON
    LEFT OUTER JOIN vn_data.cloudplatform_vulnerability_notification AS vn ON
    LEFT OUTER JOIN vn_data.cloudplatform_notification AS n ON
WHERE
    n.added IS NOT NULL
    AND n.added > CURRENT_DATE - INTERVAL '60 days'
    AND ('123456' OR rwlo.eonid NOT IN ('123456'))
GROUP BY
    n.id,
    rwlo.eonid,
    n.remediation_due_date,
    n.added
