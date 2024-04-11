from django.forms import ModelForm
from authenticator.models import AccidentFiles

class AccidentFileForm(ModelForm):
    class Meta:
        model = AccidentFiles
        fields = ['name', 'abstract']  # Include 'abstract' field

    def __init__(self, *args, **kwargs):
        super(AccidentFileForm, self).__init__(*args, **kwargs)
        self.fields['name'].error_messages['required'] = 'Please enter a name for the accident file.'
        self.fields['abstract'].error_messages['required'] = 'Please enter a summary of the accident.'  # Add validation for abstract








