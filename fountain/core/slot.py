from ..resources.constants import SLOT_DELIMITER, SLOT

import logging


class Slot():
    def __init__(self, value):
        """
        Fountain Slot Class.
        Describes the Fountain Slot structure.

        :param value: captured value
        """
        self.value = value
        sname, stype = self.parse(value)
        self.slot_name = sname
        self.slot_type = stype  # or it can be called `Entity`

    def __repr__(self):
        return '%s:%s' % (self.slot_name, self.slot_type)

    def parse(self, value=None):
        """
        parse slot_value to extract (slot_type, slot_name)

        >> e.g: utternace > I want to order a (cab|taxi) to go from {location:pickup} to {location:dropoff}
        >> slot_value = {location:pickup} | slot_name = location | slot_name = pickup
        >> slot_value = {location:dropoff} | slot_name = location | slot_name = dropoff

        :param value: captured value

        :return: a tuple (slot_type, slot_name)
        """
        if value is None:
            value = self.value

        if SLOT_DELIMITER in value:
            try:
                (slot_type, slot_name) = value.split(SLOT_DELIMITER)
            except Exception as _:
                logging.error('{} should be of format `slot_type:slot_name`'.format(value))
        else:
            slot_type, slot_name = value, value

        return slot_type, slot_name
