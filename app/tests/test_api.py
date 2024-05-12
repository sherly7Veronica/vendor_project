from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from ..models import Vendor, PurchaseOrder
from ..serializers import VendorSerializer, PurchaseOrderSerializer
from django.utils import timezone

class VendorManagementSystemTests(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Create sample vendor
        self.vendor1 = Vendor.objects.create(name='Vendor 1')
        self.vendor2 = Vendor.objects.create(name='Vendor 2')

        # Create sample purchase orders
        self.po1 = PurchaseOrder.objects.create(vendor=self.vendor1, status='COMPLETED')
        self.po2 = PurchaseOrder.objects.create(vendor=self.vendor1, status='PENDING')
        self.po3 = PurchaseOrder.objects.create(vendor=self.vendor2, status='COMPLETED')

    def test_get_vendors_list(self):
        response = self.client.get(reverse('vendors'))
        vendors = Vendor.objects.all()
        serializer = VendorSerializer(vendors, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_get_vendor_details(self):
        response = self.client.get(reverse('details', args=[self.vendor1.id]))
        vendor = Vendor.objects.get(id=self.vendor1.id)
        serializer = VendorSerializer(vendor)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_create_vendor(self):
        data = {'name': 'New Vendor'}
        response = self.client.post(reverse('vendors'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Vendor.objects.filter(name='New Vendor').exists())

    def test_get_purchase_orders_list(self):
        response = self.client.get(reverse('orders'))
        orders = PurchaseOrder.objects.all()
        serializer = PurchaseOrderSerializer(orders, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_get_purchase_order_details(self):
        response = self.client.get(reverse('orders-details', args=[self.po1.id]))
        order = PurchaseOrder.objects.get(id=self.po1.id)
        serializer = PurchaseOrderSerializer(order)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_update_purchase_order(self):
        data = {'status': 'COMPLETED'}
        response = self.client.put(reverse('orders-details', args=[self.po2.id]), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(PurchaseOrder.objects.get(id=self.po2.id).status, 'COMPLETED')

    def test_get_vendor_performance(self):
        response = self.client.get(reverse('vendors_performance'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_acknowledge_purchase_order(self):
        response = self.client.post(reverse('acknowledge_purchase_order', args=[self.po2.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(PurchaseOrder.objects.get(id=self.po2.id).acknowledgement_date is not None)


class PurchaseOrderAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.vendor1 = Vendor.objects.create(name='Vendor 1', contact_details='Contact 1', address='Address 1', vendor_code='V1')
        self.vendor2 = Vendor.objects.create(name='Vendor 2', contact_details='Contact 2', address='Address 2', vendor_code='V2')
        self.purchase_order1 = PurchaseOrder.objects.create(po_number='PO1', vendor=self.vendor1, order_date=timezone.now(), delivery_date=timezone.now(), quantity=1, status='PENDING', issue_date=timezone.now(), acknowledgement_date=timezone.now())
        self.purchase_order2 = PurchaseOrder.objects.create(po_number='PO2', vendor=self.vendor2, order_date=timezone.now(), delivery_date=timezone.now(), quantity=2, status='PENDING', issue_date=timezone.now(), acknowledgement_date=timezone.now())

    def test_get_purchase_orders(self):
        response = self.client.get(reverse('orders'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)


class VendorPerformanceAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.vendor1 = Vendor.objects.create(name='Vendor 1', contact_details='Contact 1', address='Address 1', vendor_code='V1')
        self.vendor2 = Vendor.objects.create(name='Vendor 2', contact_details='Contact 2', address='Address 2', vendor_code='V2')
        # Create more data for vendor performance testing

    def test_vendor_performance(self):
        response = self.client.get(reverse('vendors_performance'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class AcknowledgePurchaseOrderAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.vendor = Vendor.objects.create(name='Vendor 1', contact_details='Contact 1', address='Address 1', vendor_code='V1')
        self.purchase_order = PurchaseOrder.objects.create(po_number='PO1', vendor=self.vendor, order_date=timezone.now(), delivery_date=timezone.now(), quantity=1, status='PENDING', issue_date=timezone.now(), acknowledgement_date=timezone.now())

    def test_acknowledge_purchase_order(self):
        response = self.client.post(reverse('acknowledge_purchase_order', args=[self.purchase_order.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
