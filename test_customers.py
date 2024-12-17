import unittest
from hypothesis import given, example, strategies as strats
import customers

cities = [
    {'country': 'Fakeland', 'city': 'Faketown', 'iso2': 'PL'},
    {'country': 'Fakeland', 'city': 'Imaginaria', 'iso2': 'PL'},
    {'country': 'Fakeland', 'city': 'Dreamville', 'iso2': 'PL'},
    {'country': 'Fictionalonia', 'city': 'Storyville', 'iso2': 'SE'},
    {'country': 'Fictionalonia', 'city': 'Novelburg', 'iso2': 'SE'},
    {'country': 'Fictionalonia', 'city': 'Fantasia', 'iso2': 'SE'}
]


class TestShortlist(unittest.TestCase):
    def setUp(self) -> None:
        customers.seed(5)
        # hand made monkey patching
        self.orig = customers.read_shortlist
        customers.read_shortlist = lambda: cities

    def tearDown(self) -> None:
        # monkey un-patching
        customers.read_shortlist = self.orig

    def test_pick_city_gets_a_correct_city_when_called_with_true(self):
        result = customers.pick_city(True)
        expected = {
            'city': 'Dreamville',
            'country': 'Fakeland',
            'iso2': 'PL'
        }
        self.assertDictEqual(result, expected)

    def test_pick_city_gets_correct_city_when_called_with_false(self):
        result = customers.pick_city(False)
        expected = {
            'city': 'Novelburg',
            'country': 'Fictionalonia',
            'iso2': 'SE'
        }
        self.assertDictEqual(result, expected)


class TestFaker(unittest.TestCase):
    def setUp(self) -> None:
        # hand made monkey patching
        self.orig = customers.read_shortlist
        customers.read_shortlist = lambda: cities

    def tearDown(self) -> None:
        # monkey un-patching
        customers.read_shortlist = self.orig

    def test_make_customer_produces_name_and_address(self):
        new_customer = customers.make_customer(cities[3])
        self.assertEqual('Fictionalonia', new_customer['country'])
        self.assertEqual('Storyville', new_customer['city'])
        self.assertIsNotNone(new_customer.get('first_name'))
        self.assertIsNotNone(new_customer.get('last_name'))
        self.assertIsNotNone(new_customer.get('address'))
        print(new_customer)

    def test_make_customer_raises_key_error_when_given_bad_input(self):
        bad_input = {'iso': 'pl_PL'}
        with self.assertRaises(KeyError):
            customers.make_customer(bad_input)

    def test_customers_get_a_normal_like_distribution_of_age(self):
        from collections import Counter
        b_years = [customers.make_customer(cities[3])['birth_date'].year for _ in range(300)]
        year_counts = Counter(b_years)
        ordered_counts = [n for y, n in sorted(year_counts.items())]
        third = len(ordered_counts)//3
        old = sum(ordered_counts[:third]) / third
        mid = sum(ordered_counts[third:third*2]) / third
        new = sum(ordered_counts[third*2:]) / third
        self.assertTrue(old < mid and new < mid, f'{old=}, {mid=}, {new=}')


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
