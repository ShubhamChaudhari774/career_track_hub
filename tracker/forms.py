from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Application


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'class': 'form-input', 'placeholder': 'you@email.com'
    }))
    first_name = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'class': 'form-input', 'placeholder': 'First Name'
    }))
    last_name = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'class': 'form-input', 'placeholder': 'Last Name'
    }))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if 'class' not in field.widget.attrs:
                field.widget.attrs['class'] = 'form-input'
        self.fields['username'].widget.attrs['placeholder'] = 'Choose a username'
        self.fields['password1'].widget.attrs['placeholder'] = 'Create a password'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm password'

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        exclude = ['user', 'created_at', 'updated_at']
        widgets = {
            'company_name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g. Google'}),
            'position_title': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g. Software Engineer Intern'}),
            'job_type': forms.Select(attrs={'class': 'form-input'}),
            'location': forms.Select(attrs={'class': 'form-input'}),
            'job_location_city': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g. New York, NY'}),
            'date_applied': forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
            'application_deadline': forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
            'status': forms.Select(attrs={'class': 'form-input'}),
            'priority': forms.Select(attrs={'class': 'form-input'}),
            'job_posting_url': forms.URLInput(attrs={'class': 'form-input', 'placeholder': 'https://...'}),
            'salary_range': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g. $80,000 - $100,000'}),
            'recruiter_name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Recruiter full name'}),
            'recruiter_email': forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'recruiter@company.com'}),
            'recruiter_phone': forms.TextInput(attrs={'class': 'form-input', 'placeholder': '+1 (555) 000-0000'}),
            'next_interview_date': forms.DateTimeInput(attrs={'class': 'form-input', 'type': 'datetime-local'}),
            'notes': forms.Textarea(attrs={'class': 'form-input', 'rows': 4, 'placeholder': 'Interview notes, follow-up reminders, key contacts...'}),
        }


class SearchForm(forms.Form):
    q = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Search company, position, status...',
            'autofocus': True,
        })
    )
    status = forms.ChoiceField(
        required=False,
        choices=[('', 'All Statuses')] + Application.STATUS_CHOICES,
        widget=forms.Select(attrs={'class': 'form-input'})
    )
    job_type = forms.ChoiceField(
        required=False,
        choices=[('', 'All Types')] + Application.JOB_TYPE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-input'})
    )
    location = forms.ChoiceField(
        required=False,
        choices=[('', 'All Locations')] + Application.LOCATION_CHOICES,
        widget=forms.Select(attrs={'class': 'form-input'})
    )
