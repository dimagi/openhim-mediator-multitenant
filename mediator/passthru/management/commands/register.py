from django.conf import settings
from django.core.management.base import BaseCommand

from openhim_mediator_utils.main import Main


class Command(BaseCommand):
    help = 'Register mediator with OpenHIM'

    def handle(self, *args, **options):
        utils = Main(options=settings.OPENHIM_OPTIONS, conf=settings.MEDIATOR_CONF)
        if settings.OPENHIM_OPTIONS['register']:
            utils.register_mediator()
            if settings.OPENHIM_OPTIONS['heartbeat']:
                utils.activate_heartbeat()
