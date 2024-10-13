from django.contrib import admin
from .models import (
    Phone,
    Patient,
    Address,
    Doctor,
    ChangeSchedule,
    DoctorSpecialization,
    DoctorCategory,
    ServiceCost,
    Service,
    RenderedService,
    Record,
)

class DoctorAdmin(admin.ModelAdmin):
    list_display = ('id', 'LastName', 'FirstName', 'Category', 'Specialization', 'WorkSchedule')
    search_fields = ('LastName', 'FirstName', 'Category__Name', 'Specialization__Name')

class PatientAdmin(admin.ModelAdmin):
    list_display = ('id', 'LastName', 'FirstName', 'BirthDate', 'Address')
    search_fields = ('LastName', 'FirstName')

class ServiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'Name', 'Description', 'Specialization')
    search_fields = ('Name', 'Description')

# Register models with customized admin
admin.site.register(Phone)
admin.site.register(Patient, PatientAdmin)
admin.site.register(Address)
admin.site.register(Doctor, DoctorAdmin)
admin.site.register(ChangeSchedule)
admin.site.register(DoctorSpecialization)
admin.site.register(DoctorCategory)
admin.site.register(ServiceCost)
admin.site.register(Service, ServiceAdmin)
admin.site.register(RenderedService)
admin.site.register(Record)
