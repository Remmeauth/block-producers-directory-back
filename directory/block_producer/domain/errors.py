"""
Provide errors for block producer domain objects.
"""


class BlockProducerWithSpecifiedIdentifierDoesNotExistError(Exception):
    """
    Block producer with specified identifier does not exist error.
    """

    def __init__(self):
        """
        Constructor.
        """
        self.message = 'Block producer with specified identifier does not exist.'
