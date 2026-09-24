from rest_framework import viewsets, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import Invoice, MpesaTransaction
from .serializers import InvoiceSerializer, MpesaTransactionSerializer
from .mpesa_service import stk_push
import json

class InvoiceViewSet(viewsets.ModelViewSet):
    queryset=Invoice.objects.all().order_by('-created_at')
    serializer_class=InvoiceSerializer
    permission_classes=[permissions.IsAuthenticated]

class MpesaViewSet(viewsets.ModelViewSet):
    queryset=MpesaTransaction.objects.all().order_by('-created_at')
    serializer_class=MpesaTransactionSerializer
    permission_classes=[permissions.IsAuthenticated]

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def initiate_stk_push(request):
    phone=request.data.get('phone')
    amount=request.data.get('amount')
    invoice_id=request.data.get('invoice_id')
    if not phone or not amount: return Response({'error':'phone and amount required'}, status=400)
    try:
        invoice=Invoice.objects.get(id=invoice_id) if invoice_id else None
    except: invoice=None
    account_ref = invoice.invoice_no if invoice else 'AFYACARE'
    result = stk_push(phone, amount, account_ref)
    # Save transaction
    MpesaTransaction.objects.create(
        invoice=invoice, phone_number=phone, amount=amount,
        checkout_request_id=result.get('CheckoutRequestID',''),
        merchant_request_id=result.get('MerchantRequestID',''),
        status='PENDING', result_desc=str(result)
    )
    return Response(result)

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def mpesa_callback(request):
    # Safaricom will POST here
    data=request.data
    print("M-Pesa Callback:", json.dumps(data))
    try:
        stk=data['Body']['stkCallback']
        checkout_id=stk.get('CheckoutRequestID')
        result_code=stk.get('ResultCode')
        txn=MpesaTransaction.objects.filter(checkout_request_id=checkout_id).first()
        if txn:
            if result_code==0:
                # success
                meta_items=stk.get('CallbackMetadata',{}).get('Item',[])
                receipt = next((i['Value'] for i in meta_items if i['Name']=='MpesaReceiptNumber'), '')
                txn.mpesa_receipt=receipt
                txn.status='COMPLETED'
                txn.result_desc=stk.get('ResultDesc','')
                txn.save()
                # Mark invoice paid
                if txn.invoice:
                    txn.invoice.amount_paid = txn.amount
                    txn.invoice.status='PAID'
                    txn.invoice.payment_method='MPESA'
                    txn.invoice.save()
            else:
                txn.status='FAILED'
                txn.result_desc=stk.get('ResultDesc','')
                txn.save()
    except Exception as e:
        print("Callback error", e)
    return Response({'ResultCode':0,'ResultDesc':'Accepted'})
