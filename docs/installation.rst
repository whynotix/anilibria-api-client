Installation
============

``anilibria-api-client`` requires **Python 3.13** or newer.

.. code-block:: bash

   pip install anilibria-api-client

Development install
-------------------

To install with the development dependencies (pytest, ruff, etc.), use
Poetry:

.. code-block:: bash

   poetry install --with dev

Environment variables
---------------------

The integration test suite reads credentials from a ``.env`` file. Copy the
example and fill in your values:

.. code-block:: bash

   cp .env.example .env

The file contains three variables:

- ``ANILIBRIA_API_TOKEN`` — a Bearer token for authenticated requests.
- ``LOGIN`` — your Anilibria personal-account login.
- ``PASSWORD`` — your Anilibria personal-account password.

Getting a token
---------------

If you only have a login and password, obtain a token using the login
endpoint and pass it to a new client:

.. code-block:: python

   import asyncio

   from anilibria_api_client.api_client import AsyncAnilibriaAPI

   async def main() -> None:
       client = AsyncAnilibriaAPI()
       res = await client.accounts.users_auth_login(
           login="your-login", password="your-password"
       )
       authenticated = AsyncAnilibriaAPI(token=res.token)
       # use `authenticated` for requests that require a token

   asyncio.run(main())

Alternatively, use the :doc:`auth() helper </guide/authentication>` to log in
and get an authenticated client in one line.
