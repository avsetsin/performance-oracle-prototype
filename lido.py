from providers.kapi import ValidatorKey
from cl_blocks import BlockData

LIDO_DEPOSIT_AMOUNT = 32 * 10**9


def build_lido_validators_dict(deposited_keys: list[ValidatorKey], state):
    deposited_keys_set = set(map(lambda key: key.pubkey, deposited_keys))
    validators_dict = {}

    for index, validator in enumerate(state.data.validators):
        if str(validator.pubkey).lower() in deposited_keys_set:
            validators_dict[index] = validator

    return validators_dict


def build_operators_by_validator_index_dict(deposited_keys: list[ValidatorKey], state):
    deposited_keys_dict = dict(map(lambda key: (key.pubkey, (key.module_address, key.operator_index)), deposited_keys))
    operators_by_validator_index_dict: dict[int, tuple[str, int]] = {}

    for index, validator in enumerate(state.data.validators):
        pubkey = str(validator.pubkey).lower()

        if pubkey in deposited_keys_dict:
            operators_by_validator_index_dict[index] = deposited_keys_dict[pubkey]

    return operators_by_validator_index_dict


def filter_lido_blocks(data_by_blocks: dict[int, BlockData], lido_validators_dict: dict):
    filtered_data_by_blocks = {}

    for block_number, block_data in data_by_blocks.items():
        if block_data.proposer in lido_validators_dict:
            filtered_data_by_blocks[block_number] = block_data

    return filtered_data_by_blocks
