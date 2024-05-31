from django.shortcuts import render, redirect, get_object_or_404
from .forms import VetRegistrationForm, VetLoginForm, SymptomForm
from backend.models import District, Case, Ward, Farmer, Symptom
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.serializers import serialize
from django.contrib.gis.serializers import geojson
from django.http import  HttpResponseRedirect
from django.http import JsonResponse
from django.db.models import Count
import csv
from django.http import HttpResponse
from datetime import date
from django.contrib.gis.geos import Point, GEOSGeometry
from django.contrib.gis.measure import D
from django.db.models.functions import TruncMonth
from datetime import datetime, timedelta
from django.db.models import Count
from django.utils import timezone
import calendar



@login_required(login_url='vet_login')
def vet_home (request):

    # Get the logged in user's id and name
    vet_officer = request.user.vet_officer  
    vet_district = vet_officer.district  

    districts = District.objects.filter(name_2=vet_district)
    
    wards = Ward.objects.filter(district_foreign__name_2=vet_district)
    #wards with cases for different color rendering
    ward_with_cases = Ward.objects.filter(district_foreign__name_2=vet_district, case__isnull=False)

    serialized_districts = serialize('geojson', districts)
    serialized_wards = serialize('geojson', wards) 
    serialized_ward_with_cases = serialize('geojson', ward_with_cases)   
    
    #cases
    cases = Case.objects.filter(district=vet_district)
    catle_cases = Case.objects.filter(district=vet_district, spece__name='Cattle')
    
    
    
    # Get the number of cases reported for each ward
    cases_count_by_ward = Case.objects.filter(district=vet_district).values('ward').annotate(num_cases=Count('ward'))
    
    # You can access the ward ID and number of cases in the following way:
    ward_cases_dict = {}
    for ward_count in cases_count_by_ward:
        ward_id = ward_count['ward']
        num_cases = ward_count['num_cases']
        # Get the ward using the 'wards' query
        ward = wards.filter(id=ward_id).first()
        if ward:
            ward_name = ward.ward_name
            ward_cases_dict[ward_name] = {'num_cases': num_cases, 'symptoms': []}
            
    for case in cases:
        ward_name = case.ward.ward_name
        if ward_name in ward_cases_dict:
            symptoms = case.symptoms.all().values_list('name', flat=True)
            ward_cases_dict[ward_name]['symptoms'].extend(symptoms)
        else:
            symptoms = case.symptoms.all().values_list('name', flat=True)
            ward_cases_dict[ward_name] = {'num_cases': 0, 'symptoms': list(symptoms)}
        
        
       
    # Print the ward names and number of cases
    for ward in wards:
        ward_name = ward.ward_name
        num_cases = ward_cases_dict.get(ward_name, 0)  # Default to zero cases if ward not found in ward_cases_dict
        ward_cases_dict[ward_name] = num_cases
        
        
    print(ward_cases_dict)
    
        
        
    
    
    
    # Get the most common symptom in all cases
    most_common_symptom = Case.objects.filter(district=vet_district).values('symptoms__name').annotate(symptoms_count=Count('symptoms')).order_by('-symptoms_count').first()

    # Access the most common symptom and its count
    if most_common_symptom:
        symptom_name = most_common_symptom['symptoms__name']
        symptom_count = most_common_symptom['symptoms_count']
        print(f"The most common symptom in all cases is {symptom_name} with a count of {symptom_count}.")
    else:
        symptom_name = 'No no cases reported'
        symptom_count = '0'


    # to show statitics for each district on home page
    case_count = cases.count()
    ward_count = wards.count()
    catle_cases_count = catle_cases.count()
    
    # converting districts data set querry into a string for display
    districts_string = ""
    for district in districts:
        districts_string += str(district)
    
    context = {
        'districts': districts, #passing in vet officer's district
        'wards': wards, #passing in vet officer's wards
        'cases': cases, #passing in cases reported in the district 
        'serialized_districts': serialized_districts, #passing in districts in geo json format for map view
        'serialized_wards':serialized_wards, #passing in wards in geo json format for map view
        'serialized_ward_with_cases': serialized_ward_with_cases,
        'case_count': case_count, #total cases
        'symptom_name': symptom_name, #most common symptom
        'symptom_count': symptom_count, #number of times that symptom appears
        'ward_count': ward_count, #total wards in district
        'catle_cases_count':catle_cases_count, #cattles cases only
        'districts_string': districts_string, # vet officer's district 
        'ward_cases_dict': ward_cases_dict,
    }
    return render(request, 'vet_home.html', context)

