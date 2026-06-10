#!/usr/bin/env python3
"""Verify all VIN Decoder API endpoints and the Python SDK."""

from __future__ import annotations

import os
import sys
import urllib.error
import urllib.parse
import urllib.request
import json

BASE_URL = "https://vindecodervehicle.com/api/"
TEST_VIN = "WF0GXXGAJ69C71882"
TEST_BRAND = "bmw"



def get_credentials() -> tuple[str, str]:
    user = os.environ.get("VINDECODER_USER", "").strip()
    key = os.environ.get("VINDECODER_KEY", "").strip()
    if not user or not key:
        print("ERROR: Set VINDECODER_USER and VINDECODER_KEY environment variables.")
        sys.exit(1)
    return user, key


def api_request(user: str, key: str, **params) -> dict:
    query = urllib.parse.urlencode({"user": user, "key": key, **params})
    url = f"{BASE_URL}?{query}"
    req = urllib.request.Request(url, headers={"Accept": "application/json", "User-Agent": "vindecoder-verify/1.0"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        payload = json.loads(resp.read().decode("utf-8"))
    if not payload.get("success"):
        raise RuntimeError(f"API error: {payload}")
    return payload


def check(name: str, fn, plan_limited: bool = False) -> bool:
    try:
        result = fn()
        print(f"  OK  {name}")
        if isinstance(result, dict) and "summary" in result:
            print(f"       {result['summary']}")
        return True
    except urllib.error.HTTPError as exc:
        if plan_limited and exc.code == 403:
            print(f"  SKIP {name}: plan limit")
            return True
        print(f"  FAIL {name}: {exc}")
        return False
    except Exception as exc:
        print(f"  FAIL {name}: {exc}")
        return False


def main() -> None:
    user, key = get_credentials()
    print(f"\n=== VIN Decoder API Verification ===")
    print(f"User: {user}")
    print(f"VIN:  {TEST_VIN}\n")

    passed = 0
    total = 0
    car_id = None

    def run(name, fn, plan_limited: bool = False):
        nonlocal passed, total
        total += 1
        if check(name, fn, plan_limited):
            passed += 1

    def decode_vin():
        nonlocal car_id
        data = api_request(user, key, vin=TEST_VIN)["data"]
        car_id = data.get("carId")
        return {"summary": f"{data.get('make')} {data.get('model')} (carId={car_id})"}

    def decode_vin_all():
        data = api_request(user, key, vin=TEST_VIN, allCars=1)["data"]
        return {"summary": f"{len(data)} vehicles"}

    def get_engines():
        data = api_request(user, key, vin=TEST_VIN, getEngines=1)["data"]
        return {"summary": f"{len(data)} engines"}

    def get_vehicle():
        if not car_id:
            raise RuntimeError("No carId from VIN decode")
        data = api_request(user, key, carId=car_id, only=1)["data"]
        return {"summary": data.get("make", "")}

    def get_fluids():
        if not car_id:
            raise RuntimeError("No carId")
        data = api_request(user, key, carId=car_id, fluids=1)["data"]
        return {"summary": f"{len(data)} fluid entries"}

    def get_oem_parts():
        if not car_id:
            raise RuntimeError("No carId")
        data = api_request(user, key, carId=car_id, oemParts=1)["data"]
        return {"summary": f"{len(data)} OEM groups"}

    def get_repair_times():
        if not car_id:
            raise RuntimeError("No carId")
        data = api_request(user, key, carId=car_id, timeRepair=1)["data"]
        return {"summary": f"{len(data)} repair entries (plan-dependent)"}

    def list_brands():
        data = api_request(user, key, brands=1)["data"]
        return {"summary": f"{len(data)} brands"}

    def list_models():
        data = api_request(user, key, brand=TEST_BRAND, models=1)["data"]
        return {"summary": f"{len(data)} models for {TEST_BRAND}"}

    def list_variants():
        models_data = api_request(user, key, brand=TEST_BRAND, models=1)["data"]
        if not models_data:
            raise RuntimeError("No BMW models returned")
        model_slug = models_data[0].get("slug") or "3-series"
        data = api_request(user, key, brand=TEST_BRAND, model=model_slug, variants=1)["data"]
        return {"summary": f"{len(data)} variants ({model_slug})"}

    print("--- API Endpoints ---")
    run("GET /?vin= (decode VIN)", decode_vin)
    run("GET /?vin=&allCars=1", decode_vin_all)
    run("GET /?vin=&getEngines=1", get_engines)
    run("GET /?carId=&only=1", get_vehicle)
    run("GET /?carId=&fluids=1", get_fluids)
    run("GET /?carId=&oemParts=1", get_oem_parts, plan_limited=True)
    run("GET /?carId=&timeRepair=1", get_repair_times, plan_limited=True)
    run("GET /?brands=1", list_brands)
    run(f"GET /?brand={TEST_BRAND}&models=1", list_models)
    run(f"GET /?brand={TEST_BRAND}&model=<first>&variants=1", list_variants)

    print("\n--- Python SDK ---")
    try:
        from vindecodervehicle import VinDecoderClient

        client = VinDecoderClient.create(user, key)
        sdk_car_id = None
        sdk_model_slug = None

        def sdk_decode():
            nonlocal sdk_car_id
            v = client.decode_vin(TEST_VIN)
            sdk_car_id = v.car_id
            return {"summary": f"{v.full_name} (carId={sdk_car_id})"}

        def sdk_decode_all():
            return {"summary": f"{len(client.decode_vin_all(TEST_VIN))} vehicles"}

        def sdk_engines():
            return {"summary": f"{len(client.get_engines(TEST_VIN))} engines"}

        def sdk_vehicle():
            if not sdk_car_id:
                raise RuntimeError("No carId from SDK decode")
            return {"summary": client.get_vehicle(sdk_car_id).make}

        def sdk_fluids():
            if not sdk_car_id:
                raise RuntimeError("No carId")
            return {"summary": f"{len(client.get_fluid_capacities(sdk_car_id))} fluids"}

        def sdk_oem_parts():
            if not sdk_car_id:
                raise RuntimeError("No carId")
            return {"summary": f"{len(client.get_oem_parts(sdk_car_id))} OEM groups"}

        def sdk_repair_times():
            if not sdk_car_id:
                raise RuntimeError("No carId")
            return {"summary": f"{len(client.get_repair_times(sdk_car_id))} repairs"}

        def sdk_brands():
            return {"summary": f"{len(client.list_brands())} brands"}

        def sdk_models():
            return {"summary": f"{len(client.list_models(TEST_BRAND))} models"}

        def sdk_variants():
            nonlocal sdk_model_slug
            models = client.list_models(TEST_BRAND)
            if not models:
                raise RuntimeError("No BMW models returned")
            sdk_model_slug = models[0].slug
            return {"summary": f"{len(client.list_variants(TEST_BRAND, sdk_model_slug))} variants ({sdk_model_slug})"}

        run("VinDecoderClient.decode_vin()", sdk_decode)
        run("VinDecoderClient.decode_vin_all()", sdk_decode_all)
        run("VinDecoderClient.get_engines()", sdk_engines)
        run("VinDecoderClient.get_vehicle()", sdk_vehicle)
        run("VinDecoderClient.get_fluid_capacities()", sdk_fluids)
        run("VinDecoderClient.get_oem_parts()", sdk_oem_parts, plan_limited=True)
        run("VinDecoderClient.get_repair_times()", sdk_repair_times, plan_limited=True)
        run("VinDecoderClient.list_brands()", sdk_brands)
        run("VinDecoderClient.list_models()", sdk_models)
        run("VinDecoderClient.list_variants()", sdk_variants)
    except ImportError:
        print("  SKIP Python SDK (not installed)")

    print(f"\n=== Result: {passed}/{total} passed ===\n")
    sys.exit(0 if passed == total else 1)


if __name__ == "__main__":
    main()