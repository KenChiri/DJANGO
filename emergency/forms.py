from django import forms
from .models import EmergencyReport

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

  