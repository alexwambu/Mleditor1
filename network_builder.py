def create_network(chain_id: int, signer: str):
    signer_clean = signer.lower().replace("0x", "")
    extra = "0x" + "00" * 32 + signer_clean + "00" * 65
    genesis = {
        "config": {
            "chainId": chain_id,
            "clique": {"period": 5, "epoch": 30000},
            "homesteadBlock": 0,
            "eip155Block": 0,
            "londonBlock": 0
        },
        "alloc": {signer: {"balance": "1000000000000000000000"}},
        "coinbase": "0x0000000000000000000000000000000000000000",
        "difficulty": "1",
        "extraData": extra,
        "gasLimit": "8000000",
        "timestamp": "0x00"
    }
    return genesis
