import pytest
from faker import Faker
from datetime import datetime, timezone
import json
import os
from api.api_client import APIClient

fake = Faker()

def data_file(filename):
    return os.path.join(os.path.dirname(__file__), "data", filename)


@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture()
def pet_data():
    """Generate test data for a pet."""
    filename = data_file("pet_data.json")
    data = {
        "id": fake.random_int(min=1, max=100),
        "category": {
            "id": fake.random_int(min=1, max=100),
            "name": fake.word()
        },
        "name": fake.first_name(),
        "photoUrls": [fake.image_url()],
        "tags": [
            {
                "id": fake.random_int(min=1, max=100),
                "name": fake.word()
            }
        ],
        "status": fake.random_element(elements=["available", "pending", "sold"])
    }
    with open(filename, 'w', encoding='utf-8') as file_object:
        json.dump(data, file_object, ensure_ascii=False, indent=4)
    return data


@pytest.fixture
def get_id_from_pet_data():
    """Get ID from generated pet data."""
    filename = data_file("pet_data.json")
    with open(filename, 'r', encoding='utf-8') as file:
        data = json.load(file)
        return data.get('id')


