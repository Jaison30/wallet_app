from django.contrib import admin

from .models import *

# Register your models here.

admin.site.register(UserProfile)
admin.site.register(Wallets)
admin.site.register(Deposits)
admin.site.register(Withdrawals)

