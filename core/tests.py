from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from .models import Payment


class PaymentAPITests(APITestCase):

    def setUp(self):
        payment = Payment()
        payment.amount = 20
        payment.currency = Payment.USD
        payment.save()
        self.payment = payment
        self.url = reverse('core:payment-path-list')
        
    def build_single_url_path(self, id_):
        return reverse('core:payment-path-detail', args=[id_])

    def test_create_payment(self):
        payload = {
            'amount': 21,
            'currency': Payment.USD
        }
        response = self.client.post(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_create_payment_with_incomplete_payload(self):
        payload = {
            'amount': 21,
            'currency': Payment.USD
        }
        data = payload.copy()
        del data['amount']
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {
            "amount": [
                "This field is required."
            ]
        })

        data = payload.copy()
        del data['currency']
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {
            "currency": [
                "This field is required."
            ]
        })
    
    def test_create_payment_with_string_amount(self):
        payload = {
            'amount': '"21"',
            'currency': Payment.USD
        }
        response = self.client.post(self.url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {"amount": ["A valid number is required."]})
    
    def test_create_payment_with_invalid_choices_currency(self):
        payload = {
            'amount': 21,
            'currency': 'IDRs'
        }
        response = self.client.post(self.url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            str(response.data.get('currency')[0]),
            '"IDRs" is not a valid choice.'
        )
    
    def test_update_payment(self):
        url = self.build_single_url_path(self.payment.id)
        payload = {
            'amount': 21,
            'currency': self.payment.currency
        }
        response = self.client.patch(url, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_update_payment_currency(self):
        url = self.build_single_url_path(self.payment.id)
        if self.payment.currency == Payment.USD:
            currency = Payment.IDR
        else:
            currency = Payment.USD
        payload = {
            'amount': 21,
            'currency': currency
        }
        response = self.client.put(url, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            str(response.data.get('currency')[0]),
            "Unsupported update currency %s to %s" % (self.payment.currency, currency)
        )

    def test_get_list_data_payment(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_get_single_data_payment(self):
        url = self.build_single_url_path(self.payment.id)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_get_single_data_payment_with_not_found_data(self):
        url = self.build_single_url_path(-1)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, {
            "detail": "Not found."
        })
    
    def test_delete_data_payment(self):
        url = self.build_single_url_path(self.payment.id)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        with self.assertRaises(Payment.DoesNotExist):
            self.payment.refresh_from_db()
    
    def test_delete_data_payment_with_not_found_data(self):
        url = self.build_single_url_path(-1)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, {
            "detail": "Not found."
        })
