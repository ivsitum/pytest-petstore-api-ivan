# Pytest Pet Store API Tests

This repository contains automated API tests for the [Swagger Petstore API](https://petstore.swagger.io/).  
It is built with **Python** and **Pytest** to verify the functionality of the API endpoints for `pet` operation.

# Objective

- Automate API testing for:
  - `POST /pet` – Add a new pet
  - `GET /pet/{petId}` – Retrieve pet details by ID
  - `PUT /pet` – Update an existing pet
- Provide a **scalable and maintainable** structure for adding new tests.
- Demonstrate **best practices** in Python API test automation with Pytest.
- Include optional authentication header support (`api_key`).

## API & Library References

This project uses the [Swagger Petstore API](https://petstore.swagger.io/) as the backend for testing.  
The API endpoints are documented in detail here:  
[Swagger Petstore API Documentation](https://petstore.swagger.io/)

### Testing Framework
- **[Pytest](https://docs.pytest.org/)** – a Python testing framework used for organizing, executing, and reporting tests.
  - Supports fixtures for setup/teardown.
  - Enables parameterization to run tests with multiple datasets.
  - Provides rich assertion introspection.

### HTTP Client
- **[Requests](https://requests.readthedocs.io/en/latest/)** – a simple and elegant HTTP library for Python.
  - Used for sending `GET`, `POST`, and `PUT` requests to the Petstore API.
  - Supports passing custom headers (e.g., `api_key`) and request payloads in JSON format.
  - Handles response parsing for JSON and status code validation.

## Test Cases

All automated test scenarios for this project are documented in detail in the  
[`TEST_CASES.md`](TEST_CASES.md) file.  

This document includes:
- Functional coverage of the key API endpoints (`POST /pet`, `GET /pet/{petId}`, `PUT /pet`).
- Additional validation tests (status parameterization, contract checks, idempotent updates, cleanup).
- Expected request and response structures.
- Execution notes and expected outcomes.

The tests in the framework are implemented based on these documented cases to ensure traceability between requirements and automation.


## Getting Started

Follow these steps to set up and run the Petstore API automated tests locally.

### 1. Prerequisites

Ensure you have the following installed:

- **Python** 3.12 or higher
- **pip** (Python package manager)
- **Git** for version control

### Installation

Clone the repository:

 `git clone https://github.com/ivsitum/pytest-petstore-api-ivan.git`


### Create and activate a virtual environment

#### Windows

`python -m venv venv
venv\Scripts\activate`

#### Mac\Linux

`python3 -m venv venv
source venv/bin/activate`

###  Install Dependencies

`pip install -r requirements.txt`

This installs:
-pytest
-requests
-python-dotenv
-faker
 from [`requirements.txt`](requirements.txt)

### Running Tests

```
To execute all tests in the suite run:

pytest


Run tests with detailed output:

pytest -v

Show print() statements in test output

pytest -s

Stop after the first failure

pytest -x

Show extra summary info for skipped/xfailed tests

pytest -rsxX
```


## Pytest Markers

This project uses custom `pytest` markers to organize and selectively run tests.  

| Marker     | Category  | Description |
|------------|-----------|-------------|
| **pet**    | Scope     | Tests for `/pet` API endpoints. |
| **smoke**  | Purpose   | Minimal "happy path" coverage for the main interview task. |
| **negative** | Purpose | Tests for validation errors and "unhappy path" scenarios. |
| **contract** | Purpose | Lightweight checks of the response shape and data types (contract testing). |
| **auth**   | Purpose   | Authentication / `api_key` behavior checks. |
| **create** | Operation | Create a resource (POST). |
| **read**   | Operation | Retrieve a resource (GET). |
| **update** | Operation | Update a resource (PUT). |
| **delete** | Operation | Delete a resource (DELETE). |

### Running tests by marker

You can run a subset of tests using `-m` with `pytest`:

```
# Run only smoke tests
pytest -m smoke

# Run only negative tests
pytest -m negative

# Run only create operations
pytest -m create

# Combine multiple markers with boolean logic
pytest -m "pet and contract"
```