from django import forms
from .models import UserToken, Organization
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Organization, Service


class TokenForm(forms.ModelForm):
    class Meta:
        model = UserToken
        fields = ["service_type", "organization"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['organization'].queryset = Organization.objects.all()



class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "password1", "password2"]




class OrganizationForm(forms.ModelForm):
    class Meta:
        model = Organization
        fields = ['name', 'org_type']



class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['organization', 'name', 'start_time', 'end_time']
        widgets = {
            'start_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'end_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # All organizations can have multiple services now
        self.fields['organization'].queryset = Organization.objects.all()