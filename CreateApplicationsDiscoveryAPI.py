#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 22 10:07:28 2023

@author: sara.stavaski
"""

import csv
import boto3


def create_application(application_name, description):
    client = boto3.client('discovery')
    response = client.create_application(
        name=application_name,
        description=description
    )
    return response['configurationId']

def main():
    # Replace 'applications.csv' with the path to your CSV file
    csv_file = 'reiapplications.csv'

    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row

        for row in reader:
            application, description = row

            print(f'Creating application: {application}')
            try:
                configuration_id = create_application(application, description)
                print(f'Created application: {application} (ID: {configuration_id})')
            except Exception as e:
                print(f'Error creating application: {e}')

            print('---------------------------------')

if __name__ == '__main__':
    main()
