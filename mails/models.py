from django.db import models
from django.template.defaultfilters import slugify

# Create your models here.
class Campaign(models.Model):
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    date = models.DateField()
    sent = models.IntegerField()
    seen = models.IntegerField()
    replied = models.IntegerField()
    slug = models.SlugField(default="", null=False)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name.replace(' ', '-'))  # zamienia spacje na "_"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    