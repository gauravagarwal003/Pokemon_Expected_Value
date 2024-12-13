import csv
from datetime import datetime

def clean_and_convert_dict(d):
    cleaned_dict = {}
    for key, value in d.items():
        if value != "":
            cleaned_dict[key] = int(value)
    return cleaned_dict

pricesBySet = {}
rarityProbabilitiesBySet = {}

with open('rarities.csv', 'r') as file:
    csv_reader = csv.DictReader(file)
    for row in csv_reader:
        setName = row['Set']
        del row['Set']
        rarityProbabilitiesBySet[setName] = clean_and_convert_dict(row)

for setName in rarityProbabilitiesBySet:
    sum = 0
    with open(f'prices/{setName}.csv', 'r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            if not row['extNumber'].isspace(
            ) and row['extRarity'] in rarityProbabilitiesBySet[
                    setName] and float(row['marketPrice']) > 1:            
                sum += float(
                    row['marketPrice']) / rarityProbabilitiesBySet[setName][
                        row['extRarity']]
    
    pricesBySet[setName] = round(sum,2)
    
current_date = datetime.now().strftime('%Y-%m-%d')
csv_filename = "sv_packs_expected_value.csv"
file_exists = False
try:
    with open(csv_filename, mode='r', newline='') as file:
        file_exists = True
except FileNotFoundError:
    pass

with open(csv_filename, mode='a', newline='') as file:
    writer = csv.writer(file)

    if not file_exists:
        header = ['Date'] + list(pricesBySet.keys())
        writer.writerow(header)

    row = [current_date] + list(pricesBySet.values())
    writer.writerow(row)
