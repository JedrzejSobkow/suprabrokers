from django import forms
from .models import Contact

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = '__all__'
        
class CSVImportForm(forms.Form):
    csv_file = forms.FileField(label="Choose a CSV file")