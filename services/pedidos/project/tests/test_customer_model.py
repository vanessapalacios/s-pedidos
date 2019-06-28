import unittest

from sqlalchemy.exc import IntegrityError

from project import db
from project.api.models import Customer
from project.tests.base import BaseTestCase
from project.tests.utils import add_customer


class TestCustomerModel(BaseTestCase):

    def test_add_customer(self):
        user = add_customer('justatest')
        self.assertTrue(user.id)
        self.assertEqual(user.name, 'justatest')

if __name__ == '__main__':
    unittest.main()