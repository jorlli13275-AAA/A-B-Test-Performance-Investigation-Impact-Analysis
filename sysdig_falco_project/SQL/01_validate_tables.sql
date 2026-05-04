-- Validate row count for each raw table
SELECT 'raw_accounts' AS table_name, COUNT(*) AS row_count
FROM `my-sql-project-493214.sysdig_ab_test.raw_accounts`

UNION ALL

SELECT 'raw_users', COUNT(*)
FROM `my-sql-project-493214.sysdig_ab_test.raw_users`

UNION ALL

SELECT 'raw_alert_views', COUNT(*)
FROM `my-sql-project-493214.sysdig_ab_test.raw_alert_views`

UNION ALL

SELECT 'raw_investigations', COUNT(*)
FROM `my-sql-project-493214.sysdig_ab_test.raw_investigations`

UNION ALL

SELECT 'raw_remediations', COUNT(*)
FROM `my-sql-project-493214.sysdig_ab_test.raw_remediations`

UNION ALL

SELECT 'raw_feature_events', COUNT(*)
FROM `my-sql-project-493214.sysdig_ab_test.raw_feature_events`

UNION ALL

SELECT 'raw_falco_attack_alerts', COUNT(*)
FROM `my-sql-project-493214.sysdig_ab_test.raw_falco_attack_alerts`;