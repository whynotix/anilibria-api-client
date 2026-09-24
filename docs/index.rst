AniLibria-Api-Client Documentation
==================================

Python async API wrapper for AniLibria Swagger

Developed and tested with Python 3.13. While it may work with other versions (oldest and newest), they are not officially supported.

Example
-------------

.. code-block:: python

   from anilibria_api_client.api_client import AsyncAnilibriaAPI # Client
   from anilibria_api_client.exceptions import AnilibriaException, AnilibriaValidationException # Errors
   from anilibria_api_types.enums import * # Enums
   from anilibria_api_types.responses import * # Response models generated from OpenAPI
   from anilibria_api_client.helper import * # Download anime, save torrents files and more

   async def main():
      api = AsyncAnilibriaAPI()
      await api.teams.users(include="nickname")

.. toctree::
   :maxdepth: 4
   :caption: Pages:

   pages.rst