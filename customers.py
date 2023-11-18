"""
This is a module for generating new customers for the wheelie database
Each customer has an address consisting of a street address, city and country
Customer will have 40% chance to be a new customer
Each new customer will have an 85% chance to live in Poland
Cities are taken from https://simplemaps.com/data/world-cities - basic dataset
"""

import json
from functools import lru_cache
from random import choice, random, seed
import faker
from typing import List, Tuple


def toss(bias: float = 0.50) -> bool:
    return random() < bias


def pick_city(prefer_pl: bool) -> dict:
    shortlist = [itm for itm in read_shortlist() if itm['iso2'] == 'PL' or not prefer_pl]
    keys = 'city_ascii country iso2'.split()
    city = {k: v for k, v in choice(shortlist).items() if k in keys}
    return city


@lru_cache()
def read_shortlist() -> List[dict]:
    with open('cities/shortlist.json', 'r') as f:
        shortlist = json.load(f)
    return shortlist


@lru_cache()
def locale_map():
    with open('cities/locale_codes.txt', 'r') as loc_file:
        locales: List[str] = loc_file.read().splitlines()
    loc_map = {loc.rpartition('_')[2]: loc for loc in locales}
    return loc_map


def make_customer(city_record: dict) -> dict:
    faker.Faker.seed(128)
    locale = locale_map().get('iso2', 'pl_PL')
    f = faker.Faker(locale)
    return {
        'first_name': f.first_name(),
        'last_name': f.last_name(),
        'country': city_record['country'],
        'city': city_record['city_ascii'],
        'address': f.street_address()
    }


def create(bias: float) -> dict:
    return make_customer(pick_city(toss(bias)))


if __name__ == '__main__':
    # make 100 customers
    crowd = [make_customer(pick_city(toss(0.85))) for _ in range(100)]
    print(json.dumps(crowd, indent=1))
