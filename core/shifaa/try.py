from django.shortcuts import render
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

API_URL = 'https://referralapp-production.up.railway.app/api/'
PATIENTS_ENDPOINT = 'patients/'
MEDICAL_ENDPONT = 'medical-history/'
DIAGNOSTICS_ENDPOINT = 'diagnostics/'
EQUIPMENT_ENDPOINT = 'equipment/'
REFERRALS_ENDPONT = 'referrals/'

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



def index(request):
    if request.method == 'GET' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        # Determine if the request is for patients or equipment based on a query parameter or similar
        data_type = request.GET.get('data_type', None)
        
        if data_type == 'patients':
            response = authorized_request('GET', f'{API_URL}{PATIENTS_ENDPOINT}')
            if response.status_code == 200:
                patients = response.json()
                return JsonResponse({'patients': patients})
            else:
                return JsonResponse({'error': 'Unable to fetch patients'}, status=response.status_code)

        elif data_type == 'equipment':
            response = authorized_request('GET', f'{API_URL}{EQUIPMENT_ENDPOINT}')
            if response.status_code == 200:
                equipment = response.json()
                return JsonResponse({'equipment': equipment})
            else:
                return JsonResponse({'error': 'Unable to fetch equipment'}, status=response.status_code)
        else:
            return JsonResponse({'error': 'Invalid data type requested'}, status=400)
    else:
        # Render the index.html template when it's a standard request
        return render(request, 'index.html')

# Function to list all patients
def list_patients(request):
    if request.method == 'GET' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        response = authorized_request('GET', f'{API_URL}{PATIENTS_ENDPOINT}')
        if response.status_code == 200:
            patient_list = response.json()
            return JsonResponse({'patients': patient_list})
        else:
            return JsonResponse({'error': 'Unable to fetch patients'}, status=response.status_code)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)

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
        response = authorized_request('POST', f'{API_URL}{PATIENTS_ENDPOINT}', data=patient_data)
        if response.status_code == 201:
            return JsonResponse({'status': 'success', 'data': response.json()}, status=201)
        else:
            return JsonResponse({'status': 'error', 'message': response.text}, status=response.status_code)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)


@csrf_exempt
def update_patient(request, patient_id):
    if request.method == 'POST':
        update_data = {
            'first_name': request.POST.get('first_name', ''),
            'last_name': request.POST.get('last_name', ''),
            'dob': request.POST.get('dob', ''),
            'gender': request.POST.get('gender', ''),
            'contact_info': request.POST.get('contact_info', '')
        }
        response = authorized_request('PUT', f'{API_URL}{PATIENTS_ENDPOINT}{patient_id}/', data=update_data)
        if response.status_code == 200:
            return JsonResponse({'status': 'success', 'data': response.json()})
        else:
            return JsonResponse({'status': 'error', 'message': response.text}, status=response.status_code)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)

@csrf_exempt
def delete_patient(request, patient_id):
    if request.method == 'POST':
        response = authorized_request('DELETE', f'{API_URL}{PATIENTS_ENDPOINT}{patient_id}/')
        if response.status_code == 204:
            return JsonResponse({'status': 'success', 'message': 'Patient deleted'}, status=204)
        else:
            return JsonResponse({'status': 'error', 'message': response.text}, status=response.status_code)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)


def search_patient(request, patient_id):
    if request.method == 'GET':
        response = authorized_request('GET', f'{API_URL}{PATIENTS_ENDPOINT}{patient_id}/')
        if response.status_code == 200:
            patient = response.json()
            return JsonResponse({'status': 'success', 'patient': patient})
        else:
            return JsonResponse({'status': 'error', 'message': response.text}, status=response.status_code)
        

def list_equipment(request):
    if request.method == 'GET' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        response = authorized_request('GET', f'{API_URL}{EQUIPMENT_ENDPOINT}')
        if response.status_code == 200:
            equipment_list = response.json()
            return JsonResponse({'equipment': equipment_list})
        else:
            return JsonResponse({'error': 'Unable to fetch equipment'}, status=response.status_code)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)

@csrf_exempt
def add_equipment(request):
    if request.method == 'POST':
        equipment_data = {
            'hospital': 2,  # Hardcoded hospital ID
            'equipment_name': request.POST.get('equipment_name', ''),
            'description': request.POST.get('description', ''),
            'available': request.POST.get('available', 'true').lower() == 'true'
        }
        response = authorized_request('POST', f'{API_URL}{EQUIPMENT_ENDPOINT}', data=equipment_data)
        if response.status_code == 201:
            return JsonResponse({'status': 'success', 'data': response.json()}, status=201)
        else:
            return JsonResponse({'status': 'error', 'message': response.text}, status=response.status_code)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)

@csrf_exempt
def update_equipment(request, equipment_id):
    if request.method == 'POST':
        update_data = {
            'hospital': 2,  # Hardcoded hospital ID
            'equipment_name': request.POST.get('equipment_name', ''),
            'description': request.POST.get('description', ''),
            'available': request.POST.get('available', 'true').lower() == 'true'
        }
        response = authorized_request('PUT', f'{API_URL}{EQUIPMENT_ENDPOINT}{equipment_id}/', data=update_data)
        if response.status_code == 200:
            return JsonResponse({'status': 'success', 'data': response.json()})
        else:
            return JsonResponse({'status': 'error', 'message': response.text}, status=response.status_code)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)

@csrf_exempt
def delete_equipment(request, equipment_id):
    if request.method == 'POST':
        response = authorized_request('DELETE', f'{API_URL}{EQUIPMENT_ENDPOINT}{equipment_id}/')
        if response.status_code == 204:
            return JsonResponse({'status': 'success', 'message': 'Equipment deleted'}, status=204)
        else:
            return JsonResponse({'status': 'error', 'message': response.text}, status=response.status_code)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)
