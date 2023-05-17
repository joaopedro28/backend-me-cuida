from django.db import models
from base_classes.models import Base
from profiles.models import PatientProfile

class Activity(Base):
    SHIFTS = [('mat','Matutino'), ('ves','Vespertino'), ('not','Noturno'), ('mad','Madrugada')]
    ACT = [('ref','Refeição'), ('fis','Atividade Física'), ('gli','Medição de Glicemia Capilar'), ('pre','Medição de Pressão Arterial'), ('med','Uso de Medicamento')]
    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE)
    date = models.DateField()
    shift = models.CharField(max_length=3, choices=SHIFTS)
    activitytype = models.CharField(max_length=3, choices=ACT)
    picture = models.FileField(blank=True, null=True)
    description = models.CharField(max_length=500, blank=True, null=True)
    value = models.IntegerField(blank=True, null=True)

    class Meta:
        ordering = ['-date']
        verbose_name = 'Atividade'
        verbose_name_plural = 'Atividades'

    def save(self, *args, **kwargs):
        slug = str(self.patient)+' '+str(self.activitytype)+' '+self.date.strftime('%d-%m-%Y')
        super().save(field=slug, *args, **kwargs)

    def __str__(self):
        return str(self.activitytype)+" - "+self.date.strftime('%d-%m-%Y')+" - "+str(self.shift)
