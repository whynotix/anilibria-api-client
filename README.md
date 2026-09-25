# anilibria-api-client


[![pypi](https://img.shields.io/pypi/v/anilibria-api-client.svg?label=current-version)](https://pypi.org/project/anilibria-api-client/) [![LICENSE](https://img.shields.io/github/license/whynotix/anilibria-api-client)](https://github.com/whynotix/Anilibria-Api-Client/blob/main/LICENSE) [![Python](https://img.shields.io/pypi/pyversions/anilibria-api-client.svg)](https://pypi.org/project/anilibria-api-client/) [![anilibria-api-types](https://img.shields.io/pypi/v/anilibria-api-types?label=anilibria-api-types)](https://pypi.org/project/types/)

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
)  # However, even though the `types` package includes generation, I would prefer to explicitly define my own errors in the main repository and use those.
from anilibria_api_client.helper import *  # Download anime, save torrents files and more

from anilibria_api_types.enums import *  # Enums
from anilibria_api_types.responses import *  # Response models generated from OpenAPI


async def main():
    api = AsyncAnilibriaAPI()
    await api.teams.users(include="nickname")
```

## Documentation 📃

[Docs](https://anilibria-api-client.readthedocs.io/stable/)

## Issues/Contributing

### Issues

Report for any issues [here](https://github.com/whynotix/Anilibria-Api-Client/issues)

### Contributing

We approve contibuting and wait your first pull request

