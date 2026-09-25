Pagination
==========

Use ``anilibria_api_client.helper.auto_paginate`` to fetch every page of a
paginated endpoint in a single call.

.. code-block:: python

   import asyncio

   from anilibria_api_client.api_client import AsyncAnilibriaAPI
   from anilibria_api_client.helper import auto_paginate

   async def main() -> None:
       client = AsyncAnilibriaAPI()
       async with client.api:
           # Pass the bound method WITHOUT calling it.
           releases = await auto_paginate(
               client.anime.catalog_releases_get,
               limit=100,
           )
           print(len(releases))

   asyncio.run(main())

Usage notes
-----------

- Pass the bound method **without calling it** (no parentheses) — for
  example ``client.anime.catalog_releases_get``, not
  ``client.anime.catalog_releases_get()``.
- Do **not** pass ``page`` or ``limit`` yourself; ``auto_paginate`` manages
  them.
- It only works on endpoints that actually accept ``page`` and ``limit``.
  Real paginated endpoints include:

  - ``client.anime.catalog_releases_get``
  - ``client.anime.releases_list``
  - ``client.anime.torrents``
  - ``client.accounts.users_me_views_history``

- It does **not** work on ``limit``-only endpoints such as
  ``client.anime.releases_latest`` (which has no ``page`` parameter).
