#!/usr/bin/env python3
import requests
import json
import sys
from datetime import datetime

WEBHOOK_URL = "https://discord.com/api/webhooks/your_id/your_token"

def get_public_ip():
    try:
        response = requests.get("https://api.ipify.org?format=json", timeout=5)
        response.raise_for_status()
        return response.json().get("ip")
    except requests.RequestException as e:
        print(f"IP fetch error: {e}", file=sys.stderr)
        return None

def build_discord_payload(ip_address):
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
    headers = {"Content-Type": "application/json"}
    try:
        response = requests.post(WEBHOOK_URL, data=json.dumps(payload), headers=headers, timeout=10)
        response.raise_for_status()
        return True
    except requests.RequestException as e:
        print(f"Discord send error: {e}", file=sys.stderr)
        return False

def handler(request):
    ip = get_public_ip()
    if not ip:
        return {"statusCode": 500, "body": "Failed to get IP"}
    payload = build_discord_payload(ip)
    success = send_to_discord(payload)
    if success:
        return {"statusCode": 200, "body": "IP logged"}
    else:
        return {"statusCode": 500, "body": "Discord send failed"}
