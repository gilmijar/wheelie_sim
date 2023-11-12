import unittest
from hypothesis import given, example, strategies as strats
import customers

cities = [
    {'country': 'Fakeland', 'city_ascii': 'Faketown'},
    {'country': 'Fakeland', 'city_ascii': 'Imaginaria'},
    {'country': 'Fakeland', 'city_ascii': 'Dreamville'},
    {'country': 'Fictionalonia', 'city_ascii': 'Storyville'},
    {'country': 'Fictionalonia', 'city_ascii': 'Novelburg'},
    {'country': 'Fictionalonia', 'city_ascii': 'Fantasia'}
]


class TestShortlist(unittest.TestCase):
    def setUp(self) -> None:
        # hand made monkey patching
        self.orig = customers.read_shortlist
        customers.read_shortlist = lambda: cities

    def tearDown(self) -> None:
        # monkey un-patching
        customers.read_shortlist = self.orig

    def test_pick_city_gets_a_city_with_country_from_shortlist(self):
        city, country = customers.pick_city()
        self.assertTupleEqual((city, country), ('Faketown', 'Fakeland'))

    def test_pick_city_gets_correct_city_when_called_with_parameter(self):
        city, country = customers.pick_city(3)
        self.assertTupleEqual((city, country), ('Storyville', 'Fictionalonia'))


class TestRandomToss(unittest.TestCase):
    def setUp(self) -> None:
        customers.seed(7)

    @given(strats.floats(min_value=0, max_value=1, exclude_min=True, exclude_max=True))
    @example(0.5)
    def test_toss_on_average_reproduce_bias(self, bias):
        n = 100_000
        result = sum([int(customers.toss(bias)) for _ in range(n)])/n
        self.assertAlmostEqual(result, bias, places=2)


if __name__ == '__main__':
    unittest.main()
