from django.contrib import admin
from .models import EmergencyReport, CrimeReport, ChargeSheet, Witness, MedicalExamination

# Register your models here.

admin.site.register(EmergencyReport)
admin.site.register(CrimeReport)
admin.site.register(ChargeSheet)
admin.site.register(Witness)
admin.site.register(MedicalExamination)
