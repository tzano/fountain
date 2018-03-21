# -*- coding: utf-8 -*-
from os.path import join, dirname, abspath

ROOT_PATH = dirname(dirname(abspath(__file__)))
PACKAGE_NAME = "fountain"
DATA_DIR = "data"
# These are commands
CAPITALIZE = "capitalize"
ENABLE_SYNONYMS = "enable_synonyms"

# banned characters
BANNED_CHARACTERS = "/\\^%$#@~`_=+><;"

# regular expressions
REG_SLOTS = r"\{(.*?)\}" # r"\\{(.*?)\\}"
REG_RANGE = r"\{(d+?-d+?)\}"

REG_SYNONYMS = r"\((.*?)\)" # r"\(([^)]*)\)"

# delimiter
SLOT_DELIMITER = ':'
SYNONYMES_DELIMITER = '|'

# NLU Taxonomy
SYNONYMS = "synonyms"
DATA = "data"
INTENT = "intent"
INTENTS = "intents"
ENTITIES = "entities"
ENTITY = "entity"
SLOT = "slot"
SLOTS = "slots"
UTTERANCES = "utterances"
UTTERANCE = "utterance"
START = "start"
END = "end"

# supported languages
LANGUAGE_EN = "en"
LANGUAGE_AR = "ar"
