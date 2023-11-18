
from sys import argv
from datetime import date, timedelta
import random as rnd
import interaction_with_database as interaction
import customers


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
    latest_date = interaction.select_data(sql, expect_one=True)[0]
    return latest_date


def get_free_cars_on_date(the_date):
    sql = f"""SELECT inventory_id, car_id
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
    sql = f"SELECT staff_id, hired_date FROM staff WHERE hired_date < '{the_date}'"
    return interaction.select_data(sql)


def promote_employee():
    chosen_one = rnd.randint(1, 52)
    sql = f"""UPDATE store
        JOIN (select staff_id, store_id FROM staff
        ORDER BY staff_id
        LIMIT {chosen_one},1) AS choice
        USING(store_id)
        SET store_manager_id = choice.staff_id,
        last_update = NOW()"""
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


def enrich_customer_list(existing: list) -> list:
    existing_size = len(existing)
    new_ones = [customers.create(0.85) for _ in range(int(existing_size * 0.667))]
    # we just need their ids,
    # but we can't get ids, b/c the new ones weren't added to the db yet
    # but we can't add all of them since
    # we don't knw which ones will be selected
    return existing + new_ones


if __name__ == '__main__':
    GENERATE_DAYS = read_arg() or 1
    DAILY_RENTALS = 80
    RENTAL_SPREAD = 20
    rates = get_rental_rates()
    last_rental_date: date = get_latest_date()
    for day in range(1, GENERATE_DAYS + 1):
        promote_employee()
        print('.', end='')
        current_date = last_rental_date + timedelta(days=day)
        weekend_factor = int(is_weekend(current_date))
        free_cars = get_free_cars_on_date(current_date)
        staff = get_staff(current_date)
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
        customers = enrich_customer_list(get_customers_on_date(current_date))
        print('.', end='')
        rented_cars = rnd.sample(free_cars, k=day_rental_no)
        inventory_ids = [car.inventory_id for car in rented_cars]
        customer_sample = [itm.customer_id for itm in rnd.sample(customers, k=day_rental_no)]
        # TODO: create all the new customers in the database and get their ids
        rental_prices = [multiplier * rates[car.car_id] for car in rented_cars]
        staff_ids = [itm.staff_id for itm in rnd.choices(staff, k=day_rental_no)]
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
