import pytest
from app import app, entries

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        # reset state before each test
        entries.clear()
        yield client

def test_add_entry_with_happiness(client):
    # Test adding an entry with happiness
    response = client.post('/add_entry', data={'content': 'Test Entry Content', 'happiness': '😃'})

    # Check if the response is a redirect to the index page
    assert response.status_code == 302
    assert response.headers['Location'] == '/'

    # Check if the entry was added to the database with the correct happiness
    entry = entries[0]
    assert entry is not None
    assert entry.content == 'Test Entry Content'
    assert entry.happiness == '😃'
