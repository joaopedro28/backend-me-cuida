from django.contrib import admin
from .models import DocumentType

class DocumentTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'status')

admin.site.register(DocumentType, DocumentTypeAdmin)
