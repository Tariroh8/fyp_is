from django import forms
from django.forms import ModelForm
from backend.models import Farmer, Case
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model


# farmer registration form // create a user and feeds into the Farmer model
class FarmerRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = Farmer
        fields = ['name', 'email', 'species_owned', 'district', 'ward', 'password']
        
    def save(self, commit=True):
        farmer = super().save(commit=False)
        if commit:
            user = User.objects.create_user(
                username=self.cleaned_data['email'],
                email=self.cleaned_data['email'],
                password=self.cleaned_data['password']
            )
            farmer.user = user
            farmer.save()
            self.save_m2m()  # Save many-to-many relationships
        return farmer
    

# farmer login form
class FarmerLoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    


# farmer report case form
class CaseForm(forms.ModelForm):
    

        
    class Meta:
        model = Case
        fields = ('spece', 'symptoms', 'district', 'ward', 'farmer1', 'lat', 'long', 'description')
        
