from django.core.management.base import BaseCommand
from django.utils import timezone
from shop.models import Cart

class Command(BaseCommand):
  help = 'Remove expired cart items'

  def handle(self, *args, **options):
    expiration_time = timezone.now() - timezone.timedelta(hours=24)
    Cart.objects.filter(created__lt=expiration_time).delete()
    self.stdout.write(self.style.SUCCESS('Expired cart items removed'))

    