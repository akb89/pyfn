"""XML processing error.

Error raised by the XML unmarshalling process
"""

__all__ = ['XMLProcessingError']


class XMLProcessingError(Exception):
    """A specific exception for invalid method."""

    def __init__(self, message):  # pylint:disable=W0235
        """Init function."""
        super().__init__(message)
