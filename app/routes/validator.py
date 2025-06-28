from fastapi import APIRouter
import httpx
import os

router = APIRouter()

SOLANA_VALIDATOR_API = os.getenv("SOLANA_VALIDATOR_API")

@router.get("/validator-status")
async def validator_status():
    json_rpc_request = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getSlot",
        "params": []
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(SOLANA_VALIDATOR_API, json=json_rpc_request)
        data = response.json()

    slot = data.get("result", "unknown")

    return {
        "node": "solana-validator-01",
        "status": "online",
        "slot": slot,
        "uptime": "72 hours"
    }

