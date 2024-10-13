from django.db import models
from django.contrib.auth.models import User


# class Person(models.Model):
#     LastName = models.CharField(max_length=100)
#     FirstName = models.CharField(max_length=100)
#     MiddleName = models.CharField(max_length=100, blank=True, null=True)
#
#     def __str__(self):
#         return f'{self.LastName} {self.FirstName}'


class Address(models.Model):
    Region = models.CharField(max_length=100)
    City = models.CharField(max_length=100)
    Street = models.CharField(max_length=100)
    House = models.IntegerField()
    Letter = models.CharField(max_length=10, blank=True, null=True)
    Building = models.IntegerField(blank=True, null=True)
    Apartment = models.IntegerField(blank=True, null=True)
    ZipCode = models.IntegerField()

    def __str__(self):
        return f'{self.City}, {self.Street}, {self.House}'


class Patient(models.Model):
    LastName = models.CharField(max_length=100)
    FirstName = models.CharField(max_length=100)
    MiddleName = models.CharField(max_length=100, blank=True, null=True)
    # Person = models.ForeignKey(Person, on_delete=models.CASCADE)
    BirthDate = models.DateField()
    Address = models.ForeignKey(Address, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return f'{self.LastName} {self.FirstName}'


class DoctorCategory(models.Model):
    Name = models.CharField(max_length=100)

    def __str__(self):
        return self.Name


class DoctorSpecialization(models.Model):
    Name = models.CharField(max_length=100)

    def __str__(self):
        return self.Name


class Doctor(models.Model):
    Photo = models.ImageField(upload_to='photos/doctor/', blank=True, null=True)  # Фото
    LastName = models.CharField(max_length=100)
    FirstName = models.CharField(max_length=100)
    MiddleName = models.CharField(max_length=100, blank=True, null=True)
    Category = models.ForeignKey(DoctorCategory, on_delete=models.PROTECT)
    Specialization = models.ForeignKey(DoctorSpecialization, on_delete=models.PROTECT)
    WorkSchedule = models.TextField()

    def __str__(self):
        return f'Dr. {self.LastName} {self.FirstName}'


class Phone(models.Model):
    Patient = models.ForeignKey(Patient, on_delete=models.CASCADE, blank=True, null=True)
    Doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, blank=True, null=True)
    Phone = models.CharField(max_length=15)
    Note = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f'{self.Phone} ({self.Note})'


class ChangeSchedule(models.Model):
    Doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    Absence = models.BooleanField(default=False)
    StartDate = models.DateField()
    EndDate = models.DateField()
    StartTime = models.TimeField(blank=True, null=True)
    EndTime = models.TimeField(blank=True, null=True)

    def __str__(self):
        return f'Schedule change for Dr. {self.Doctor}'


class Service(models.Model):
    Specialization = models.ForeignKey(DoctorSpecialization, on_delete=models.CASCADE)
    Name = models.CharField(max_length=255)
    Description = models.TextField()

    def __str__(self):
        return self.Name


class ServiceCost(models.Model):
    Service = models.ForeignKey(Service, on_delete=models.CASCADE)
    Category = models.ForeignKey(DoctorCategory, on_delete=models.CASCADE, blank=True, null=True)
    Cost = models.IntegerField()

    def __str__(self):
        return f'{self.Service} - {self.Cost}'


class Record(models.Model):
    Patient = models.ForeignKey(Patient, on_delete=models.PROTECT)
    Author = models.ForeignKey(User, on_delete=models.PROTECT)
    Doctor = models.ForeignKey(Doctor, on_delete=models.PROTECT)
    Date = models.DateField()
    Time = models.TimeField()
    Service = models.ForeignKey(Service, on_delete=models.PROTECT)

    def __str__(self):
        return f'Record for {self.Patient} with Dr. {self.Doctor}'


class RenderedService(models.Model):
    Record = models.ForeignKey(Record, on_delete=models.PROTECT)
    ServiceCost = models.ForeignKey(ServiceCost, on_delete=models.PROTECT)

    def __str__(self):
        return f'Service: {self.ServiceCost}'
