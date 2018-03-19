class Intent:
    def __init__(self, intent_name):
        """
        Fountain Intent Class.
        Describes the Fountain Intent structure.

        :param intent_name:
        """
        self.intent_name = intent_name
        self.utterances = []

    def __repr__(self):
        return self.intent_name
