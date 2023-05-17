from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from documents.models import DocumentType
from .models import HealthProfile, PatientProfile

UserModel = get_user_model()

class ProfileAbstractForm(forms.ModelForm):
    name = forms.CharField(label='Nome Completo')
    cpf = forms.CharField(label='CPF', max_length=14)
    username = forms.CharField(label='Nome de Usuário', max_length=150)
    email = forms.EmailField(label='E-Mail')


# Profissionais de Saúde
class HealthAbstractForm(ProfileAbstractForm):
    specialty = forms.ChoiceField(label='Área de Atuação', choices=HealthProfile.SPEC)
    documenttype = forms.ModelChoiceField(label='Documento', queryset=DocumentType.objects.filter(status=True), empty_label='Selecionar')
    documentnumber = forms.CharField(label='')

    class Meta:
        model = HealthProfile
        fields = ['name', 'cpf', 'specialty', 'admin', 'documenttype', 'documentnumber']

class HealthUpdateForm(HealthAbstractForm):
    def save(self):
        self.user = self.instance.user
        self.user.username = self.cleaned_data['username']
        self.user.email = self.cleaned_data['email']

        self.user.save()
        return super().save()

class HealthCreateForm(HealthAbstractForm):
    password = forms.CharField(label='Senha', widget=forms.PasswordInput())
    confirm = forms.CharField(label='Confirmar Senha', widget=forms.PasswordInput())

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm = cleaned_data.get("confirm")

        if password != confirm:
            self.add_error('confirm', "A confirmação de senha não corresponde!")

        validate_password(password)
        return cleaned_data

    def save(self):
        self.user = UserModel()
        self.user.username = self.cleaned_data['username']
        self.user.email = self.cleaned_data['email']
        self.user.set_password(self.cleaned_data['password'])

        self.instance.user = self.user
        self.user.save()
        return super().save()


# Pacientes
class PatientAbstractForm(ProfileAbstractForm):
    health = forms.ModelMultipleChoiceField(label='Profissional de Saúde', queryset=HealthProfile.objects.filter(status=True))

    class Meta:
        model = PatientProfile
        fields = ['name', 'cpf', 'health']

class PatientUpdateForm(PatientAbstractForm):
    def save(self):
        self.user = self.instance.user
        self.user.username = self.cleaned_data['username']
        self.user.email = self.cleaned_data['email']

        self.user.save()
        return super().save()

class PatientCreateForm(PatientAbstractForm):
    password = forms.CharField(label='Senha', widget=forms.PasswordInput())
    confirm = forms.CharField(label='Confirmar Senha', widget=forms.PasswordInput())

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm = cleaned_data.get("confirm")

        if password != confirm:
            self.add_error('confirm', "A confirmação de senha não corresponde!")

        validate_password(password)
        return cleaned_data

    def save(self):
        self.user = UserModel()
        self.user.username = self.cleaned_data['username']
        self.user.email = self.cleaned_data['email']
        self.user.set_password(self.cleaned_data['password'])

        self.instance.user = self.user
        self.user.save()
        return super().save()
