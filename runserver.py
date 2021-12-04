from django.core.management import setup_environ, call_command
import settings

setup_environ(settings)
call_command('runserver')
