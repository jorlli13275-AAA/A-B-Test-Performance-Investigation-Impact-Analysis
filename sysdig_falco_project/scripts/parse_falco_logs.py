import csv
import re
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[1]

RAW_DIR = BASE_DIR / "data" / "raw" / "Falco_Alerts_of_Simulated_Attacks"
OUTPUT_DIR = BASE_DIR / "data" / "processed"
OUTPUT_FILE = OUTPUT_DIR / "raw_falco_attack_alerts.csv"


def extract_between(text, start_pattern, end_pattern=None):
    """
    Extract text between a starting pattern and an optional ending pattern.
    """
    try:
        start_index = text.index(start_pattern) + len(start_pattern)
        if end_pattern:
            end_index = text.index(end_pattern, start_index)
            return text[start_index:end_index].strip()
        return text[start_index:].strip()
    except ValueError:
        return ""


def extract_regex(text, pattern):
    match = re.search(pattern, text)
    return match.group(1).strip() if match else ""


def parse_line(line, alert_id, source_file):
    line = line.strip()

    rule_name = extract_between(line, "rule=", ", desc=")

    desc_full = extract_between(line, "desc=", ", parameter=")
    event_time = ""
    description = ""

    desc_match = re.match(r"([0-9:.]+):\s*(.*)", desc_full)
    if desc_match:
        event_time = desc_match.group(1)
        description = desc_match.group(2)
    else:
        description = desc_full

    priority = extract_regex(line, r"priority=([^,\s]+)")
    user_name = extract_regex(line, r"user=([^,\s]+)")
    user_loginuid = extract_regex(line, r"user_loginuid=([^,\s]+)")

    command = extract_regex(line, r"command=([^,]+)")
    k8s_namespace = extract_regex(line, r"k8s\.ns=([^,\s]+)")

    pod_name = extract_regex(line, r"k8s\.pod=([^,\s]+)")
    if not pod_name:
        pod_name = extract_regex(line, r"pod=([^,\s]+)")

    container_id = extract_regex(line, r"container=([^,\s]+)")
    if not container_id:
        container_id = extract_regex(line, r"container_id=([^,\s]+)")

    image_name = extract_regex(line, r"image=([^,\s]+)")
    tags = extract_regex(line, r"tag=(\[.*?\]|[^,]+)")

    label = "attack" if line.endswith("attack") else ""

    return {
        "alert_id": alert_id,
        "source_file": source_file,
        "rule_name": rule_name,
        "event_time": event_time,
        "description": description,
        "priority": priority,
        "container_id": container_id,
        "pod_name": pod_name,
        "image_name": image_name,
        "user_name": user_name,
        "user_loginuid": user_loginuid,
        "command": command,
        "k8s_namespace": k8s_namespace,
        "tags": tags,
        "label": label,
        "raw_line": line,
    }


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    txt_files = list(RAW_DIR.glob("*.txt"))

    if not txt_files:
        print(f"No TXT files found in: {RAW_DIR}")
        return

    rows = []
    alert_id = 1

    for txt_file in txt_files:
        with txt_file.open("r", encoding="utf-8", errors="ignore") as file:
            for line in file:
                line = line.strip()

                if not line:
                    continue

                if not line.startswith("rule="):
                    continue

                parsed_row = parse_line(
                    line=line,
                    alert_id=alert_id,
                    source_file=txt_file.name,
                )

                rows.append(parsed_row)
                alert_id += 1

    fieldnames = [
        "alert_id",
        "source_file",
        "rule_name",
        "event_time",
        "description",
        "priority",
        "container_id",
        "pod_name",
        "image_name",
        "user_name",
        "user_loginuid",
        "command",
        "k8s_namespace",
        "tags",
        "label",
        "raw_line",
    ]

    with OUTPUT_FILE.open("w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print("Done!")
    print(f"Files processed: {len(txt_files)}")
    print(f"Rows created: {len(rows)}")
    print(f"Output file: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()