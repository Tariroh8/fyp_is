from django.shortcuts import render, redirect, get_object_or_404
from .forms import FarmerRegistrationForm, FarmerLoginForm, CaseForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from backend.models import District, Case, Symptom
from django.core.serializers import serialize
from django.contrib.gis.serializers import geojson
from django.http import  HttpResponseRedirect
from django.contrib import messages
from backend.models import Farmer
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.db.models import Q



def register(request):
    submitted = False
    if request.method == "POST":
        form = FarmerRegistrationForm(request.POST)
        if form.is_valid():
            farmer = form.save()
            submitted = True
            return HttpResponseRedirect('/register?submitted=True')
    else:
        form = FarmerRegistrationForm()
        if 'submitted' in request.GET:
            submitted = True
    
    return render(request, 'farmer_register.html', {'form': form, 'submitted': submitted})

def farmer_login(request):
    if request.method == 'POST':
        form = FarmerLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('farm_home')
            else:
                form.add_error(None, 'Invalid email or password.')
    else:
        form = FarmerLoginForm()
    
    return render(request, 'farmer_login.html', {'form': form})

def farmer_logout(request):
    logout(request)
    return redirect('login') 


@login_required(login_url='login')
def report_case(request):
    if request.method == 'POST':
        form = CaseForm(request.POST)
        if form.is_valid():
            form.save()
            district = form.cleaned_data.get('district')  # Assuming 'district' is a field in the form
            
            # Send alert to users in the district with the appropriate tag
            farmers_in_district = Farmer.objects.filter(district=district)
            for farmer in farmers_in_district:
                message = 'A new report has been submitted in your district.'
                messages.add_message(request, messages.INFO, message, extra_tags=farmer.district)
            return redirect('register')  # Redirect to a success page
    else:
        form = CaseForm()
    
    return render(request, 'report_case.html', {'form': form})


class Farmers_home(LoginRequiredMixin, ListView):
    model = Case
    template_name = 'farm_home.html'
    context_object_name = 'cases'

    def get_queryset(self):
        queryset = super().get_queryset()
        farmer = self.request.user.farmer

        # Get the date range from user input
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')

        if farmer and start_date and end_date:
            # Filter cases by district and date range
            queryset = queryset.filter(
                Q(district=farmer.district) &
                Q(date__range=[start_date, end_date])
            ).order_by('-date')
        elif farmer:
            # Filter cases by district only
            queryset = queryset.filter(district=farmer.district).order_by('-date')

        return queryset
    
class Farmers_case(DetailView):
    model= Case
    template_name= 'farm_case.html'
    

class MapView(View):
    model =Case
    template_name = 'farmers_map.html'
    
    
def symptom_detail(request, symptom_id):
    symptom = Symptom.objects.get(id=symptom_id)
    return render(request, 'symptom_detail.html', {'symptom': symptom})