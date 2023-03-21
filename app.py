from database import connect_to_db
from utils import extract_and_upload_csv, extract_and_upload_xml, extract_and_upload_json, run_query

connect_to_db(filename='my_database.sqlite')

extract_and_upload_csv('data/user_data.csv')
extract_and_upload_xml('data/user_data.xml')
extract_and_upload_json('data/user_data.json')

run_query()
