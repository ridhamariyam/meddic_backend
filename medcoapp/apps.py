from django.apps import AppConfig


class MedcoappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'medcoapp'
    
    def ready(self):
        import medcoapp.signal
