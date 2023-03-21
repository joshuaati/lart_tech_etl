from pony.orm import *

db = Database()

class FinanceInfo(db.Entity):
    _table_ = 'finance'

    firstName = Required(str)
    lastName = Required(str)
    age = Required(int)
    iban = Required(str, unique=True)
    credit_card_number = Required(str)
    credit_card_security_code = Required(str)
    credit_card_start_date = Required(str)
    credit_card_end_date = Required(str)
    address_main = Optional(str)
    address_city = Optional(str)
    address_postcode = Optional(str)
    debt = Optional(Json)


class VehicleInfo(db.Entity):
    _table_ = 'vehicle'

    firstName = Required(str)
    lastName = Required(str)
    age = Required(int)
    sex = Required(str)
    vehicle_make = Optional(str)
    vehicle_model = Optional(str)
    vehicle_year = Optional(int)
    vehicle_type = Optional(str)
    PrimaryKey(firstName, lastName, sex, age)


class IndividualInfo(db.Entity):
    _table_ = 'individual'

    firstName = Required(str)
    lastName = Required(str)
    age = Required(int)
    sex = Required(str)
    retired = Optional(str)
    dependants = Optional(str)
    marital_status = Optional(str)
    salary = Optional(str)
    pension = Optional(int)
    company = Optional(str)
    commute_distance = Optional(float)
    address_postcode = Optional(str)
    PrimaryKey(firstName, lastName, sex, age)


def connect_to_db(filename=':memory:', create_tables=True):
    db.bind(provider='sqlite', filename=filename, create_db=True)
    db.generate_mapping(create_tables=create_tables)
