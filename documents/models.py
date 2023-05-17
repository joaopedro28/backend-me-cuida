from django.db import models
from django.urls import reverse
from base_classes.models import Base

class DocumentType(Base):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=500, blank=True)

    class Meta:
        ordering = ['-pk']
        verbose_name = 'Tipo de Documento'
        verbose_name_plural = 'Tipos de Documento'

    def save(self, *args, **kwargs):
        super().save(field=self.name, *args, **kwargs)

    def get_absolute_url(self):
        return reverse('list_documenttype')

    def __str__(self):
        return self.name
