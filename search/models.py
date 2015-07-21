from django.db import models


# Create your models here.
class Name(models.Model):
    module_name = models.CharField(max_length=255)
    name = models.CharField(max_length=63)
    is_from_all = models.BooleanField(default=False)
