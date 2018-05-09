#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `fountain` package."""

import pytest
from fountain.data_generator import DataGenerator


SAMPLE_FILE_PATH = 'tests/sample.yaml'

def test_render_template():
    fname = SAMPLE_FILE_PATH
    data_generator = DataGenerator()
    rendered_data = data_generator.render(fname)
    assert (set() == (set(rendered_data.keys()) - set(['get_weather_condition', 'book_cab'])))


def test_parse():
    fname = SAMPLE_FILE_PATH
    data_generator = DataGenerator()
    results = data_generator.parse(fname)
    passible_results = [('book_cab', 'book a cab to airport'), ('book_cab', 'book a cab to city center'),
                        ('book_cab', 'book a taxi to airport'), ('book_cab', 'book a taxi to city center'),
                        ('get_weather_condition', "what's the weather in New York"),
                        ('get_weather_condition', "what's the weather in Chicago"),
                        ('get_weather_condition', 'what is the weather in New York'),
                        ('get_weather_condition', 'what is the weather in Chicago'),
                        ('get_weather_condition', 'is it rainy in Melbourne'),
                        ('get_weather_condition', 'is it rainy in Sydney'),
                        ('get_weather_condition', 'is it chilly in Melbourne'),
                        ('get_weather_condition', 'is it chilly in Sydney'),
                        ('get_weather_condition', 'is it cold in Melbourne'),
                        ('get_weather_condition', 'is it cold in Sydney')]
    assert (set() == (set(results) - set(passible_results)))


def test_get_synonymes_slots():
    data_generator = DataGenerator()

    intent = "status_inquiry"
    utterance_sample = "(what is the|what's the) status"

    assert data_generator.get_synonymes_slots(utterance_sample) == ["what is the|what's the"]


def test_get_synonymes():
    data_generator = DataGenerator()
    utterance_sample = "(what is the|what's the) status"
    assert [["what is the", "what's the"]] == data_generator.get_synonymes(utterance_sample)


def test_get_slots():
    intent = "food_ingredients"
    utterance_sample = "What Are the Ingredients in {food:food}?"
    data_generator = DataGenerator()
    assert data_generator.get_slots(utterance_sample) == ["food:food"]


def test_leverage_synonymes():
    data_generator = DataGenerator()
    utterance_sample = "(what is the|what's the) status"
    assert list(data_generator.leverage_synonymes(utterance_sample)) == ["what is the status", "what's the status"]
    utterance_sample = "what is the status"
    assert list(data_generator.leverage_synonymes(utterance_sample)) == ['what is the status']


def test_is_builtin_entity():
    data_generator = DataGenerator()
    assert True == data_generator.is_builtin_entity('fountain:city')
    assert False == data_generator.is_builtin_entity('FOUNTAIN:TEST')
