from fastapi import APIRouter
import httpx
import time

router = APIRouter()

SOLANA_VALIDATOR_API = "https://api.mainnet-beta.solana.com"

# Simple in-memory slot history (last 20 slots)
slot_history = []

@router.get("/validator-status")
async def validator_status():
    json_rpc_request = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getSlot",
        "params": []
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(SOLANA_VALIDATOR_API, json=json_rpc_request, timeout=10)
            data = response.json()
            slot = data.get("result", None)
            status = "online" if slot is not None else "offline"
        except Exception:
            slot = None
            status = "offline"

    # Update slot history (max 20)
    if slot is not None:
        slot_history.append(slot)
        if len(slot_history) > 20:
            slot_history.pop(0)

    # Dummy balance and uptime (replace with real calls if needed)
    balance = "123.456 SOL"
    uptime = "72 hours"

    return {
        "node": "solana-validator-01",
        "status": status,
        "slot": slot or "unknown",
        "uptime": uptime,
        "balance": balance,
        "slot_history": slot_history
    }

