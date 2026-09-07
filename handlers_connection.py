"""Connection management for Harness CCM Connector."""
from __future__ import annotations
import uuid, json
from typing import Any
from imperal_sdk import ActionResult
from app import chat
from schemas import NoParams, ConnectParams, ConnectionIdParams, ConnectionRecord, ConnectionList, DeleteResult
from harness_ccm_connector_client import HarnessCCMClient

_SECRET = "harness_ccm_connector_connections"

def _mask(v: str) -> str:
    return v[:4] + "…" + v[-4:] if len(v) > 8 else "***"

async def _load_conns(ctx) -> list[dict]:
    raw = await ctx.secrets.get(_SECRET)
    if not raw: return []
    try: data = json.loads(raw)
    except: return []
    return data if isinstance(data, list) else []

async def _save_conns(ctx, conns: list[dict]) -> None:
    await ctx.secrets.set(_SECRET, json.dumps(conns))

async def resolve_client(ctx, connection_id: str = "") -> HarnessCCMClient:
    conns = await _load_conns(ctx)
    if not conns:
        raise ValueError("No Harness CCM connections configured. Use connect_harness_ccm_connector first.")
    conn = conns[0]
    if connection_id:
        for c in conns:
            if c["id"] == connection_id:
                conn = c
                break
    return HarnessCCMClient(api_key=conn["api_key"], base_url=conn.get("base_url", ""))

@chat.function("connect_harness_ccm_connector", "Connect Harness CCM account via credentials.", action_type="write", chain_callable=True, event="harness-ccm-connector.connect_harness_ccm_connector", effects=["create:connection"], data_model=ConnectionRecord)
async def connect_harness_ccm_connector(params: ConnectParams, ctx) -> ActionResult:
    client = HarnessCCMClient(api_key=params.api_key, base_url=params.base_url)
    res = await client.verify_auth()
    if res.get("status") == "error":
        return ActionResult.error(f"Failed to connect to Harness CCM: {res.get('error')}")
    conns = await _load_conns(ctx)
    cid = f"conn_{uuid.uuid4().hex[:8]}"
    rec = {
        "id": cid,
        "label": params.label or "Primary Harness CCM",
        "api_key": params.api_key,
        "masked_key": _mask(params.api_key),
        "base_url": params.base_url,
        "is_active": True
    }
    for c in conns: c["is_active"] = False
    conns.append(rec)
    await _save_conns(ctx, conns)
    return ActionResult.success(rec, summary=f"Connected Harness CCM ({rec['label']}).")

@chat.function("list_connections", "List configured Harness CCM connections.", action_type="read", chain_callable=True, event="harness-ccm-connector.list_connections", effects=["read:connections"], data_model=ConnectionList)
async def list_connections(params: NoParams, ctx) -> ActionResult:
    conns = await _load_conns(ctx)
    items = [{
        "id": c["id"],
        "label": c["label"],
        "masked_key": c.get("masked_key", "***"),
        "base_url": c.get("base_url", "https://app.harness.io/gateway/ccm/api"),
        "is_active": c.get("is_active", False)
    } for c in conns]
    return ActionResult.success({"connections": items, "total": len(items)}, summary=f"Found {len(items)} connection(s).")

@chat.function("disconnect_harness_ccm_connector", "Disconnect Harness CCM account and delete stored credentials.", action_type="destructive", chain_callable=True, event="harness-ccm-connector.disconnect_harness_ccm_connector", effects=["delete:connection"], data_model=DeleteResult)
async def disconnect_harness_ccm_connector(params: ConnectionIdParams, ctx) -> ActionResult:
    conns = await _load_conns(ctx)
    if not conns:
        return ActionResult.error("No connections to disconnect.")
    if params.connection_id:
        conns = [c for c in conns if c["id"] != params.connection_id]
    else:
        conns.clear()
    await _save_conns(ctx, conns)
    return ActionResult.success({"success": True, "message": "Disconnected successfully."}, summary="Disconnected Harness CCM connection.")
