from django.shortcuts import render
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

API_URL = 'https://referralapp-production.up.railway.app/api/patients/'

TOKEN = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzI5NDk2MjIwLCJpYXQiOjE3Mjg2MzIyMjAsImp0aSI6Ijc5YjAxZmY3ZDFkMDQ3MTJhODZjYmU3NzdlNTBjZjUxIiwidXNlcl9pZCI6Mn0.B41AhET49y_uhut7FfHFvu3VeWGpdR4k83f5itvn404'

# Function to make authorized requests
def authorized_request(method, url, data=None):
    headers = {
        'Authorization': f'Bearer {TOKEN}'
    }
    
    if method == 'GET':
        return requests.get(url, headers=headers)
    elif method == 'POST':
        return requests.post(url, headers=headers, data=data)
    elif method == 'PUT':
        return requests.put(url, headers=headers, data=data)
    elif method == 'DELETE':
        return requests.delete(url, headers=headers)

# View all patients
def index(request):
    if request.method == 'GET':
        response = authorized_request('GET', API_URL)
        if response.status_code == 200:
            patients = response.json()
            return render(request, 'index.html', {'patients': patients})
        else:
            return JsonResponse({'error': 'Unable to fetch patients'}, status=response.status_code)

# Add a new patient
@csrf_exempt
def add_patient(request):
    if request.method == 'POST':
        patient_data = {
            'first_name': request.POST.get('first_name', ''),
            'last_name': request.POST.get('last_name', ''),
            'dob': request.POST.get('dob', ''),
            'gender': request.POST.get('gender', ''),
            'contact_info': request.POST.get('contact_info', ''),
        }
        response = authorized_request('POST', API_URL, data=patient_data)
        if response.status_code == 201:
            return JsonResponse({'status': 'success', 'data': response.json()}, status=201)
        else:
            return JsonResponse({'status': 'error', 'message': response.text}, status=response.status_code)

# Update an existing patient
@csrf_exempt
def update_patient(request, patient_id):
    if request.method == 'POST':
        update_data = {
            'first_name': request.POST.get('first_name', ''),
            'last_name': request.POST.get('last_name', ''),
            'dob': request.POST.get('dob', ''),
            'gender': request.POST.get('gender', ''),
            'contact_info': request.POST.get('contact_info', ''),
        }
        response = authorized_request('PUT', f'{API_URL}{patient_id}/', data=update_data)
        if response.status_code == 200:
            return JsonResponse({'status': 'success', 'data': response.json()})
        else:
            return JsonResponse({'status': 'error', 'message': response.text}, status=response.status_code)

# Delete a patient
@csrf_exempt
def delete_patient(request, patient_id):
    if request.method == 'POST':
        response = authorized_request('DELETE', f'{API_URL}{patient_id}/')
        if response.status_code == 204:
            return JsonResponse({'status': 'success', 'message': 'Patient deleted'}, status=204)
        else:
            return JsonResponse({'status': 'error', 'message': response.text}, status=response.status_code)
