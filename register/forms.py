from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User, ProfileImage
from django.utils.translation import gettext_lazy as _


class RoleSelectionForm(forms.Form):
    role = forms.ChoiceField(
        choices=User.ROLE_CHOICE,
        widget=forms.RadioSelect
    )


class CustomerRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    phone_number = forms.CharField(required=True)

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'phone_number',  'password1', 'password2']


class VendorRegisterForm(CustomerRegisterForm):
    company_name = forms.CharField(required=True)
    vendor_license = forms.ImageField(required=True)

    class Meta(CustomerRegisterForm.Meta):
        fields = CustomerRegisterForm.Meta.fields + ['company_name', 'vendor_license']

class ProfileImageForm(forms.ModelForm):
    class Meta:
        model = ProfileImage
        fields = ['image']
        


class CustomLoginForm(AuthenticationForm):
    username = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))