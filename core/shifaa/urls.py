from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('patients/', views.index, name='view_patients'),
    path('patients/add/', views.add_patient, name='add_patient'),
    path('patients/update/<int:patient_id>/', views.update_patient, name='update_patient'),
    path('patients/<int:patient_id>/', views.search_patient, name='view_patient'),
    path('patients/delete/<int:patient_id>/', views.delete_patient, name='delete_patient'),
]