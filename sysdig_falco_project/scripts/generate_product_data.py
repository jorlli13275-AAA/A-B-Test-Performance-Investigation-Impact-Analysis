import csv
import random
from pathlib import Path
from datetime import datetime, timedelta

BASE_DIR = Path(__file__).resolve().parents[1]

INPUT_FILE = BASE_DIR / "data" / "processed" / "raw_falco_attack_alerts.csv"
OUTPUT_DIR = BASE_DIR / "data" / "processed"

random.seed(42)


def random_timestamp(base_time):
    delta = timedelta(minutes=random.randint(1, 120))
    return base_time + delta


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Load alerts
    with INPUT_FILE.open("r", encoding="utf-8") as f:
        reader = list(csv.DictReader(f))

    # =====================
    # ACCOUNTS
    # =====================
    accounts = []
    for i in range(1, 21):
        accounts.append({
            "account_id": i,
            "account_name": f"company_{i}",
            "company_size": random.choice(["small", "medium", "enterprise"]),
            "industry": random.choice(["fintech", "health", "ecommerce", "saas"]),
            "cloud_provider": random.choice(["aws", "gcp", "azure"]),
            "plan_type": random.choice(["free", "pro", "enterprise"]),
            "created_at": "2026-01-01"
        })

    # =====================
    # USERS
    # =====================
    users = []
    user_id = 1
    for acc in accounts:
        for _ in range(random.randint(2, 5)):
            users.append({
                "user_id": user_id,
                "account_id": acc["account_id"],
                "user_role": random.choice([
                    "security_engineer",
                    "devops_engineer",
                    "platform_engineer"
                ]),
                "created_at": "2026-01-01"
            })
            user_id += 1

    # =====================
    # ALERT VIEWS
    # =====================
    alert_views = []
    investigations = []
    remediations = []
    feature_events = []

    alert_view_id = 1
    investigation_id = 1
    remediation_id = 1
    event_id = 1

    for alert in reader:
        account = random.choice(accounts)
        user = random.choice([u for u in users if u["account_id"] == account["account_id"]])

        base_time = datetime(2026, 5, 1, 10, 0, 0)

        view_time = base_time + timedelta(minutes=random.randint(0, 1000))

        group = random.choice(["control", "treatment"])

        alert_views.append({
            "alert_view_id": alert_view_id,
            "alert_id": alert["alert_id"],
            "user_id": user["user_id"],
            "account_id": account["account_id"],
            "view_timestamp": view_time,
            "experiment_group": group,
            "workflow_version": "runtime_context_panel" if group == "treatment" else "old_page"
        })

        # Investigation probability (treatment mejor)
        if group == "treatment":
            investigate_prob = 0.75
        else:
            investigate_prob = 0.55

        if random.random() < investigate_prob:
            start_time = random_timestamp(view_time)

            investigations.append({
                "investigation_id": investigation_id,
                "alert_id": alert["alert_id"],
                "user_id": user["user_id"],
                "account_id": account["account_id"],
                "investigation_started_at": start_time,
                "investigation_completed_at": random_timestamp(start_time),
                "outcome": random.choice([
                    "remediated",
                    "dismissed_false_positive",
                    "escalated"
                ])
            })

            # Remediation only some
            if random.random() < 0.6:
                remediations.append({
                    "remediation_id": remediation_id,
                    "alert_id": alert["alert_id"],
                    "user_id": user["user_id"],
                    "account_id": account["account_id"],
                    "remediation_timestamp": random_timestamp(start_time),
                    "remediation_type": random.choice([
                        "patch_vulnerability",
                        "kill_container",
                        "restrict_permission"
                    ])
                })
                remediation_id += 1

            # Feature usage
            if group == "treatment":
                feature_events.append({
                    "event_id": event_id,
                    "user_id": user["user_id"],
                    "account_id": account["account_id"],
                    "alert_id": alert["alert_id"],
                    "event_timestamp": start_time,
                    "event_name": "opened_runtime_context_panel",
                    "experiment_group": group
                })
                event_id += 1

            investigation_id += 1

        alert_view_id += 1

    # =====================
    # SAVE FILES
    # =====================

    def save_csv(name, data):
        if not data:
            return
        keys = data[0].keys()
        with (OUTPUT_DIR / name).open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(data)

    save_csv("raw_accounts.csv", accounts)
    save_csv("raw_users.csv", users)
    save_csv("raw_alert_views.csv", alert_views)
    save_csv("raw_investigations.csv", investigations)
    save_csv("raw_remediations.csv", remediations)
    save_csv("raw_feature_events.csv", feature_events)

    print("Done generating product data!")


if __name__ == "__main__":
    main()