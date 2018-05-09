#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `fountain` package."""

import pytest

from fountain.core.utterance import Utterance
from fountain.resources.utils import preprocess_data


def test_preprocess():
    intent = "food_ingredients"
    utterance_sample = "What Are the Ingredients in {food}?"
    utterance_sample_preprocessed = "what are the ingredients in {food}?"

    assert preprocess_data(utterance_sample) == utterance_sample_preprocessed


def test_validate():
    intent = "food_ingredients"
    utterance_sample = "What Are the Ingredients in {food}?"
    utterance_sample_non_validated = "what are the //ingredients// in {food}?"

    utterance = Utterance(intent, utterance_sample)
    assert utterance.validate(utterance_sample) == True
    assert utterance.validate(utterance_sample_non_validated) == False
