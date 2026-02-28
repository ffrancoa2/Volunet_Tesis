from django import forms
from .models import Help

class HelpForm(forms.ModelForm):
    class Meta:
        model = Help
        fields = [
            'title', 'description', 'category', 'location',
            'date_start', 'date_end', 'contact_number', 'bank_account',
            'amount', 'evidence_pdf', 'evidence_image', 'dni_copy'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'date_start': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'date_end': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'contact_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 0991234567'}),
            'bank_account': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 0123456789'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Monto solicitado', 'step': '0.01'}),
            'evidence_pdf': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'evidence_image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'dni_copy': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        start = cleaned_data.get("date_start")
        end = cleaned_data.get("date_end")
        if start and end and end < start:
            self.add_error("date_end", "La fecha de fin no puede ser anterior a la fecha de inicio.")
        return cleaned_data
