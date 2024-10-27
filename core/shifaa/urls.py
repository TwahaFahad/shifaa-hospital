from django.urls import path
from ..appcore.old import views

urlpatterns = [
    path('', views.index, name='index'),
    
    path('patients/', views.list_patients, name='list_patients'),
    path('patients/add/', views.add_patient, name='add_patient'),
    path('patients/update/<int:patient_id>/', views.update_patient, name='update_patient'),
    path('patients/delete/<int:patient_id>/', views.delete_patient, name='delete_patient'),
    
    path('equipment/', views.list_equipment, name='list_equipment'),
    path('equipment/add/', views.add_equipment, name='add_equipment'),
    path('equipment/update/<int:equipment_id>/', views.update_equipment, name='update_equipment'),
    path('equipment/delete/<int:equipment_id>/', views.delete_equipment, name='delete_equipment'),
    
    path('patients/<int:patient_id>/diagnostic/add/', views.add_diagnostic, name='add_diagnostic'),
    path('patients/<int:patient_id>/referral/add/', views.add_referral, name='add_referral'),
    path('patients/<int:patient_id>/history/add/', views.add_medical_history, name='add_medical_history'),
    
    path('referrals/', views.list_referrals, name='list_referrals'),
    path('referrals/update/<int:referral_id>/', views.update_referral, name='update_referral'),
    
    path('patients/<int:patient_id>/diagnostic/', views.get_diagnostics, name='patient_diagnostic'),
    
    path('patients/<int:patient_id>/medicals/', views.get_medicals, name='patient_medicals'),
    
    path('base/', views.base_view, name='base'),
]