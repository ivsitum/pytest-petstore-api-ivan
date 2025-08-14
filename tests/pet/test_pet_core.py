import pytest
import random
from utilities.response_validator import ResponseValidator

class TestPetsAPI:
    validator = ResponseValidator()

    @pytest.mark.pet
    @pytest.mark.create
    @pytest.mark.smoke
    @pytest.mark.contract
    def test_T001_post_create_pet_minimal_valid(self, api_client, pet_data):
        pet_data["photoUrls"] = ["https://en.wikipedia.org/wiki/File:Weisse_welpen.jpg"]
        response = api_client.post("/pet", pet_data)
        json_data = response.json()
        print("API JSON response:", json_data)
        self.validator.validate_status_code(response, 200)
        self.validator.validate_json_response(response)
        self.validator.validate_json_value(response, "id", pet_data["id"])
        self.validator.validate_json_value(response, "name", pet_data["name"])

    @pytest.mark.pet
    @pytest.mark.read
    @pytest.mark.contract
    def test_T002_get_pet_by_id(self, api_client, get_id_from_pet_data):
        pet_id = get_id_from_pet_data
        response = api_client.get(f"/pet/{pet_id}")
        json_data = response.json()
        print("API JSON response:", json_data)
        self.validator.validate_status_code(response, 200)
        self.validator.validate_json_response(response)
        self.validator.validate_json_value(response, "id", pet_id)
        # Petstore always returns these fields if pet exists
        assert "name" in json_data
        assert "photoUrls" in json_data

    @pytest.mark.pet
    @pytest.mark.update
    def test_T003_put_update_pet_name_and_status(self, api_client, pet_data):
        pet_data["status"] = "sold"
        pet_data["name"] = "UpdatedName"
        response = api_client.put("/pet", pet_data)
        json_data = response.json()
        print("API JSON response:", json_data)
        self.validator.validate_status_code(response, 200)
        self.validator.validate_json_value(response, "id", pet_data["id"])
        self.validator.validate_json_value(response, "name", "UpdatedName")
        self.validator.validate_json_value(response, "status", "sold")

    @pytest.mark.pet
    @pytest.mark.read
    def test_T004_get_pet_unknown_id(self, api_client):
        unknown_id = random.randint(10**11, 10**12 - 1)
        response = api_client.get(f"/pet/{unknown_id}")
        print("API JSON response:", response.json())
        # Petstore returns 404 for unknown IDs
        self.validator.validate_status_code(response, 404)

    @pytest.mark.pet
    @pytest.mark.negative
    def test_T005_post_pet_missing_name(self, api_client, pet_data):
        pet_data.pop("name", None)
        response = api_client.post("/pet", pet_data)
        print("API JSON response:", response.json())
        #Petstore returns 200 and creates the pet
        self.validator.validate_status_code(response, 200)

    @pytest.mark.pet
    @pytest.mark.negative
    def test_T006_post_pet_invalid_id_type(self, api_client, pet_data):
        pet_data["id"] = "abc"
        response = api_client.post("/pet", pet_data)
        print("API JSON response:", response.json())
        # Petstore returns 500 for invalid id type
        self.validator.validate_status_code(response, 500)

    @pytest.mark.pet
    @pytest.mark.negative
    def test_T007_put_pet_missing_id(self, api_client, pet_data):
        pet_data.pop("id", None)
        response = api_client.put("/pet", pet_data)
        print("API JSON response:", response.json())
        # Petstore returns 200 and assigns a new ID
        self.validator.validate_status_code(response, 200)

    @pytest.mark.pet
    @pytest.mark.auth
    def test_T008_auth_header_check(self, api_client, pet_data):
        response = api_client.post("/pet", pet_data, headers={})
        print("API JSON response:", response.json())
        #Petstore does not enforce auth — returns 200
        self.validator.validate_status_code(response, 200)
