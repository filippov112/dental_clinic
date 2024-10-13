from django import forms
from django.contrib.auth.forms import AuthenticationForm as BaseAuthenticationForm
from .models import Patient, Record, Doctor
from .models import Phone, Address
import datetime


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Record
        fields = ['Patient', 'Doctor', 'Date', 'Time', 'Service']
        widgets = {
            'Date': forms.DateInput(attrs={'type': 'date'}),
            'Time': forms.TimeInput(attrs={'type': 'time'}),
        }

    def clean_date(self):
        date = self.cleaned_data.get('Date')
        if date < datetime.date.today():
            raise forms.ValidationError("Appointment date cannot be in the past.")
        return date


class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['LastName', 'FirstName', 'MiddleName', 'BirthDate']
        widgets = {
            'BirthDate': forms.DateInput(attrs={'type': 'date', 'placeholder': 'yyyy-mm-dd (DOB)'}),
        }

    def clean_birthdate(self):
        birthdate = self.cleaned_data.get('BirthDate')
        if birthdate >= datetime.date.today():
            raise forms.ValidationError("Birthdate cannot be today or in the future.")
        return birthdate


class AuthenticationForm(BaseAuthenticationForm):
    username = forms.CharField(
        label='Username',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'})
    )
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})
    )


class ReportForm(forms.Form):
    REPORT_CHOICES = [
        ('report_doctor_revenue', 'Doctor Revenue Report'),
        ('report_clinic_revenue', 'Clinic Revenue Report'),
        ('report_price_list', 'Price List Report')
    ]

    report_type = forms.ChoiceField(
        choices=REPORT_CHOICES,
        label="Report Type",
        widget=forms.Select(attrs={'onchange': 'updateFormFields()'})
    )

    doctor = forms.ModelChoiceField(
        queryset=Doctor.objects.all(),
        label="Doctor",
        required=False,
        widget=forms.Select()
    )

    month = forms.DateField(
        label="Month",
        required=False,
        widget=forms.SelectDateWidget(
            years=range(datetime.datetime.now().year - 10, datetime.datetime.now().year + 1),
            empty_label=("Year", "Month", "Day")
        )
    )

    def clean(self):
        cleaned_data = super().clean()
        report_type = cleaned_data.get('report_type')
        doctor = cleaned_data.get('doctor')
        month = cleaned_data.get('month')

        if report_type == 'report_doctor_revenue' and not doctor:
            self.add_error('doctor', 'Doctor is required for the Doctor Revenue report.')
        if report_type in ['report_doctor_revenue', 'report_clinic_revenue'] and not month:
            self.add_error('month', 'Month is required for this report.')

        return cleaned_data


class PhoneForm(forms.ModelForm):
    class Meta:
        model = Phone
        fields = ['Phone', 'Note']  # Include the fields you want in the form


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['Region', 'City', 'Street', 'House', 'Letter', 'Building', 'Apartment', 'ZipCode']