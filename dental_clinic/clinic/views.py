# views.py
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import (
    Doctor, Service, Patient, Record, ChangeSchedule,
    DoctorCategory, DoctorSpecialization, ServiceCost, Address, Phone
)
from .forms import (
    AppointmentForm, PatientForm, AuthenticationForm, ReportForm, AddressForm, PhoneForm
)

from django.db.models import Sum
import datetime
import pdfkit
from django.template.loader import get_template

from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.contrib import messages
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.conf import settings
from django import forms


def home(request):
    """
    Renders the home page with navigation buttons.
    """
    return render(request, 'clinic/home.html')


def login_view(request):
    """
    Handles user authentication.
    """
    if request.user.is_authenticated:
        return redirect('employee_menu')

    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('employee_menu')
    else:
        form = AuthenticationForm()

    return render(request, 'clinic/login.html', {'form': form})


def logout_view(request):
    """
    Logs out the user.
    """
    logout(request)
    return redirect('home')


def doctor_list(request):
    """
    Displays a list of doctors with optional search filters.
    """
    doctors = Doctor.objects.all()
    specializations = DoctorSpecialization.objects.all()
    categories = DoctorCategory.objects.all()

    # Search filters
    specialization = request.GET.get('specialization')
    if specialization:
        doctors = doctors.filter(Specialization=DoctorSpecialization.objects.get(id=specialization))

    category = request.GET.get('category')
    if category:
        doctors = doctors.filter(Category=DoctorCategory.objects.get(id=category))

    return render(request, 'clinic/doctor_list.html', {'doctors': doctors, 'specializations': specializations, 'categories':categories})


def doctor_detail(request, doctor_id):
    """
    Shows detailed information about a specific doctor, including schedule changes.
    """
    doctor = get_object_or_404(Doctor, pk=doctor_id)
    schedule_changes = ChangeSchedule.objects.filter(Doctor=doctor)

    return render(request, 'clinic/doctor_detail.html', {
        'doctor': doctor,
        'schedule_changes': schedule_changes
    })


def service_list(request):
    search_query = request.GET.get('search', '')
    specialization_id = request.GET.get('specialization', '')

    services = Service.objects.all()

    if search_query:
        services = services.filter(Name__icontains=search_query)

    if specialization_id:
        services = services.filter(Specialization_id=specialization_id)

    paginator = Paginator(services, 9)  # 9 services per page
    page = request.GET.get('page')
    services = paginator.get_page(page)

    specializations = DoctorSpecialization.objects.all()

    context = {
        'services': services,
        'specializations': specializations
    }
    return render(request, 'clinic/service_list.html', context)


