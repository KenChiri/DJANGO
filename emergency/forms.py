from django import forms
from .models import EmergencyReport
from .models import CrimeReport
from django.forms import fields

class EmergencyReportForm(forms.ModelForm):
    class Meta:
        model = EmergencyReport
        fields = ['message', 'photo', 'scene_description', 'location']
        labels = {
            'message': 'Enter the Accident Details:',
            'photo': 'Upload a Photo (optional):',
            'scene_description': 'Describe the Accident Scene:',
            'location': 'Accident Location:',
        }


class CrimeReportForm(forms.ModelForm):
    class Meta:
        model = CrimeReport
        fields = [
            'crime_type',
            'incident_date',
            'incident_time',
            'location',
            'witness_name1',
            'witness_phone1',
            'witness_name2',
            'witness_phone2',
            'evidence_description',
            'photo',
            'message',
        ]
        widgets = {
            'incident_date': forms.DateInput(attrs={'type': 'date'}),
            'incident_time': forms.TimeInput(attrs={'type': 'time'}),
        }

    def __init__(self, *args, **kwargs):
        super(CrimeReportForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control form-field'




from django import forms
from django.contrib.auth import get_user_model  # Assuming Officer is a user

class MedicalExaminationForm(forms.Form):

    part_1_fields = (
        'officer',
        
    )

    # Part 1: To be completed by the Police Officer Requesting Examination
    officer = forms.ModelChoiceField(queryset=get_user_model().objects.all(), label='From (Requesting Officer)')
    reference_number = forms.CharField(label='Reference Number')
    date = forms.DateField(label='Date (DD/MM/YYYY)')
    to_facility = forms.CharField(label='To (Hospital/Dispensary)')
    person_examined_name = forms.CharField(label='Name of the Person Being Examined')
    person_examined_address = forms.CharField(label='Address of the Person Being Examined')
    alleged_offense_date = forms.DateField(label='Date and Time of Alleged Offense (Optional)', required=False)
    alleged_offense_details = forms.CharField(label='Brief Details of the Alleged Offense', widget=forms.Textarea)
    officer_commanding_station_name = forms.CharField(label='Name of the Officer Commanding Station')
    officer_commanding_station_signature = forms.CharField(label='Signature of the Officer Commanding Station')

    # Part II: Medical Details (To be completed by Medical Officer)
    medical_officer_reference = forms.CharField(label='Medical Officer\'s Reference Number')
    clothing_state = forms.CharField(label='State of Clothing (tears, stains, blood, etc.)')
    general_medical_history = forms.CharField(label='General Medical History (relevant to offense)', widget=forms.Textarea)
    general_physical_exam = forms.CharField(label='General Physical Examination (appearance, drugs/alcohol, demeanor)', widget=forms.Textarea)

    # Section B: To be completed by Medical Officer in Assault Cases
    # (Consider using a separate form for Section B if details are extensive)
    injuries_details = forms.CharField(label='Details of site, situation, shape and depth of injuries sustained (Head & Neck, Thorax & Abdomen, Upper Limbs, Lower Limbs)', widget=forms.Textarea)
    injuries_age = forms.CharField(label='Approximate Age of Injuries (hours, days, weeks)')
    weapon_type = forms.CharField(label='Probable Type of Weapon(s) Causing Injury', required=False)
    prior_treatment = forms.CharField(label='Treatment Received Prior to Examination (if any)', required=False)
    clinical_results = forms.CharField(label='Immediate Clinical Results and Assessed Degree (Harm/Grievous Harm)', widget=forms.Textarea)
    medical_officer_name = forms.CharField(label='Name and Signature of Medical Officer/Practitioner')
    medical_officer_date = forms.DateField(label='Date (DD/MM/YYYY)')
