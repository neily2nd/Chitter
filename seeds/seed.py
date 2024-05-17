import os
import sys

# Add the root directory to the module search path
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(root_dir)
sys.path.append("..")

from models import User, Peep
from peewee import SqliteDatabase

# Connect to your database
db = SqliteDatabase('Chitter.db')

# Define seed database function
def seed_database():
    with db:
        print("Dropping existing tables...")
        # Drop existing tables
        db.drop_tables([User, Peep], safe=True)
        print("Tables dropped successfully.")

        print("Creating tables...")
        # Create tables
        db.create_tables([User, Peep])
        print("Tables created successfully.")

# Call the seed_database() function
seed_database()