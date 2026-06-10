"""Main SDK client."""

from __future__ import annotations

import re
from typing import Any

from .exceptions import ApiError, AuthenticationError, InvalidArgumentError
from .http import HttpClient
from .models import (
    Brand,
    Engine,
    FluidCapacity,
    OemPartGroup,
    RepairTime,
    Variant,
    Vehicle,
    VehicleModel,
)

VIN_PATTERN = re.compile(r"^[A-HJ-NPR-Z0-9]+$")


class VinDecoderClient:
    DEFAULT_BASE_URL = "https://vindecodervehicle.com/api/"

    def __init__(
        self,
        user: str,
        api_key: str,
        *,
        base_url: str = DEFAULT_BASE_URL,
        http_client: HttpClient | None = None,
    ) -> None:
        self.user = user
        self.api_key = api_key
        self.base_url = base_url
        self._http = http_client or HttpClient()

    @classmethod
    def create(cls, user: str, api_key: str, *, base_url: str | None = None) -> VinDecoderClient:
        return cls(user=user, api_key=api_key, base_url=base_url or cls.DEFAULT_BASE_URL)

    def request(self, **params: Any) -> dict[str, Any]:
        query = {"user": self.user, "key": self.api_key, **params}
        status, body = self._http.get(self.base_url, query)
        payload = self._http.decode_json(body)

        if status in (401, 403):
            raise AuthenticationError(self._extract_error(payload, "Authentication failed."), status, payload)

        if status >= 400:
            raise ApiError(self._extract_error(payload, "API request failed."), status, payload)

        if not payload.get("success"):
            raise ApiError(self._extract_error(payload, "API returned success=false."), status, payload)

        return payload

    def decode_vin(self, vin: str) -> Vehicle:
        normalized = self._validate_vin(vin)
        payload = self.request(vin=normalized)
        data = payload.get("data")
        if not isinstance(data, dict):
            raise InvalidArgumentError("Expected a single vehicle in the API response.")
        return Vehicle.from_dict(data)

    def decode_vin_all(self, vin: str) -> list[Vehicle]:
        normalized = self._validate_vin(vin)
        payload = self.request(vin=normalized, allCars=1)
        data = payload.get("data")
        if not isinstance(data, list):
            return []
        return [Vehicle.from_dict(item) for item in data]

    def get_engines(self, vin: str) -> list[Engine]:
        normalized = self._validate_vin(vin)
        payload = self.request(vin=normalized, getEngines=1)
        data = payload.get("data")
        if not isinstance(data, list):
            return []
        return [Engine.from_dict(item) for item in data]

    def get_vehicle(self, car_id: int) -> Vehicle:
        self._validate_car_id(car_id)
        payload = self.request(carId=car_id, only=1)
        data = payload.get("data")
        if not isinstance(data, dict):
            raise InvalidArgumentError("Expected a single vehicle in the API response.")
        return Vehicle.from_dict(data)

    def get_fluid_capacities(self, car_id: int) -> list[FluidCapacity]:
        self._validate_car_id(car_id)
        payload = self.request(carId=car_id, fluids=1)
        data = payload.get("data")
        if not isinstance(data, list):
            return []
        return [FluidCapacity.from_dict(item) for item in data]

    def get_oem_parts(self, car_id: int) -> list[OemPartGroup]:
        self._validate_car_id(car_id)
        payload = self.request(carId=car_id, oemParts=1)
        data = payload.get("data")
        if not isinstance(data, list):
            return []
        return [OemPartGroup.from_dict(item) for item in data]

    def get_repair_times(self, car_id: int) -> list[RepairTime]:
        self._validate_car_id(car_id)
        payload = self.request(carId=car_id, timeRepair=1)
        data = payload.get("data")
        if not isinstance(data, list):
            return []
        return [RepairTime.from_dict(item) for item in data]

    def list_brands(self) -> list[Brand]:
        payload = self.request(brands=1)
        data = payload.get("data")
        if not isinstance(data, list):
            return []
        return [Brand.from_dict(item) for item in data]

    def list_models(self, brand: str) -> list[VehicleModel]:
        brand_slug = self._normalize_slug(brand, "brand")
        payload = self.request(brand=brand_slug, models=1)
        data = payload.get("data")
        if not isinstance(data, list):
            return []
        return [VehicleModel.from_dict(item) for item in data]

    def list_variants(self, brand: str, model: str) -> list[Variant]:
        brand_slug = self._normalize_slug(brand, "brand")
        model_slug = self._normalize_slug(model, "model")
        payload = self.request(brand=brand_slug, model=model_slug, variants=1)
        data = payload.get("data")
        if not isinstance(data, list):
            return []
        return [Variant.from_dict(item) for item in data]

    @staticmethod
    def _validate_vin(vin: str) -> str:
        normalized = vin.strip().upper()
        if len(normalized) < 8 or len(normalized) > 17:
            raise InvalidArgumentError(f"VIN must be between 8 and 17 characters. Got {len(normalized)}.")
        if not VIN_PATTERN.match(normalized):
            raise InvalidArgumentError("VIN contains invalid characters.")
        return normalized

    @staticmethod
    def _validate_car_id(car_id: int) -> None:
        if car_id <= 0:
            raise InvalidArgumentError("car_id must be a positive integer.")

    @staticmethod
    def _normalize_slug(value: str, field: str) -> str:
        normalized = value.strip().lower()
        if not normalized:
            raise InvalidArgumentError(f"{field} must not be empty.")
        return normalized

    @staticmethod
    def _extract_error(payload: dict[str, Any], fallback: str) -> str:
        for key in ("message", "error", "detail"):
            value = payload.get(key)
            if isinstance(value, str) and value:
                return value
        return fallback