"""
This is a module for generating new customers for the wheelie database
Each customer has an address consisting of a street address, city and country
For each customer there will be a 40% chance of having a new street,
for each street there will be a 40% chance of being in a new city.
Cities are taken from https://simplemaps.com/data/world-cities - basic dataset
"""

import json
from random import random, seed
import faker
from typing import List


def read_shortlist() -> List[dict]:
    with open('shortlist.json', 'r') as f:
        shortlist = json.load(f)
    return shortlist


def pick_city(n: int = 0):
    shortlist = read_shortlist()
    city = shortlist[n]
    return city['city_ascii'], city['country']


def toss(bias: float = 0.50) -> bool:
    return random() < bias

