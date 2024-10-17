from django.urls import reverse
from django.utils.encoding import force_str, force_bytes #
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.shortcuts import redirect, render
from django.contrib import messages #Used for displaying the error messages on the html templates
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string #captures a html file with some text and then it will render it to text that will be dipsplayed to the user
from accuReport import settings
from authenticator.forms import AccidentFileForm
from authenticator.models import Officer
from django.contrib.auth import get_user_model
from django.contrib.messages import success
from django.contrib.messages import get_messages
from django.core.mail import EmailMessage, send_mail
from django.contrib.auth import logout
from django.contrib.auth import login as auth_login #it will be used inside the activate function so that it doesn't damage the default django login.
from django.db.models import Q 
from . tokens import generate_token
from django.http import HttpRequest
from .models import AccidentDraft, AccidentFiles
import json
from django.contrib.auth.tokens import default_token_generator



# Create your views here.



def signup(request):
    if request.method == "POST":
        # Get the data from the POST request
        firstname = request.POST.get("fname")
        lastname = request.POST.get("lname")
        userName = request.POST.get("userId")
        email = request.POST.get("email")
        nationalId = request.POST.get("idNo")
        policeNo = request.POST.get("policeNumber")
        password = request.POST.get("pwd")
        passwordRepeat = request.POST.get("pwdRepeat")

        # Before creating the user we have to autheticate the values entered

        try:
            officer = Officer.objects.create_user(username=userName, email=email, password=password)
         # Set additional fields
            officer.first_name = firstname
            officer.last_name = lastname
            officer.national_id = nationalId
            officer.police_number = policeNo
            #set hashed password
            officer.set_password(password)
            officer.is_active = False
            officer.save()
        except:
            if Officer.objects.filter(username=userName).exists():
                messages.error(request, "username already exist! Please try some other username",)
                return render(request,'authenticator/signup.html')
                
            
            if Officer.objects.filter(email=email).exists():
                messages.error(request, 'Email Already Registered')
                return render(request,'authenticator/signup.html')
                
            
            if Officer.objects.filter(police_number=policeNo).exists():
                messages.error(request, "Invalid police number, already registered.")
                return render(request,'authenticator/signup.html')
            

            if Officer.objects.filter(national_id = nationalId).exists() :
                messages.error(request, "Invalid national Id, already registered.")
                return render(request,'authenticator/signup.html')
                
            
            if not userName.isalnum():
                messages.error(request, "Invalid Username")
                return render(request,'authenticator/signup.html')
            
        #Create the user  only if the validation pass


        success(request, "Your Account created Successully.  We will send you an Email for Activation")
        #take him to the login page is the signup is successfull


        #Welcome confirmation mail
        subject = "Welcome to AccuReport."
        message = "Hello " + officer.first_name + "\n" + "Welcome to AccuReport! \nThank you for visiting our website, an automated way to handle accidents and crime reports\nWe have also sent you a confirmation email, please confirm that this is your email address. \n\nThank You\nTeamAccuReport"
        from_email = settings.EMAIL_HOST_USER
        to_list = [officer.email]
        send_mail(subject, message, from_email, to_list, fail_silently=True)

        #email address confirmation Email
        current_site = get_current_site(request)
        email_subject = "Confirm your Email @  Accureport -Login"
        message2 = render_to_string("email_confirmation.html", {
            'name': officer.first_name,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(officer.pk)),
            'token': generate_token.make_token(officer)
        })

        email = EmailMessage(
            email_subject, 
            message2, 
            settings.EMAIL_HOST_USER, 
            [officer.email],
        )
        email.fail_silently = True
        email.send()
        return redirect('login')
    
    
    return render(request, "authenticator/signup.html")


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        officer = Officer.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Officer.DoesNotExist):
        officer = None
    
    if officer is not None and generate_token.check_token(officer, token):
        officer.is_active = True
        #User profile. signup confrirmation = Tru
        officer.save()
        auth_login(request,officer) #I encountered an error whereby I had two login functions login and login so I had to import as auth_login separately to handle the user authenitcation
        messages.success(request, 'Your account has been activated successfully')
        return redirect('login')
    else:
        return render(request, "activation_failed.html")





