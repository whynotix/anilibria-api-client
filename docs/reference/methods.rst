Methods
=======

Endpoint methods are generated from the OpenAPI schema and live in the
external ``anilibria_api_types`` package. They are grouped into the
``AccountsMethod``, ``AnimeMethod``, ``AppMethod``, ``MediaMethod`` and
``TeamsMethod`` classes, which all inherit from ``BaseMethod``.

.. autoclass:: anilibria_api_types.methods.base_method.BaseMethod
   :members:
   :show-inheritance:

Accounts
--------

.. autoclass:: anilibria_api_types.codegen.methods.accounts.AccountsMethod
   :members:
   :show-inheritance:

Anime
-----

.. autoclass:: anilibria_api_types.codegen.methods.anime.AnimeMethod
   :members:
   :show-inheritance:

App
---

.. autoclass:: anilibria_api_types.codegen.methods.app.AppMethod
   :members:
   :show-inheritance:

Media
-----

.. autoclass:: anilibria_api_types.codegen.methods.media.MediaMethod
   :members:
   :show-inheritance:

Teams
-----

.. autoclass:: anilibria_api_types.codegen.methods.teams.TeamsMethod
   :members:
   :show-inheritance:
