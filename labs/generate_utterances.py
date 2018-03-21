# -*- coding: utf-8 -*-

try:
    from fountain.data_generator import DataGenerator
except:
    import sys
    sys.path.append('../')
    from fountain.data_generator import DataGenerator

import logging
if __name__ == "__main__":
    logging.info('Using `fountain` to generate data')
    # DataGenerator
    data_generator = DataGenerator()
    # load template
    template_fname = 'utterances_template.yaml'
    results = data_generator.parse(template_fname)
    utterances_csv = 'utterances.csv'
    data_generator.to_csv(utterances_csv)
    utterances_json = 'utterances.json'
    data_generator.to_json(utterances_json)

    # case where you have builtin slot
    template_fname = 'utterances_template_builtin.yaml'
    results = data_generator.parse(template_fname)
    utterances_csv = 'utterances_builtin.csv'
    data_generator.to_csv(utterances_csv)
    utterances_json = 'utterances_builtin.json'
    data_generator.to_json(utterances_json)

