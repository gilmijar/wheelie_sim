import datetime
import random as rnd
from sys import argv
from datetime import date, timedelta
import interaction_with_database as interaction
import customers as customer_gen
from typing import List, Union, Callable
from collections import namedtuple, defaultdict


def read_arg(limit=365):
    if len(argv) > 1:
        try:
            days = int(argv[1])
            if days > limit:
                raise Exception(f'Too many days to process. cannot exceed {limit}')
            else:
                return days
        except ValueError:
            return None


def get_rental_rates():
    sql = "SELECT car_id, rental_rate FROM car"
    result = interaction.select_data(sql)
    rental_rates = {item.car_id: int(item.rental_rate) for item in result}
    return rental_rates


def get_customers_on_date(the_date):
    sql = f"SELECT customer_id FROM customer WHERE create_date < '{the_date}'"
    return interaction.select_data(sql)


def get_latest_date():
    sql = "SELECT MAX(rental_date) FROM rental"
    latest_date = interaction.select_data(sql, expect_one=True)[0] or datetime.date(2017, 1, 2)
    return latest_date


def get_free_cars_on_date(the_date):
    sql = f"""SELECT inventory_id, car_id, store_id
                FROM inventory inv
                WHERE create_date < '{the_date}'
                AND (sell_price is null OR last_update > '{the_date}')
                AND NOT EXISTS (
                    SELECT distinct inventory_id
                    FROM rental
                    WHERE rental.inventory_id = inv.inventory_id
                    AND '{the_date}' BETWEEN rental_date AND return_date
                )
    """
    return interaction.select_data(sql)


def get_staff(the_date):
    sql = f"SELECT staff_id, store_id, hired_date FROM staff WHERE hired_date < '{the_date}'"
    return interaction.select_data(sql)


def promote_employee():
    the_date = current_date  # copy from outer scope
    chosen_one = rnd.randint(1, 52)
    sql = f"""UPDATE store
        JOIN (select staff_id, store_id FROM staff
        ORDER BY staff_id
        LIMIT {chosen_one},1) AS choice
        USING(store_id)
        SET store_manager_id = choice.staff_id,
        last_update = '{date.isoformat(the_date)}'"""
    interaction.run_dml(sql)


def is_weekend(the_date: date):
    friday_num = 4
    return the_date.weekday() > friday_num


def calculate_multiplier(the_date: date):
    mult = 1
    if the_date.month in (7, 8):
        mult *= 1.2
    if is_weekend(the_date):
        mult *= 1.5
    return mult


def enrich_customer_list(existing: list, min_cnt: int) -> list:
    existing_size = len(existing)
    target_cnt = int(existing_size * 0.667)
    if (existing_size + target_cnt) < min_cnt:
        target_cnt = min_cnt
    new_ones = [customer_gen.create for _ in range(target_cnt)]
    return existing + new_ones


def filter_dict(*desired_keys) -> Callable:
    """Create a function that can extract target keys and their values from a dict"""
    def extract(subject: dict) -> dict:
        return {k: v for k, v in subject.items() if k in desired_keys}
    return extract


def create_customers(customer_mix: List[Union[tuple, Callable]]) -> List[tuple]:
    the_day = current_date  # copy from outer scope
    old_ones = [itm for itm in customer_mix if isinstance(itm, tuple)]
    new_ones = [itm(0.85) for itm in customer_mix if not isinstance(itm, tuple)]
    countries = list(map(filter_dict('country'), new_ones))
    interaction.insert_dict(countries, 'country')
    distinct_countries = ', '.join({f"'{itm['country']}'" for itm in countries})
    country_map = {r[1]: r[0] for r in interaction.select_data(
        f"select country_id, country from country where country in ({distinct_countries})"
    )}

    cities = map(filter_dict('city', 'country'), new_ones)
    cities_prep = [{'city': d['city'], 'country_id': country_map[d['country']]} for d in cities]
    interaction.insert_dict(cities_prep, 'city')
    distinct_cities = ', '.join({f"'{itm['city']}{itm['country_id']}'" for itm in cities_prep})
    city_map = {(r[1], r[2]): r[0] for r in interaction.select_data(
        f"select city_id, city, country_id from city where concat(city, country_id) in ({distinct_cities})"
    )}

    addresses = map(filter_dict('address', 'city', 'country', 'postal_code'), new_ones)
    addr_prep = [{
        'address': d['address'],
        'city_id': city_map[(d['city'], country_map[d['country']])],
        'postal_code': d['postal_code'],
        'last_update': date.isoformat(the_day)
    } for d in addresses]
    interaction.insert_dict(addr_prep, 'address')
    distinct_addr = ', '.join({f"'{itm['address']}{itm['city_id']}'" for itm in addr_prep})
    address_map = {
        tuple(r[1:]): r[0] for r in interaction.select_data(
            f"select address_id, address, city_id from address where concat(address, city_id) in ({distinct_addr})"
        )
    }

    people = map(
        filter_dict('first_name', 'last_name', 'email', 'birth_date', 'address', 'city', 'country'),
        new_ones
    )
    people_prep = [{
        'first_name': d['first_name'],
        'last_name': d['last_name'],
        'email': d['email'],
        'birth_date': d['birth_date'],
        'address_id': address_map[(
            d['address'],
            city_map[(
                d['city'],
                country_map[d['country']]
            )],
        )],
        'create_date': date.isoformat(the_day)
    } for d in people]
    interaction.insert_dict(people_prep, 'customer')
    distinct_people = ', '.join({f"'{itm['first_name']}{itm['last_name']}{itm['address_id']}'" for itm in people_prep})
    sql = f"select customer_id, first_name, last_name from customer " \
          f"where concat(first_name, last_name, address_id) in ({distinct_people})"
    new_people = interaction.select_data(sql)
    return old_ones + new_people