@login_required(login_url='vet_login')
def download_cases_csv(request):
    vet_officer = request.user.vet_officer
    vet_district = vet_officer.district
    cases = Case.objects.filter(district=vet_district)

    # Create a CSV file
    response = HttpResponse(content_type='text/csv')
    today = date.today().strftime("%Y-%m-%d")
    filename = f"{vet_district}-cases-as-at-{today}.csv"
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    # Create a CSV writer
    writer = csv.writer(response)

    # Write header row with field names
    field_names = [field.name for field in Case._meta.fields]
    writer.writerow(field_names)

    # Write data rows
    for case in cases:
        row = []
        for field in field_names:
            if field == 'symptoms':
                symptoms = ', '.join([symptom.name for symptom in getattr(case, field).all()])
                row.append(symptoms)
            else:
                row.append(getattr(case, field))
        writer.writerow(row)

    return response

def ward_map_view(request, district_foreign, ward_name):
    
    vet_officer = request.user.vet_officer  
    vet_district = vet_officer.district
    
    # Retrieve the ward selected by vet officer
    ward = Ward.objects.filter(district_foreign=district_foreign, ward_name=ward_name)
    cases = Case.objects.filter(district=vet_district, ward__in=ward)
    farmers = Farmer.objects.filter(district=vet_district, ward__in=ward)
    
    print(farmers)
    
    
    serialized_ward = serialize('geojson', ward) 
    

    # Pass the ward data to the template context
    context = {
        'ward': ward,
        'farmers': farmers,
        'cases': cases,
        'serialized_ward': serialized_ward,
    }

    return render(request, 'ward_map.html', context)


def vet_register(request):
    submitted = False
    if request.method == "POST":
        form = VetRegistrationForm(request.POST)
        if form.is_valid():
            vet_officer = form.save()
            submitted = True
            return HttpResponseRedirect('/register?submitted=True')
    else:
        form = VetRegistrationForm()
        if 'submitted' in request.GET:
            submitted = True
    
    return render(request, 'vet_register.html', {'form': form, 'submitted': submitted})

def vet_login(request):
    if request.method == 'POST':
        form = VetLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('vet_home')
            else:
                form.add_error(None, 'Invalid email or password.')
    else:
        form = VetLoginForm()
    
    return render(request, 'vet_login.html', {'form': form})






def national_vet_statistics(request):
   
