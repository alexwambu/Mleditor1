import os, time, json, requests
from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse, JSONResponse

from network_builder import create_network
from token_builder import deploy_token

app = FastAPI()

MEMORY_SERVERS = [
    "https://storagememory-2-bngo.onrender.com",
    "https://storagemem.onrender.com"
]

DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

@app.get("/", response_class=HTMLResponse)
def index():
    with open("static_index.html") as f:
        return f.read()

@app.post("/build-network")
def build_network(chain_id: int = Form(...), signer: str = Form(...)):
    genesis = create_network(chain_id, signer)
    path = os.path.join(DATA_DIR, f"genesis_{chain_id}.json")
    with open(path, "w") as f:
        json.dump(genesis, f, indent=2)
    replicate(path)
    return {"status": "ok", "chain_id": chain_id, "file": path}

@app.post("/deploy-token")
def deploy_token_api(name: str = Form(...), symbol: str = Form(...), supply: int = Form(...)):
    result = deploy_token(name, symbol, supply)
    path = os.path.join(DATA_DIR, f"{symbol}_token.json")
    with open(path, "w") as f:
        json.dump(result, f, indent=2)
    replicate(path)
    return {"status": "deployed", "token": symbol, "contract": result}

@app.get("/health")
def health():
    return {"status": "ok", "service": "Ethereum Builder"}

def replicate(filepath):
    for peer in MEMORY_SERVERS:
        try:
            with open(filepath, "rb") as f:
                requests.post(f"{peer}/upload", files={"file": (os.path.basename(filepath), f)}, timeout=5)
        except Exception as e:
            print(f"[SYNC FAIL] {peer}: {e}")

def keep_alive():
    while True:
        print("💓 Heartbeat: Builder active")
        time.sleep(18)

import threading
threading.Thread(target=keep_alive, daemon=True).start()
