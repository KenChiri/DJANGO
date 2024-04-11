from django.shortcuts import redirect, render
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth import get_user_model
from .forms import EmergencyReportForm, CrimeReportForm, MedicalExaminationForm
from .models import EmergencyReport, CrimeReport, MedicalExamination
from django.core import serializers
from django.contrib import messages


User = get_user_model()



def report_emergency(request):
    if request.method == 'POST':
        # Identify form type based on hidden field
        form_type = request.POST.get('report_type')
        if form_type == 'accident_report':
            form = EmergencyReportForm(request.POST, request.FILES)
        elif form_type == 'crime_report':
            form = CrimeReportForm(request.POST, request.FILES)
        else:
            form = None

        if form and form.is_valid():
            # Save the form data
            form.save()
            messages.success(request, 'Your report has been sent. Thank you!')
            return HttpResponseRedirect('home')  # Redirect to home page after successful form submission
        else:
            messages.error(request, 'There was an error with your submission. Please try again.')
    # Just initialize both forms for the initial rendering
    emergency_form = EmergencyReportForm()
    crime_form = CrimeReportForm()
    return render(request, 'emergency/home.html', {'emergency_form': emergency_form, 'crime_form': crime_form})



def crime_alerts(request):
    fname = request.session.get('fname')
    if not fname:
        return redirect('login')
    
    reports= CrimeReport.objects.order_by('-created_at')
    if request.headers.get('X-Requested-With')== 'XMLHttpRequest':
        data = serializers.serialize('json', reports)
        return JsonResponse(data, safe=False)
    else:
        context = {'reports': reports, 'fname': fname}
        return render(request, 'emergency/crime_alerts.html', context )


def accident_alerts(request):
    fname = request.session.get('fname')
    if not fname:
        return redirect('login')
    
    reports = EmergencyReport.objects.order_by('-created_at')
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        data = serializers.serialize('json', reports)
        return JsonResponse(data, safe=False)
    else:
        context = {'reports': reports, 'fname': fname}
        return render(request, 'emergency/accident_alerts.html', context)



from django.http import HttpResponse
from .models import ChargeSheet

def process_charge_sheet(request):
    if request.method == 'POST':
        # Capture form data from request.POST
        court_file_no = request.POST.get('courtcaseNo')
        odpp_case_no = request.POST.get('odpp_case_no')
        odpp_station = request.POST.get('odpp_station')
        police_case_no = request.POST.get('police_case_no')
        ob_number = request.POST.get('ob_number')
        date_drafted = request.POST.get('date_drafted')
        christian_name = request.POST.get('christian_name')
        fathers_name = request.POST.get('fathers_name')
        id_number = request.POST.get('id_number')
        gender = request.POST.get('gender')
        nationality = request.POST.get('nationality')
        age = request.POST.get('age')
        address = request.POST.get('address')
        charge = request.POST.get('charge')
        particulars_of_offense = request.POST.get('particularsOfOffense')
        date_of_arrest = request.POST.get('dateOfArrest')
        is_warranted = request.POST.get('iswaranted')
        apprehension_date = request.POST.get('apprehensionDate')
        status = request.POST.get('status')
        complaint_address = request.POST.get('complaint_address')
        witness = request.POST.get('witness')
        sentence = request.POST.get('sentence')
        prosecutor = request.POST.get('prosecutor')

        # Create and save ChargeSheet object
        charge_sheet = ChargeSheet(
            court_file_no=court_file_no,
            odpp_case_no=odpp_case_no,
            odpp_station=odpp_station,
            police_case_no=police_case_no,
            ob_number=ob_number,
            date_drafted=date_drafted,
            christian_name=christian_name,
            fathers_name=fathers_name,
            id_number=id_number,
            gender=gender,
            nationality=nationality,
            age=age,
            address=address,
            charge=charge,
            particulars_of_offense=particulars_of_offense,
            date_of_arrest=date_of_arrest,
            is_warranted=is_warranted,
            apprehension_date=apprehension_date,
            status=status,
            complaint_address=complaint_address,
            witness=witness,
            sentence=sentence,
            prosecutor=prosecutor
        )
        charge_sheet.save()

        return HttpResponse('Charge sheet submitted successfully.')
    else:
        return HttpResponse('Invalid request method.')



    
def abstract (request):
    fname = request.session.get('fname')
    if not fname:
        return redirect('login')
    
    context = {'fname': fname}
    return render(request, 'emergency/abstract.html', context)


def charges (request):
    fname = request.session.get('fname')
    if not fname:
        return redirect('login')
    

    context = {'fname': fname}
    return render(request, 'emergency/chargesheet.html', context)

def medical (request):
    fname = request.session.get('fname')
    if not fname:
        return redirect('login')
    
    
    if request.method == 'POST':
        form = MedicalExaminationForm(request.POST or None)
        if form.is_valid():
            # Part 1: To be completed by the Police Officer Requesting Examination
            officer = form.cleaned_data['officer']
            reference_number = form.cleaned_data['reference_number']
            date = form.cleaned_data['date']
            to_facility = form.cleaned_data['to_facility']
            person_examined_name = form.cleaned_data['person_examined_name']
            person_examined_address = form.cleaned_data['person_examined_address']
            alleged_offense_date = form.cleaned_data['alleged_offense_date']
            alleged_offense_details = form.cleaned_data['alleged_offense_details']
            officer_commanding_station_name = form.cleaned_data['officer_commanding_station_name']
            officer_commanding_station_signature = form.cleaned_data['officer_commanding_station_signature']

            # Part II: Medical Details (To be completed by Medical Officer)
            medical_officer_reference = form.cleaned_data['medical_officer_reference']
            clothing_state = form.cleaned_data['clothing_state']
            general_medical_history = form.cleaned_data['general_medical_history']
            general_physical_exam = form.cleaned_data['general_physical_exam']

            # Section B: To be completed by Medical Officer in Assault Cases
            injuries_details = form.cleaned_data['injuries_details']
            injuries_age = form.cleaned_data['injuries_age']
            weapon_type = form.cleaned_data['weapon_type']
            prior_treatment = form.cleaned_data['prior_treatment']
            clinical_results = form.cleaned_data['clinical_results']
            medical_officer_name = form.cleaned_data['medical_officer_name']
            medical_officer_date = form.cleaned_data['medical_officer_date']




            examination = MedicalExamination.objects.create(
                officer=officer,
                reference_number=reference_number,
                date=date,
                to_facility=to_facility,
                person_examined_name=person_examined_name,
                person_examined_address=person_examined_address,
                alleged_offense_date=alleged_offense_date,
                alleged_offense_details=alleged_offense_details,
                officer_commanding_station_name=officer_commanding_station_name,
                officer_commanding_station_signature=officer_commanding_station_signature,
                medical_officer_reference=medical_officer_reference,
                clothing_state=clothing_state,
                general_medical_history=general_medical_history,
                general_physical_exam=general_physical_exam,
                injuries_details=injuries_details,
                injuries_age=injuries_age,
                weapon_type=weapon_type,
                prior_treatment=prior_treatment,
                clinical_results=clinical_results,
                medical_officer_name=medical_officer_name,
                medical_officer_date=medical_officer_date
            )

            messages.success(request, "Successfully Filed the Medical report, Thank you!" )

        else:
            messages.error(request, "Form submission failed. Please try again.")

    else:
        form = MedicalExaminationForm()
        context = {'fname': fname, 'form': form}
        return render(request, 'emergency/medicalreport.html', context)
