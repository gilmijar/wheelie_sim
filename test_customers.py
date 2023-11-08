import unittest
import customers

cities = [
    {'country': 'Fakeland', 'city_ascii': 'Faketown'},
    {'country': 'Fakeland', 'city_ascii': 'Imaginaria'},
    {'country': 'Fakeland', 'city_ascii': 'Dreamville'},
    {'country': 'Fictionalonia', 'city_ascii': 'Storyville'},
    {'country': 'Fictionalonia', 'city_ascii': 'Novelburg'},
    {'country': 'Fictionalonia', 'city_ascii': 'Fantasia'}
]


class MyTestCase(unittest.TestCase):
    def test_pick_city_gets_a_city_with_country_from_shortlist(self):
        self.orig = customers.read_shortlist
        customers.read_shortlist = lambda: [{
            'city_ascii': 'Unbingu',
            'country': 'Lemuria'
        }]
        city, country = customers.pick_city()
        self.assertTupleEqual((city, country), ('Unbingu', 'Lemuria'))


if __name__ == '__main__':
    unittest.main()
