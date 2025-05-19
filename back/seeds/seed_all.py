import sys
import os

# Add parent directory to path so we can import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import seed functions from each collection script
from seeds.seed_collection import seed_spiderman_collection
from seeds.seed_underworld import seed_underworld_collection
from seeds.seed_blade import seed_blade_collection
from seeds.seed_percy_jackson import seed_percy_jackson_collection


def seed_all_collections():
    """Seed all movie collections"""
    print("=== Starting to seed all movie collections ===")
    print("\n1. Spider-Man Collection")
    seed_spiderman_collection()
    
    print("\n2. Underworld Collection")
    seed_underworld_collection()
    
    print("\n3. Blade Collection")
    seed_blade_collection()
    
    print("\n4. Percy Jackson Collection")
    seed_percy_jackson_collection()
    
    print("\n=== All collections have been seeded successfully ===")


if __name__ == "__main__":
    seed_all_collections()
