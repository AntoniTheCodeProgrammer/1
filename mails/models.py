from django.db import models

# Create your models here.
class Campaign(models.Model):
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    date = models.DateField()
    sent = models.IntegerField()
    seen = models.IntegerField()
    replied = models.IntegerField()
    
    def __str__(self):
        return self.name
    