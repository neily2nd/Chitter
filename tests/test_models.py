import pytest
from models import User, Peep
from seeds.seed import seed_database

# Fixture to seed the database before each test
@pytest.fixture(autouse=True)
def setup_database():
    seed_database()

# Test case to create a peep
def test_create_peep():
    # Create a new user
    user = User.create(username='test_user', email='test@example.com', password='password', name='Test User')

    # Create a peep for the user
    Peep.create(user=user, content='Test peep content')

    # Retrieve the created peep
    peep = Peep.get(Peep.user == user)

    # Assert that the peep content matches
    assert peep.content == 'Test peep content'

