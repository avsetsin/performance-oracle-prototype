from os import getenv
from urllib import parse

from providers.fetch import fetch_json


def cl_fetch_json(endpoint: str):
    url = getenv("CL_URL")

    if url is None:
        raise Exception("CL_URI environment variable not set")

    return fetch_json("get", parse.urljoin(url, endpoint))


def fetch_node_version():
    return cl_fetch_json("eth/v1/node/version")


def fetch_config_spec():
    return cl_fetch_json("eth/v1/config/spec")


def fetch_beacon_header(block_id="head"):
    return cl_fetch_json(f"eth/v1/beacon/headers/{block_id}")


def fetch_beacon_block(block_id="head"):
    return cl_fetch_json(f"eth/v2/beacon/blocks/{block_id}")


def fetch_beacon_block_header(block_id="head"):
    return cl_fetch_json(f"eth/v1/beacon/headers/{block_id}")


def fetch_beacon_state(state_id="head"):
    return cl_fetch_json(f"eth/v2/debug/beacon/states/{state_id}")
