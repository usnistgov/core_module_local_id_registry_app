core_module_local_id_registry_app
=================================

Local ID registry module

Quick start
===========

1. Add "core_module_local_id_registry_app" to your INSTALLED_APPS setting
-------------------------------------------------------------------------

.. code:: python

    INSTALLED_APPS = [
      ...
      'core_module_local_id_registry_app',
    ]

2. Include the core_module_local_id_registry_app URLconf in your project urls.py
--------------------------------------------------------------------------------

.. code:: python

    url(r'^', include('core_module_local_id_registry_app.urls')),