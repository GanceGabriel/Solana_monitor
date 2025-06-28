
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import httpx

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Solana RPC endpoint (public mainnet)
SOLANA_VALIDATOR_API = "https://api.mainnet-beta.solana.com"

@app.get("/validator-status")
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

@app.get("/", response_class=HTMLResponse)
async def root():
    with open("index.html", "r") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content)

