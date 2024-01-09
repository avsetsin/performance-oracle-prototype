from concurrent.futures import ThreadPoolExecutor

from providers import fetch_block_by_number


def fetch_withdrawals(start_block: int, end_block: int, max_workers=200):
    print("Fetching withdrawals for blocks range:", f"{start_block}-{end_block}")

    withdrawals_by_block: dict[int, list[dict]] = {}
    hashes_by_block: dict[int, (str, str)] = {}

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        for result in executor.map(
            lambda block_number: fetch_block_by_number(block_number, True), range(start_block, end_block + 1)
        ):
            block_number = int(result.number, 16)
            withdrawals_by_block[block_number] = result.withdrawals
            hashes_by_block[block_number] = (result.hash, result.parentHash)

    for block_number, (_, parent_hash) in hashes_by_block.items():
        if block_number == start_block:
            continue

        if parent_hash != hashes_by_block[block_number - 1][0]:
            raise Exception("Withdrawals fetching failed: parent hash mismatch")

    return withdrawals_by_block
