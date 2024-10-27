from django.shortcuts import render
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

API_URL = 'https://referralapp-production.up.railway.app/api/'
PATIENTS_ENDPOINT = 'patients/'
MEDICAL_ENDPONT = 'medical-history/'
DIAGNOSTICS_ENDPOINT = 'diagnostics/'
EQUIPMENT_ENDPOINT = 'equipment/'
REFERRALS_ENDPOINT = 'referrals/'
HOSPITALS_ENDPOINT = 'hospitals/'

TOKEN = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzMwNDM5MTEwLCJpYXQiOjE3Mjk1NzUxMTAsImp0aSI6ImE2MTUwYmRjNzI5NzQ4NzI4ZjdlOTZkZjg0MTU3NjQxIiwidXNlcl9pZCI6Mn0.wLNg6ggBbG1k8RWfJExkZhuvN32m5DE6p10NcbPhzPA'

#Function to make authorized requests
# def authorized_request(method, url, data=None):
#     headers = {
#         'Authorization': f'Bearer {TOKEN}'
#     }
    
#     if method == 'GET':
#         return requests.get(url, headers=headers)
#     elif method == 'POST':
#         return requests.post(url, headers=headers, data=data)
#     elif method == 'PUT':
#         return requests.put(url, headers=headers, data=data)
#     elif method == 'DELETE':
#         return requests.delete(url, headers=headers)

def authorized_request(method, url, data=None):
    headers = {
        'Authorization': f'Bearer {TOKEN}'
    }
    
    try:
        if method == 'GET':
            response = requests.get(url, headers=headers)
        elif method == 'POST':
            response = requests.post(url, headers=headers, data=data)
        elif method == 'PUT':
            response = requests.put(url, headers=headers, data=data)
        elif method == 'DELETE':
            response = requests.delete(url, headers=headers)
        
        response.raise_for_status()
        return response

    except requests.exceptions.HTTPError as errh:
        print ("Http Error:", errh)
    except requests.exceptions.ConnectionError as errc:
        print ("Error Connecting:", errc)
    except requests.exceptions.Timeout as errt:
        print ("Timeout Error:", errt)
    except requests.exceptions.RequestException as err:
        print ("Something Else:", err)
    
    if response.status_code == 400:
        print(f"Error Response: {response.text}")
    
    return response



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
            
        elif data_type == 'referrals':
            response = authorized_request('GET', f'{API_URL}{REFERRALS_ENDPOINT}')
            if response.status_code == 200:
                referrals = referrals.json()
                return JsonResponse({'referrals': referrals})
            else:
                return JsonResponse({'error': 'Unable to fetch referrals'}, status=response.status_code)
        
        else:
            return JsonResponse({'error': 'Invalid data type requested'}, status=400)
    else:
        # Render the index.html template when it's a standard request
        return render(request, 'index.html')
    


def base_view(request):
    if request.method == 'GET' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        # Determine 
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
            
        elif data_type == 'referrals':
            response = authorized_request('GET', f'{API_URL}{REFERRALS_ENDPOINT}')
            if response.status_code == 200:
                referrals = referrals.json()
                return JsonResponse({'referrals': referrals})
            else:
                return JsonResponse({'error': 'Unable to fetch referrals'}, status=response.status_code)
        
        else:
            return JsonResponse({'error': 'Invalid data type requested'}, status=400)
    else:
        # Render 
        return render(request, 'index copy.html')


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
    
# def list_referrals(request):
#     if request.method == 'GET' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
#         response = authorized_request('GET', f'{API_URL}{REFERRALS_ENDPOINT}')
#         if response.status_code == 200:
#             referral_list = response.json()
#             return JsonResponse({'referrals': referral_list})
#         else:
#             return JsonResponse({'error': 'Unable to fetch referrals'}, status=response.status_code)
#     else:
#         return JsonResponse({'error': 'Invalid request method'}, status=405)

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
            'gender': request.POST.get('gender', '').capitalize(),
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

def get_diagnostics(request, patient_id):
    if request.method == 'GET':
        response = authorized_request('GET', f'{API_URL}{DIAGNOSTICS_ENDPOINT}?patient={patient_id}')
        if response.status_code == 200:
            diagnostics_list = response.json()
            return JsonResponse({'status': 'success', 'diagnostics': diagnostics_list})
        else:
            return JsonResponse({'status': 'error', 'message': response.text}, status=response.status_code)

def get_medicals(request, patient_id):
    if request.method == 'GET':
        response = authorized_request('GET', f'{API_URL}{MEDICAL_ENDPONT}?patient={patient_id}')
        if response.status_code == 200:
            medics_list = response.json()
            return JsonResponse({'status': 'success', 'medicals': medics_list})
        else:
            return JsonResponse({'status': 'error', 'message': response.text}, status=response.status_code)
        

