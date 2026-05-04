-- File: 03_investigation_rate.sql
-- Purpose: Compare investigation rate between control and treatment groups

SELECT
  av.experiment_group,
  COUNT(DISTINCT av.alert_view_id) AS total_views,
  COUNT(DISTINCT inv.investigation_id) AS total_investigations,
  SAFE_DIVIDE(
    COUNT(DISTINCT inv.investigation_id),
    COUNT(DISTINCT av.alert_view_id)
  ) AS investigation_rate
FROM `my-sql-project-493214.sysdig_ab_test.raw_alert_views` av
LEFT JOIN `my-sql-project-493214.sysdig_ab_test.raw_investigations` inv
  ON av.alert_id = inv.alert_id
  AND av.user_id = inv.user_id
GROUP BY av.experiment_group
ORDER BY investigation_rate DESC;