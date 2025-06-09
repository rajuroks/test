WITH images_0605 AS (
  SELECT DISTINCT image_digest FROM vm_data.cloudplatform_vmarc_vulnerability_details
  WHERE TO_CHAR(vulnerability_first_seen, 'YYYY-MM-DD') = '2025-06-05'
),
images_0604 AS (
  SELECT DISTINCT image_digest FROM vm_data.cloudplatform_vmarc_vulnerability_details
  WHERE TO_CHAR(vulnerability_first_seen, 'YYYY-MM-DD') = '2025-06-04'
)
SELECT image_digest
FROM images_0605
WHERE image_digest NOT IN (SELECT image_digest FROM images_0604);
