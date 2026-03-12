from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Application


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=50, required=True)
    last_name = forms.CharField(max_length=50, required=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

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
            'date_applied': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 4}),
            'company_name': forms.TextInput(attrs={'placeholder': 'e.g. Google, Amazon'}),
            'position_title': forms.TextInput(attrs={'placeholder': 'e.g. Software Engineer Intern'}),
            'location': forms.TextInput(attrs={'placeholder': 'e.g. San Francisco, CA'}),
            'job_url': forms.URLInput(attrs={'placeholder': 'https://...'}),
            'recruiter_name': forms.TextInput(attrs={'placeholder': 'Recruiter full name'}),
            'recruiter_email': forms.EmailInput(attrs={'placeholder': 'recruiter@company.com'}),
            'salary_range': forms.TextInput(attrs={'placeholder': 'e.g. $80,000 - $100,000'}),
        }
