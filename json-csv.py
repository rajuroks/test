
WITH query_month(month, year) AS (
  VALUES(6, 2025)
),
query_date_range AS (
  SELECT
    (MAKE_DATE(query_month.year, query_month.month, 1))::timestamptz AS start_date,
    (MAKE_DATE(query_month.year, query_month.month, 1) + interval '1 month')::timestamptz AS end_date
  FROM query_month
),
rating_map(priority, exploitability, duration_days) AS (
  VALUES
    -- Add your mappings here, e.g.,
    ('High', 'High', 30),
    ('Medium', 'High', 45)
    -- etc.
)
SELECT
  vd.provider,
  vd.cvss_v3_temporal_score AS temporal_score,
  COUNT(DISTINCT vd.unique_id) AS count_gt_30d_notified,
  vd.notification_date + (interval '1 day' * r.duration_days) AS new_remediation_due_date
FROM
  vm_data.cloudplatform_vmarc_vulnerability_details AS vd
JOIN
  query_date_range AS qdr ON TRUE
JOIN
  rating_map AS r
  ON vd.priority = r.priority AND vd.exploitability = r.exploitability
WHERE
  vd.cvss_v3_temporal_score >= 9.4
  AND vd.vulnerability_first_seen < qdr.end_date
  AND vd.vulnerability_last_seen >= qdr.start_date
  AND vd.type != 'CI'
  AND vd.notification_id IS NOT NULL
  AND (vd.vulnerability_last_seen - vd.notification_date) > interval '30 day'
GROUP BY
  vd.provider, temporal_score, new_remediation_due_date
ORDER BY
  temporal_score DESC;
