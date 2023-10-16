from django.db import models

# Create your models here.
class user(models.Model):
    user_id = models.IntegerField(blank=True, null=False)
    user_name = models.CharField(max_length=15, blank=True, null=False)

class Meta:
    managed = True
    db_table = 'user'
