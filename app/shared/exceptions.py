class EduGraphError(Exception):
    """Base exception for EduGraph domain errors."""


class ParserError(EduGraphError):
    """Raised when the dataset cannot be parsed correctly."""


class AlgorithmError(EduGraphError):
    """Raised for issues in graph algorithms (cycles, invalid states)."""


class AuthorizationError(EduGraphError):
    """Raised when a user is not authorized to access a resource."""
