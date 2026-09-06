"""Extension declaration, capabilities, health check for Harness CCM Connector."""
from __future__ import annotations
import json
from imperal_sdk import ChatExtension, Extension

ext = Extension(
    "harness_ccm-connector",
    version="0.1.0",
    display_name="Harness CCM",
    icon="icon.svg",
    capabilities=["harness_ccm:manage"],
    description="Official Imperal connector for Harness CCM (C30. Email Marketing & Newsletter). Manage operations securely."
)

chat = ChatExtension(ext)

@ext.health_check
async def health_check(ctx) -> dict:
    raw = await ctx.secrets.get("harness_ccm_connections")
    try:
        count = len(json.loads(raw)) if raw else 0
    except Exception:
        count = 0
    return {
        "healthy": True,
        "detail": f"{count} Harness CCM connection(s) configured." if count else "Not connected yet."
    }
