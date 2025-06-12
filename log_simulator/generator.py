import random
import json
import csv
import os
from datetime import datetime, timedelta
from pathlib import Path

SERVICES = ['auth', 'billing', 'inventory']
LEVELS = ['DEBUG', 'INFO', 'WARN', 'ERROR']
MESSAGES = {
    'auth': ['User login success', 'Invalid password', 'Token expired'],
    'billing': ['Payment processed', 'Card declined', 'Refund issued'],
    'inventory': ['Item stock updated', 'Out of stock', 'Inventory sync failed']
}

OUTPUT_DIR = Path("output_logs/")
NUM_LOGS = 100


def generate_log_entry(service: str) -> dict:
    return {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "service": service,
        "level": random.choices(LEVELS, weights=[0.2, 0.5, 0.2, 0.1])[0],
        "message": random.choice(MESSAGES[service]),
        "context": {
            "user_id": str(random.randint(1000, 9999)),
            "request_id": f"req_{random.randint(10000, 99999)}"
        }
    }


def write_json_logs(service: str, entries: list, output_path: Path):
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(entries, f, indent=2)


def write_csv_logs(service: str, entries: list, output_path: Path):
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["timestamp", "service", "level", "message", "context"])
        writer.writeheader()
        for entry in entries:
            row = entry.copy()
            row["context"] = json.dumps(row["context"])
            writer.writerow(row)


def main(format: str = "json"):
    for service in SERVICES:
        logs = [generate_log_entry(service) for _ in range(NUM_LOGS)]
        timestamp = datetime.utcnow().strftime("%Y-%m-%dT%H-%M-%S")
        file_name = f"logs-{service}-{timestamp}.{format}"
        output_path = OUTPUT_DIR / service / datetime.utcnow().strftime("%Y-%m-%d") / file_name

        if format == "json":
            write_json_logs(service, logs, output_path)
        elif format == "csv":
            write_csv_logs(service, logs, output_path)
        else:
            raise ValueError("Unsupported format. Use 'json' or 'csv'.")

        print(f"[+] Generated {len(logs)} logs for {service} → {output_path}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Generate fake logs for services.")
    parser.add_argument("--format", choices=["json", "csv"], default="json", help="Output format (json or csv)")
    args = parser.parse_args()

    main(format=args.format)
