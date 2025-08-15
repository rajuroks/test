
WITH base AS (
  SELECT
      v.owner,
      v.type,
      o.grn,
      v.cve,
      v.product_name,
      v.product_version,
      v.vulnerability_last_seen,
      /* integer days, date-to-date avoids TZ issues */
      (CURRENT_DATE - v.overdue_notification_date::date) AS days_overdue
  FROM cloudplatform_vmarc_vulnerability_details_materialized v
  LEFT JOIN cloudplatform_ownership o
    ON v.owner = o.eonid
  WHERE
      v.overdue_notification_date < NOW() - INTERVAL '90 days'
      AND v.vulnerability_last_seen >= NOW() - INTERVAL '3 days'
)
SELECT
    owner,
    type,
    grn,
    cve,
    product_name,
    product_version,
    vulnerability_last_seen,
    days_overdue,
    COUNT(*) AS finding_count
FROM base
WHERE days_overdue >= 190        -- remove or adjust as needed
GROUP BY
    owner, type, grn, cve, product_name, product_version,
    vulnerability_last_seen, days_overdue
ORDER BY days_overdue DESC;
