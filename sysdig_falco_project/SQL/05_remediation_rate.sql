-- File: 05_remediation_rate.sql
-- Purpose: Compare remediation rate between control and treatment groups

SELECT
  av.experiment_group,
  COUNT(DISTINCT inv.investigation_id) AS total_investigations,
  COUNT(DISTINCT rem.remediation_id) AS total_remediations,
  SAFE_DIVIDE(
    COUNT(DISTINCT rem.remediation_id),
    COUNT(DISTINCT inv.investigation_id)
  ) AS remediation_rate
FROM `my-sql-project-493214.sysdig_ab_test.raw_alert_views` av
LEFT JOIN `my-sql-project-493214.sysdig_ab_test.raw_investigations` inv
  ON av.alert_id = inv.alert_id
  AND av.user_id = inv.user_id
LEFT JOIN `my-sql-project-493214.sysdig_ab_test.raw_remediations` rem
  ON inv.alert_id = rem.alert_id
  AND inv.user_id = rem.user_id
GROUP BY av.experiment_group
ORDER BY remediation_rate DESC; 