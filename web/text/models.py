from django.db import models

from django.utils.timezone import now

from user_profile.models import Profile


class TextFile(models.Model):
    create_time = models.DateTimeField(default=now)
    file = models.FileField(upload_to="text_files")
    file_name = models.CharField(max_length=255, default="")
    request_type = models.IntegerField(default=0)
    ip = models.CharField(max_length=30, default="unknown")
    model_type = models.IntegerField(default=0)
    tmp_code = models.CharField(blank=True, null=True, max_length=512)
    ret = models.FileField(upload_to="results", blank=True, null=True)
    return_text = models.FileField(upload_to="return_files", blank=True, null=True)
    finish_flag = models.IntegerField(default=0)
    profile = models.ForeignKey(Profile, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.file.name

# Create your models here.
