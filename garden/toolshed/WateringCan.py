import os
import re
import narrator

from random import random
from glob import glob

import inventory
from inventory.Item import Factory
from inventory.Item import FixtureSpec

class WateringCan(FixtureSpec):

    soils = {
        "ClaySoil": .5,
        "SandySoil": .75,
        "LoamSoil": .25
    }

    def __init__(self):
        super().__init__()
        self.grow_chance = 0
        self.n = narrator.Narrator()
        self.n.path.change({"act": 3, "scene": 0})
        
    def validate(self):
        scenes = []
        inv = inventory.items.list
        if not self.is_sandy(inv):
            scenes.append(3)
        if not self.is_fertilizer(inv):
            scenes.append(4)
        if scenes:
            self.n.path.scene = scenes[0]
            return False
        return True

    def survey(self):
        return glob(f"*Seed*.py")

    def count(self):
        seeds = {}
        seed_files = self.survey()
        for seed in seed_files:
            name, ext = seed.split(".")
            name = re.search(
                r"[a-zA-Z]+", 
                name
            ).group(0)
            try:
                seeds[name] += 1
            except KeyError:
                seeds[name] = 1
        if len(seeds) == 0:
            self.n.path.scene = 1
            self.n.narrate()
            exit()
        return seeds
    
    def is_sandy(self, inv: dict = {}) -> bool:
        for item in inv:
            if item in ["ClaySoil", "LoamSoil", "SandySoil"]:
                self.grow_chance = self.soils[item]
                inventory.items.trash(item, 10)
                return True
        return False

    def is_fertilizer(self, inv: dict = {}) -> bool:
        for item in inv:
            if item in ["Fertilizer"]:
                inventory.items.trash(item, 1)
                return True
        return False
    
    def water(self, folder: str = "."):
        if self.validate() and random() >= self.grow_chance:
            for seed in self.seeds:
                amount = self.seeds[seed]
                grown_name = seed.replace("Seed", "")
                print(f"GROWING {amount} {seed}")
                for _ in range(amount):
                    Factory(grown_name)
                for file in self.survey():
                    os.remove(file)
            return
        print("You water the soil, but it doesn't seem to sprout.")
    
    def use(self, location: str = "."):
        os.chdir(location)
        self.seeds = self.count()
        self.water(location)

can = WateringCan()