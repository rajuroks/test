
SELECT
  COUNT(CASE 
          WHEN vulnerability_last_seen <= notification_date + INTERVAL '3 days' 
          THEN 1 
        END) AS remediated_count,

  COUNT(CASE 
          WHEN vulnerability_last_seen > notification_date + INTERVAL '3 days' 
          THEN 1 
        END) AS outstanding_count

FROM (
  SELECT vulnerability_last_seen, notification_date
  FROM your_view_name
  WHERE notification_date BETWEEN '2025-06-01' AND '2025-06-15'
) sub;
