
import base64, requests, datetime
from django.conf import settings

def get_mpesa_token():
    env = settings.MPESA_ENV
    url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials" if env == "sandbox" else "https://api.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
    try:
        r = requests.get(url, auth=(settings.MPESA_CONSUMER_KEY, settings.MPESA_CONSUMER_SECRET), timeout=15)
        r.raise_for_status()
        return r.json().get("access_token")
    except Exception as e:
        print(f"Token error: {e}")
        return None

def stk_push(phone, amount, bill_id, description="AfyaCare Bill"):
    token = get_mpesa_token()
    if not token:
        return {"success": False, "message": "Could not get MPESA token - check CONSUMER_KEY/SECRET in Render"}

    # Format phone to 254...
    phone = phone.strip().replace(" ", "")
    if phone.startswith("0"):
        phone = "254" + phone[1:]
    if phone.startswith("+"):
        phone = phone[1:]
    
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    password_str = settings.MPESA_SHORTCODE + settings.MPESA_PASSKEY + timestamp
    password = base64.b64encode(password_str.encode()).decode()

    env = settings.MPESA_ENV
    url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest" if env == "sandbox" else "https://api.safaricom.co.ke/mpesa/stkpush/v1/processrequest"

    payload = {
        "BusinessShortCode": settings.MPESA_SHORTCODE,
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": int(float(amount)),
        "PartyA": phone,
        "PartyB": settings.MPESA_SHORTCODE,
        "PhoneNumber": phone,
        "CallBackURL": settings.MPESA_CALLBACK_URL,
        "AccountReference": f"AFYA{bill_id}",
        "TransactionDesc": description[:20]
    }

    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    try:
        r = requests.post(url, json=payload, headers=headers, timeout=20)
        data = r.json()
        print(f"STK Response: {data}")
        if data.get("ResponseCode") == "0":
            return {"success": True, "checkout_id": data.get("CheckoutRequestID"), "message": data.get("CustomerMessage")}
        else:
            return {"success": False, "message": data.get("errorMessage") or data.get("ResponseDescription") or str(data)}
    except Exception as e:
        return {"success": False, "message": str(e)}
