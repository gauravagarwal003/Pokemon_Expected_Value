import csv
from datetime import datetime
import requests
import os

urlBySet = {
    "Scarlet & Violet Base Set":
        "https://tcgcsv.com/tcgplayer/3/22873/ProductsAndPrices.csv",
    "Paldea Evolved":
        "https://tcgcsv.com/tcgplayer/3/23120/ProductsAndPrices.csv",
    "Obsidian Flames":
        "https://tcgcsv.com/tcgplayer/3/23228/ProductsAndPrices.csv",
    "151":
        "https://tcgcsv.com/tcgplayer/3/23237/ProductsAndPrices.csv",
    "Paradox Rift":
        "https://tcgcsv.com/tcgplayer/3/23286/ProductsAndPrices.csv",
    "Paldean Fates":
        "https://tcgcsv.com/tcgplayer/3/23353/ProductsAndPrices.csv",
    "Temporal Forces":
        "https://tcgcsv.com/tcgplayer/3/23381/ProductsAndPrices.csv",
    "Twilight Masquerade":
        "https://tcgcsv.com/tcgplayer/3/23473/ProductsAndPrices.csv",
    "Stellar Crown":
        "https://tcgcsv.com/tcgplayer/3/23537/ProductsAndPrices.csv",
    "Surging Sparks":
        "https://tcgcsv.com/tcgplayer/3/23651/ProductsAndPrices.csv",
    "Prismatic Evolutions":
        "https://tcgcsv.com/tcgplayer/3/23821/ProductsAndPrices.csv"
}

def updatePrices():
    # Create the 'prices' folder if it doesn't exist
    if not os.path.exists('prices'):
        os.makedirs('prices')

    # Loop through the urlBySet dictionary and fetch data
    for set in urlBySet:
        response = requests.get(urlBySet[set])
        if response.status_code == 200:
            # Write the response content to a CSV file inside the 'prices' folder
            with open(f'prices/{set}.csv', 'w', newline='', encoding='utf-8') as f:
                f.write(response.text)
        else:
            print(f"Failed to retrieve the CSV file for {set}. Status code: {response.status_code}")

def clean_and_convert_dict(d):
    cleaned_dict = {}
    for key, value in d.items():
        if value != "":
            cleaned_dict[key] = int(value)
    return cleaned_dict

pricesBySet = {}
rarityProbabilitiesBySet = {}
updatePrices()

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
            if not row['extNumber'].isspace():
                if row['marketPrice'] and float(row['marketPrice']) > 1:       
                    if row['extRarity'] in rarityProbabilitiesBySet[setName]: 
                        sum += float(row['marketPrice']) / rarityProbabilitiesBySet[setName][row['extRarity']]
                    else:
                        masterBallPattern = 'Master Ball Pattern'
                        pokeBallPattern = 'Poke Ball Pattern'
                        if masterBallPattern in row['name']:
                            sum += float(row['marketPrice']) / rarityProbabilitiesBySet[setName][masterBallPattern]    
                        elif pokeBallPattern in row['name']:
                            sum += float(row['marketPrice']) / rarityProbabilitiesBySet[setName][pokeBallPattern]
    
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
