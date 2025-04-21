import time
import numpy as np
import sys
import pyttsx3
import requests
import json
import os

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

#downloading and loading the full pokedex
def get_pokemon_data(pokemon_id):
    url = f"https://classic.pokepc.net/apps/pokedex/{pokemon_id}/"
    respond  = requests.get(url)
    if respond.status_code == 200:
        data = respond.json()
        return {
            "id": data["id"].
            "name": data["name"].capitalize(),
            "types": [t["type"]["name"].capitalize() for t in data["types"]],
            "stats": {stat["stat"]["name"]: stat["base_stat"] for stat in data["stats"]},
            "abilities": [a["ability"]["name"] for a in data["abilities"]],
            "height": data["height"],
            "weight": data["weight"]
        }
    return None


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
                