def fill_in_payments():
    the_date = current_date  # copy from outer scope
    sql = [
        "DROP TEMPORARY TABLE IF EXISTS unpaid_rentals",
        f"""
        CREATE TEMPORARY TABLE unpaid_rentals
        SELECT
        rental.customer_id,
        rental_id, 
        datediff(return_date, rental_date) * rental_rate as amount,
        date_add('{date.isoformat(the_date)}', INTERVAL floor(rand()*-4) DAY) as payment_date,
        '{date.isoformat(the_date)}' as last_update
        FROM rental
        LEFT JOIN payment
        USING (rental_id)
        WHERE payment_id is null
        AND rental.return_date is not null
        AND payment_deadline < date_add('{date.isoformat(the_date)}', INTERVAL -1*floor(rand()*-20) DAY);
        """,
        """
        INSERT IGNORE payment (
            customer_id, rental_id, amount, payment_date, last_update
        )
        SELECT * FROM unpaid_rentals LIMIT 1000000;
        """
    ]
    for query in sql:
        interaction.run_dml(query)


if __name__ == '__main__':
    # rnd.seed = 6  # guaranteed to be random
    GENERATE_DAYS = read_arg(limit=3653) or 1
    DAILY_RENTALS = 80
    RENTAL_SPREAD = 20
    rates = get_rental_rates()
    last_rental_date: date = get_latest_date()
    for day in range(1, GENERATE_DAYS + 1):
        print('.', end='')
        current_date = last_rental_date + timedelta(days=day)
        promote_employee()
        weekend_factor = int(is_weekend(current_date))
        free_cars = get_free_cars_on_date(current_date)
        staff = get_staff(current_date)
        if not staff:
            print('No staff on this day')
            continue
        staff_by_store = defaultdict(list)
        for row in staff:
            staff_by_store[row.store_id].append(row.staff_id)
        adjusted_rentals = rnd.randint(DAILY_RENTALS - RENTAL_SPREAD, DAILY_RENTALS + RENTAL_SPREAD)
        increase_factor = 1 + 0.5 * weekend_factor
        day_rental_no = min(
            len(free_cars),
            int(adjusted_rentals * increase_factor)
        )
        if day_rental_no == 0:
            print(f'No cars to rent on {current_date}')
            continue
        multiplier = calculate_multiplier(current_date)
        customers = enrich_customer_list(get_customers_on_date(current_date), min_cnt=day_rental_no)
        print('.', end='')
        rented_cars = rnd.sample(free_cars, k=day_rental_no)
        inventory_ids = [car.inventory_id for car in rented_cars]
        created_customers = create_customers([itm for itm in rnd.sample(customers, k=day_rental_no)])
        customer_sample = [itm.customer_id for itm in created_customers]
        rental_prices = [multiplier * rates[car.car_id] for car in rented_cars]
        staff_ids = [rnd.choice(staff_by_store[car.store_id]) for car in rented_cars if staff_by_store[car.store_id]]
        rental_dates = [current_date] * day_rental_no
        return_dates = [current_date + timedelta(days=rnd.randint(2-weekend_factor, 12-4*weekend_factor))
                        for _ in rented_cars]
        payment_deadlines = [ret_date + timedelta(days=7) for ret_date in return_dates]
        creation_dates = rental_dates
        print('.', end='')
        insertion_items = zip(
            inventory_ids,
            customer_sample,
            rental_prices,
            staff_ids,
            rental_dates,
            return_dates,
            payment_deadlines,
            creation_dates
        )
        keys = 'inventory_id customer_id rental_rate staff_id rental_date return_date payment_deadline create_date'\
            .split()
        insert_list = [
            {k: v for k, v in zip(keys, item)} for item in insertion_items
        ]
        remaining_free = len(free_cars) - day_rental_no
        weekend = "It's weekend!"
        print(f'Generate day {day} ({current_date}) of {GENERATE_DAYS}. '
              f'Rent {day_rental_no} cars, leaving {remaining_free} free cars. '
              f'{weekend * weekend_factor}')
        interaction.insert_dict(insert_list, 'rental')
        # now fill in missing payments
        fill_in_payments()
