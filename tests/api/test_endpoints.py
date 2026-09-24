import pytest
import allure
import requests
from utils.config import Config

@allure.epic("REST API Test Suite")
@allure.feature("User Management Endpoints")
@pytest.mark.api
class TestUserApi:

    @property
    def headers(self):
        # reqres.in requires an x-api-key header on every request (free key: https://reqres.in)
        return {"x-api-key": Config.REQRES_API_KEY} if Config.REQRES_API_KEY else {}

    @allure.story("Get Paginated Users List")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("Verify GET /users returning status 200 and valid JSON data structure.")
    def test_get_users_list(self):
        url = f"{Config.API_BASE_URL}/users?page=2"
        
        with allure.step(f"Send GET request to {url}"):
            response = requests.get(url, headers=self.headers, timeout=10)
        
        with allure.step("Validate response status code and schema"):
            assert response.status_code == 200, f"Expected 200, got {response.status_code}"
            data = response.json()
            assert "data" in data
            assert len(data["data"]) > 0
            assert "email" in data["data"][0]

    @allure.story("Create New User")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("Verify POST /users creates user record and returns status 201 with generated ID.")
    def test_create_user(self):
        url = f"{Config.API_BASE_URL}/users"
        payload = {"name": "Apex Tester", "job": "Lead SDET"}
        
        with allure.step(f"Send POST request to {url}"):
            response = requests.post(url, json=payload, headers=self.headers, timeout=10)
            
        with allure.step("Validate 201 Created and payload attributes"):
            assert response.status_code == 201, f"Expected 201, got {response.status_code}"
            res_data = response.json()
            assert res_data["name"] == payload["name"]
            assert res_data["job"] == payload["job"]
            assert "id" in res_data
            assert "createdAt" in res_data

    @allure.story("Update Existing User")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.description("Verify PUT /users/{id} updates user details with status 200.")
    def test_update_user(self):
        url = f"{Config.API_BASE_URL}/users/2"
        payload = {"name": "Apex Tester", "job": "Principal QA Engineer"}
        
        with allure.step(f"Send PUT request to {url}"):
            response = requests.put(url, json=payload, headers=self.headers, timeout=10)
            
        with allure.step("Validate 200 OK response and updated job title"):
            assert response.status_code == 200
            res_data = response.json()
            assert res_data["job"] == payload["job"]
            assert "updatedAt" in res_data

    @allure.story("Delete User")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.description("Verify DELETE /users/{id} returns status 204 No Content.")
    def test_delete_user(self):
        url = f"{Config.API_BASE_URL}/users/2"
        
        with allure.step(f"Send DELETE request to {url}"):
            response = requests.delete(url, headers=self.headers, timeout=10)
            
        with allure.step("Validate status code 204 No Content"):
            assert response.status_code == 204
