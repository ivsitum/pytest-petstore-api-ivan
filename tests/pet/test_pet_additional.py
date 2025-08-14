import pytest
import random
import time
from utilities.response_validator import ResponseValidator


class TestPetsAdditional:
    validator = ResponseValidator()
    @pytest.mark.pet
    @pytest.mark.create
    @pytest.mark.contract
    @pytest.mark.parametrize("status_value", ["available", "pending", "sold"])
    def test_T009_post_parametrized_status(self, api_client, pet_data, status_value):
        pet_data["status"] = status_value
        pet_data["photoUrls"] = ["https://example.com/ok.png"]
        r = api_client.post("/pet", pet_data)
        body = r.json()
        print("API JSON response:", body)
        self.validator.validate_status_code(r, 200)
        self.validator.validate_json_response(r)
        self.validator.validate_json_value(r, "id", pet_data["id"])
        self.validator.validate_json_value(r, "status", status_value)

    @pytest.mark.pet
    @pytest.mark.contract
    def test_T010_contract_types(self, api_client):
        pet_data = {
            "id": random.randint(1000, 999999),
            "category": {"id": 42, "name": "dark"},
            "name": "Troy",
            "photoUrls": ["https://example.com/ok.png"],
            "tags": [{"id": 23, "name": "see"}],
            "status": "pending"
        }

        r_post = api_client.post("/pet", pet_data)
        self.validator.validate_status_code(r_post, 200)
        posted_pet = r_post.json()
        pet_id = posted_pet["id"]
        print(f"POST JSON: {posted_pet}")
        # Retry GET up to 3 times if 404
        # After creating a pet the backend may take a short time to respond
        fetched_pet = None
        for attempt in range(3):
            r_get = api_client.get(f"/pet/{pet_id}")
            if r_get.status_code == 200:
                fetched_pet = r_get.json()
                break
            time.sleep(2)
        assert fetched_pet, f"Pet {pet_id} not found after retries"

        print(f"GET JSON: {fetched_pet}")
        assert isinstance(fetched_pet["id"], int)
        assert isinstance(fetched_pet["name"], str)
        assert isinstance(fetched_pet["photoUrls"], list)
        assert all(isinstance(url, str) for url in fetched_pet["photoUrls"])

    @pytest.mark.pet
    @pytest.mark.update
    def test_T011_put_twice_same_payload(self, api_client, pet_data):
        pet_data["photoUrls"] = ["https://example.com/ok.png"]
        self.validator.validate_status_code(api_client.post("/pet", pet_data), 200)
        pet_data["name"] = "SameName"
        pet_data["status"] = "available"
        first_put_response = api_client.put("/pet", pet_data)
        self.validator.validate_status_code(first_put_response, 200)
        second_put_response = api_client.put("/pet", pet_data)
        self.validator.validate_status_code(second_put_response, 200)
        first_put_json = first_put_response.json()
        second_put_json = second_put_response.json()
        print("PUT #1 JSON:", first_put_json)
        print("PUT #2 JSON:", second_put_json)
        assert second_put_json["id"] == pet_data["id"]
        assert second_put_json["name"] == "SameName"
        assert second_put_json["status"] == "available"

    @pytest.mark.pet
    @pytest.mark.delete
    def test_T012_cleanup_delete_created_pet(self, api_client, pet_data):
        image_url = "https://en.wikipedia.org/wiki/File:Gera062005sed.jpg"
        pet_data["photoUrls"] = [image_url]
        create_response = api_client.post("/pet", pet_data)
        self.validator.validate_status_code(create_response, 200)
        pet_id = pet_data["id"]
        delete_response = api_client.delete(f"/pet/{pet_id}")
        print(f"DELETE response: {delete_response.status_code} {delete_response.text}")
        self.validator.validate_status_code_in(delete_response, [200, 404])