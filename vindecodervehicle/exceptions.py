"""Exception types for the VIN Decoder Vehicle SDK."""


class VinDecoderError(Exception):
    """Base exception for all SDK errors."""


class InvalidArgumentError(VinDecoderError):
    """Raised when input validation fails."""


class NetworkError(VinDecoderError):
    """Raised when a network request fails."""


class ApiError(VinDecoderError):
    """Raised when the API returns an error response."""

    def __init__(self, message: str, status_code: int | None = None, response_body: dict | None = None):
        super().__init__(message)
        self.status_code = status_code
        self.response_body = response_body


class AuthenticationError(ApiError):
    """Raised when authentication fails."""