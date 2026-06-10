"""Typed models for API responses."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


def _str(value: Any) -> str:
    return "" if value is None else str(value)


def _int_or_none(value: Any) -> int | None:
    if value is None or value == "":
        return None
    return int(value)


def _float_or_none(value: Any) -> float | None:
    if value is None or value == "":
        return None
    return float(value)


@dataclass(slots=True)
class Vehicle:
    car_id: int
    vin: str
    make: str
    model: str
    year: str
    year_end: str
    description: str
    body: str
    fuel: str
    engine: str
    cubic_capacity_ccm: int | None
    cubic_capacity_liters: float | None
    power_hp_from: int | None
    power_hp_to: int | None
    kw_power_from: Any
    kw_power_to: Any
    cylinder: int | None
    drive: str
    valves: int | None
    fuel_mixture_formation: str
    aspiration: str
    cylinder_design: str
    cooling_type: str
    tonnage: str
    axle_load_from_kg: Any
    axle_load_to_kg: Any
    axle_style: str
    axle_type: str
    axle_body: str
    axle_configuration: str
    wheel_mounting: str
    brake_type: str
    hmd_mfr_model_name: str

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Vehicle:
        return cls(
            car_id=int(data.get("carId", 0)),
            vin=_str(data.get("vin")),
            make=_str(data.get("make")),
            model=_str(data.get("model")),
            year=_str(data.get("year")),
            year_end=_str(data.get("yearEnd")),
            description=_str(data.get("description")),
            body=_str(data.get("body")),
            fuel=_str(data.get("fuel")),
            engine=_str(data.get("engine")),
            cubic_capacity_ccm=_int_or_none(data.get("cubicCapacityCcm")),
            cubic_capacity_liters=_float_or_none(data.get("cubicCapacityLiters")),
            power_hp_from=_int_or_none(data.get("powerHpFrom")),
            power_hp_to=_int_or_none(data.get("powerHpTo")),
            kw_power_from=data.get("kwPowerFrom"),
            kw_power_to=data.get("kwPowerTo"),
            cylinder=_int_or_none(data.get("cylinder")),
            drive=_str(data.get("drive")),
            valves=_int_or_none(data.get("valves")),
            fuel_mixture_formation=_str(data.get("fuelMixtureFormation")),
            aspiration=_str(data.get("aspiration")),
            cylinder_design=_str(data.get("cylinderDesign")),
            cooling_type=_str(data.get("coolingType")),
            tonnage=_str(data.get("tonnage")),
            axle_load_from_kg=data.get("axleLoadFromKg"),
            axle_load_to_kg=data.get("axleLoadToKg"),
            axle_style=_str(data.get("axleStyle")),
            axle_type=_str(data.get("axleType")),
            axle_body=_str(data.get("axleBody")),
            axle_configuration=_str(data.get("axleConfiguration")),
            wheel_mounting=_str(data.get("wheelMounting")),
            brake_type=_str(data.get("brakeType")),
            hmd_mfr_model_name=_str(data.get("hmdMfrModelName")),
        )

    @property
    def full_name(self) -> str:
        return f"{self.make} {self.model} {self.description}".strip()


@dataclass(slots=True)
class FluidCapacity:
    item: str
    qualifier: str
    value: str
    quantity_unit: str
    additional_info: str

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> FluidCapacity:
        return cls(
            item=_str(data.get("ItemMPText")),
            qualifier=_str(data.get("QualColTextStr")),
            value=_str(data.get("ValueText")),
            quantity_unit=_str(data.get("ADQuantityTextStr")),
            additional_info=_str(data.get("AddTextStr")),
        )


@dataclass(slots=True)
class OemPart:
    manufacturer: str
    oe_number: str

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> OemPart:
        return cls(
            manufacturer=_str(data.get("manufacturer")),
            oe_number=_str(data.get("oe_number")),
        )


@dataclass(slots=True)
class OemPartGroup:
    group: str
    shortname: str
    name: str
    parts: list[OemPart] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> OemPartGroup:
        return cls(
            group=_str(data.get("group")),
            shortname=_str(data.get("shortname")),
            name=_str(data.get("name")),
            parts=[OemPart.from_dict(part) for part in data.get("parts", [])],
        )


@dataclass(slots=True)
class RepairTime:
    work_name: str
    part_name: str
    hours: str

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> RepairTime:
        return cls(
            work_name=_str(data.get("workname")),
            part_name=_str(data.get("partname")),
            hours=_str(data.get("hours")),
        )


@dataclass(slots=True)
class Brand:
    name: str
    slug: str

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Brand:
        return cls(name=_str(data.get("name")), slug=_str(data.get("slug")))


@dataclass(slots=True)
class VehicleModel:
    name: str
    slug: str

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> VehicleModel:
        return cls(name=_str(data.get("name")), slug=_str(data.get("slug")))


@dataclass(slots=True)
class Variant:
    type_name: str
    type_years: str
    full_title: str

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Variant:
        return cls(
            type_name=_str(data.get("typeName")),
            type_years=_str(data.get("typeYears")),
            full_title=_str(data.get("fullTitle")),
        )


@dataclass(slots=True)
class Engine:
    brand: str
    model: str
    description: str
    kilo_watts: int | None
    from_date: str
    until: str
    engine_details: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Engine:
        return cls(
            brand=_str(data.get("Brand")),
            model=_str(data.get("Model")),
            description=_str(data.get("Description")),
            kilo_watts=_int_or_none(data.get("kiloWatts")),
            from_date=_str(data.get("From")),
            until=_str(data.get("Until")),
            engine_details=data.get("EngineDetails") or {},
        )

    @property
    def engine_code(self) -> str | None:
        code = self.engine_details.get("EngineCode")
        return _str(code) if code else None