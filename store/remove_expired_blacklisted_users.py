from django.core.management.base import BaseCommand
from .models import BlacklistedUser
from django.utils import timezone


class Command(BaseCommand):
  help = 'Remove expired blacklisted users'

  def handle(self, *args, **options):
    expired_blacklisted_users = BlacklistedUser.objects.filter(expires_at__lt=timezone.now())
    expired_blacklisted_users.delete()
    self.stdout.write(self.style.SUCCESS('Expired blacklisted users removed'))
    return super().handle(*args, **options)
