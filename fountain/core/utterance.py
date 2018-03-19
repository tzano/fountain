from ..resources.constants import BANNED_CHARACTERS, REG_RANGE, REG_SLOTS, REG_SYNONYMS, SYNONYMES_DELIMITER
import re
import itertools
from slot import Slot
from entity import Entity
from ..resources.builtin import FOUNTAIN_BUILTIN
from ..resources.utils import preprocess_text


class Utterance:
    def __init__(self, intent, utterance_sample, slots=[]):
        """
        Fountain Utterance Class.
        Describes the Fountain Utterance structure.

        :param intent:
        :param utterance_sample:
        """
        self.intent = intent
        self.utterance_sample = utterance_sample
        self.slots = slots

    def __repr__(self):
        return self.utterance_sample

    def validate(self, utterance_sample=None):
        """
        validate_utterance

        :param utterance_sample: utterance sample

        :return: Boolean indicating whether the utterance contains invalide values or no
        """
        if utterance_sample is None:
            utterance_sample = self.utterance_sample

        chs_found = set(BANNED_CHARACTERS).intersection(utterance_sample)
        return chs_found == set()

    def get_slots(self, utterance_sample=None):
        """
        get slots

        :param utterance_sample: utterance sample

        :return: A list of slot (string)
        """
        if utterance_sample is None:
            utterance_sample = self.utterance_sample

        utterance_sample = preprocess_text(utterance_sample)
        return re.findall(REG_SLOTS, utterance_sample)

    def generate(self, utterance_sample, slots):
        """
        parse and generate from slots

        :param utterance_sample:
        :param slots:

        :return: A list of entities
        """
        utterance_sample = preprocess_text(utterance_sample)

        generated_utterances = []
        if self.contains_slots(utterance_sample):
            slots_pos = [[(slot_value, slot) for slot in slots.get(slot_value, [])] for slot_value in
                         self.get_slots(utterance_sample)]

            all_pos_combinations = itertools.product(*slots_pos)

            for poss_combs in all_pos_combinations:
                _utterance_sample = utterance_sample
                for slot_value, value in poss_combs:
                    _utterance_sample = _utterance_sample.replace('{%s}' % (slot_value), value)
                    slot_type, slot_name = Slot(slot_value).parse()
                    start_index = _utterance_sample.find(value)
                    end_index = start_index + len(value)
                    self.slots.append(Entity(slot_name, slot_type, value, start_index, end_index))

                generated_utterances += [_utterance_sample]

            return generated_utterances
        else:
            return [utterance_sample]

    def contains_slots(self, utterance_sample=None):
        """
        check if it has slots

        e.g: What Are the Ingredients in {food}?

        :param utterance_sample: utterance sample

        :return: Boolean indicating whether the utterance contains slots or no
        """
        return self.get_slots(utterance_sample) != []

    def get_range_slots(self, utterance_sample=None):
        """
        get range slot

        e.g: book a table for {1-5} people

        :param utterance_sample: utterance sample

        :return: A list of range slots
        """
        if utterance_sample is None:
            utterance_sample = self.utterance_sample

        utterance_sample = preprocess_text(utterance_sample)
        return re.findall(REG_RANGE, utterance_sample)

    def is_builtin_entity(self, entity_value):
        """
        check if the slot is of a built-in type

        :param entity_value: the entity value

        :return: True if the `value` is supported by `Foutain`
        """
        return entity_value in FOUNTAIN_BUILTIN