def user_login(request):
    #initialize messages before the conditional block

    msg = get_messages(request)
    if request.method == 'POST':
        identification = request.POST.get('credentials')
        password = request.POST.get("pwd")
        
  
        #Authentication with various fields
        officer = get_user_model()
        try:
            #fetch the users who match any of these fields
            officer = Officer.objects.get(Q(username=identification)  | Q(email=identification) | Q(police_number=identification))
            if officer.check_password(password):
                auth_login(request, officer)
                fname = officer.first_name + " " + officer.last_name
                request.session['fname'] = fname
                messages.success(request, "Welcome back " + fname)
                return redirect('index')    
            else:
                messages.error(request, "Incorrect password")
        except Officer.DoesNotExist:
            messages.error(request, "No such user.")
            return redirect('login')


   
        
    return render(request, "authenticator/login.html", {'messages': msg})





def index(request):
    # If 'fname' does not exist in session, redirect to login page
    if 'fname' not in request.session:
        return redirect('login')
    
    # Retrieve 'fname' from session
    fname = request.session['fname']
    
    return render(request, "authenticator/index.html", {'fname': fname})


def user_logout(request):
    logout(request)
    messages.success(request, "Logged Out")
    return redirect('login')


def create_accident_draft(request):
    if request.method == 'POST':
        scene = request.POST.get('scene')
        # Create a new AccidentDraft instance and save it
        accident_draft = AccidentDraft(scene=scene)
        accident_draft.save()
        # Redirect to a success page or display confirmation message
        messages.success(request, "Draft saved Successfully")  # Replace 'success_url' with your desired URL
    else:
        # Render the form for GET requests
        return render(request, 'accident_draft_form.html')



#function view for mail verification
# ... other imports


# ... other code


def mailOTP(request):
    if request.method == 'POST':
        userMail = request.POST.get('credentials')

        officer = get_user_model()

        try:
            officer = Officer.objects.get(Q(email=userMail))
        except Officer.DoesNotExist:
            messages.error(request, "Email does not exist.")
            return render(request, "authenticator/email_verification.html")

        current_site = get_current_site(request)
        subject = "Password Reset Request"
        message = render_to_string("pwd_reset_email.html", {
            'user': officer,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(officer.pk)),
            'token': default_token_generator.make_token(officer),
        })
        email = EmailMessage(subject, message, settings.EMAIL_HOST_USER, [officer.email])
        email.send()

        messages.success(request, "Password reset email sent.")

    return render(request, "authenticator/email_verification.html")


