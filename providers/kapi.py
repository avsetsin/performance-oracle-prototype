from os import getenv
from urllib import parse

from providers.fetch import fetch_json


class ValidatorKey:
    def __init__(self, pubkey: str, operator_index: int, module_address: str):
        self.pubkey = str(pubkey).lower()
        self.operator_index = int(operator_index)
        self.module_address = str(module_address).lower()


def kapi_fetch_json(endpoint: str, params={}):
    url = getenv("KAPI_URL")

    if url is None:
        raise Exception("KAPI_URI environment variable not set")

    return fetch_json("get", parse.urljoin(url, endpoint), params=params)


def fetch_used_keys(block_number: int):
    result = kapi_fetch_json("v1/keys", {"used": "true"})

    if int(result.meta.elBlockSnapshot.blockNumber) < block_number:
        raise Exception("KAPI returned outdated data")

    return list(
        map(
            lambda key: ValidatorKey(key.key, key.operatorIndex, key.moduleAddress),
            result.data,
        )
    )
