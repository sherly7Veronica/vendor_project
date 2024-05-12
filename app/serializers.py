from rest_framework import serializers
from .models import *
# from django.contrib.auth.models import User


class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        # fields = ('id', 'name', 'phone_number', 'address', 'unique_code')
        fields = '__all__'      

class PurchaseOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrder
        # fields = ('order_number', 'vendor', 'total_amount', 'order_date')  
        fields = '__all__'      

# class userSerializers(serializers.ModelSerializer):
 
#     class Meta:
#         model = User
#         fields =  '__all__'        