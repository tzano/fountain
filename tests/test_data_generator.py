#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `fountain` package."""

import pytest
from fountain.data_generator import DataGenerator


def test_render_template():
    fname = 'sample.yaml'
    data_generator = DataGenerator()
    rendered_data = data_generator.render(fname)
    assert(set() == (set(rendered_data.keys()) - set(['get_weather_condition', 'book_cab'])))

def test_parse():
    fname = 'sample.yaml'
    data_generator = DataGenerator()
    results = data_generator.parse(fname)
    passible_results = ['book a cab to airport', 'book a cab to city center', 'book a taxi to airport',
                          'book a taxi to city center', "what's the weather in New York",
                          "what's the weather in Chicago", 'what is the weather in New York',
                          'what is the weather in Chicago', 'is it rainy in Melbourne', 'is it rainy in Sydney',
                          'is it chilly in Melbourne', 'is it chilly in Sydney', 'is it cold in Melbourne',
                          'is it cold in Sydney']
    assert(set() == (set(results) - set(passible_results)))


def test_get_synonymes_slots():
    data_generator = DataGenerator()

    intent = "status_inquiry"
    utterance_sample = "(what is the|what's the) status"

    assert data_generator.get_synonymes_slots(utterance_sample) == ["what is the|what's the"]


def test_get_synonymes():
    data_generator = DataGenerator()
    utterance_sample = "(what is the|what's the) status"
    assert [["what is the", "what's the"]] == data_generator.get_synonymes(utterance_sample)


def test_leverage_synonymes():
    data_generator = DataGenerator()
    utterance_sample = "(what is the|what's the) status"
    assert list(data_generator.leverage_synonymes(utterance_sample)) == ["what is the status", "what's the status"]
    utterance_sample = "what is the status"
    assert list(data_generator.leverage_synonymes(utterance_sample)) == ['what is the status']

