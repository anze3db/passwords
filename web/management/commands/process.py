from django.core.management.base import BaseCommand, CommandError
from web.models import Password
from django.db import transaction
#from web.models import PasswordUnique


class Command(BaseCommand):
    args = ''
    help = 'Processes passwords in queue'

    def handle(self, *args, **options):
        
        transaction.enter_transaction_management()
        transaction.managed(True)
        
        unprocessed = Password.objects.all().filter(processed = False)[:1000]
        for p in unprocessed:
            p.process_unique()
            p.save()
            
        transaction.commit()
        
        