from django.db import models
from django.contrib.auth.models import User
from django.contrib.gis.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

class Region(models.Model):
    fid = models.IntegerField(null=True)
    objectid_1 = models.FloatField(null=True)
    admin3name = models.CharField(max_length=254, null=True)
    admin3pcod = models.CharField(max_length=254, null=True)
    admin2name = models.CharField(max_length=254, null=True)
    admin2pcod = models.CharField(max_length=254, null=True)
    admin1name = models.CharField(max_length=254, null=True)
    admin1pcod = models.CharField(max_length=254, null=True)
    shape_leng = models.FloatField(null=True)
    shape_area = models.FloatField(null=True)
    case_recor = models.CharField(max_length=254, null=True)
    num_of_cas = models.CharField(max_length=254, null=True)
    hotspot = models.CharField(max_length=254, null=True)
    geom = models.MultiPolygonField(srid=-1)
    def __str__(self): return self.admin3name
    
class DistrictManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().order_by('name_2')
    
class WardManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().order_by('district')

class District(models.Model):
    id_0 = models.BigIntegerField(null=True)
    iso = models.CharField(max_length=3, null=True)
    name_0 = models.CharField(max_length=75, null=True)
    id_1 = models.BigIntegerField(null=True)
    name_1 = models.CharField(max_length=75, null=True)
    id_2 = models.BigIntegerField(null=True)
    name_2 = models.CharField(max_length=75, null=True)
    type_2 = models.CharField(max_length=50, null=True)
    engtype_2 = models.CharField(max_length=50, null=True)
    nl_name_2 = models.CharField(max_length=75, null=True)
    varname_2 = models.CharField(max_length=150, null=True)
    geom = models.MultiPolygonField()
    objects = DistrictManager()
    def __str__(self): return self.name_2
    
class Ward(models.Model):
    fid = models.IntegerField(null=True)
    objectid_1 = models.FloatField(null=True)
    ward_name = models.CharField(max_length=254, null=True)
    admin3pcod = models.CharField(max_length=254, null=True)
    district = models.CharField(max_length=254, null=True)
    district_foreign = models.ForeignKey(District, on_delete = models.CASCADE, null=True)
    admin2pcod = models.CharField(max_length=254, null=True)
    province = models.CharField(max_length=254, null=True)
    admin1pcod = models.CharField(max_length=254, null=True)
    shape_leng = models.FloatField(null=True)
    shape_area = models.FloatField(null=True)
    geom = models.MultiPolygonField()
    objects = WardManager()

    def __str__(self):
        return f"{self.district} -ward- {self.ward_name}"
    
    
class Spece(models.Model):
    name = models.CharField(max_length=15, null=True)
    Description = models.CharField(max_length=254, null=True,blank=True)
    def __str__(self): return self.name
    
  
class Animalcases(models.Model):
    pkid = models.BigIntegerField(null=True)
    spicies = models.CharField(max_length=254, null=True)
    symptoms = models.CharField(max_length=254, null=True)
    date = models.CharField(max_length=24, null=True)
    district = models.ForeignKey(District, on_delete = models.CASCADE)
    geom = models.MultiPointField()
    farmer3 = models.CharField(max_length=254, null=True)
    def __str__(self): return self.farmer3
    
class Symptom(models.Model):
    name = models.CharField(max_length=75, null=True)
    shona_name = models.CharField(max_length=75, null=True, blank=True)
    ndebele_name = models.CharField(max_length=75, null=True, blank=True)
    spece = models.ForeignKey(Spece, on_delete = models.CASCADE, null=True)
    affected_part = models.CharField(max_length=254, null=True, blank=True)
    image = models.ImageField(upload_to="symptoms/images", null=True, blank=True)
    general_description = models.CharField(max_length=254, null=True, blank=True)
    shona_description = models.CharField(max_length=75, null=True, blank=True)
    ndebele_description = models.CharField(max_length=75, null=True, blank=True)
    veterinarian_description = models.CharField(max_length=254, null=True, blank=True)
    def __str__(self): return self.name
    
    
class Disease(models.Model):
    disease_id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=75, null=True)
    spece_affected = models.ForeignKey(Spece, on_delete = models.CASCADE, null=True)
    symptoms = models.ManyToManyField(Symptom,blank=True)
    description = models.CharField(max_length=1000, null=True, blank=True)
    vector_associated = models.CharField(max_length=75, null=True, blank=True)
    def __str__(self): return self.name
       
       
class Farmer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=254, null=True, blank=True)
    phone = models.CharField(max_length=75, null=True)
    email = models.EmailField(max_length=254, null=True, blank=True)
    species_owned = models.ManyToManyField(Spece,blank=True)
    district = models.ForeignKey(District, on_delete = models.CASCADE, null=True)
    ward = models.ForeignKey(Ward, on_delete = models.CASCADE, null=True)
    def __str__(self): return self.name
    
    
class Case(models.Model):
    case_id = models.BigAutoField(primary_key=True, blank=True)
    spece = models.ForeignKey(Spece, on_delete = models.CASCADE, null=True, blank=True)
    symptoms = models.ManyToManyField(Symptom, blank=True)
    date = models.DateField(("Date"), auto_now_add=True, null=True, blank=True)
    district = models.ForeignKey(District, on_delete = models.CASCADE, null=True, blank=True)
    ward = models.ForeignKey(Ward, on_delete = models.CASCADE, null=True)
    farmer1 = models.ForeignKey(Farmer, on_delete = models.CASCADE, null=True)
    lat = models.FloatField( null=True, blank=True)  # latitude of the place where the animal was found
    long = models.FloatField(null=True, blank=True)  # longitude of the place where the animal was found
    description = models.CharField(max_length=254, null=True, blank=True)
    def __str__(self):
        if self.description:
         return self.description
        else:
            return f"Case {self.case_id}"
    
    
class Vet_officer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=254, null=True, blank=True)
    email = models.EmailField(max_length=254, null=True, blank=True)
    district = models.ForeignKey(District, on_delete = models.CASCADE, null=True)
    
    def __str__(self):return self.name
    
    