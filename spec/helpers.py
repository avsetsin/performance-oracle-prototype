from spec.constants import SLOTS_PER_EPOCH


def compute_epoch_at_slot(slot: int) -> int:
    """
    Return the epoch number at ``slot``.
    https://github.com/ethereum/consensus-specs/blob/dev/specs/phase0/beacon-chain.md#compute_epoch_at_slot
    """
    return slot // SLOTS_PER_EPOCH


def compute_start_slot_at_epoch(epoch: int) -> int:
    """
    Return the start slot of ``epoch``.
    https://github.com/ethereum/consensus-specs/blob/dev/specs/phase0/beacon-chain.md#compute_start_slot_at_epoch
    """
    return epoch * SLOTS_PER_EPOCH


def compute_end_slot_at_epoch(epoch: int) -> int:
    return compute_start_slot_at_epoch(epoch + 1) - 1
