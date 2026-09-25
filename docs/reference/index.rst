API reference
=============

This section documents every public part of ``anilibria-api-client``: the
high-level client, the raw HTTP transport, the generated endpoint methods,
the Pydantic response models, exceptions, and the download/pagination
helpers.

.. grid:: 1 2 2 2
   :gutter: 3

   .. grid-item-card:: Client
      :link: client
      :link-type: doc

      The ``AsyncAnilibriaAPI`` high-level client and the raw ``API``
      transport layer.

   .. grid-item-card:: Methods
      :link: methods
      :link-type: doc

      Endpoint methods generated from the OpenAPI schema.

   .. grid-item-card:: Models
      :link: models
      :link-type: doc

      Pydantic response models generated from OpenAPI.

   .. grid-item-card:: Responses
      :link: responses
      :link-type: doc

      The public re-export of the generated response models.

   .. grid-item-card:: Exceptions
      :link: exceptions
      :link-type: doc

      Exception types raised by the client.

   .. grid-item-card:: Helpers
      :link: helpers
      :link-type: doc

      Authentication, pagination, and download helpers.

.. toctree::
   :hidden:

   client
   methods
   models
   responses
   exceptions
   helpers
