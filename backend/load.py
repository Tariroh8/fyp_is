from pathlib import Path
from django.contrib.gis.utils import LayerMapping
from .models import District, Animalcases, Ward, Region


#py manage.py ogrinspect C:\Users\PC\Desktop\Final_year_project\animalpoints.shp Health_cases --mapping --multi --name-field pkuid --null true

# Auto-generated `LayerMapping` dictionary for District model
district_mapping = {
    'id_0': 'ID_0',
    'iso': 'ISO',
    'name_0': 'NAME_0',
    'id_1': 'ID_1',
    'name_1': 'NAME_1',
    'id_2': 'ID_2',
    'name_2': 'NAME_2',
    'type_2': 'TYPE_2',
    'engtype_2': 'ENGTYPE_2',
    'nl_name_2': 'NL_NAME_2',
    'varname_2': 'VARNAME_2',
    'geom': 'MULTIPOLYGON',
}


# Auto-generated `LayerMapping` dictionary for Animalcases model
animalcases_mapping = {
    'pkuid': 'pkuid',
    'spicies': 'spicies',
    'symptoms': 'symptoms',
    'date': 'date',
    'district': 'district',
    'farmer': 'farmer',
    'geom': 'MULTIPOINT',
}

# Auto-generated `LayerMapping` dictionary for Ward model
ward_mapping = {
    'fid': 'fid',
    'objectid_1': 'OBJECTID_1',
    'admin3name': 'admin3Name',
    'admin3pcod': 'admin3Pcod',
    'admin2name': 'admin2Name',
    'admin2pcod': 'admin2Pcod',
    'admin1name': 'admin1Name',
    'admin1pcod': 'admin1Pcod',
    'shape_leng': 'Shape_Leng',
    'shape_area': 'Shape_Area',
    'case_recor': 'case_recor',
    'num_of_cas': 'num_of_Cas',
    'hotspot': 'hotspot',
    'geom': 'MULTIPOLYGON',
}


# Auto-generated `LayerMapping` dictionary for Region model
region_mapping = {
    'fid': 'fid',
    'objectid_1': 'OBJECTID_1',
    'admin3name': 'admin3Name',
    'admin3pcod': 'admin3Pcod',
    'admin2name': 'admin2Name',
    'admin2pcod': 'admin2Pcod',
    'admin1name': 'admin1Name',
    'admin1pcod': 'admin1Pcod',
    'shape_leng': 'Shape_Leng',
    'shape_area': 'Shape_Area',
    'case_recor': 'case_recor',
    'num_of_cas': 'num_of_Cas',
    'hotspot': 'hotspot',
    'geom': 'MULTIPOLYGON',
}


district_shp = Path(__file__).resolve().parent / 'maps'/ 'ZWE_adm2.shp'
health_case_shp = Path(__file__).resolve().parent / 'maps'/'animal_cases'/'cases.shp'
wards_shp = Path(__file__).resolve().parent / 'maps'/'adm3_Wards.shp'
region_shp = Path(__file__).resolve().parent / 'maps'/'Old_Natural_Farming_Regions.shp'



def run(verbose = True):
    lm = LayerMapping(District, district_shp, district_mapping, transform=False)
    lm.save(strict=True, verbose=verbose)
    
    
def run1(verbose = True):
    lm = LayerMapping(Animalcases, health_case_shp, animalcases_mapping, transform=False)
    lm.save(strict=True, verbose=verbose)
    
def run2(verbose = True):
    lm = LayerMapping(Ward, wards_shp, ward_mapping, transform=False)
    lm.save(strict=False, verbose=verbose)
    
def run3(verbose = True):
    lm = LayerMapping(Region, region_shp, region_mapping, transform=False)
    lm.save(strict=True, verbose=verbose)
