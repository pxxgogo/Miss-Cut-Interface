from django.contrib import admin
from user_profile.models import Profile


class AccountAdmin(admin.ModelAdmin):
    fieldsets = [
        ('email', {'fields': ['email']}),
        ('files_num', {'fields': ['files_num']}),
        ('finished_check_num', {'fields': ['finished_check_num']}),
        ('finished_sending_flag', {'fields': ['finished_sending_flag']}),

    ]
    list_display = ('email', 'files_num', 'finished_sending_flag', 'finished_check_num')


admin.site.register(Profile, AccountAdmin)
# Register your models here.
