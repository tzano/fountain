import pytest
from fountain.core.slot import Slot


def test_parse():
    slot_value = 'location:pickup'
    _slot_type, _slot_name = 'location', 'pickup'

    slot = Slot(slot_value)
    slot_type, slot_name = slot.parse(slot_value)

    assert _slot_type == slot_type
    assert _slot_name == slot_name

