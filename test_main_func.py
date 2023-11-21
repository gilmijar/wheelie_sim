import unittest
import main

customer = [
    {
        'first_name': 'Ilia',
        'last_name': 'Gilmijarow',
        'country': 'AAAAAAA',
        'city': 'BBBBBBB',
        'address': 'CCCCCCCCCCC',
        'email': 'i.gilmijarow@yahoo.com',
        'birth_date': '1980-01-01',
        'postal_code': '99-999'
    }
]


class MyTestCase(unittest.TestCase):
    def test_something(self):
        result = main.create_customers(customer)
        self.assertIsInstance(result, int)


if __name__ == '__main__':
    unittest.main()
