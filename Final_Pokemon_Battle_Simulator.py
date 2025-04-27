#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: caravirgin
"""

import time
import random
import sys
import pyttsx3
import requests
import json
import os
from bs4 import BeautifulSoup


#Google voice to text to narrate
voice = pyttsx3.init()

def narrate(text):
    voice.say(text)
    voice.runAndWait()

#delay text printing
def delay_print(s):
    for c in s:
        sys.stdout.write(c)
        sys.stdout.flush()
        time.sleep(0.05)
        
def scrape_move_ids_and_names():
    move_id_to_name = {}
    
    base_url = "https://www.serebii.net/attackdex-swsh/"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(base_url, headers=headers)
    
    if response.status_code != 200:
        print("Failed to load Serebii Moves page.")
        return move_id_to_name

    soup = BeautifulSoup(response.content, 'html.parser')
    move_table = soup.find('table', {'class': 'attacklist'})
    if not move_table:
        print("Failed to find the moves table.")
        return move_id_to_name

    rows = move_table.find_all('tr')
    
    for row in rows:
        cols = row.find_all('td')
        if len(cols) > 1:
            move_id = cols[0].text.strip()  # The move ID
            move_name = cols[1].text.strip()  # The move name
            
            if move_id and move_name:
                move_id_to_name[move_id] = move_name

    return move_id_to_name

# Call the function to scrape and print the move ID to name mapping
move_id_to_name = scrape_move_ids_and_names()
print(move_id_to_name)
        
def scrape_pokemon_moves(pokedex,moves_filename="serebii_moves.json"):
    if os.path.exists(moves_filename):
        print("Serebii moves already scraped. Loading...")
        with open(moves_filename, "r") as f:
            return json.load(f)
    base_url = "https://www.serebii.net/pokemon/"
    moves_data = {}
    
    headers = {"User-Agent": "Mozill/5.0"}
    
    for pokemon in pokedex:
        name = pokemon['name'].lower()
        url = f"{base_url}{name}/"
        
        print(f"Scraping {name} for moves...")
        response = requests.get(url, headers = headers)
        
        if response.status_code != 200:
            print(f"Failed to load {url}")
            moves_data[name] = []
            continue

        soup = BeautifulSoup(response.content, 'html.parser')
        
        tables = soup.find_all('table')
        
        moves_table = None

        for table in tables:
            headers = table.find_all('th')
            if len(headers) == 5:  # Level | Move | Type | Category | Power
                moves_table = table
                break
        
        moves_section = soup.find('h2', string = "Attacks")  # Find the moves link
        if not moves_section:
            print(f"No moves section found for {name}")
            moves_data[name] = []  # No moves data available
            continue
        
        # Find the next table which should have the moves list
        moves_table = moves_section.find_next('table')
        if not moves_table:
            print(f"No moves table found for {name}")
            moves_data[name] = []  # No moves table available
            continue
        
        moves = []

        rows = moves_table.find_all('tr')[1:]  # Skipping the header row
        
        for row in rows:
            colms = row.find_all('td')
            if len(colms) > 2:
                move = colms[1].get_text(strip=True)
                moves.append(move)

        if not moves:
            print(f"No moves found for {name}")
        
        moves_data[name] = moves  
    
    return moves_data

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
        
        print(f"Row for {name}: {r.prettify()}")
        
        type1 = colms[4].find("a")["href"].split("/type/")[-1] if colms[4].find("a") else None
        type2 = colms[5].find("a")["href"].split("/type/")[-1] if colms[5].find("a") else None
        
        if not type1:
            type1 = "Unkown"
            if type2 is None:
                type2 = "Unknown"
                

        pokedex.append({
            "number": number,
            "name": name,
            "types": [type1] if not type2 == "Unkown" else [type1,type2]
        })

    with open(filename,"w") as f:
        json.dump(pokedex, f, indent = 2)
    print(f"Saved {len(pokedex)} Pokémon to {filename}")

def load_serebii_pokedex(filename="serebii_pokedex.json"):
    with open(filename, "r") as f:
        return json.load(f)

class Pokemon:
    def __init__(self, name, types, moves, EVs, health, level = None):
        self.name = name
        self.types = types
        self.moves = moves
        self.attack = EVs['ATTACK']
        self.defense = EVs['DEFENSE']
        self.bars = 20 
        self.level = level or random.randint(1,100)

            
    def choose_random_move(self):
        if not self.moves:
            print(f"{self.name} has no moves to chosse from!")
            return None
        return random.choice(self.moves)
    
    def fight(self, Pokemon2, move_id_to_name):
        print("-------POKEMON BATTLE------")
        narrate("A New battle begins!")
        time.sleep(1)
        
        print(f"\n{self.name}")
        narrate(f"{self.name} enters the battle!")
        print("TYPE/", self.types)
        print("ATTACK/", self.attack)
        print("DEFENSE/", self.defense)
        print("LVL/", self.level)
        time.sleep(1)
        
        print("\nVS")
        print("-------POKEMON BATTLE------")
        print(f"\n{Pokemon2.name}")
        narrate(f"{Pokemon2.name} enters the battle!")

        print("TYPE/", Pokemon2.types)
        print("ATTACK/", Pokemon2.attack)
        print("DEFENSE/", Pokemon2.defense)
        print("LVL/", Pokemon2.level)
        time.sleep(1)
        
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
            narrate(f"\n{self.name} attacks!")
            time.sleep(1)
            move = self.choose_random_move()
            if move is None:
                print(f"{self.name} can't attack this turn!")
                continue
            move_name = move_id_to_name.get(move, move)
            print(f"{self.name} uses {move_name}")
            
            damage = int(self.attack * self_effectiveness)
            Pokemon2.bars -= damage / 10
            enemy_hp = Pokemon2.bars
            print(f"{Pokemon2.name} now has {max(0, enemy_hp):.1f} health bars.")
        
            if self_message:
                print(self_message)
                narrate(self_message)
                time.sleep(1)
            if enemy_hp <= 0:
                print(f"\n{Pokemon2.name} fainted!")
                narrate(f"\n{Pokemon2.name} fainted!")
                break
        
            #player 2 attacks second
            print(f"\n{Pokemon2.name} attacks!")
            narrate(f"\n{Pokemon2.name} attacks!")
            time.sleep(1)
            
            enemy_move = Pokemon2.choose_random_move()
            if enemy_move is None:
                print(f"{Pokemon2.name} can't attack this turn!")
                continue
            enemy_move_name = move_id_to_name.get(enemy_move, enemy_move)
            print(f"{Pokemon2.name} uses {enemy_move_name}")
            
            enemy_damage = int(Pokemon2.attack * enemy_effectiveness)
            self.bars -= enemy_damage / 10
            self_hp = self.bars
            print(f"{self.name} now has {max(0, self_hp):.1f} health bars.")

            if enemy_message:
                print(enemy_message)
                narrate(enemy_message)
                time.sleep(1)

            if self_hp <= 0:
                print(f"\n{self.name} fainted!")
                narrate(f"\n{self.name} fainted!")
                break
                
def create_random_pokedex(pokedex, moves_data):
    entry = random.choice(pokedex)
    name = entry['name']
    types = entry['types']
    moves = moves_data.get(name.lower(),[])
    if not moves:
        print(f"No moves found for {name}, assigning default moves...")
        moves = ["Tackle", "Growl", "Leer"]
    EVs = {
        'ATTACK': random.randint(40,100),
        'DEFENSE': random.randint(40,100)
    }
    health = random.randint(50,100)
    level = random.randint(1,100)
    return Pokemon(name,types,moves,EVs, health, level)

if __name__ == "__main__":
    scrape_pokedex()
    pokedex = load_serebii_pokedex()
    moves_data = scrape_pokemon_moves(pokedex)
    
    print("\nCreating two random Pokémon...\n")


    p1 = create_random_pokedex(pokedex,moves_data)
    p2 = create_random_pokedex(pokedex,moves_data)

    p1.fight(p2,move_id_to_name)
