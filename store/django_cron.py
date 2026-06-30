from django_cron import CronJobBase, Schedule
from .models import BlacklistedUser
from django.utils import timezone


class RemoveExpiredBlacklistedUser(CronJobBase):
  RUN_AT_TIMES = ['00:00']

  schedule = Schedule(run_at_times=RUN_AT_TIMES)
  code = 'store.remove_expired_blacklisted_users'

  def do(self):
    expired_blacklisted_user = BlacklistedUser.objects.filter(expires_at_lt=timezone.now())
    expired_blacklisted_user.delete()
    