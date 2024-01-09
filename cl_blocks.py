from concurrent.futures import ThreadPoolExecutor
from requests import HTTPError

from providers import fetch_beacon_block


class BlockData:
    def __init__(self, proposer: str):
        self.proposer = int(proposer)


def fetch_beacon_block_if_exist(slot_number: int):
    try:
        return fetch_beacon_block(slot_number)
    except HTTPError as error:
        if error.response.status_code != 404:
            raise error

    return None


def fetch_cl_blocks(start_slot: int, end_slot: int, max_workers=10):
    print("Fetching CL blocks in slot range:", f"{start_slot}-{end_slot}")

    data_by_block: dict[int, BlockData] = {}
    hashes_by_block: dict[int, (str, str)] = {}
    first_block_number: int = None

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        for result in executor.map(
            lambda slot_number: fetch_beacon_block_if_exist(slot_number), range(start_slot, end_slot + 1)
        ):
            if result is None:
                continue

            execution_payload = result.data.message.body.execution_payload
            block_number = int(execution_payload.block_number)
            data_by_block[block_number] = BlockData(result.data.message.proposer_index)
            hashes_by_block[block_number] = (execution_payload.block_hash, execution_payload.parent_hash)

            if first_block_number is None:
                first_block_number = block_number

    for block_number, (_, parent_hash) in hashes_by_block.items():
        if block_number == first_block_number:
            continue

        if parent_hash != hashes_by_block[block_number - 1][0]:
            raise Exception("CL blocks fetching failed: parent hash mismatch")

    return data_by_block
