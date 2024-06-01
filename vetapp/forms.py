from django import forms
from django.forms import ModelForm
from backend.models import Farmer, Case, Vet_officer, Symptom, Spece
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model


# farmer registration form // create a user and feeds into the Farmer model
class VetRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = Vet_officer
        fields = ['name', 'email', 'district','password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")

    def save(self, commit=True):
        vet_officer = super().save(commit=False)
        if commit:
            user = User.objects.create_user(
                username=self.cleaned_data['email'],
                email=self.cleaned_data['email'],
                password=self.cleaned_data['password']
            )
            vet_officer.user = user
            vet_officer.save()
            self.save_m2m()  # Save many-to-many relationships
        return vet_officer
    
    
# Vet login form
class VetLoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    
class SymptomForm(forms.ModelForm):
    class Meta:
        model = Symptom
        fields = ['name', 'shona_name', 'ndebele_name', 'spece', 'affected_part', 'image', 'general_description', 'shona_description', 'ndebele_description', 'veterinarian_description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'shona_name': forms.TextInput(attrs={'class': 'form-control'}),
            'ndebele_name': forms.TextInput(attrs={'class': 'form-control'}),
            'spece': forms.Select(attrs={'class': 'form-control'}),
            'affected_part': forms.TextInput(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control-file'}),
            'general_description': forms.Textarea(attrs={'class': 'form-control'}),
            'shona_description': forms.Textarea(attrs={'class': 'form-control'}),
            'ndebele_description': forms.Textarea(attrs={'class': 'form-control'}),
            'veterinarian_description': forms.Textarea(attrs={'class': 'form-control'}),
        }
