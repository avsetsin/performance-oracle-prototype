from os import getenv

from providers.fetch import fetch_json


rpc_id: int = 0


def el_fetch_json(method: str, params: list):
    url = getenv("EL_URL")

    if url is None:
        raise Exception("EL_URL environment variable not set")

    global rpc_id
    rpc_id += 1

    json = fetch_json(
        method="post",
        url=url,
        json={"jsonrpc": "2.0", "method": method, "params": params, "id": rpc_id},
    )

    return json.result


def fetch_block_by_hash(block_hash: str, detailed=True):
    return el_fetch_json("eth_getBlockByHash", [block_hash, detailed])


def fetch_block_by_number(block_number: str | int, detailed=True):
    return el_fetch_json("eth_getBlockByNumber", [hex(block_number), detailed])
