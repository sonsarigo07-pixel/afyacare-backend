import base64, requests, datetime
from django.conf import settings
from decouple import config

def get_mpesa_token():
    consumer_key = settings.MPESA_CONSUMER_KEY
    consumer_secret = settings.MPESA_CONSUMER_SECRET
    env = settings.MPESA_ENV
    base_url = 'https://sandbox.safaricom.co.ke' if env=='sandbox' else 'https://api.safaricom.co.ke'
    url = f"{base_url}/oauth/v1/generate?grant_type=client_credentials"
    r = requests.get(url, auth=(consumer_key, consumer_secret))
    r.raise_for_status()
    return r.json()['access_token'], base_url

def stk_push(phone, amount, account_ref, description="AfyaCare Payment"):
    token, base_url = get_mpesa_token()
    shortcode = settings.MPESA_SHORTCODE
    passkey = settings.MPESA_PASSKEY
    timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    password = base64.b64encode(f"{shortcode}{passkey}{timestamp}".encode()).decode()

    # Normalize phone to 2547XXXXXXXX
    if phone.startswith('0'): phone = '254' + phone[1:]
    if phone.startswith('+'): phone = phone[1:]

    headers = {'Authorization': f'Bearer {token}'}
    payload = {
        "BusinessShortCode": shortcode,
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": int(amount),
        "PartyA": phone,
        "PartyB": shortcode,
        "PhoneNumber": phone,
        "CallBackURL": settings.MPESA_CALLBACK_URL,
        "AccountReference": account_ref,
        "TransactionDesc": description
    }
    url = f"{base_url}/mpesa/stkpush/v1/processrequest"
    resp = requests.post(url, json=payload, headers=headers)
    return resp.json()
