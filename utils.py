import csv
import json
from xml.etree import ElementTree
from pony.orm import *
from database import db, VehicleInfo, IndividualInfo, FinanceInfo

@db_session
def extract_and_upload_csv(filename):
    '''This function extracts information from a csv file and uploads it to a database'''
    with open(filename, newline='') as csv_file:
        reader = csv.reader(csv_file)
        next(reader)  # skip the header row
        data = [{
            'firstName': row[0],
            'lastName': row[1],
            'age': row[2],
            'sex': row[3],
            'vehicle_make': row[4],
            'vehicle_model': row[5],
            'vehicle_year': row[6],
            'vehicle_type': row[7],
        } for row in reader]

        try:
            [VehicleInfo(**row) for row in data]
        except Exception as e:
            print(f'Error: {e}')
            db.rollback()
        else:
            print(f'Successfully inserted {len(data)} rows from csv.')

@db_session
def extract_and_upload_xml(filename):
    '''This function extracts information from an xml file and uploads it to a database'''
    try:
        xml = ElementTree.parse(filename)
        root = xml.getroot()
        indiv_info = [child.attrib for child in root]
        
        with db_session:
            for info in indiv_info:
                IndividualInfo(**info)
    except Exception as e:
        print(f'Error: {e}')
        db.rollback()
    else:
        db.commit()
        print(f'Successfully inserted {len(indiv_info)} rows from xml.')

@db_session
def extract_and_upload_json(filename):
    '''This function extracts information from a json file and uploads it to a database'''
    with open(filename) as json_file:
        finance_info = json.load(json_file)
        
        try:
            for info in finance_info:
                FinanceInfo(**info)
        except Exception as e:
            print(f'Error: {e}')
            db.rollback()
        else:
            print(f'Successfully inserted {len(finance_info)} rows from json.')

@db_session
def convert_to_json(query, outfilename):
    '''This function converts the query results to json'''
    # Get the header and value for each row and Create a dictionary using key, value pair 
    json_joined = [dict((query.description[i][0], value) for i, value in enumerate(row)) for row in query.fetchall()]
    with open(outfilename, 'w') as json_file:
        json.dump(json_joined, json_file) 

@db_session
def run_query():        # Function would run the query at every call 
        db.execute('''CREATE TABLE joined AS 
                        SELECT  ind.firstName, ind.lastName, ind.age, ind.sex, ind.marital_status, ind.retired, ind.dependants, 
                                ind.salary, ind.pension, ind.company, ind.commute_distance, veh.vehicle_make, veh.vehicle_model, 
                                veh.vehicle_year, veh.vehicle_type, fin.address_main, fin.address_city, 
                                fin.address_postcode, fin.iban, fin.credit_card_number, fin.credit_card_security_code, 
                                fin.credit_card_start_date, fin.credit_card_end_date, fin.debt   
                        FROM individual AS ind
                        LEFT JOIN vehicle AS veh
                                ON ind.firstName = veh.firstName 
                                AND ind.lastName = veh.lastName
                                AND ind.age = veh.age
                        LEFT JOIN finance AS fin
                                ON ind.firstName = fin.firstName
                                AND ind.lastName = fin.lastName
                                AND ind.age = fin.age         
        ''') # The result of the query is returned to be used in another function