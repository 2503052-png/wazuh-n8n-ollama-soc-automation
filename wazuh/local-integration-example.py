#!/usr/bin/env python3
"""
Illustrative Wazuh-to-n8n forwarding example.

IMPORTANT:
- This is a template, not a drop-in Wazuh integration.
- Verify Wazuh's expected command-line arguments and integration interface
  for your installed version before deployment.
- Protect the webhook with authentication/network controls in real deployments.
- Do not log secrets or full sensitive alert payloads.
"""
import json
import os
import sys
import urllib.request
import urllib.error

WEBHOOK_URL = os.environ.get(
    "N8N_WEBHOOK_URL",
    "http://<WINDOWS_VMNET8_IP>:5678/webhook/wazuh-alert"
)
TIMEOUT_SECONDS = 10


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: local-integration-example.py <alert-json-file>", file=sys.stderr)
        return 2

    alert_path = sys.argv[1]
    try:
        with open(alert_path, "r", encoding="utf-8") as f:
            alert = json.load(f)
    except (OSError, json.JSONDecodeError) as exc:
        print(f"Unable to read alert JSON: {exc}", file=sys.stderr)
        return 1

    if "<WINDOWS_VMNET8_IP>" in WEBHOOK_URL:
        print("Set N8N_WEBHOOK_URL to your reachable n8n production webhook URL.", file=sys.stderr)
        return 2

    payload = json.dumps(alert).encode("utf-8")
    request = urllib.request.Request(
        WEBHOOK_URL,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=TIMEOUT_SECONDS) as response:
            if not 200 <= response.status < 300:
                print(f"Webhook returned HTTP {response.status}", file=sys.stderr)
                return 1
    except (urllib.error.URLError, TimeoutError) as exc:
        print(f"Webhook request failed: {exc}", file=sys.stderr)
        return 1

    print("Alert forwarded successfully.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
