from django.db import models
import uuid
from django.contrib.auth.models import User

# Create your models here.


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    customer_xid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    
    def __str__(self):
        return str(self.customer_xid)

class Deposits(models.Model):
    deposited_by = models.ForeignKey(UserProfile, related_name='deposited_by', on_delete=models.CASCADE, null=True,
                                     blank=True)
    amount = models.IntegerField(default=0)
    reference_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    deposited_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return str(self.reference_id)

class Withdrawals(models.Model):
    withdrawn_by = models.ForeignKey(UserProfile, related_name='withdrawn_by', on_delete=models.CASCADE, null=True,
                                     blank=True)
    amount = models.IntegerField(default=0)
    reference_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    withdrawn_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return str(self.reference_id)

class Wallets(models.Model):
    ENABLED = 'EN'
    DISABLED = 'DS'
    CHOICES = (
        (ENABLED, "enabled"),
        (DISABLED, "disabled"),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owned_by = models.ForeignKey(UserProfile, related_name='owned_by', on_delete=models.CASCADE)
    withdrawn_reference_id = models.ForeignKey(Withdrawals, related_name='withdrawals', on_delete=models.CASCADE, null=True, blank=True)
    deposited_reference_id = models.ForeignKey(Deposits, related_name='Deposits', on_delete=models.CASCADE, null=True, blank=True)
    status = models.CharField(max_length=2, choices=CHOICES, default=ENABLED)
    balance = models.IntegerField(default=0)
    enabled_at = models.DateTimeField(auto_now=False)
    disabled_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return str(self.id)