def pwdReset(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = Officer.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Officer.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            new_password = request.POST.get("new_pwd")
            confirm_password = request.POST.get("pwdRepeat")

            if new_password == confirm_password:
                user.set_password(new_password)
                user.save()
                messages.success(request, "Password reset successfully.")
                return redirect('login')
            else:
                messages.error(request, "Passwords do not match.")
        else:
            return render(request, "authenticator/password-reset.html")
    else:
        return render(request, "authenticator/reset_failed.html")
    



def create_file(request):
    fname = request.session.get('fname')
    if not fname:
        return redirect('login')

    if request.method == 'POST':
        form = AccidentFileForm(request.POST)
        if form.is_valid():
            AccidentFiles = form.save()
            try:
                fileName = AccidentFiles.name  # Access the specific field for file name
            except AttributeError:
                fileName = "File Name Not Available"  # Handle potential missing field

            try:
                abstract = AccidentFiles.abstract
            except AttributeError:
                abstract = "Abstract not provided"  # Set a default value or handle the error differently

            # Here's where you'd handle creating an actual file outside the database (optional)
            # (e.g., storing the file on the filesystem or using a cloud storage service)

            # Handle success (e.g., redirect to a success page)
            messages.success(request, "File Created successfully!")
            return redirect('index')
    else:
        form = AccidentFileForm()

    context = {'form': form, 'fname': fname}
    return render(request, 'authenticator/index.html', context)


def submit_abstract(request):
    if request.method == 'POST':
        # Bind the form with the POST data
        form = AccidentFileForm(request.POST)
        if form.is_valid():
            # Save the form data to the database
            accident_file = form.save()

            # Process and save additional data from the form
            # Example: Retrieve data from the submitted form
            officer_in_charge = request.POST.get('officer_in_charge')
            division = request.POST.get('division')
            pic_address = request.POST.get('picAddress')
            date = request.POST.get('date')
            our_ref = request.POST.get('our_ref')
            police_ref = request.POST.get('policeRef')
            victim_name = request.POST.get('victimName')
            victim_address = request.POST.get('victimAddress')
            date_of_accident = request.POST.get('date_of_accident')
            time_of_accident = request.POST.get('time_of_accident')
            place_of_accident = request.POST.get('place_of_accident')
            report_station = request.POST.get('reportStation')
            vehicle_owner = request.POST.get('vehicleOwner')
            vehicle_reg_no = request.POST.get('OwVehicleRegNo')
            insurance_company = request.POST.get('insuranceCompany')
            completed_inv = request.POST.get('completedInv')
            charged = request.POST.get('charged')
            charged_rider = request.POST.get('chargedRider')
            charged_vehicle = request.POST.get('chargedVehicle')
            charge_name = request.POST.get('chargeName')
            case_file_number = request.POST.get('caseFileNumber')
            investigation_officer = request.POST.get('investigationOfficer')
            investigation_result = request.POST.get('investigationResult')
            accident_reg_no = request.POST.get('accidentRegNo')
            charge_date = request.POST.get('chargeDate')
            injured_person = request.POST.get('injuredPerson')
            person_class = request.POST.get('personClass')
            person_address = request.POST.get('personAddress')
            injury_nature = request.POST.get('injuryNature')
            # Retrieve other form fields similarly
            
            # Create a new abstract file and save it
            # Example: Generate a report and save it to a file
            # For simplicity, let's assume you're just saving the form data to a text file
           # Create a new abstract file and save it
            # Example: Generate a report and save it to a file
            # For simplicity, let's assume you're just saving the form data to a text file
            with open('abstract_report.txt', 'a') as file:
                file.write(f"Officer in Charge: {officer_in_charge}\n")
                file.write(f"Division: {division}\n")
                file.write(f"P.O. Box: {pic_address}\n")
                file.write(f"Date: {date}\n")
                file.write(f"Our Reference No: {our_ref}\n")
                file.write(f"Police Reference No: {police_ref}\n")
                file.write(f"Victim Name: {victim_name}\n")
                file.write(f"Victim Address: {victim_address}\n")
                file.write(f"Date of Accident: {date_of_accident}\n")
                file.write(f"Time of Accident: {time_of_accident}\n")
                file.write(f"Place of Accident: {place_of_accident}\n")
                file.write(f"Report Station: {report_station}\n")
                file.write(f"Vehicle Owner: {vehicle_owner}\n")
                file.write(f"Vehicle Registration Number: {vehicle_reg_no}\n")
                file.write(f"Insurance Company: {insurance_company}\n")
                file.write(f"Completed Investigation: {completed_inv}\n")
                file.write(f"Charged: {charged}\n")
                file.write(f"Charged Rider: {charged_rider}\n")
                file.write(f"Charged Vehicle: {charged_vehicle}\n")
                file.write(f"Charge Name: {charge_name}\n")
                file.write(f"Case File Number: {case_file_number}\n")
                file.write(f"Investigation Officer: {investigation_officer}\n")
                file.write(f"Investigation Result: {investigation_result}\n")
                file.write(f"Accident Register/OB Number: {accident_reg_no}\n")
                file.write(f"Charge Date: {charge_date}\n")
                file.write(f"Injured Person: {injured_person}\n")
                file.write(f"Person Class: {person_class}\n")
                file.write(f"Person Address: {person_address}\n")
                file.write(f"Injury Nature: {injury_nature}\n")
                # Write other form field data similarly


            return redirect('success_url')  # Redirect to a success page or URL
    else:
        form = AccidentFileForm()
    return render(request, 'submit_abstract.html', {'form': form})
