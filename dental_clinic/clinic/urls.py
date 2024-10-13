from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about_us, name='about_us'),
    path('employee_menu/', views.employee_menu, name='employee_menu'),

    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('password_reset/', views.password_reset, name='password_reset'),

    path('doctors/', views.doctor_list, name='doctor_list'),
    path('doctors/<int:doctor_id>/', views.doctor_detail, name='doctor_detail'),

    path('services/', views.service_list, name='service_list'),
    path('services/<int:service_id>/', views.service_detail, name='service_detail'),

    path('patient/', views.patient_list, name='patient_list'),
    path('patient/new/', views.add_patient, name='add_patient'),
    path('patient/<int:patient_id>/', views.patient_detail, name='patient_detail'),
    path('patient/<int:patient_id>/edit/', views.edit_patient, name='edit_patient'),
    path('patient/<int:patient_id>/add_phone/', views.add_phone, name='add_phone'),
    path('phone/delete/<int:phone_id>/', views.delete_phone, name='delete_phone'),
    path('patient/<int:patient_id>/add_address/', views.add_address, name='add_address'),
    path('patient/<int:patient_id>/confirm_delete/', views.confirm_delete_patient, name='confirm_delete_patient'),
    path('patient/<int:patient_id>/delete/', views.delete_patient, name='delete_patient'),

    path('appointments/new/', views.create_appointment, name='create_appointment'),
    path('records/<int:record_id>/delete/', views.delete_record, name='delete_record'),

    path('reports/', views.report_generation, name='report_generation'),
]
