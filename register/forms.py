from django.forms import ModelForm, DateTimeInput, Select, TextInput
from .models import Reception

class ReceptionForm(ModelForm):
    class Meta:
        model = Reception
        fields = ['doctor', 'datetime', 'patient']
        widgets = {'datetime': DateTimeInput(attrs={'class': 'datepicker form-control'}),
                   'doctor': Select(attrs={'class': 'form-control'}),
                   'patient': TextInput(attrs={'class': 'form-control'}),
                   }