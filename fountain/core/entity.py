class Entity():
    def __init__(self, slot_name, slot_type, value, start_index, end_index):
        """
        Fountain Entity Class.
        Describes the Fountain Entity structure.

        :param slot_name: slot name
        :param slot_type: slot type
        :param value: value
        :param start_index: start index
        :param end_index: end index
        """
        self.slot_name = slot_name
        self.slot_type = slot_type  # or it can be called Entity
        self.value = value
        self.start_index = start_index
        self.end_index = end_index

    def __repr__(self):
        return self.value


    def get_slot_name(self):
        """
        Get the entity's slot name.
        :return: Entity's name.
        """
        return self.slot_name

    def get_slot_type(self):
        """
        Get the entity's slot type.
        :return: Entity's type.
        """
        return self.type

    def get_start_index(self):
        """
        Get the entity's start index.
        :return: Entity's start index.
        """
        return self.start_index

    def get_end_idx(self):
        """
        Get the entity's end index.
        :return: Entity's end index.
        """
        return self.end_index

    @property
    def json(self):
        return {"slot_name": self.slot_name,
                "entity": self.slot_type,
                "value": self.value,
                "range": {"start": self.start_index, "end": self.end_index}}
