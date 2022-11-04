#!/bin/python
import csv
import hashlib
import json
import sys
import os


def convert_to_json():
    f = ''
    teamName = ''
    teamCount = 0
    totalNum = 0
    if os.path.exists(sys.argv[1]):
        f = f'{sys.argv[1]}'
        print("will start process now ")
    else:
        print("File not found")

    # Checks if the NFT_JSON directory exist and create one if it doesnt
    if os.path.exists('NFT_JSON'):
        print('yes')
        pass
    else:
        os.mkdir("NFT_JSON")

    if os.path.exists('filename.output.csv'):
        os.remove('filename.output.csv')
    else:
        pass

    # open the csv file name passed as argument
    with open(f, 'r') as f1:
        csv_file = csv.DictReader(f1)

        """ Iterate through the csv_file
        checking for row with team name and counting them, 
        also counting the rows with valid input """

        for row in csv_file:
            if row['TEAM NAMES'].lower().startswith('team'):
                teamCount += 1
            elif row['TEAM NAMES'].lower() == None:
                pass
            else:
                totalNum += 1;

    with open(f, 'r') as f1:
        csv_file = csv.DictReader(f1)
        fieldnames = [i for i in csv_file.fieldnames] + ['HASH']

        with open('filename.output.csv', 'w') as outputfile:
            writer = csv.DictWriter(outputfile, fieldnames=fieldnames)
            writer.writeheader()

        for row in csv_file:
            if row['TEAM NAMES']:
                teamName = row['TEAM NAMES']

            name = row['Name']
            description = row['Description']
            series_num = row['Series Number']
            gender = row['Gender']
            series_total = totalNum

            json_form = {

                "format": "CHIP-0007",
                "name": f"{name}",
                "description": f"{description}",
                "minting_tool": f"{teamName}",
                "sensitive_content": False,
                "series_number": series_num,
                "series_total": series_total,
                "attributes": [
                    {
                        "trait_type": "Gender",
                        "value": f"{gender}"
                    },
                ],
                "collection": {
                    "name": "Zuri NFT Tickets for Free Lunch",
                    "id": "b774f676-c1d5-422e-beed-00ef5510c64d",
                    "attributes": [
                        {
                            "type": "description",
                            "value": "Rewards for accomplishments during HNGi9."
                        }
                    ]
                },
            }

            if row['Attributes']:
                j = row['Attributes']
                j = j.split(';')
                for i in j:
                    tmp = i.split(':')
                    s1 = tmp[0].strip(" ")
                    s2 = ""
                    try:
                        s2 = tmp[1]
                    except Exception as e:
                        pass
                    json_form['attributes'].append({"trait_type": s1, "value": s2})
            hash = hashlib.sha256(str(json_form).encode()).hexdigest()
            # json_form['hash'] = hash
            row['HASH'] = hash

            with open('filename.output.csv', 'a') as outputfile:
                writer = csv.DictWriter(outputfile, fieldnames=fieldnames)
                writer.writerow(row)

            with open(f'NFT_JSON/{row["Filename"]}.json', 'w') as json_file:
                json_file.write(json.dumps(json_form, indent=4))


convert_to_json()
