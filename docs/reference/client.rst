Client
======

``anilibria_api_client.api_client.AsyncAnilibriaAPI`` is the high-level async
client. It exposes the endpoint methods through its ``accounts``, ``anime``,
``app``, ``media`` and ``teams`` attributes. Underneath it uses
``anilibria_api_client.base_api.api_class.API``, a raw aiohttp transport that
closes its session after each request unless it is used as an async context
manager (``async with client.api``).

.. automodule:: anilibria_api_client.api_client
   :members:

Raw transport
-------------

.. autoclass:: anilibria_api_client.base_api.api_class.API
   :members:
   :show-inheritance:
