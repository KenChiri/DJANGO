from django.db import models
#from django.contrib.gis.geos import PointField


# Create your models here.

class CrimeReport(models.Model):
    # Crime Description
    crime_type = models.CharField(max_length=255)
    incident_date = models.DateField()
    incident_time = models.TimeField()
    location = models.CharField(max_length=255)

    # Witnesses (Optional)
    witness_name1 = models.CharField(max_length=255, blank=True)
    witness_phone1 = models.CharField(max_length=20, blank=True)
    witness_name2 = models.CharField(max_length=255, blank=True)
    witness_phone2 = models.CharField(max_length=20, blank=True)

    # Evidence (Optional)
    evidence_description = models.TextField(blank=True)
    photo = models.ImageField(upload_to='media/crime_photos/', blank=True)

    # Additional details (Optional)
    message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Anonymous Crime Report: {self.id} - {self.crime_type}"



class EmergencyReport(models.Model):
    message = models.TextField()
    photo = models.ImageField(upload_to='media/emergency_photos/', blank=True)
    scene_description = models.TextField()
    location = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Emergency Report: {self.id}"

class Location(models.Model):
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    address = models.CharField(max_length=255, blank=True)

    # Foreign key to EmergencyReport if needed
    # report = models.ForeignKey(EmergencyReport, on_delete=models.CASCADE)



#Chargesheet model
from django.core.validators import RegexValidator

class ChargeSheet(models.Model):
    court_file_no = models.CharField(max_length=50, unique=True)  # Ensure unique court file number
    odpp_case_no = models.CharField(max_length=50, unique=True)  # Ensure unique ODPP case number
    odpp_station = models.CharField(max_length=100)
    police_case_no = models.CharField(max_length=50, unique=True)  # Ensure unique police case number

    ob_number = models.CharField(max_length=50, validators=[RegexValidator(regex='^\d+$', message='OB number must be digits only')])  # Validate OB number format

    date_drafted = models.DateField(auto_now_add=True)  # Automatically set draft date

    christian_name = models.CharField(max_length=100)
    fathers_name = models.CharField(max_length=100, blank=True)  # Allow fathers_name to be blank

    id_number = models.CharField(max_length=20, unique=True, validators=[RegexValidator(regex='^\d+$', message='ID number must be digits only')])  # Ensure unique ID number and validate format

    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female')])

    nationality = models.CharField(max_length=50)
    age = models.PositiveIntegerField()  # Ensure age is positive

    address = models.TextField()

    charge = models.TextField()
    particulars_of_offense = models.TextField()

    date_of_arrest = models.DateField(blank=True, null=True)  # Allow date_of_arrest to be blank and null

    is_warranted = models.CharField(max_length=10, choices=[('with', 'With'), ('without', 'Without')])

    apprehension_date = models.DateField(blank=True, null=True)  # Allow apprehension_date to be blank and null

    status = models.CharField(max_length=50)

    complaint_address = models.TextField()

    # Add a ManyToManyField for Witnesses (assuming a separate Witness model exists)
    witnesses = models.ManyToManyField('Witness', blank=True)

    sentence = models.TextField(blank=True)  # Allow sentence to be blank

    prosecutor = models.CharField(max_length=100)

    def __str__(self):
        return f"Charge Sheet: {self.court_file_no}"
    




class Witness(models.Model):
    name = models.CharField(max_length=100)
    statement = models.TextField()

    def __str__(self):
        return f"Witness: {self.name}"
    



from django.db import models
from django.contrib.auth import get_user_model

class MedicalExamination(models.Model):

    # Part 1: To be completed by the Police Officer Requesting Examination
    officer = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='medical_examinations')
    reference_number = models.CharField(max_length=255)
    date = models.DateField()
    to_facility = models.CharField(max_length=255)
    person_examined_name = models.CharField(max_length=255)
    person_examined_address = models.CharField(max_length=255)
    alleged_offense_date = models.DateField(blank=True, null=True)
    alleged_offense_details = models.TextField(blank=True)
    officer_commanding_station_name = models.CharField(max_length=255)
    officer_commanding_station_signature = models.CharField(max_length=255)

    # Part II: Medical Details (To be completed by Medical Officer)
    medical_officer_reference = models.CharField(max_length=255)
    clothing_state = models.CharField(max_length=255)
    general_medical_history = models.TextField()
    general_physical_exam = models.TextField()

    # Section B: To be completed by Medical Officer in Assault Cases
    injuries_details = models.TextField()
    injuries_age = models.CharField(max_length=255)
    weapon_type = models.CharField(max_length=255, blank=True)
    prior_treatment = models.CharField(max_length=255, blank=True)
    clinical_results = models.TextField()
    medical_officer_name = models.CharField(max_length=255)
    medical_officer_date = models.DateField()


    def __str__(self):
        return f"Medical Examination - {self.reference_number}"


