from django.apps import AppConfig


class PollsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'polls'


class UsersConfig(AppConfig):
    name = 'polls'

    def ready(self):
        pass
