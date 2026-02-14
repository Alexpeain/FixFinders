from django.apps import AppConfig

class ProvidersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'providers'

    # If you need to import signals or other things, do it inside the ready() method
    # but NEVER import models at the top level here.
