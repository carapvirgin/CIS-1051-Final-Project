#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import random
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
        print("Serebii Pokédex already scraped.")
        return
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers = headers)

    if response.status_code != 200:
        print("Failed to load Serebii page.")
        return

    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.find("table", {"class": "dextable"})
    pokedex = []
    rows = table.find_all("tr")[2:] #skips headers
    
    for r in rows:
        colms = r.find_all("td")
        if len(colms) < 6:
            continue

        number = colms[0].text.strip()
        name = colms[3].text.strip()
        
        type1_img = colms[4].img
        type2_img = colms[5].img if colms[5].img else None
        
        type1 = colms[4].img["alt"] if type1_img and "alt" in type1_img.attrs else None
        type2 = colms[5].img["alt"] if type2_img and "alt" in type2_img.attrs else None

        pokedex.append({
            "number": number,
            "name": name,
            "types": [type1] if not type2 else [type1,type2]
        })

    with open(filename,"w") as f:
        json.dump(pokedex, f, indent = 2)
    print(f"Saved {len(pokedex)} Pokémon to {filename}")

def load_serebii_pokedex(filename="serebii_pokedex.json"):
    with open(filename, "r") as f:
        return json.load(f)

class Pokemon:
    def __init__(self, name, types, moves, EVs, health):
        self.name = name
        self.types = types
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
        
        #Pokemon Types and Advantages
        types_and_advantages = {
            'Normal': [],
            'Fire': ['Grass', 'Ice','Bug','Steel'],
            'Water': ['Fire', 'Ground', 'Rock'],
            'Grass': ['Water', 'Ground', 'Rock'],
            'Electric': ['Water', 'Flying'],
            'Rock': ['Fire', 'Ice', 'Flying', 'Bug'],
            'Ground': ['Fire', 'Electric', 'Rock', 'Poison', 'Steel'],
            'Psychic': ['Fighting', 'Poison'],
            'Fighting': ['Normal', 'Rock', 'Ice', 'Dark', 'Steel'],
            'Dark': ['Psychic', 'Ghost'],
            'Ghost': ['Psychic', 'Ghost'],
            'Ice': ['Grass', 'Ground', 'Flying', 'Dragon'],
            'Flying': ['Grass','Fighting', 'Bug'],
            'Poison': ['Grass', 'Fairy'],
            'Bug': ['Grass', 'Psychic', 'Dark'],
            'Dragon': ['Dragon'],
            'Steel': ['Ice', 'Rock', 'Fairy'],
            'Fairy': ['Fighting', 'Dragon', 'Dark']
        }
        
        self_effectiveness = 1
        enemy_effectiveness = 1
        self_message = ""
        enemy_message = ""
    
        for self_type in self.types:
            for enemy_type in Pokemon2.types:
                if enemy_type in types_and_advantages.get(self_type, []):
                    self_effectiveness = 2
                    self_message = "It's super effective!"
                elif self_type in types_and_advantages.get(enemy_type, []):
                    self_effectiveness = 0.5
                    self_message = "It's not very effective ..."
        for enemy_type in Pokemon2.types:
            for self_type in self.types:
                if self_type in types_and_advantages.get(enemy_type, []):
                    enemy_effectiveness = 2
                    enemy_message = "It's super effective!"
                elif enemy_type in types_and_advantages.get(self_type, []):
                    enemy_effectiveness = 0.5
                    enemy_message = "It's not very effective ..."
                
        self_hp = self.bars
        enemy_hp = Pokemon2.bars
    
        while self_hp > 0 and enemy_hp > 0:
            #player 1 attacks first
            print(f"\n{self.name} attacks!")
            time.sleep(1)
            damage = int(self.attack * self_effectiveness)
            Pokemon2.bars -= damage / 10
            enemy_hp = Pokemon2.bars
            print(f"{Pokemon2.name} now has {max(0, enemy_hp):.1f} health bars.")
        
            if self_message:
                print(self_message)
                time.sleep(1)
            if enemy_hp <= 0:
                print(f"\n{Pokemon2.name} fainted!")
                break
        
            #player 2 attacks second
            print(f"\n{Pokemon2.name} attacks!")
            time.sleep(1)
            damage = int(Pokemon2.attack * enemy_effectiveness)
            self.bars -= damage / 10
            self_hp = self.bars
            print(f"{self.name} now has {max(0, self_hp):.1f} health bars.")

            if enemy_message:
                print(enemy_message)
                time.sleep(1)

            if self_hp <= 0:
                print(f"\n{self.name} fainted!")
                break
                
def create_random_pokedex(pokedex):
    entry = random.choice(pokedex)
    name = entry['name']
    types = entry['types']
    moves = []
    EVs = {
        'ATTACK': random.randint(40,100),
        'DEFENSE': random.randint(40,100)
    }
    health = random.randint(50,100)
    return Pokemon(name,types,moves,EVs, health)

if __name__ == "__main__":
    scrape_pokedex()
    pokedex = load_serebii_pokedex()

    print("\nCreating two random Pokémon...\n")
    p1 = create_random_pokedex(pokedex)
    p2 = create_random_pokedex(pokedex)

    p1.fight(p2)