def service_detail(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    service_prices = ServiceCost.objects.filter(Service=service)
    related_services = Service.objects.filter(Specialization=service.Specialization).exclude(id=service.id)

    context = {
        'service': service,
        'service_prices': service_prices,
        'related_services': related_services
    }
    return render(request, 'clinic/service_detail.html', context)


def about_us(request):
    """
    Renders the 'About Us' page with clinic and contact information.
    """
    return render(request, 'clinic/about.html')


@login_required
def employee_menu(request):
    """
    Displays the employee menu with access to additional functionalities.
    """
    return render(request, 'clinic/employee_menu.html')


@login_required
def create_appointment(request):
    """
    Handles the creation of a new doctor's appointment.
    """
    if request.method == "POST":
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.Author = request.user
            appointment.save()
            return redirect('patient_detail', patient_id=request.POST.get('Patient'))
    else:
        form = AppointmentForm()

    return render(request, 'clinic/create_appointment.html', {'form': form})


@login_required
def patient_list(request):
    query = request.GET.get('q', '')
    patient_list = Patient.objects.filter(LastName__icontains=query)  # Search functionality
    paginator = Paginator(patient_list, 10)  # 10 patients per page
    page_number = request.GET.get('page')
    patients = paginator.get_page(page_number)

    # Search filters
    last_name = request.GET.get('LastName')
    if last_name:
        patients = patients.filter(LastName__icontains=last_name)

    first_name = request.GET.get('FirstName')
    if first_name:
        patients = patients.filter(FirstName__icontains=first_name)

    context = {
        'patients': patients,
    }
    return render(request, 'clinic/patient_list.html', context)


@login_required
def patient_detail(request, patient_id):
    """
    Shows detailed information about a specific patient, including records.
    """
    patient = get_object_or_404(Patient, pk=patient_id)
    records = Record.objects.filter(Patient=patient)

    return render(request, 'clinic/patient_detail.html', {
        'patient': patient,
        'records': records
    })


@login_required
def delete_record(request, record_id):
    """
    Deletes a specific medical record associated with a patient.
    """
    record = get_object_or_404(Record, pk=record_id)
    if request.method == 'POST':
        record.delete()
        return redirect('patient_detail', patient_id=record.Patient.id)

    return render(request, 'clinic/delete_record_confirm.html', {'record': record})


@login_required
def add_patient(request):
    """
    Handles the addition of a new patient.
    """
    if request.method == "POST":
        form = PatientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('patient_list')
    else:
        form = PatientForm()

    return render(request, 'clinic/add_patient.html', {'form': form})


@login_required
def edit_patient(request, patient_id):
    """
    Handles editing an existing patient's information.
    """
    patient = get_object_or_404(Patient, pk=patient_id)
    if request.method == "POST":
        form = PatientForm(request.POST, instance=patient)
        if form.is_valid():
            form.save()
            return redirect('patient_detail', patient_id=patient.id)
    else:
        form = PatientForm(instance=patient)

    return render(request, 'clinic/edit_patient.html', {
        'form': form,
        'patient': patient
    })


def render_pdf(url_template, contexto):
    template = get_template(url_template)
    html = template.render(contexto)
    return pdfkit.from_string(
        html,
        False,
        options={'encoding': "utf-8", },
        configuration=pdfkit.configuration(wkhtmltopdf=settings.WKHTMLTOPDF_PATH),
        css=settings.STATIC_ROOT + "/../mainapp/static/reports/css/reports.css"
    )


def get_context_report(report, doctor=None, month=None):
    if report == 'report_doctor_revenue':
        # Ensure both doctor and month are provided for this report
        if not doctor or not month:
            raise ValueError("Doctor and Month are required for this report.")

        # Filter records for the given doctor and month
        records = Record.objects.filter(Doctor=doctor, Date__month=month.month, Date__year=month.year)
        total_revenue = records.aggregate(total=Sum('renderedservice__ServiceCost__Cost'))['total'] or 0

        # Prepare the context for the report
        context = {
            'doctor': doctor,
            'month': month.strftime('%B %Y'),
            'total_revenue': total_revenue,
        }

    elif report == 'report_clinic_revenue':
        # Ensure month is provided for this report
        if not month:
            raise ValueError("Month is required for this report.")

        # Filter all records for the clinic for the given month
        records = Record.objects.filter(Date__month=month.month, Date__year=month.year)
        total_revenue = records.aggregate(total=Sum('renderedservice__ServiceCost__Cost'))['total'] or 0

        # Prepare the context for the clinic revenue report
        context = {
            'month': month.strftime('%B %Y'),
            'total_revenue': total_revenue,
        }

    elif report == 'report_price_list':
        # Get all services and their prices by category and specialization
        services = ServiceCost.objects.select_related('Service', 'Category', 'Service__Specialization')

        # Prepare the context for the price list report
        context = {
            'services': services,
        }

    else:
        raise ValueError("Invalid report type.")

    return context


from datetime import datetime
@login_required
def report_generation(request):
    """
    Handles the selection and generation of various reports.
    """
    if request.method == 'POST':
        post = {
            'month': datetime.strptime(request.POST.get('month', '1900-01'), '%Y-%m'),
            'report_type': request.POST.get('report_type', ''),
            'doctor': request.POST.get('doctor', None)
        }
        form = ReportForm(post)
        if form.is_valid():
            report_type = form.cleaned_data['report_type']
            doctor = form.cleaned_data.get('doctor')
            month = form.cleaned_data.get('month')

            # Validate month and year for specific reports
            if report_type in ['report_doctor_revenue', 'report_clinic_revenue'] and not month:
                form.add_error(None, 'Month and Year are required for this report.')
            else:
                try:
                    # Get context based on report type
                    context = get_context_report(report_type, doctor, month)

                    # Map report type to corresponding template
                    template_map = {
                        'report_doctor_revenue': 'clinic/report_doctor_revenue.html',
                        'report_clinic_revenue': 'clinic/report_clinic_revenue.html',
                        'report_price_list': 'clinic/report_price_list.html',
                    }

                    template = template_map.get(report_type)

                    # Generate PDF
                    pdf = render_pdf(template, context)
                    response = HttpResponse(pdf, content_type="application/pdf")
                    response['Content-Disposition'] = "attachment;"
                    return response

                except ValueError as e:
                    form.add_error(None, str(e))

    form = ReportForm()
    doctors = Doctor.objects.all()
    return render(request, 'clinic/report_generation.html', {'form': form, 'doctors': doctors})


class PasswordResetForm(forms.Form):
    email = forms.EmailField(label="Email", max_length=254)


def password_reset(request):
    if request.method == "POST":
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = User.objects.get(email=email)
                # Generate token and uid
                token = default_token_generator.make_token(user)
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                reset_link = f"{request.scheme}://{request.get_host()}/reset/{uid}/{token}/"

                # Email content
                subject = "Password Reset Request"
                message = render_to_string('clinic/password_reset_email.html', {
                    'user': user,
                    'reset_link': reset_link,
                })

                send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])
                messages.success(request, "Password reset link sent to your email.")
                return redirect('login')  # Redirect to login page
            except User.DoesNotExist:
                messages.error(request, "No user found with this email.")
    else:
        form = PasswordResetForm()
    return render(request, 'clinic/password_reset.html', {'form': form})


