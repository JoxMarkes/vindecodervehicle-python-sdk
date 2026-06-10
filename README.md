# VIN Decoder Vehicle — Python SDK

[![CI](https://github.com/JoxMarkes/vindecodervehicle-python-sdk/actions/workflows/ci.yml/badge.svg)](https://github.com/JoxMarkes/vindecodervehicle-python-sdk/actions/workflows/ci.yml)
[![PyPI](https://img.shields.io/pypi/v/vindecodervehicle-sdk.svg)](https://pypi.org/project/vindecodervehicle-sdk/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

Official Python SDK for the **[VIN Decoder Vehicle API](https://vindecodervehicle.com)**.

## Features

- Zero runtime dependencies (stdlib only)
- Python 3.9+
- Typed dataclass models
- All API endpoints supported

## Installation

```bash
pip install vindecodervehicle-sdk
```

## Quick Start

```python
from vindecodervehicle import VinDecoderClient

client = VinDecoderClient.create(user="YOUR_USER", api_key="YOUR_API_KEY")

vehicle = client.decode_vin("WF0GXXGAJ69C71882")
print(vehicle.full_name)  # BMW 3 Coupe (E92) 316 i
print(vehicle.make)       # BMW
print(vehicle.car_id)     # 55565
```

## API Reference

### VIN

```python
vehicle = client.decode_vin("WF0GXXGAJ69C71882")
vehicles = client.decode_vin_all("WF0GXXGAJ69C71882")
engines = client.get_engines("WF0GXXGAJ69C71882")
```

### Vehicle by carId

```python
vehicle = client.get_vehicle(55565)
fluids = client.get_fluid_capacities(55565)
parts = client.get_oem_parts(55565)
repairs = client.get_repair_times(55565)
```

### Catalog

```python
brands = client.list_brands()
models = client.list_models("bmw")
variants = client.list_variants("bmw", "3-series")
```

## Error Handling

```python
from vindecodervehicle import (
    ApiError,
    AuthenticationError,
    InvalidArgumentError,
)

try:
    vehicle = client.decode_vin("INVALID")
except InvalidArgumentError:
    pass
except AuthenticationError:
    pass
except ApiError as exc:
    print(exc.status_code, exc.response_body)
```

## Links

- [API Documentation](https://vindecodervehicle.com/api/doc/)
- [PHP SDK](https://github.com/JoxMarkes/vindecodervehicle-php-sdk)
- [Node.js SDK](https://github.com/JoxMarkes/vindecodervehicle-node-sdk)
- [JavaScript SDK](https://github.com/JoxMarkes/vindecodervehicle-js-sdk)

## License

MIT