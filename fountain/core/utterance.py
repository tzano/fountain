from ..resources.constants import BANNED_CHARACTERS, REG_RANGE
import re
import itertools
from ..resources.builtin import FOUNTAIN_BUILTIN
from ..resources.utils import preprocess_data


class Utterance:
    def __init__(self, intent, utterance_sample, entities=[]):
        """
        Fountain Utterance Class.
        Describes the Fountain Utterance structure.

        :param intent:
        :param utterance_sample:
        """
        self.intent = intent
        self.utterance_sample = utterance_sample
        self.entities = entities

    def __repr__(self):
        return self.utterance_sample

    def __str__(self):
        return "intent: {}\t utterance: {}".format(self.intent, self.utterance_sample)

    @property
    def json(self):
        return [{
            "text": self.utterance_sample,
            "intent": self.intent,
            "entities": [
                {
                    "start": entity.start_index,
                    "end": entity.end_index,
                    "value": entity.value,
                    "entity": entity.slot_type
                }
            ]
        } for entity in self.entities]

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

    def get_range_slots(self, utterance_sample=None):
        """
        get range slot

        e.g: book a table for {1-5} people

        :param utterance_sample: utterance sample

        :return: A list of range slots
        """
        if utterance_sample is None:
            utterance_sample = self.utterance_sample

        utterance_sample = preprocess_data(utterance_sample)
        return re.findall(REG_RANGE, utterance_sample)
