# -*- coding: utf-8 -*-

"""Main module."""

import io
import itertools
import json
import logging
import re

import yaml

from .core.utterance import Utterance
from .core.slot import Slot
from .core.entity import Entity
from .resources.builtin import FOUNTAIN_BUILTIN, RESOURCES
from .resources.constants import UTTERANCE, SLOTS, REG_SLOTS, REG_SYNONYMS, SYNONYMES_DELIMITER
from .resources.utils import preprocess_data, get_builtin_resources


class DataGenerator():
    """Data Generator class to process file"""

    def __init__(self, file_name=None, language='en'):
        self.file_name = file_name
        self.language = language
        self.utterances = []

    def clear(self):
        """
        clear utterances

        :return:
        """
        self.utterances = []

    def render(self, file_name):
        """
        :param file_name: is the file that contains

        :return:
        """
        logging.info('Render file: {}'.format(file_name))

        try:
            with io.open(file_name) as f:
                rendered_data = yaml.load(f)
                return rendered_data
        except yaml.YAMLError as exc:
            logging.error('Error: \n {}'.format(exc))
            return None

    def get_synonymes(self, utterance_sample=None):
        """
        parse utterance sample

        :param utterance_sample: utterance sample
        """
        synonymes_slots = self.get_synonymes_slots(utterance_sample)
        synonymes = [synonymes_slot.split(SYNONYMES_DELIMITER) for synonymes_slot in synonymes_slots]
        return synonymes

    def get_synonymes_slots(self, utterance_sample=None):
        """
        get synonymes slots

        :param utterance_sample: utterance sample

        :return: A list of slot (string)
        """

        utterance_sample = preprocess_data(utterance_sample)
        return re.findall(REG_SYNONYMS, utterance_sample)

    def leverage_synonymes(self, utterance_sample):
        """
        replace `synonymes slot` with one synonym

        :param utterance_sample: utterance sample
        :param synonym: synonym

        return Generator
        """

        if self.contains_synonymes_slots(utterance_sample):
            synonymes_all = [[(synonym, synonymes_slot) for synonym in synonymes_slot.split(SYNONYMES_DELIMITER)] for
                             synonymes_slot in self.get_synonymes_slots(utterance_sample)]

            all_combinations = itertools.product(*synonymes_all)

            for poss_combs in all_combinations:
                utterance = utterance_sample
                for synonym_value, synonymes_slot in poss_combs:
                    utterance = utterance.replace("({})".format(synonymes_slot), synonym_value)

                yield utterance

        else:
            yield utterance_sample

    def contains_synonymes_slots(self, utterance_sample=None):
        """
        check if it has synonyme slot

        :param utterance_sample: utterance sample

        """
        return self.get_synonymes_slots(utterance_sample) != []

    def get_slots(self, utterance_sample=None):
        """
        get slots

        :param utterance_sample: utterance sample

        :return: A list of slot (string)
        """

        utterance_sample = preprocess_data(utterance_sample)
        return re.findall(REG_SLOTS, utterance_sample)

    def _check_slots(self, utterance_sample, slots):
        """

        :param utterance_sample:
        :param slots: set
        :return:
        """
        set_slots = {}
        if self.contains_slots(utterance_sample):
            set_slots = {slot_value for slot_value in self.get_slots(utterance_sample) if
                         not self.is_builtin_entity(slot_value)}

        return set_slots == set(slots)

    def generate(self, intent_name, utterance_sample, slots):
        """
        parse and generate from slots
        :param intent_name:
        :param utterance_sample:
        :param slots:
        :return: A list of entities
        """

        if self.contains_slots(utterance_sample):
            slots_all = list()
            for slot_value in self.get_slots(utterance_sample):
                slots_lst = list()
                if self.is_builtin_entity(slot_value):
                    for slot in get_builtin_resources(self.language, slot_value):
                        slots_lst += [(slot_value, slot)]
                else:
                    for slot in slots.get(slot_value, []):
                        slots_lst += [(slot_value, slot)]
                slots_all += [slots_lst]

            all_combinations = itertools.product(*slots_all)

            for poss_combs in all_combinations:
                utterance = utterance_sample
                entities = list()
                for slot_value, value in poss_combs:
                    utterance = utterance.replace('{%s}' % (slot_value), value)
                    slot_type, slot_name = Slot(slot_value).parse()
                    start_index = utterance.find(value)
                    end_index = start_index + len(value)
                    entities.append(Entity(slot_name, slot_type, value, start_index, end_index))

                yield Utterance(intent=intent_name, utterance_sample=utterance, entities=entities)

        else:
            yield Utterance(intent=intent_name, utterance_sample=utterance_sample, entities=[])

    def contains_slots(self, utterance_sample=None):
        """
        check if it has slots

        e.g: What Are the Ingredients in {food}?

        :param utterance_sample: utterance sample

        :return: Boolean indicating whether the utterance contains slots or no
        """
        return self.get_slots(utterance_sample) != []

    def parse(self, file_name=None):
        """
        The method takes all slots and make a full cartesian product of all the synonymes and slot sample values

        :param file_name: is the file that contains the template and the examples

        :return:
        """
        if file_name is None:
            if self.file_name is not None:
                data = self.render(self.file_name)
            else:
                logging.error('Please add a file name to process it.')
        else:
            self.clear()
            data = self.render(file_name)

        generated_utterances = []
        for intent_name, intent_data in data.iteritems():
            for utterance_data in intent_data:
                utterance_str = utterance_data.get(UTTERANCE, None)
                slots = utterance_data.get(SLOTS, {})

                print(utterance_str, self._check_slots(utterance_str, slots))
                # preprocess_data
                if slots is not None and all(slots.values()):
                    slots = preprocess_data(slots)
                    utterance_str = preprocess_data(utterance_str)

                    for utterance_sample in self.leverage_synonymes(utterance_str):
                        for generated_utterance in self.generate(intent_name, utterance_sample, slots):
                            generated_utterances += [(intent_name, generated_utterance.utterance_sample)]
                            self.utterances.append(generated_utterance)
                else:
                    logging.error(
                        'You did not add any samples to one of the slots for utterance {}'.format(utterance_str))

        return generated_utterances

    def get_all_builtin_entities(self):
        """
        get all builtin slot types

        :return: (list of strings) list of all slot types
        """
        return FOUNTAIN_BUILTIN

    def is_builtin_entity(self, entity_value):
        """
        check if the slot is of a built-in type

        :param entity_value: the entity value

        :return: True if the `value` is supported by `Foutain`
        """
        builtin_preprocessed = set(map(lambda x: preprocess_data(x), FOUNTAIN_BUILTIN))
        return (entity_value in FOUNTAIN_BUILTIN) or (entity_value in builtin_preprocessed)

    def to_csv(self, dataset_path):
        with io.open(dataset_path, "w", encoding="utf8") as f:
            header = u"{}\t{}\n".format("intent", "utterance")
            f.write(header)
            for utterance in self.utterances:
                f.write(u"{}\t{}\n".format(utterance.intent, utterance.utterance_sample))

    def to_json(self, dataset_path):
        """exoport in json format"""
        with io.open(dataset_path, "w", encoding="utf8") as f:
            data = reduce(lambda x, y: x + y, map(lambda u: u.json, self.utterances))
            data = json.dumps(data, ensure_ascii=False, encoding='utf8', indent=4, sort_keys=True)
            f.write(data)
