"""
=============================================================================
INTEGRATION TESTS - test_api.py
=============================================================================

WHAT ARE INTEGRATION TESTS?
  Integration tests check that MULTIPLE COMPONENTS work TOGETHER.
  Here we test the API endpoints, which means:
    - The Flask server must be running
    - The request must be parsed correctly
    - The greeter functions must be called
    - The response must be formatted correctly

  Integration tests are SLOWER than unit tests because they:
    - Start a real server
    - Make real HTTP requests
    - Test the full request/response cycle

IN THE CI/CD PIPELINE:
  Unit tests run FIRST (fast, catch most bugs)
  Integration tests run SECOND (slower, catch wiring issues)
  If unit tests fail, integration tests DON'T RUN (fail fast!)

HOW TO RUN:
  pytest tests/integration/test_api.py -v

EXPERIMENT:
  1. Break the API routing (change a path in api.py)
  2. Unit tests still pass! (they test greeter.py directly)
  3. Integration tests FAIL! (they test the full API)
  This shows WHY you need BOTH types of tests!
=============================================================================
"""

import json
import pytest
from app.api import app


# ===========================================================================
# TEST FIXTURE: Flask test client
# ===========================================================================

@pytest.fixture(scope="module")
def client():
    """
    WHAT IS A FIXTURE?
    A fixture sets up resources needed for tests.
    Flask provides a built-in test client that simulates HTTP requests
    without actually starting a real server on a port.

    scope="module" means: create ONCE for all tests in this file
    (not once per test -- that would be slow!)
    """
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


# ===========================================================================
# TEST GROUP 1: Health Check Endpoint
# ===========================================================================

class TestHealthEndpoint:
    """
    Health checks are CRITICAL in CI/CD pipelines.
    After deploying, the pipeline calls /health to verify the app is alive.
    If /health fails, the deployment is rolled back!
    """

    def test_health_returns_200(self, client):
        """Health endpoint should return 200 OK."""
        response = client.get("/health")
        assert response.status_code == 200

    def test_health_returns_correct_body(self, client):
        """Health endpoint should include status and version."""
        response = client.get("/health")
        data = response.get_json()

        assert data["status"] == "healthy"
        assert data["service"] == "greeter-api"
        assert "version" in data


# ===========================================================================
# TEST GROUP 2: Root Endpoint
# ===========================================================================

class TestRootEndpoint:
    """Tests for the root / endpoint."""

    def test_root_returns_200(self, client):
        """Root endpoint should return 200 OK."""
        response = client.get("/")
        assert response.status_code == 200

    def test_root_returns_welcome_message(self, client):
        """Root should return a welcome message."""
        response = client.get("/")
        data = response.get_json()
        assert "message" in data
        assert "Greeter" in data["message"]

    def test_root_lists_endpoints(self, client):
        """Root should list available endpoints."""
        response = client.get("/")
        data = response.get_json()
        assert "endpoints" in data
        assert len(data["endpoints"]) > 0


# ===========================================================================
# TEST GROUP 3: GET /greet Endpoint
# ===========================================================================

class TestGreetGetEndpoint:
    """Tests for GET /greet -- greeting via query parameter."""

    def test_greet_with_name(self, client):
        """GET /greet?name=Alice should return a greeting."""
        response = client.get("/greet?name=Alice")
        assert response.status_code == 200
        data = response.get_json()
        assert "greeting" in data
        assert "Alice" in data["greeting"]

    def test_greet_includes_count(self, client):
        """Response should include total greeting count."""
        response = client.get("/greet?name=Bob")
        data = response.get_json()
        assert "total_greetings" in data
        assert isinstance(data["total_greetings"], int)

    def test_greet_missing_name_returns_400(self, client):
        """GET /greet without name should return 400."""
        response = client.get("/greet")
        assert response.status_code == 400
        data = response.get_json()
        assert "error" in data


# ===========================================================================
# TEST GROUP 4: POST /greet Endpoint
# ===========================================================================

class TestGreetPostEndpoint:
    """Tests for POST /greet -- greeting via JSON body."""

    def test_post_greet_basic(self, client):
        """POST /greet with JSON body should return a greeting."""
        response = client.post(
            "/greet",
            data=json.dumps({"name": "Charlie"}),
            content_type="application/json"
        )
        assert response.status_code == 200
        data = response.get_json()
        assert "greeting" in data
        assert "Charlie" in data["greeting"]

    def test_post_greet_with_farewell(self, client):
        """POST /greet with farewell=true should include farewell message."""
        response = client.post(
            "/greet",
            data=json.dumps({"name": "Dana", "farewell": True}),
            content_type="application/json"
        )
        assert response.status_code == 200
        data = response.get_json()
        assert "greeting" in data
        assert "farewell" in data
        assert "Dana" in data["farewell"]

    def test_post_greet_missing_name_returns_400(self, client):
        """POST /greet without name field should return 400."""
        response = client.post(
            "/greet",
            data=json.dumps({"wrong_field": "value"}),
            content_type="application/json"
        )
        assert response.status_code == 400

    def test_post_greet_invalid_json_returns_400(self, client):
        """Sending non-JSON data should return 400, not crash the server."""
        response = client.post(
            "/greet",
            data="this is not json",
            content_type="application/json"
        )
        assert response.status_code == 400


# ===========================================================================
# TEST GROUP 5: GET /time Endpoint
# ===========================================================================

class TestTimeEndpoint:
    """Tests for the /time endpoint."""

    def test_time_returns_200(self, client):
        """Time endpoint should return 200 OK."""
        response = client.get("/time")
        assert response.status_code == 200

    def test_time_returns_utc(self, client):
        """Time response should include UTC time info."""
        response = client.get("/time")
        data = response.get_json()
        assert "time" in data
        assert data["time"]["timezone"] == "UTC"

    def test_time_returns_system_info(self, client):
        """Time response should include system information."""
        response = client.get("/time")
        data = response.get_json()
        assert "system" in data
        assert "os" in data["system"]
        assert "python_version" in data["system"]


# ===========================================================================
# TEST GROUP 6: Error Handling
# ===========================================================================

class TestErrorHandling:
    """
    Testing error cases is just as important as testing success cases.
    In production, bad requests WILL happen. The API must handle them
    gracefully, not crash.
    """

    def test_not_found_returns_404(self, client):
        """Requesting a non-existent endpoint should return 404."""
        response = client.get("/nonexistent")
        assert response.status_code == 404

    def test_not_found_returns_json(self, client):
        """404 response should be JSON, not HTML."""
        response = client.get("/nonexistent")
        data = response.get_json()
        assert "error" in data

    def test_method_not_allowed_returns_405(self, client):
        """Using wrong HTTP method should return 405."""
        response = client.delete("/health")
        assert response.status_code == 405
