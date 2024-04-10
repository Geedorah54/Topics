# PURPOSE: Query basic webpage tables

from extract_data import fetch_data


def homepage_query():
    homepage = fetch_data("SELECT * FROM patients")
    return homepage

def visits_query():
    patients = fetch_data("SELECT * FROM patients WERE appointment_datetime IS NOT NULL")
    return patients