import time
import numpy as np
import sys
import pyttsx3
import requests
import json
import os
from bs4 import BeautifulSoup

#Google voice to text to narrate
voice = pyttsx3.init()
voice.say("Pikachu used Thunderbolt!")
voice.runAndWait()

#delay text printing
def delay_rint(s):
    for c in s:
        sys.stdout.write(c)
        sys.stdout.flush()
        time.sleep(0.05)

#scraping the website to access each section and full pokedex
def scrape_pokedex(url="https://www.serebii.net/pokemon/nationalpokedex.shtml", filename="serebii_pokedex.json"):
    if os.path.exists(filename):
        print("Serebii Pokédex already scarped.")
        return
    headers = {"User-Agent": "Mozilla/5.0"}
    response = request.get(url, headers = headers)

if response.status_code != 200:
    print("Failed to load Serebii page.")
    return

soup = BeautifulSoup(response.content, html.parser")
table = soup.find("table", {"class": "dextable"})
pokedex = []
rows = table.find_all("tr")[2:] #skips headers
    
for r in rows:
    colms = row.find_all("td")
    if len(colms) < 6:
        continue

    number = colms[0].text.strip()
    name = colms[3].text.strip()
    type1 = colms[4].img["alt"]
    type2 = colms[5].img["alt"]

    pokedex.append({
        "number": number,
        "name": name,
        "types": [type1] if not type2 else [type1,type2]
    })

with open(filename,"w") as f:
    json.dump(pokedex, f, indent = 2)
print(f"Saved {len(pokedex)} Pokémon to {filename}")

def load_serebii_pokedex(filename="serebii_pokedex.json")
    with open(filename, "r") as f:
        return json.load(f)

class Pokemon:
    def __init__(self, name, types, moves, EVs, health):
        self.name = name
        self.types - types
        self.moves = moves
        self.attack = EVs['ATTACK']
        self.defense = EVs['DEFENSE']
        self.bars = 20 
    
    def fight(self, Pokemon2):
        print("-------POKEMON BATTLE------")
        print(f"\n{self.name}")
        print("TYPE/", self.types)
        print("ATTACK/", self.attack)
        print("DEFENSE/", self.defense)
        print("LVL/", 3*(1 + np.mean([self.attack, self.defense])))
        print("\nVS")
        print("-------POKEMON BATTLE------")
        print(f"\n{Pokemon2.name}")
        print("TYPE/", Pokemon2.types)
        print("ATTACK/", Pokemon2.attack)
        print("DEFENSE/", Pokemon2.defense)
        print("LVL/", 3*(1 + np.mean([Pokemon2.attack, Pokemon2.defense])))
        print("\nVS")
        
        time.sleep(2)
        
        #Pokemon Types
        types = ['Fire', 'Water', 'Grass', 'Rock', 'Ground', 'Ice', 'Psychic', 'Ghost', 'Fighting', 'Steel', 'Poision', 'Fairy', 'Dark']
        if k in enumerate(types):
            if self.types == k:
 def create_random_pokedex(pokedex):
     entry = random.choice(pokedex)
      name = entry['name']
      types = entry['types']
      moves = []
      EVs = {
         'ATTACK': random.randit(40,100),
            'DEFENSE': random.randit(40,100)
      }
       health = random.randit(50,100)
       return Pokemon(name,types,moves,EVs, health)
if __name__ == "__main__":
    scrape_serebii_pokedex()
    pokedex = load_serebii_pokedex()

    print("\nCreating two random Pokémon...\n")
    p1 = create_random_pokemon(pokedex)
    p2 = create_random_pokemon(pokedex)

    p1.fight(p2)

         
