"""
This is a module for generating new customers for the wheelie database
Each customer has an address consisting of a street address, city and country
Customer will have 40% chance to be a new customer
Each new customer will have an 85% chance to live in Poland
Cities are taken from https://simplemaps.com/data/world-cities - basic dataset
"""

import json
from functools import lru_cache
from random import choice, random, seed, gauss
import faker
from typing import List, Tuple
from datetime import date, timedelta


def age_normal_dist(mean=40, sigma=12, lo=20, hi=80):
    """ random result between lo and hi, with normal-ish distribution"""
    if lo >= hi:
        raise ValueError(f'lower cutoff age should be lower than hight cutoff age. Currently {lo}, {hi}')
    x = lo - 1
    while not (lo <= x <= hi):
        x = gauss(mean, sigma)
    return int(round(x, 0))


def toss(bias: float = 0.50) -> bool:
    return random() < bias


def pick_city(prefer_pl: bool) -> dict:
    shortlist = [itm for itm in read_shortlist() if itm['iso2'] == 'PL' or not prefer_pl]
    keys = 'city country iso2'.split()
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


def make_birthday(from_date, year_shift):
    if isinstance(from_date, str):
        yr = date.fromisoformat(from_date).year + year_shift
    elif isinstance(from_date, date):
        yr = from_date.year + year_shift
    elif isinstance(from_date, int):
        yr = from_date + year_shift
    else:
        raise ValueError('from_date must be iso ormat string, date object ot year as integer')
    day_offset = timedelta(days=int(random()*365))
    birthday = date(yr, 1, 1) + day_offset
    return birthday


def make_customer(city_record: dict, the_day: date) -> dict:
    locale = locale_map().get('iso2', 'pl_PL')
    f = faker.Faker(locale)
    first_name = f.first_name()
    last_name = f.last_name()
    email_first_name = first_name[0] if toss(0.3) else first_name
    age = age_normal_dist(mean=40, sigma=12, lo=20, hi=70)
    birthday = make_birthday(the_day, -1*age)
    return {
        'first_name': first_name,
        'last_name': last_name,
        'country': city_record['country'],
        'city': city_record['city'],
        'address': f.street_address(),
        'email': f"{email_first_name}.{last_name}@{f.free_email_domain()}",
        'birth_date': birthday,
        'postal_code': f.postcode()
    }


def create(the_day, bias: float) -> dict:
    return make_customer(pick_city(toss(bias)), the_day)


if __name__ == '__main__':
    # make 100 customers
    crowd = [make_customer(pick_city(toss(0.85))) for _ in range(100)]
    print(json.dumps(crowd, indent=1))
