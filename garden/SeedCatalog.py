import os
import json
import narrator

from inventory import Acquire
from inventory import Factory
from inventory import FixtureSpec

class Catalog(FixtureSpec):

    def __init__(self, seed_name: str = ""):
        """ Load seed catalog """
        super().__init__()
        self.seeds = self.load()
  
    @staticmethod
    def load(filename: str = ".catalog.json") -> dict:
        """ Load catalog from file """
        catalog = {}
        with open(filename, "r") as fh:
            catalog = json.load(fh)
        return catalog["seeds"]
  
    def display(self) -> None:
        """ Display seed varietals """
        for seed in self.seeds:
            idx = self.seeds.index(seed) + 1
            print(f"{idx}. {seed['name']}")
  
    def use(self):
        self.display()

def main():
    # Setup the catalog
    seed_catalog = Catalog()
    # Create the narrator
    n = narrator.Narrator()
    # Set the proper path
    n.path.change({"act": 2, "scene": 0})
    # Narrate the scene
    n.narrate()
    # Ask user to select seeds
    while True:
        seed_catalog.display()
        choice = input("SELECT SEED NUMBER: ")
        # If no choice made, end choice-making
        if not choice: break
        try:
            # Create the file for selected seed
            choice = int(choice) - 1
            seed_name = seed_catalog.seeds[choice]["name"]
            file_name = seed_catalog.seeds[choice]["file"]
            # TODO: Address title casing issue in inventory
            Factory(f"{seed_name} Seed")
            Acquire(f"{file_name}.py")
            # Display success
            n.path.scene = 2
        except:
            n.path.scene = 1
            exit()
        n.narrate()

if __name__ == "__main__":
  main()