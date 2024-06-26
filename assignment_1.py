# -*- coding: utf-8 -*-
"""Assignment 1.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1d6_U0JZavElyyPMYIPCvwhMe4f8a8r5s

Internship Assignment
"""

#Importing required libraries

import json
from datetime import datetime
import csv
import os

#Assign File path

patient_file = "/content/Patient.ndjson"
condition_file = "/content/Condition.ndjson"
encounter_file = "/content/Encounter.ndjson"
encounter_icu_file = "/content/EncounterICU.ndjson"

# function to convert Unix Timestamp

def to_unix(timestamp):
   return int(datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S%z").timestamp())

# Function to read and parse JSON files

def read_json(file_path):
    data = []
    # Created an empty list to store json file data
    with open(file_path, "r") as f:
        for line in f:
            json_data = json.loads(line)
            data.append(json_data)
    # we will read the file and return a list of dictionaries
    return data

# Our output csv file where we will store the data

output_csv = "/content/output_csv.csv"

# Storing our json data in variables

patients = read_json(patient_file)
conditions = read_json(condition_file)
encounters = read_json(encounter_file)
encounters_icu = read_json(encounter_icu_file)

# Creating a dictionary to hold patient id and thire associated conditions

patient_conditions = {}
for condition in conditions:
    patient_id = condition['subject']['reference'].split('/')[-1]
    condition_data = {
        'code': condition['code']['coding'][0]['code'],
        'description': condition['code']['coding'][0]['display']
    }
    if patient_id in patient_conditions:
        patient_conditions[patient_id].append(condition_data)
    else:
        patient_conditions[patient_id] = [condition_data]

# Creating a dictionary to store timestamps

patient_condition_timestamps = []
all_encounters = encounters + encounters_icu
for patient_id, conditions_list in patient_conditions.items():
    for condition in conditions_list:
        condition_code = condition['code']
        for encounter in all_encounters:
            if encounter['subject']['reference'].split('/')[-1] == patient_id:
                encounter_start_time = encounter['period']['start']
                patient_condition_timestamps.append({
                    'pid': patient_id,
                    'time': encounter_start_time,
                    'code': condition_code,
                    'description': condition['description']
                })
                break

"""Final Ouput file"""

with open(output_csv, mode='w', newline='') as csv_file:
    fieldnames = ['pid', 'time', 'code', 'description']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

    writer.writeheader()
    for record in patient_condition_timestamps:
        record['time'] = to_unix(record['time'])
        writer.writerow(record)

print("ouptut csv file generated")