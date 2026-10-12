# Petstore API Test Automation

![API Tests](https://github.com/amnataj/petstore-api-tests/actions/workflows/tests.yml/badge.svg)

Automated API test suite for the [Swagger Petstore](https://petstore.swagger.io) (v2), built with **Python, pytest and requests**. It covers CRUD flows, negative cases, and response schema validation, runs in CI on every push, and documents where the API deviates from its own spec.

## Tech stack
- Python 3.10, pytest, requests
- jsonschema for response contract validation
- pytest-html for reports
- GitHub Actions for CI

## Project structure
```
api/          reusable API client (base URL, session, request logging)
schemas/      JSON schemas for response validation
tests/
  conftest.py       fixtures: client, pet payload, created pet with cleanup
  test_pet_crud.py  create, read, update, delete, find by status
  test_negative.py  invalid IDs, invalid status, missing required fields
pytest.ini    markers (smoke, regression) and config
.github/workflows/tests.yml   CI pipeline
```

## Design decisions
- **Independent tests:** every test creates its own pet with a random ID and cleans up afterwards, because the public Petstore instance is shared with other users.
- **Reusable client:** all HTTP calls go through one `ApiClient` class, so URL, headers, timeouts and logging live in one place.
- **Known bugs as strict xfail:** spec deviations are kept as `xfail(strict=True)` tests. The suite stays green, the bugs stay documented, and a test fails loudly if the API is ever fixed.

## Run locally
```
git clone https://github.com/amnataj/petstore-api-tests.git
cd petstore-api-tests
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
pytest -v --html=reports/report.html --self-contained-html
```
Run only quick checks with `pytest -m smoke`.

## Findings: spec deviations found
| ID | Endpoint | Spec says | Actual behavior | Severity |
|---|---|---|---|---|
| BUG-001 | `GET /pet/findByStatus?status=invalid` | 400 Invalid status value | 200 OK with an empty list | Low |
| BUG-002 | `POST /pet` with required fields missing | 405 Invalid input | 200 OK, pet is created without `name` and `photoUrls` | Medium |

## CI
Tests run automatically on every push and pull request. The HTML report is attached to each run as a downloadable artifact in the Actions tab.

## Roadmap
- Store and user endpoint tests
- Retry handling for server flakiness
- Allure reporting
