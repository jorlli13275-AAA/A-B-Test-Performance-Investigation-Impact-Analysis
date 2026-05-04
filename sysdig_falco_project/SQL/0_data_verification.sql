-- Distribution of alerts by priority level
SELECT 
  priority,
  COUNT(*) AS total_alerts
FROM `my-sql-project-493214.sysdig_ab_test.raw_falco_attack_alerts`
GROUP BY priority
ORDER BY total_alerts DESC;

-- Top 10 most frequent Falco rules (attack types)
SELECT 
  rule_name,
  COUNT(*) AS total_alerts
FROM `my-sql-project-493214.sysdig_ab_test.raw_falco_attack_alerts`
GROUP BY rule_name
ORDER BY total_alerts DESC
LIMIT 10;