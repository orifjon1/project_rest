from django.db import models


class Help(models.Model):
   shior = models.CharField(max_length=35, blank=True)
   birth_date = models.DateField(null=True, blank=True)
   phone_number = models.CharField(max_length=12, blank=True)

   class Meta:
      abstract = True
