
SELECT
  COUNT(*) AS remediated_count
FROM (
  SELECT
    notification_id,
    unique_id,
    cve,
    COALESCE(image_digest, 'n/a') AS asset_image_group,
    MAX(vulnerability_last_seen) AS vulnerability_last_seen
  FROM your_view_name
  WHERE notification_date IS NOT NULL
    AND notification_date BETWEEN '2025-06-01' AND '2025-06-15'
  GROUP BY notification_id, unique_id, cve, COALESCE(image_digest, 'n/a')
) sub
WHERE vulnerability_last_seen::date <= CURRENT_DATE - INTERVAL '3 days';
