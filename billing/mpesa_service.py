
import requests, base64
from datetime import datetime
from decouple import config
def get_access_token():
    key=config('MPESA_CONSUMER_KEY', default=''); secret=config('MPESA_CONSUMER_SECRET', default='')
    if not key: return None
    url='https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
    r=requests.get(url, auth=(key, secret)); return r.json().get('access_token')
def stk_push(phone, amount, callback_url):
    token=get_access_token()
    if not token: return {'error':'MPESA keys not set'}
    shortcode=config('MPESA_SHORTCODE', default='174379'); passkey=config('MPESA_PASSKEY', default='')
    timestamp=datetime.now().strftime('%Y%m%d%H%M%S')
    password=base64.b64encode(f"{shortcode}{passkey}{timestamp}".encode()).decode()
    payload={"BusinessShortCode":shortcode,"Password":password,"Timestamp":timestamp,"TransactionType":"CustomerPayBillOnline","Amount":int(amount),"PartyA":phone,"PartyB":shortcode,"PhoneNumber":phone,"CallBackURL":callback_url,"AccountReference":"AfyaCare","TransactionDesc":"Clinic Bill"}
    headers={'Authorization':f'Bearer {token}'}
    url='https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest'
    r=requests.post(url, json=payload, headers=headers); return r.json()
