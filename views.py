
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from .models import Bill
from .serializers import BillSerializer
from .mpesa_service import stk_push

@api_view(['GET'])
def health_check(request):
    return Response({"status": "online", "backend": "AfyaCare v10.25", "supabase": "connected"})

@api_view(['POST'])
def create_bill_and_push(request):
    try:
        data = request.data
        phone = data.get('phone')
        amount = data.get('amount')
        patient_name = data.get('patient_name','Patient')
        description = data.get('description','Clinic Bill')

        if not phone or not amount:
            return Response({"success": False, "message": "Phone and amount required"}, status=400)

        bill = Bill.objects.create(
            patient_name=patient_name,
            phone=phone,
            amount=amount,
            description=description,
            status='pending'
        )

        result = stk_push(phone, amount, bill.id, description)

        if result.get('success'):
            bill.mpesa_checkout_id = result.get('checkout_id','')
            bill.save()
            return Response({
                "success": True,
                "message": "✅ REAL STK Push Sent! Tell parent to check phone NOW",
                "bill_id": bill.id,
                "checkout_id": result.get('checkout_id'),
                "bill": BillSerializer(bill).data
            })
        else:
            bill.status = 'failed'
            bill.save()
            return Response({
                "success": False,
                "message": f"STK Failed: {result.get('message')}",
                "bill_id": bill.id
            }, status=400)

    except Exception as e:
        return Response({"success": False, "message": str(e)}, status=500)

@api_view(['GET'])
def list_bills(request):
    bills = Bill.objects.all().order_by('-created_at')[:50]
    return Response(BillSerializer(bills, many=True).data)

@csrf_exempt
def mpesa_callback(request):
    try:
        body = json.loads(request.body.decode('utf-8'))
        print(f"MPESA CALLBACK: {body}")
        # You can parse and update bill status here
        stk = body.get('Body',{}).get('stkCallback',{})
        checkout_id = stk.get('CheckoutRequestID')
        result_code = stk.get('ResultCode')
        if checkout_id:
            try:
                bill = Bill.objects.filter(mpesa_checkout_id=checkout_id).first()
                if bill:
                    if result_code == 0:
                        bill.status = 'paid'
                        # Get receipt
                        items = stk.get('CallbackMetadata',{}).get('Item',[])
                        for item in items:
                            if item.get('Name') == 'MpesaReceiptNumber':
                                bill.mpesa_receipt = item.get('Value','')
                    else:
                        bill.status = 'failed'
                    bill.save()
            except Exception as e:
                print(f"Callback save error: {e}")
        return JsonResponse({"ResultCode": 0, "ResultDesc": "Accepted"})
    except Exception as e:
        print(f"Callback error: {e}")
        return JsonResponse({"ResultCode": 0, "ResultDesc": "Accepted"})
