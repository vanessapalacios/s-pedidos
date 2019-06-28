
import json
import unittest
# from project import db
# from project.api.models import User
from project.tests.base import BaseTestCase
from project.tests.utils import add_customer


#   def add_user(username, email):
#   user = User(username=username, email=email)
#   db.session.add(user)
#   db.session.commit()
#   return user


class TestCustomerService(BaseTestCase):
    """Tests para el servicio Users."""

    
    def test_sigle_customer_no_id(self):
        """Asegúrese de que se arroje un error si no se
        proporciona una identificación."""
        with self.client:
            response = self.client.get('/customer/blah')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn('El usuario no existe', data['mensaje'])
            self.assertIn('failed', data['status'])

    def test_single_customer_incorrect_id(self):
        """Asegurando de que se arroje un error si la
        identificación no existe."""

        with self.client:
            response = self.client.get('/customer/999')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)

    def test_single_customer(self):
        """ Asegurando de que el cliente individual
        se comporte correctamente."""
        customer = add_customer('vanessa')
        with self.client:
            response = self.client.get(f'/customer/{customer.id}')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn('vanessa', data['data']['name'])
            self.assertIn('success', data['status'])


if __name__ == '__main__':
    unittest.main()