from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls.base import reverse
from base_classes.models import Base
from profiles.models import HealthProfile, PatientProfile

class Appointment(Base):
    date = models.DateField()
    previous = models.OneToOneField('self', blank=True, null=True, on_delete=models.CASCADE)
    health = models.ForeignKey(HealthProfile, on_delete=models.CASCADE)
    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE)
    mean = models.DecimalField(max_digits=2, decimal_places=1, validators=[MinValueValidator(1), MaxValueValidator(5)])
    quantitative0 = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    quantitative1 = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    quantitative2 = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    quantitative3 = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    quantitative4 = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    note = models.CharField(max_length=1024, blank=True)

    class Meta:
        ordering = ['-pk']
        verbose_name = 'Consulta'
        verbose_name_plural = 'Consultas'

    def get_absolute_url(self):
        return reverse('list_appointment')
    
    def save(self, *args, **kwargs):
        appointments = Appointment.objects.filter(status=True, patient=self.patient)
        if appointments:
            self.previous = appointments.order_by('-date').first()

        slug = str(self.patient)+' '+str(self.health)+' '+str(self.date)
        super().save(field=slug, *args, **kwargs)

    def __str__(self):
        return self.slug
