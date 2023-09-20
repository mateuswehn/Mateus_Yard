import inventory

from inventory import Acquire
from inventory.Item import Factory
from inventory.Item import FixtureSpec

class SoilMixer(FixtureSpec):

    mixes = {
        "Loam": {
            "Sand": .20,
            "Silt": .30,
            "Clay": .50
        },
        "Sandy": {
            "Sand": .80,
            "Silt": .10,
            "Clay": .10
        },
        "Clay": {
            "Sand": .10,
            "Silt": .10,
            "Clay": .80
        }
    }

    def __init__(self):
        super().__init__()
        self.soils = {}
        inv = inventory.items.list
        for item in inv:
            if item in ["Clay", "Silt", "Sand"]:
                self.soils[item] = inv[item]["quantity"]
    
    def evaluate(self):
        possible = None
        total = sum(
            list(self.soils.values())
        )
        self.soils = dict(
            sorted(
                self.soils.items(),
                reverse = True
            )
        )
        materials = list(map(
            lambda material: self.soils[material] / total,
            list(self.soils.keys())
        ))
        for kind in self.mixes:
            ingredients = sorted(
                self.mixes[kind].items(),
                key = lambda amt: amt[0],
                reverse = True
            )
            for _ in range(len(materials)):
                possible = kind
                requirement = ingredients[_][1]
                if materials[_] < requirement:
                    possible = None
                    break
            if possible: break
        return possible

    def mix(self):
        inv = inventory.items.list
        for item in inv:
            if "Soil" in item:
                return
        product = self.evaluate()
        if not product:
            print("⚠️  Not enough ingredients to make a soil.")
            return
        for item in self.soils:
            inventory.items.trash(item, 10)
        Factory(f"{product}Soil") 
        Acquire(f"{product}Soil.py")

    def use(self):
        self.mix()

mixer = SoilMixer()