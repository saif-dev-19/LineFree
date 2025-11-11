from django import forms
from .models import UserToken, Organization, Service
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class TokenForm(forms.ModelForm):
    organization = forms.ModelChoiceField(
        queryset=Organization.objects.all(),
        empty_label="Select an organization",
        widget=forms.Select(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-colors',
            'id': 'id_organization'
        })
    )
    service_type = forms.ModelChoiceField(
        queryset=Service.objects.none(),
        empty_label="Select a service",
        widget=forms.Select(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-colors',
            'id': 'id_service_type'
        })
    )

    class Meta:
        model = UserToken
        fields = ["organization", "service_type"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['organization'].queryset = Organization.objects.all()
        
        # If organization is provided, filter services
        if 'organization' in self.data:
            try:
                organization_id = int(self.data.get('organization'))
                self.fields['service_type'].queryset = Service.objects.filter(
                    organization_id=organization_id
                ).order_by('name')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            # If editing existing token, show services for that organization
            self.fields['service_type'].queryset = self.instance.organization.services.all()

    def clean(self):
        cleaned_data = super().clean()
        organization = cleaned_data.get('organization')
        service_type = cleaned_data.get('service_type')
        
        if organization and service_type:
            # Server-side validation: ensure service belongs to selected organization
            if service_type.organization != organization:
                raise forms.ValidationError(
                    "The selected service does not belong to the selected organization."
                )
        
        return cleaned_data



class RegisterForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-colors',
            'placeholder': 'Username'
        })
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-colors',
            'placeholder': 'Password'
        })
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-colors',
            'placeholder': 'Confirm Password'
        })
    )

    class Meta:
        model = User
        fields = ["username", "password1", "password2"]




class OrganizationForm(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-500 outline-none transition-colors',
            'placeholder': 'Organization Name'
        })
    )
    org_type = forms.ChoiceField(
        choices=Organization.ORG_TYPES,
        widget=forms.Select(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-500 outline-none transition-colors'
        })
    )

    class Meta:
        model = Organization
        fields = ['name', 'org_type']



class ServiceForm(forms.ModelForm):
    organization = forms.ModelChoiceField(
        queryset=Organization.objects.all(),
        empty_label="Select an organization",
        widget=forms.Select(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-colors'
        })
    )
    name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-colors',
            'placeholder': 'Service Name'
        })
    )
    start_time = forms.TimeField(
        widget=forms.TimeInput(attrs={
            'type': 'time',
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-colors'
        })
    )
    end_time = forms.TimeField(
        widget=forms.TimeInput(attrs={
            'type': 'time',
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-colors'
        })
    )

    class Meta:
        model = Service
        fields = ['organization', 'name', 'start_time', 'end_time']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['organization'].queryset = Organization.objects.all()