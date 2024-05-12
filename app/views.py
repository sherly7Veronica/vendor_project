from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Vendor, PurchaseOrder
from .serializers import VendorSerializer, PurchaseOrderSerializer


@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def vendor_details(request, vendor_id):
    try:
        vendor = Vendor.objects.get(pk=vendor_id)
    except Vendor.DoesNotExist:
        return Response({"error": "Vendor not found"}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = VendorSerializer(vendor)
        return Response(serializer.data)    

    elif request.method == 'PUT':
        serializer = VendorSerializer(vendor, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        vendor.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

@api_view(['GET', 'POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def vendors(request):
    if request.method == 'GET':
        vendors = Vendor.objects.all()
        serializer = VendorSerializer(vendors, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = VendorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET', 'POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def purchase_orders(request):
    if request.method == 'GET':
        orders = PurchaseOrder.objects.all()
        serializer = PurchaseOrderSerializer(orders, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = PurchaseOrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def update_orders(request, po_id): 
    try: 
        order = PurchaseOrder.objects.get(pk=po_id)
    except PurchaseOrder.DoesNotExist:
        return Response({'error': "Order ID not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':  
        serializer = PurchaseOrderSerializer(order)
        return Response(serializer.data)
         
    elif request.method == 'PUT':    
        serializer = PurchaseOrderSerializer(order, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)       


def calculate_on_time_delivery_rate(vendor):
    on_time_delivery_count = PurchaseOrder.objects.filter(vendor=vendor, status='COMPLETED', delivery_date__lte=F('acknowledgement_date')).count() 
    total_orders_count = PurchaseOrder.objects.filter(vendor=vendor, status='COMPLETED').count()
    return (on_time_delivery_count/total_orders_count)*100 if total_orders_count >0 else 0

def calculate_quality_rating_avg(vendor):
    return PurchaseOrder.objects.filter(vendor=vendor, status='COMPLETED').aggregate(avg_quality_rating=Avg('quality_rating'))['avg_quality_rating'] or 0

def calculate_average_response_time(vendor):
    return PurchaseOrder.objects.filter(vendor=vendor, status='COMPLETED').aggregate(avg_response_time=Avg(ExpressionWrapper(F('acknowledgement_date') - F('issue_date'), output_field=FloatField())))['avg_response_time'] or 0

def calculate_fulfillment_rate(vendor):
    fulfilled_orders_count = PurchaseOrder.objects.filter(vendor=vendor, status='COMPLETED', issue_date__lte=F('acknowledgement_date')).count()
    total_orders_count = PurchaseOrder.objects.filter(vendor=vendor, status='COMPLETED').count()
    return (fulfilled_orders_count / total_orders_count) * 100 if total_orders_count > 0 else 0

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def vendor_performance(request):
    if request.method == 'GET':
        vendor_performance_data = []
        vendors = Vendor.objects.all()
        for vendor in vendors:
            on_time_delivery_rate = calculate_on_time_delivery_rate(vendor)
            quality_rating_avg = calculate_quality_rating_avg(vendor)
            average_response_time = calculate_average_response_time(vendor)
            fulfillment_rate = calculate_fulfillment_rate(vendor)
            vendor_performance_data.append({
                'vendor_name': vendor.name,
                'on_time_delivery_rate': on_time_delivery_rate,
                'quality_rating_avg': quality_rating_avg,
                'average_response_time': average_response_time,
                'fulfillment_rate': fulfillment_rate,
            })
        return JsonResponse({'vendor_performance': vendor_performance_data})
    else:
        return JsonResponse({'error': 'Method not allowed.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)    
    

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def acknowledge_purchase_order(request, po_id):
    if request.method == 'POST':
        purchase_order = get_object_or_404(PurchaseOrder, pk=po_id)
        purchase_order.acknowledgement_date = timezone.now()
        purchase_order.save()
        return JsonResponse({'message': f'Purchase order {po_id} acknowledged successfully.'})
    else:
        return JsonResponse({'error': 'Method not allowed.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
