from django.contrib import admin
from user_profile.models import Profile


class AccountAdmin(admin.ModelAdmin):
    fieldsets = [
        ('email', {'fields': ['email']}),
        ('files_num', {'fields': ['files_num']}),
        ('finished_num', {'fields': ['finished_num']}),

    ]
    list_display = ('email', 'files_num', 'finished_num')


admin.site.register(Profile, AccountAdmin)
# Register your models here.
