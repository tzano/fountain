# -*- coding: utf-8 -*-

"""Main module."""

import io
import yaml
import logging
import re
from resources.builtin import FOUNTAIN_BUILTIN
from resources.constants import UTTERANCE, SLOTS, REG_SYNONYMS, SYNONYMES_DELIMITER
from core.utterance import Utterance
import itertools
from resources.utils import preprocess_text


class DataGenerator():
    """Data Generator class to process file"""

    def __init__(self, file_name=None, language='en'):
        self.file_name = file_name
        self.language = language
        self.utterances = []

    @property
    def json(self):
        """exoport in json format"""
        return dict(language=self.language,
                    utterances=self.utterances)

    def get_synonymes(self, utterance_sample=None):
        """
        parse utterance sample

        :param utterance_sample: utterance sample
        """
        synonymes_slots = self.get_synonymes_slots(utterance_sample)
        synonymes = [_.split(SYNONYMES_DELIMITER) for _ in synonymes_slots]
        return synonymes

    def get_synonymes_slots(self, utterance_sample=None):
        """
        get synonymes slots

        :param utterance_sample: utterance sample

        :return: A list of slot (string)
        """
        if utterance_sample is None:
            utterance_sample = self.utterance_sample

        utterance_sample = preprocess_text(utterance_sample)
        return re.findall(REG_SYNONYMS, utterance_sample)

    def leverage_synonymes(self, utterance_sample):
        """
        replace `synonymes slot` with one synonym

        :param utterance_sample: utterance sample
        :param synonym: synonym

        return Generator
        """

        utterance_sample = preprocess_text(utterance_sample)

        if self.contains_synonymes_slots(utterance_sample):
            synonymes_pos = [[(synonym, synonymes_slot) for synonym in synonymes_slot.split(SYNONYMES_DELIMITER)] for
                             synonymes_slot in self.get_synonymes_slots(utterance_sample)]

            all_pos_combinations = itertools.product(*synonymes_pos)

            for poss_combs in all_pos_combinations:
                _utterance_sample = utterance_sample
                for synonym_value, synonymes_slot in poss_combs:
                    _utterance_sample = _utterance_sample.replace("({})".format(synonymes_slot), synonym_value)

                yield _utterance_sample

        else:
            yield utterance_sample

    def contains_synonymes_slots(self, utterance_sample=None):
        """
        check if it has synonyme slot

        :param utterance_sample: utterance sample

        """
        return self.get_synonymes_slots(utterance_sample) != []

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
            data = self.render(file_name)

        generated_utterances = []
        for intent_name, intent_data in data.iteritems():
            for utterance_data in intent_data:
                utterance_str = utterance_data.get(UTTERANCE, None)
                slots = utterance_data.get(SLOTS, None)
                for utterance_sample in self.leverage_synonymes(utterance_str):
                    utterance = Utterance(intent_name, utterance_sample)
                    generated_utterances += utterance.generate(utterance_sample, slots)
                    self.utterances.append(utterance)
        return generated_utterances

    def to_csv(self, dataset_path):
        with io.open(dataset_path, "w", encoding="utf8") as f:
            f.write("\t".join(['utterance']))
            for utterance in self.utterances:
                f.write(utterance)

    def get_all_builtin_entities(self):
        """
        get all builtin slot types

        :return: (list of strings) list of all slot types
        """
        return FOUNTAIN_BUILTIN
