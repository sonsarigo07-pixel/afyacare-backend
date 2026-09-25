
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Patient,Bill,Payment
from .serializers import PatientSerializer,BillSerializer
from .mpesa_service import stk_push
from decouple import config

@api_view(['GET'])
def health(request): return Response({'status':'ok','backend':'AfyaCare online'})

@api_view(['GET','POST'])
def patients(request):
    if request.method=='POST':
        s=PatientSerializer(data=request.data)
        if s.is_valid(): s.save(); return Response(s.data, status=201)
        return Response(s.errors, status=400)
    from .models import Patient
    return Response(PatientSerializer(Patient.objects.all(), many=True).data)

@api_view(['GET','POST'])
def bills(request):
    if request.method=='POST':
        s=BillSerializer(data=request.data)
        if s.is_valid(): s.save(); return Response(s.data, status=201)
        return Response(s.errors, status=400)
    from .models import Bill
    return Response(BillSerializer(Bill.objects.all(), many=True).data)

@api_view(['POST'])
def push_stk(request):
    phone=request.data.get('phone'); amount=request.data.get('amount',1); bill_id=request.data.get('bill_id')
    if not phone: return Response({'error':'phone required'}, status=400)
    # format phone 2547...
    if phone.startswith('0'): phone='254'+phone[1:]
    if phone.startswith('7'): phone='254'+phone
    callback=config('MPESA_CALLBACK_URL', default=request.build_absolute_uri('/api/billing/mpesa/callback/'))
    result=stk_push(phone, amount, callback)
    if bill_id:
        try:
            b=Bill.objects.get(id=bill_id)
            Payment.objects.create(bill=b, amount=amount, phone=phone, status=result.get('ResponseCode','pending'))
        except: pass
    return Response(result)

@api_view(['POST'])
def mpesa_callback(request):
    print("MPESA CALLBACK", request.data)
    return Response({'ResultCode':0,'ResultDesc':'Accepted'})
