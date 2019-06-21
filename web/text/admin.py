from django.contrib import admin
from text.models import TextFile


class AccountAdmin(admin.ModelAdmin):
    fieldsets = [
        ('create_time', {'fields': ['create_time']}),
        ('file', {'fields': ['file']}),
        ('file_name', {'fields': ['file_name']}),
        ('request_type', {'fields': ['request_type']}),
        ('ip', {'fields': ['ip']}),
        ('model_type', {'fields': ['model_type']}),
        ('ret', {'fields': ['ret']}),
        ('return_text', {'fields': ['return_text']}),
        ('finish_flag', {'fields': ['finish_flag']}),
        ('profile', {'fields': ['profile']}),

    ]
    list_display = ('create_time', 'file', 'file_name', 'request_type', 'ip', 'model_type', 'ret', 'return_text', 'finish_flag', 'get_profile_email')

    def get_profile_email(self, obj):
        if obj.profile:
            return obj.profile.email
        return "unknown"
    get_profile_email.short_description = 'profile_email'
    get_profile_email.admin_order_field = 'profile__email'


admin.site.register(TextFile, AccountAdmin)
# Register your models here.
