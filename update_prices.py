import requests
import os

urlBySet = {
    "Base Set":
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
        "https://tcgcsv.com/tcgplayer/3/23651/ProductsAndPrices.csv"
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

updatePrices()

