Authentication
==============

The ``anilibria_api_client.helper.auth`` helper performs a one-line login and
returns a new ``AsyncAnilibriaAPI`` instance authenticated with the returned
Bearer token.

.. code-block:: python

   import asyncio

   from anilibria_api_client.api_client import AsyncAnilibriaAPI
   from anilibria_api_client.helper import auth

   async def main() -> None:
       client = AsyncAnilibriaAPI()
       authenticated = await auth(client, "your-login", "your-password")
       # `authenticated` sends the Bearer token on every request
       profile = await authenticated.accounts.users_me_profile()

   asyncio.run(main())

.. seealso::

   :doc:`/installation` for setting up credentials via ``.env``.