#https://referralapp-production.up.railway.app/api/hospitals/?name=Mwaiwathu
        

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


@csrf_exempt
def add_diagnostic(request, patient_id):
    if request.method == 'POST':
        diagnostic_data = {
            'patient': patient_id,
            'diagnostic_type': request.POST.get('diagnostic_type', ''),
            'result': request.POST.get('result', ''),
            'date_taken': request.POST.get('date_taken', ''),
            'notes': request.POST.get('notes', '')
        }
        response = authorized_request('POST', f'{API_URL}{DIAGNOSTICS_ENDPOINT}', data=diagnostic_data)
        if response.status_code == 201:
            return JsonResponse({'status': 'success', 'data': response.json()}, status=201)
        else:
            return JsonResponse({'status': 'error', 'message': response.text}, status=response.status_code)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)


@csrf_exempt
def add_referral(request, patient_id):
    if request.method == 'POST':
        referral_data = {
            'patient': patient_id,
            'referred_from': 2,
            'referred_to': request.POST.get('referred_to', ''),
            'referral_reason': request.POST.get('referral_reason', ''),
            'referral_date': request.POST.get('referral_date', ''),
            'status': 'Pending'
        }
        response = authorized_request('POST', f'{API_URL}{REFERRALS_ENDPOINT}', data=referral_data)
        if response.status_code == 201:
            return JsonResponse({'status': 'success', 'data': response.json()}, status=201)
        else:
            return JsonResponse({'status': 'error', 'message': response.text}, status=response.status_code)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)


@csrf_exempt
def add_medical_history(request, patient_id):
    if request.method == 'POST':
        medical_data = {
            'patient': patient_id,
            'condition': request.POST.get('condition', ''),
            'treatment': request.POST.get('treatment', ''),
            'start_date': request.POST.get('start_date', ''),
            'end_date': request.POST.get('end_date', None),
            'notes': request.POST.get('notes', '')
        }
        response = authorized_request('POST', f'{API_URL}{MEDICAL_ENDPONT}', data=medical_data)
        if response.status_code == 201:
            return JsonResponse({'status': 'success', 'data': response.json()}, status=201)
        else:
            return JsonResponse({'status': 'error', 'message': response.text}, status=response.status_code)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)
    
    

def list_referrals(request):
    response = authorized_request('GET', f'{API_URL}{REFERRALS_ENDPOINT}')
    if response.status_code == 200:
        referrals = response.json()

       
        for referral in referrals:
            patient_id = referral['patient']
            referred_from_id = referral['referred_from']
            referred_to_id = referral['referred_to']
            
            
            patient_response = authorized_request('GET', f'{API_URL}{PATIENTS_ENDPOINT}{patient_id}/')
            if patient_response.status_code == 200:
                patient_data = patient_response.json()
                referral['patient_name'] = f"{patient_data['first_name']} {patient_data['last_name']}"
            else:
                referral['patient_name'] = 'Unknown'

            from_hospital_response = authorized_request('GET', f'{API_URL}{HOSPITALS_ENDPOINT}{referred_from_id}/')
            if from_hospital_response.status_code == 200:
                referral['referred_from_name'] = from_hospital_response.json()['name']
            else:
                referral['referred_from_name'] = 'Unknown'

            
            to_hospital_response = authorized_request('GET', f'{API_URL}{HOSPITALS_ENDPOINT}{referred_to_id}/')
            if to_hospital_response.status_code == 200:
                referral['referred_to_name'] = to_hospital_response.json()['name']
            else:
                referral['referred_to_name'] = 'Unknown'

        return JsonResponse({'referrals': referrals})
    else:
        return JsonResponse({'error': 'Unable to fetch referrals'}, status=response.status_code)


@csrf_exempt
def update_referral(request, referral_id):
    if request.method == 'POST':
        # Fetch existing referral
        referral_response = authorized_request('GET', f'{API_URL}{REFERRALS_ENDPOINT}{referral_id}/')
        if referral_response.status_code == 200:
            referral = referral_response.json()

            
            if referral['referred_to'] == 2 and referral['status'] == 'Pending':
                referral['status'] = 'Accepted'
                update_response = authorized_request('PUT', f'{API_URL}{REFERRALS_ENDPOINT}{referral_id}/', data=referral)
                if update_response.status_code == 200:
                    return JsonResponse({'status': 'success', 'message': 'Referral accepted'})
                else:
                    return JsonResponse({'status': 'error', 'message': 'Unable to update referral'}, status=update_response.status_code)
            else:
                return JsonResponse({'status': 'error', 'message': 'Invalid referral update'}, status=400)
        else:
            return JsonResponse({'status': 'error', 'message': 'Referral not found'}, status=referral_response.status_code)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)
    
