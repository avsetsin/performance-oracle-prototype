from providers.consensus_layer import fetch_beacon_header, fetch_beacon_state
from providers.kapi import fetch_used_keys
from delta_balances import get_validator_delta_balances
from spec import compute_epoch_at_slot, compute_end_slot_at_epoch
from lido import build_lido_validators_dict, build_operators_by_validator_index_dict, filter_lido_blocks
from utils import to_eth, format_gwei, PerformanceTimer
from cl_blocks import fetch_cl_blocks


REPORT_FRAME_IN_EPOCHS = 23


def get_slots_for_report():
    """
    returns mocked ref slots
    """
    header_result = fetch_beacon_header("finalized")
    finalized_slot = int(header_result.data.header.message.slot)

    frame_end_epoch = compute_epoch_at_slot(finalized_slot) - 1
    frame_start_epoch = frame_end_epoch - REPORT_FRAME_IN_EPOCHS + 1

    current_report_slot = compute_end_slot_at_epoch(frame_end_epoch)
    previous_report_slot = compute_end_slot_at_epoch(frame_start_epoch - 1)

    assert previous_report_slot > 0

    return previous_report_slot, current_report_slot


def main():
    timer = PerformanceTimer()

    previous_report_slot, current_report_slot = get_slots_for_report()
    print("Mock report slots fetched:", f"{previous_report_slot}-{current_report_slot}", timer.tick())

    previous_report_state = fetch_beacon_state(previous_report_slot)
    print("Previous report state fetched for slot:", previous_report_state.data.slot, timer.tick())

    current_report_state = fetch_beacon_state(current_report_slot)
    print("Current report state fetched for slot", current_report_state.data.slot, timer.tick())

    assert previous_report_state.finalized == True and current_report_state.finalized == True

    current_report_block = int(current_report_state.data.latest_execution_payload_header.block_number)
    print(f"Current report state block number: {current_report_block}")

    deposited_keys = fetch_used_keys(current_report_block)
    print("Deposited keys fetched:", len(deposited_keys), timer.tick())

    lido_validators_dict = build_lido_validators_dict(deposited_keys, current_report_state)
    print("Lido validator indices:", len(lido_validators_dict), timer.tick())

    operators_by_validator_index_dict = build_operators_by_validator_index_dict(deposited_keys, current_report_state)
    print("Operators by validator index dict built", timer.tick())

    delta_balances, total_delta, withdrawals = get_validator_delta_balances(
        previous_report_state, current_report_state, lido_validators_dict
    )
    print()
    print("Delta balances fetched:", format_gwei(sum(delta_balances.values())), timer.tick())
    print("Delta balances on CL:", format_gwei(total_delta))
    print("Withdrawals:", format_gwei(withdrawals))

    print()
    data_by_blocks = fetch_cl_blocks(int(previous_report_state.data.slot) + 1, int(current_report_state.data.slot))
    print("CL blocks fetched:", len(data_by_blocks), timer.tick())

    lido_blocks = filter_lido_blocks(data_by_blocks, lido_validators_dict)
    print("Lido CL blocks filtered:", len(lido_blocks), timer.tick())

    result: dict[str, dict[int, (int, int)]] = {}
    for index, delta_balance in delta_balances.items():
        module_address, operator_index = operators_by_validator_index_dict[index]
        result[module_address]: dict[int, (int, int)] = result.get(module_address, {})

        (total_rewards, total_penalties) = result[module_address].get(operator_index, (0, 0))
        total_rewards += delta_balance
        total_penalties += delta_balance if delta_balance < 0 else 0

        result[module_address][operator_index] = (total_rewards, total_penalties)

    print()
    print("Delta balances grouped by operator:")
    for module_address, operator_index_balances in result.items():
        print("Module:", module_address)
        for operator_index, (rewards, penalties) in sorted(operator_index_balances.items()):
            print(
                f"#{format(operator_index, '02d')} operator rewards: {format(to_eth(rewards), '+10.5f')} eth, penalties: {format(to_eth(penalties), '+10.5f')} eth"
            )


main()
