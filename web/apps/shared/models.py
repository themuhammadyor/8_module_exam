from django.db import models

class AbstractBaseModel(models.Model):
    creat_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
