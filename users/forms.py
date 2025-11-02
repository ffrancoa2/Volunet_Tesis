from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
import datetime

User = get_user_model()  

class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'name', 'last_name', 'sex', 'date', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de usuario'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Correo electrónico', 'required': True}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellido'}),
            'sex': forms.Select(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'Fecha de nacimiento', 'type': 'date', 'max': datetime.date.today().isoformat()}),
        }

    # 🔹 Ahora está dentro de la clase
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)


        self.fields['password1'].label = 'Contraseña'
        self.fields['password2'].label = 'Confirmar contraseña'

        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Contraseña'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirmar contraseña'
        })

    # 🔹 Validación de email único
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Este correo electrónico ya está en uso.")
        return email

    # 🔹 Validación de edad y fecha
    def clean_date(self):
        date = self.cleaned_data.get('date')
        if not date:
            return date

        today = datetime.date.today()

        if date > today:
            raise forms.ValidationError("La fecha de nacimiento no puede ser en el futuro.")

        age = today.year - date.year - ((today.month, today.day) < (date.month, date.day))
        if age < 12:
            raise forms.ValidationError("Debes tener al menos 12 años para registrarte.")
        return date


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        label='Nombre de usuario',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': ''
        })
    )
    password = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': ''
        })
    )
