from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
import datetime

User = get_user_model()

class UserForm(forms.ModelForm):
    password1 = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña'}),
        required=True
    )
    password2 = forms.CharField(
        label='Confirmar contraseña',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirmar contraseña'}),
        required=True
    )

    class Meta:
        model = User
        fields = [
            'email', 'name', 'last_name', 'sex', 'date',
            'phone_number', 'dni', 'profile_image'
        ]
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Correo electrónico', 'required': True}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombres'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellidos'}),
            'sex': forms.Select(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'max': datetime.date.today().isoformat()}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Número de teléfono'}),
            'dni': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Cédula o DNI'}),
            'profile_image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

    def clean_password2(self):
        p1 = self.cleaned_data.get('password1')
        p2 = self.cleaned_data.get('password2')
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError("Las contraseñas no coinciden.")
        return p2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Este correo electrónico ya está registrado.")
        return email

    def clean_date(self):
        date = self.cleaned_data.get('date')
        if not date:
            return date
        today = datetime.date.today()
        if date > today:
            raise forms.ValidationError("La fecha de nacimiento no puede ser en el futuro.")
        age = today.year - date.year - ((today.month, today.day) < (date.month, date.day))
        if age < 18:
            raise forms.ValidationError("Debes tener al menos 12 años para registrarte.")
        return date
    
    def clean_dni(self):
        dni = self.cleaned_data.get('dni')

        if not dni or not dni.isdigit() or len(dni) != 10:
            raise forms.ValidationError("La cédula debe tener exactamente 10 dígitos numéricos.")

        provincia = int(dni[:2])
        if provincia < 1 or provincia > 24:
            raise forms.ValidationError("El código de provincia no es válido (01-24).")

        tercer_digito = int(dni[2])
        if tercer_digito >= 6:
            raise forms.ValidationError("El tercer dígito no corresponde a una persona natural.")

        coeficientes = [2, 1, 2, 1, 2, 1, 2, 1, 2]
        verificador = int(dni[9])
        total = 0

        for i in range(9):
            valor = int(dni[i]) * coeficientes[i]
            if valor >= 10:
                valor -= 9
            total += valor

        digito_calculado = 10 - (total % 10) if total % 10 != 0 else 0

        if digito_calculado != verificador:
            raise forms.ValidationError("La cédula ingresada no es válida.")

        return dni


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(
        label='Correo electrónico',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Correo electrónico'
        })
    )

class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'email', 'name', 'last_name', 'sex', 'date',
            'phone_number', 'dni', 'profile_image'
        ]
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'sex': forms.Select(attrs={'class': 'form-control'}),
            # 🔹 Formato correcto para que se muestre en el input type="date"
            'date': forms.DateInput(
                attrs={'class': 'form-control', 'type': 'date'},
                format='%Y-%m-%d'
            ),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'dni': forms.TextInput(attrs={'class': 'form-control'}),
            'profile_image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        # 🔹 Si hay una fecha guardada, la mostramos en formato correcto
        if self.instance and self.instance.date:
            self.fields['date'].initial = self.instance.date.strftime('%Y-%m-%d')
