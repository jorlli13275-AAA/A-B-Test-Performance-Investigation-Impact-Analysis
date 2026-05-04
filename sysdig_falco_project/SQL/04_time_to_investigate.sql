-- File: 04_time_to_investigate.sql
-- Purpose: Compare average time to investigate between control and treatment groups

SELECT
  av.experiment_group,
  COUNT(DISTINCT inv.investigation_id) AS total_investigations,
  ROUND(
    AVG(
      TIMESTAMP_DIFF(
        inv.investigation_started_at,
        av.view_timestamp,
        MINUTE
      )
    ),
    2
  ) AS avg_minutes_to_investigate
FROM `my-sql-project-493214.sysdig_ab_test.raw_alert_views` av
JOIN `my-sql-project-493214.sysdig_ab_test.raw_investigations` inv
  ON av.alert_id = inv.alert_id
  AND av.user_id = inv.user_id
GROUP BY av.experiment_group
ORDER BY avg_minutes_to_investigate ASC;