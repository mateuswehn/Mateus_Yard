from inventory import Factory
from inventory import Acquire
from inventory import FixtureSpec

class FertilizerDispenser(FixtureSpec):

    def __init__(self):
        super().__init__()

    @staticmethod
    def dispense():
        Factory("Fertilizer")
        Acquire("Fertilizer.py")

dispenser = FertilizerDispenser()