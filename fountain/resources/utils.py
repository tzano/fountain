from builtin import RESOURCES, PERCENTAGE_BUILTIN_SLOTS
from constants import ROOT_PATH, DATA_DIR
import random
import io

def preprocess_text(text):
    """
    preprocess the text to standarize the name

    :param text: text

    :return: preprocessed text
    """
    # lower case the text
    text = text.lower()
    return text


def get_builtin_resources(lang, builtin_slot):
    """

    :param lang:
    :param builtin_slot:
    :return:
    """
    builtin_slot_fname = RESOURCES[builtin_slot.upper()]
    # path to dataset
    fpath = "{}/{}/{}/{}".format(ROOT_PATH, DATA_DIR, lang, builtin_slot_fname)

    items = load_data(fpath)
    n_items = len(items)
    return random.sample(items, int(n_items * PERCENTAGE_BUILTIN_SLOTS))


def load_data(dataset_path):
    """
    load data from a file

    :param dataset_path:
    :return: a list of all the items in the file
    """
    items = []
    with io.open(dataset_path, "r", encoding="utf8") as f:
        for line in f:
            items.append(line.rstrip())
    return items
