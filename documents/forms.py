from django.forms import ModelForm
from .models import DocumentType

# Create the form class.
class DocumentTypeForm(ModelForm):
    class Meta:
        model = DocumentType
        fields = ['name', 'description']
        labels = {'descrição': 'Descrição'}