# Calculate the start date for the previous 12 months
    current_date = timezone.now().date()
    start_date = current_date - timedelta(days=365)

    # Query the cases for the previous 12 months, including the current month
    cases_by_month = Case.objects.filter(date__gte=start_date).annotate(
        month=TruncMonth('date')
    ).values('month').annotate(
        count=Count('pk')
    ).order_by('month')

    # Generate the list of months and case counts
    months = []
    case_counts = []

    # Iterate over the previous 12 months, including the current month
    current_month = start_date.replace(day=1)
    while current_month <= current_date.replace(day=1):
        # Check if there is a corresponding entry in the cases_by_month queryset
        matching_case = next(
            (case for case in cases_by_month if case['month'] == current_month),
            None
        )
        if matching_case:
            # Case exists for the current month
            month_name = calendar.month_name[current_month.month]  # Convert month number to month name
            months.append(month_name)
            case_counts.append(matching_case['count'])
        else:
            # No case for the current month, record zero
            month_name = calendar.month_name[current_month.month]  # Convert month number to month name
            months.append(month_name)
            case_counts.append(0)

        # Move to the next month
        current_month = (current_month + timedelta(days=32)).replace(day=1)

    # Print the list of months and case counts
    for month, count in zip(months, case_counts):
        print(month, count)
        
    cases_by_district = Case.objects.filter(date__gte=start_date).annotate(
        month=TruncMonth('date')
    ).values('district__name_2').annotate(
        count=Count('pk')
    ).order_by('district__name_2')

    # Generate the list of districts and case counts
    districts = []
    district_case_counts = []

    # Iterate over the districts and case counts
    for case in cases_by_district:
        districts.append(case['district__name_2'])
        district_case_counts.append(case['count'])

    
    
    # print(districts,district_case_counts)
        
    farmer_counts = Farmer.objects.values('district__name_2').annotate(count=Count('district__name_2'))

    farmer_districts = [farmer_count['district__name_2'] for farmer_count in farmer_counts]
    farmer_count = [farmer_count['count'] for farmer_count in farmer_counts]
    
    
    # Query all cases  to ge symptoms count
    cases_all = Case.objects.all()

    # Count symptoms across all cases
    symptom_counts = cases_all.values('symptoms__id', 'symptoms__name').annotate(count=Count('symptoms__id'))
    
    
    symptoms_name = []
    symptoms_counts = []
    
    for symptom_count in symptom_counts:
        symptom_name = symptom_count['symptoms__name']
        count = symptom_count['count']
        symptoms_name.append(symptom_name)
        symptoms_counts.append(count)
    
    print(symptoms_counts)
    
    
    # Calculate the start date as 5 days ago
    start_date = current_date - timedelta(days=5)

    # Initialize lists to store the dates and case counts
    last_5_days = []
    count_per_day = []

    # Iterate over the past 5 days
    current_day = start_date
    while current_day <= current_date:
        # Query the cases for the current day
        cases_current_day = Case.objects.filter(date=current_day).count()

        # Append the current day and case count to the lists
        last_5_days.append(current_day)
        count_per_day.append(cases_current_day)

        # Move to the next day
        current_day += timedelta(days=1)
        
    for day, count in zip(last_5_days, count_per_day):
        print(day, count)
        
    # Query all cases  to ge symptoms count
    district_all = District.objects.all()
    serialized_districts_all = serialize('geojson', district_all)
    
    context = {
        'months': months,
        'case_counts': case_counts,
        'districts': districts,
        'district_case_counts': district_case_counts,
        'farmer_districts': farmer_districts,
        'farmer_count': farmer_count,
        'symptoms_counts': symptoms_counts,
        'symptoms_name': symptoms_name,
        'last_5_days': last_5_days,
        'count_per_day': count_per_day,
        'cases_all': cases_all,
        'serialized_districts_all': serialized_districts_all,
    }

    return render(request, 'national_statics.html', context)



@login_required(login_url='vet_login')
def cases_map(request):
    # Get the selected district ID, start date, end date, and symptoms from the form
    selected_district_id = request.POST.get('district_id')
    all_districts = District.objects.all()
    all_symptoms = Symptom.objects.all()
    start_date_str = request.POST.get('start_date')
    end_date_str = request.POST.get('end_date')
    selected_symptoms = request.POST.getlist('symptoms')

    # Filter the districts based on the selected district ID
    if selected_district_id:
        selected_district = District.objects.get(id=selected_district_id)
        districts = District.objects.filter(id=selected_district_id)
        ward_with_cases = Ward.objects.filter(district=selected_district, case__isnull=False)
    else:
        selected_district = None
        districts = District.objects.all()
        ward_with_cases = None

    # Filter the cases based on the selected district and date range
    cases = Case.objects.all()
    if start_date_str and end_date_str:
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
        cases = cases.filter(date__range=(start_date, end_date))
    if selected_district_id:
        cases = cases.filter(district=selected_district)

    # Filter the cases based on the selected symptoms
    if selected_symptoms:
        cases = cases.filter(symptoms__name__in=selected_symptoms).distinct()

    # Serialize the districts to GeoJSON format
    serialized_districts = serialize('geojson', districts)
    if ward_with_cases is not None:
        serialized_ward_with_cases = serialize('geojson', ward_with_cases)
    else:
        serialized_ward_with_cases = 'null'

    context = {
        'start_date': start_date_str,
        'end_date': end_date_str,
        'districts': districts,
        'serialized_ward_with_cases': serialized_ward_with_cases,
        'all_districts': all_districts,
        'selected_district': selected_district,
        'cases': cases,
        'serialized_districts': serialized_districts,
        'selected_symptoms': selected_symptoms,
        'all_symptoms': all_symptoms,
    }

    return render(request, 'cases_map.html', context)


def symptom_create(request):
    if request.method == 'POST':
        form = SymptomForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('symptom_list')
    else:
        form = SymptomForm()
    return render(request, 'symptom_form.html', {'form': form})

def symptom_list(request):
    symptoms = Symptom.objects.all()
    return render(request, 'symptom_list.html', {'symptoms': symptoms})