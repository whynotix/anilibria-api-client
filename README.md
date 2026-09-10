# Anilibria-Api-Client


[![pypi](https://img.shields.io/pypi/v/anilibria-api-client.svg)](https://pypi.org/project/anilibria-api-client/) [![LICENSE](https://img.shields.io/github/license/whynotix/anilibria-api-client)](https://github.com/whynotix/Anilibria-Api-Client/blob/main/LICENSE) [![Python](https://img.shields.io/pypi/pyversions/anilibria-api-client.svg)](https://pypi.org/project/anilibria-api-client/)

> [!CAUTION]  
> **It is not an official wrapper.** [Official AniLibria's Swagger](https://anilibria.top/api/docs/v1)

Anilibria-API-Client - this a async client to work with Anilibria API, use a aiohttp. Full writed at python

## Installing

Developed and tested with Python 3.13. While it may work with other versions (oldest and newest), they are not officially supported.

### pip

```bash
$ pip install anilibria-api-client
```

## Usage

```python
from anilibria_api_client.api_client import AsyncAnilibriaAPI  # Client
from anilibria_api_client.exceptions import (
    AnilibriaException,
    AnilibriaValidationException,
)  # Errors
from anilibria_api_client.types import *  # Types for some methods
from anilibria_api_client.models import *  # Input models for some methods
from anilibria_api_client.responses import *  # Response models generated from OpenAPI
from anilibria_api_client.helper import *  # Download anime, save torrents files and more


async def main():
    async with AsyncAnilibriaAPI() as api:
        await api.teams.users(include="nickname")

    api = AsyncAnilibriaAPI()  # like js support
    await api.teams.users(include="nickname")
```

## Documentation 📃

[Docs](https://anilibria-api-client.readthedocs.io/stable/)

## Issues/Contributing

### Issues

Report for any issues [here](https://github.com/whynotix/Anilibria-Api-Client/issues)

### Contributing

We approve contibuting and wait your first pull request