def add_phone(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)

    if request.method == "POST":
        form = PhoneForm(request.POST)
        if form.is_valid():
            phone = form.save(commit=False)
            phone.Patient = patient  # Associate the phone number with the patient
            phone.save()
            messages.success(request, "Phone number added successfully.")
            return redirect('patient_detail', patient_id=patient.id)  # Redirect to patient detail page
    else:
        form = PhoneForm()

    return render(request, 'clinic/add_phone.html', {'form': form, 'patient': patient})


def add_address(request, patient_id):
    # Get the patient object
    patient = get_object_or_404(Patient, id=patient_id)

    if request.method == "POST":
        form = AddressForm(request.POST)

        if form.is_valid():
            # Delete the old address if it exists
            if patient.Address:
                patient.Address.delete()

            # Create a new address object but don't save it yet
            address = form.save()

            # Link the new address to the patient and save the patient
            patient.Address = address
            patient.save()

            messages.success(request, "Address successfully added/updated.")
            return redirect('patient_detail', patient_id=patient.id)
    else:
        # If there is an existing address, prepopulate the form with it
        if patient.Address:
            form = AddressForm(instance=patient.Address)
        else:
            form = AddressForm()

    return render(request, 'clinic/add_address.html', {'form': form, 'patient': patient})


def confirm_delete_patient(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    return render(request, 'clinic/confirm_delete.html', {'patient': patient})


def delete_patient(request, patient_id):
    # Check if the request is a POST request
    if request.method == "POST":
        # Retrieve the patient object or return a 404 if not found
        patient = get_object_or_404(Patient, id=patient_id)
        # Delete the patient
        patient.delete()
        # Show a success message
        messages.success(request, "Patient deleted successfully.")
        # Redirect to the patient list
        return redirect('patient_list')
    else:
        # If the request is not POST, redirect back to the patient detail or list
        messages.error(request, "Invalid request method.")
        return redirect('patient_list')


def delete_phone(request, phone_id):
    """
    Deletes a phone number based on the provided phone ID.
    Redirects back to the patient detail page with a success message.
    """
    phone = get_object_or_404(Phone, id=phone_id)

    # Save the patient ID for redirection after deletion
    patient_id = phone.Patient.id

    # Delete the phone object
    phone.delete()

    # Add a success message
    messages.success(request, 'Phone number deleted successfully.')

    # Redirect to the patient detail page
    return redirect('patient_detail', patient_id=patient_id)

