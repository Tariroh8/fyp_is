
from django.contrib import admin
from leaflet.admin import LeafletGeoAdmin
from .models import District, Animalcases, Disease, Case,  Spece, Symptom, Ward, Farmer, Vet_officer

class DistrictAdmin(LeafletGeoAdmin):
    list_display = ('name_2', 'varname_2')
    search_fields = ('name_2',)
    
class WardAdmin(LeafletGeoAdmin):
    list_display = ('district', 'ward_name', 'province')
    search_fields = ('district','province')
    

class AnimalcasesAdmin(LeafletGeoAdmin):
    list_display = ('district', 'spicies', 'symptoms')
    search_fields = ('spicies', 'district')
    

class DiseaseAdmin(LeafletGeoAdmin):
    list_display = ('disease_id', 'name','spece_affected')
    search_fields = ('name','spece_affected')
    
class CaseAdmin(LeafletGeoAdmin):
    list_display = ('case_id', 'spece', 'lat', 'ward')
    search_fields = ('symptoms', 'spece')
   
class Vet_officerAdmin(LeafletGeoAdmin):
    list_display = ('name', 'district')
    search_fields = ('name', 'district')
    
class FarmerAdmin(LeafletGeoAdmin):
    list_display = ('name', 'email', 'district')
    search_fields = ('name', 'district')
    
class SymptomAdmin(LeafletGeoAdmin):
    list_display = ('name', 'spece', 'affected_part')
    search_fields = ('name', 'spece')
    

admin.site.register(District, DistrictAdmin)
admin.site.register(Animalcases, AnimalcasesAdmin)
admin.site.register(Disease, DiseaseAdmin)
admin.site.register(Case, CaseAdmin)
admin.site.register(Vet_officer, Vet_officerAdmin)
admin.site.register(Spece)
admin.site.register(Symptom, SymptomAdmin)
admin.site.register(Ward,WardAdmin)
admin.site.register(Farmer,FarmerAdmin)
