import csv

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
    with open(f'{setName}.csv', 'r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            if not row['extNumber'].isspace(
            ) and row['extRarity'] in rarityProbabilitiesBySet[
                    setName] and float(row['marketPrice']) > 1:            
                sum += float(
                    row['marketPrice']) / rarityProbabilitiesBySet[setName][
                        row['extRarity']]
    
    pricesBySet[setName] = sum

pricesBySet = dict(sorted(pricesBySet.items(), key=lambda item: item[1]))

for set in pricesBySet:
    print(f"{set}: ${pricesBySet[set]}")
