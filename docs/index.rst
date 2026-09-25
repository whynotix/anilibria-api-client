:html_theme.sidebar_secondary.remove: true

.. container:: hero

   .. container:: hero-kicker

      async · Python 3.13 · aiohttp

   .. container:: hero-title

      anilibria-api-client

   .. container:: hero-lede

      A typed, asynchronous Python client for the AniLibria Swagger API.
      Automatic pagination, one-line authentication, and torrent or m3u8
      video downloads.

   .. container:: hero-actions

      .. button-link:: https://pypi.org/project/anilibria-api-client/
         :color: primary
         :shadow:

         pip install anilibria-api-client

      .. button-ref:: quickstart
         :color: secondary
         :outline:
         :ref-type: doc

         Start in 60 seconds

.. container:: badge-row

   .. image:: https://img.shields.io/pypi/v/anilibria-api-client.svg
      :target: https://pypi.org/project/anilibria-api-client/
      :alt: PyPI version

   .. image:: https://img.shields.io/pypi/pyversions/anilibria-api-client.svg
      :target: https://pypi.org/project/anilibria-api-client/
      :alt: Python versions

   .. image:: https://img.shields.io/github/license/whynotix/anilibria-api-client
      :target: https://github.com/whynotix/Anilibria-Api-Client/blob/main/LICENSE
      :alt: License

   .. image:: https://img.shields.io/pypi/v/anilibria-api-types?label=anilibria-api-types
      :target: https://pypi.org/project/anilibria-api-types/
      :alt: anilibria-api-types version

.. caution::

   This project is not an official AniLibria wrapper. The upstream API is
   documented in the `official Swagger UI <https://anilibria.top/api/docs/v1>`_.

.. grid:: 1 2 2 4
   :gutter: 3

   .. grid-item-card:: Async by default
      :link: reference/client
      :link-type: doc
      :class-card: feature-card

      ``AsyncAnilibriaAPI`` can pool an ``aiohttp`` session or close it
      automatically after every request. Use ``async with`` when you want
      the pooled session.

   .. grid-item-card:: Helper functions
      :link: reference/helpers
      :link-type: doc
      :class-card: feature-card

      ``auth()``, ``auto_paginate()``, torrent saving, and multithreaded
      m3u8 video downloads, all async.

   .. grid-item-card:: Typed responses
      :link: reference/responses
      :link-type: doc
      :class-card: feature-card

      Pydantic models generated from the OpenAPI schema and re-exported
      from ``anilibria_api_types.responses``.

   .. grid-item-card:: Predictable errors
      :link: reference/exceptions
      :link-type: doc
      :class-card: feature-card

      ``AnilibriaException`` for request failures, and
      ``AnilibriaValidationException``, which carries the raw HTTP 422
      payload.

Quickstart
----------

.. code-block:: python
   :caption: quickstart.py

   import asyncio

   from anilibria_api_client.api_client import AsyncAnilibriaAPI


   async def main() -> None:
       async with AsyncAnilibriaAPI() as api:
           teams = await api.teams.users(include="nickname")
           print(teams)


   asyncio.run(main())

.. toctree::
   :hidden:
   :caption: Getting started

   installation
   quickstart

.. toctree::
   :hidden:
   :caption: Guide

   guide/authentication
   guide/pagination
   guide/downloads

.. toctree::
   :hidden:
   :caption: API reference

   reference/index
