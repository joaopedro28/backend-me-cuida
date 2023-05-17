from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.urls import reverse
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from base_classes.models import Base
from documents.models import DocumentType

UserModel = get_user_model()

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

class Profile(Base):
    user = models.OneToOneField(UserModel, null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=500)
    cpf = models.CharField(max_length=14)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        super().save(field=self.name, *args, **kwargs)

class HealthProfile(Profile):
    SPEC = [('enf','Enfermeiro'), ('med','Médico'), ('psi','Psicólogo'), ('edf','Educação Física')]
    specialty = models.CharField(max_length=3, choices=SPEC)
    documentnumber = models.CharField(max_length=50)
    documenttype = models.ForeignKey(DocumentType, on_delete=models.CASCADE, related_name='health')
    admin = models.BooleanField(default=False)

    class Meta:
        ordering = ['-pk']
        verbose_name = 'Profissional da Saúde'
        verbose_name_plural = 'Profissionais da Saúde'

    def get_absolute_url(self):
        return reverse('list_health')

    def __str__(self):
        return self.name+" ("+self.get_specialty_display()+")"

class PatientProfile(Profile):
    health = models.ManyToManyField(HealthProfile)

    class Meta:
        ordering = ['-pk']
        verbose_name = 'Paciente'
        verbose_name_plural = 'Pacientes'

    def get_absolute_url(self):
        return reverse('list_patient')

    def __str__(self):
        return self.name
