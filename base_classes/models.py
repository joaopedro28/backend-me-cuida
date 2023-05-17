from django.db import models
from django.utils.text import slugify

class Base(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True)
    status = models.BooleanField(default=True)

    class Meta:
        abstract = True

    def save(self, field, *args, **kwargs):
        super().save(*args, **kwargs)

        if not self.slug:
            slug=slugify(field)

            slugCounter = type(self).objects.filter(slug__contains = slug.strip()).count()
            if slugCounter > 0:
                slug = slug+"-"+str(slugCounter)
            
            self.slug = slug.strip()
            self.save()
