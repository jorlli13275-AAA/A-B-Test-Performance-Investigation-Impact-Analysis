import csv
from collections import Counter
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[1]

INPUT_FILE = BASE_DIR / "data" / "processed" / "raw_falco_attack_alerts.csv"


def clean_tags(tags):
    if not tags:
        return []

    return (
        tags.replace("[", "")
        .replace("]", "")
        .replace('"', "")
        .split(",")
    )


def main():
    rows = []

    with INPUT_FILE.open("r", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        rows = list(reader)

    print("\n=== BASIC SUMMARY ===")
    print(f"Total alerts: {len(rows)}")

    print("\n=== ALERTS BY PRIORITY ===")
    priority_counts = Counter(row["priority"] for row in rows)
    for priority, count in priority_counts.most_common():
        print(f"{priority}: {count}")

    print("\n=== TOP 10 RULES ===")
    rule_counts = Counter(row["rule_name"] for row in rows)
    for rule, count in rule_counts.most_common(10):
        print(f"{rule}: {count}")

    print("\n=== TOP 10 PODS ===")
    pod_counts = Counter(row["pod_name"] for row in rows if row["pod_name"])
    for pod, count in pod_counts.most_common(10):
        print(f"{pod}: {count}")

    print("\n=== TOP IMAGES ===")
    image_counts = Counter(row["image_name"] for row in rows if row["image_name"])
    for image, count in image_counts.most_common(10):
        print(f"{image}: {count}")

    print("\n=== TOP TAGS ===")
    tag_counter = Counter()

    for row in rows:
        for tag in clean_tags(row["tags"]):
            tag = tag.strip()
            if tag:
                tag_counter[tag] += 1

    for tag, count in tag_counter.most_common(15):
        print(f"{tag}: {count}")


if __name__ == "__main__":
    main()