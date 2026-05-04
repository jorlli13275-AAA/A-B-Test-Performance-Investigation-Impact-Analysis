-- A/B test group distribution
SELECT
  experiment_group,
  COUNT(*) AS total_alert_views
FROM `my-sql-project-493214.sysdig_ab_test.raw_alert_views`
GROUP BY experiment_group
ORDER BY total_alert_views DESC;