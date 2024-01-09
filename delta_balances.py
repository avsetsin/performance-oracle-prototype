from lido import LIDO_DEPOSIT_AMOUNT
from withdrawals import fetch_withdrawals


def get_validator_cl_delta_balances(start_state, end_state, validators_dict: dict[int, dict]):
    assert int(end_state.data.slot) > int(start_state.data.slot)

    total_delta_balance: int = 0
    result: dict[int, int] = {}

    for index, validator in enumerate(end_state.data.validators):
        if index in validators_dict:
            start_balance = LIDO_DEPOSIT_AMOUNT
            end_balance = int(end_state.data.balances[index])

            if index < len(start_state.data.balances):
                assert validator.pubkey == start_state.data.validators[index].pubkey
                start_balance = int(start_state.data.balances[index])

            validator_delta_balance = end_balance - start_balance
            result[index] = validator_delta_balance
            total_delta_balance += validator_delta_balance

    return result, total_delta_balance


def get_validator_el_delta_balances(start_state, end_state, validators_dict: dict[int, dict]):
    start_block = int(start_state.data.latest_execution_payload_header.block_number) + 1
    end_block = int(end_state.data.latest_execution_payload_header.block_number)

    assert start_block <= end_block

    total_withdrawals: int = 0
    withdrawals_by_validator: dict[int, int] = {}
    withdrawals_by_block = fetch_withdrawals(start_block, end_block)

    for _, withdrawals in withdrawals_by_block.items():
        for withdrawal in withdrawals:
            index = int(withdrawal.validatorIndex, 16)
            if index in validators_dict:
                withdrawn_amount = int(withdrawal.amount, 16)
                withdrawals_by_validator[index] = withdrawals_by_validator.get(index, 0) + withdrawn_amount
                total_withdrawals += withdrawn_amount

    return withdrawals_by_validator, total_withdrawals


def get_validator_delta_balances(start_state, end_state, validators_dict: dict[int, dict]):
    cl, total_delta = get_validator_cl_delta_balances(start_state, end_state, validators_dict)
    el, withdrawals = get_validator_el_delta_balances(start_state, end_state, validators_dict)

    result: dict[int, int] = {}

    for index in validators_dict:
        if index in cl:
            result[index] = cl[index]

        if index in el:
            assert index in result
            result[index] += el[index]

    return result, total_delta, withdrawals
