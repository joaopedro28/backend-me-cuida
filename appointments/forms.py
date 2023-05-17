from django import forms
from datetime import date
from profiles.models import HealthProfile, PatientProfile
from .models import Appointment

# Form para registro de consultas
class AppointmentForm(forms.ModelForm):
    STARS = [(1,'1'), (2,'2'), (3,'3'), (4,'4'), (5,'5')]
    date = forms.DateField(label='Data:', initial=date.today())
    previous = forms.ModelChoiceField(label='Consulta Anterior', queryset=Appointment.objects.filter(status=True), widget=forms.HiddenInput())
    health = forms.ModelChoiceField(label='Profissional de Saúde', queryset=HealthProfile.objects.filter(status=True))
    patient = forms.ModelChoiceField(label='Paciente', queryset=PatientProfile.objects.filter(status=True))
    mean = forms.IntegerField(label='Média', widget=forms.HiddenInput())
    quantitative0 = forms.ChoiceField(label='Pergunta 1:', choices=STARS)
    quantitative1 = forms.ChoiceField(label='Pergunta 2:', choices=STARS)
    quantitative2 = forms.ChoiceField(label='Pergunta 3:', choices=STARS)
    quantitative3 = forms.ChoiceField(label='Pergunta 4:', choices=STARS)
    quantitative4 = forms.ChoiceField(label='Pergunta 5:', choices=STARS)
    note = forms.CharField(label='Observações:', max_length=500, widget=forms.Textarea)

    class Meta:
        model = Appointment
        fields = ['date', 'previous', 'patient', 'quantitative0', 'quantitative1', 'quantitative2', 'quantitative3', 'quantitative4', 'note']

    def clean(self):
        cleaned_data = super().clean()
        if not cleaned_data['previous']:
            cleaned_data['previous'] = Appointment.objects.filter(patient=cleaned_data.get("patient")).order_by("-date").first()
        if not cleaned_data['mean']:
            mean = round(float(cleaned_data.get("quantitative0")+cleaned_data.get("quantitative1")+cleaned_data.get("quantitative2")+cleaned_data.get("quantitative3")+cleaned_data.get("quantitative4"))/5, 1)
            cleaned_data['mean'] = mean

        return cleaned_data
