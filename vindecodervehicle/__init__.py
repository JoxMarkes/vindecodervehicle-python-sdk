"""Official Python SDK for the VIN Decoder Vehicle API."""

from .client import VinDecoderClient
from .exceptions import (
    ApiError,
    AuthenticationError,
    InvalidArgumentError,
    NetworkError,
    VinDecoderError,
)
from .models import (
    Brand,
    Engine,
    FluidCapacity,
    OemPart,
    OemPartGroup,
    RepairTime,
    Variant,
    Vehicle,
    VehicleModel,
)

__all__ = [
    "ApiError",
    "AuthenticationError",
    "Brand",
    "Engine",
    "FluidCapacity",
    "InvalidArgumentError",
    "NetworkError",
    "OemPart",
    "OemPartGroup",
    "RepairTime",
    "Variant",
    "Vehicle",
    "VehicleModel",
    "VinDecoderClient",
    "VinDecoderError",
]

__version__ = "1.0.0"