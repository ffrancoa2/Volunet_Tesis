from django import forms
from .models import Help
import datetime

class HelpForm(forms.ModelForm):
    class Meta:
        model = Help
        fields = [
            'title',
            'description',
            'category',
            'location',
            'lat',
            'lng',
            'date_start',
            'date_end',
            'account_number',
            'amount',
        ]

        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el título de la ayuda'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4
            }),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Seleccione en el mapa para agregar coordenadas'
            }),
            'lat': forms.HiddenInput(),
            'lng': forms.HiddenInput(),
            'date_start': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'min': datetime.date.today().isoformat()
            }),
            'date_end': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'min': (datetime.date.today() + datetime.timedelta(days=1)).isoformat()
            }),
            'account_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Número de cuenta bancaria',
                
            }),
            'amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Monto solicitado'
            }),
        }

        labels = {
            'title': 'Título',
            'description': 'Descripción',
            'category': 'Categoría',
            'location': 'Ubicación',
            'date_start': 'Fecha de inicio',
            'date_end': 'Fecha de fin',
            'account_number': 'Número de cuenta',
            'amount': 'Monto solicitado',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # La ubicación no será requerida por defecto
        self.fields['location'].required = False

    def clean(self):
        cleaned_data = super().clean()
        category = cleaned_data.get('category')
        account_number = cleaned_data.get('account_number')
        amount = cleaned_data.get('amount')
        start = cleaned_data.get('date_start')
        end = cleaned_data.get('date_end')

        category_normalized = (category or "").lower().strip()

        # 💰 Validación especial para "Dinero"
        if category_normalized == 'dinero':
            if not account_number:
                self.add_error('account_number', 'Debe ingresar el número de cuenta.')
            else:
                if not account_number.isdigit():
                    self.add_error('account_number', 'El número de cuenta solo debe contener dígitos.')
                elif len(account_number) < 10 or len(account_number) > 20:
                    self.add_error('account_number', 'El número de cuenta debe tener entre 10 y 20 dígitos.')

            if not amount:
                self.add_error('amount', 'Debe ingresar el monto solicitado.')

            # Se limpia la ubicación (no se requiere en dinero)
            cleaned_data['location'] = None
            cleaned_data['lat'] = None
            cleaned_data['lng'] = None

        else:
            # Categorías normales: se requiere ubicación
            if not cleaned_data.get('location'):
                self.add_error('location', 'Debe ingresar una ubicación o seleccionarla en el mapa.')

        # 🗓️ Validación de fechas
        if not start or not end:
            self.add_error('date_end', 'Debe ingresar la fecha de inicio y fin.')
        elif start > end:
            self.add_error('date_end', 'La fecha de fin debe ser posterior a la de inicio.')

        return cleaned_data
