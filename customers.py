"""
This is a module for generating new customers for the wheelie database
Each customer has an address consisting of a street address, city and country
For each customer there will be a 40% chance of having a new street,
for each street there will be a 40% chance of being in a new city.
Cities are taken from https://simplemaps.com/data/world-cities - basic dataset
"""

import faker
import json
