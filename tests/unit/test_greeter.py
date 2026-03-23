"""
=============================================================================
UNIT TESTS - test_greeter.py
=============================================================================

WHAT ARE UNIT TESTS?
  Unit tests check INDIVIDUAL FUNCTIONS in isolation.
  They are the FASTEST tests in the pipeline.
  They don't need a running server, database, or network.

  In a CI/CD pipeline, unit tests run FIRST because:
    - They are fast (milliseconds each)
    - They catch most bugs
    - Quick feedback for developers

HOW THIS FILE WORKS:
  - Each function starting with "test_" is a TEST CASE
  - pytest discovers and runs all test_ functions automatically
  - If any assert fails, the test FAILS and the pipeline STOPS

HOW TO RUN:
  pytest tests/unit/test_greeter.py -v

EXPERIMENT:
  1. Run tests (they should all pass)
  2. Break a function in greeter.py (e.g., change the greeting text)
  3. Run tests again -- watch them FAIL
  4. Fix the function -- watch them PASS again
  This is exactly what happens in a CI/CD pipeline on every commit!
=============================================================================
"""

import pytest
from app.greeter import greet, farewell, get_greeting_count, get_server_time, get_system_info


# ===========================================================================
# TEST GROUP 1: greet() function
# ===========================================================================

class TestGreet:
    """Tests for the greet() function."""

    def test_greet_basic(self):
        """Greeting a name should return a welcome message."""
        result = greet("Alice")
        assert "Alice" in result
        assert "Hello" in result

    def test_greet_includes_lab_name(self):
        """The greeting should mention the lab name."""
        result = greet("Student")
        assert "GitHub Actions Basics Lab" in result

    def test_greet_strips_whitespace(self):
        """Names with extra whitespace should be trimmed."""
        result = greet("  Bob  ")
        assert "Bob" in result
        # Should NOT have extra spaces in the greeting
        assert "  Bob  " not in result

    def test_greet_empty_name_raises_error(self):
        """
        THIS IS AN IMPORTANT TEST PATTERN:
        We test that ERRORS are raised correctly.
        In CI/CD, we want to make sure error handling works!
        """
        with pytest.raises(ValueError, match="Name cannot be empty"):
            greet("")

    def test_greet_none_name_raises_error(self):
        """Passing None should raise ValueError."""
        with pytest.raises(ValueError, match="Name cannot be empty"):
            greet(None)

    def test_greet_whitespace_only_raises_error(self):
        """A name with only spaces should be treated as empty."""
        with pytest.raises(ValueError, match="Name cannot be empty"):
            greet("   ")


# ===========================================================================
# TEST GROUP 2: farewell() function
# ===========================================================================

class TestFarewell:
    """Tests for the farewell() function."""

    def test_farewell_basic(self):
        """Farewell should include the name and a goodbye."""
        result = farewell("Charlie")
        assert "Goodbye" in result
        assert "Charlie" in result

    def test_farewell_includes_happy_message(self):
        """Farewell should include an encouraging message."""
        result = farewell("Dana")
        assert "Happy automating" in result

    def test_farewell_empty_name_raises_error(self):
        with pytest.raises(ValueError, match="Name cannot be empty"):
            farewell("")

    def test_farewell_none_raises_error(self):
        with pytest.raises(ValueError, match="Name cannot be empty"):
            farewell(None)

    def test_farewell_strips_whitespace(self):
        """Farewell should trim whitespace from names."""
        result = farewell("  Eve  ")
        assert "Eve" in result
        assert "  Eve  " not in result


# ===========================================================================
# TEST GROUP 3: get_greeting_count() function
# ===========================================================================

class TestGreetingCount:
    """Tests for the get_greeting_count() function."""

    def test_greeting_count_is_integer(self):
        """Count should always be an integer."""
        count = get_greeting_count()
        assert isinstance(count, int)

    def test_greeting_count_increments(self):
        """Each call to greet() should increment the counter."""
        before = get_greeting_count()
        greet("Counter-Test")
        after = get_greeting_count()
        assert after == before + 1

    def test_greeting_count_increments_multiple(self):
        """Multiple greetings should increment by the correct amount."""
        before = get_greeting_count()
        greet("Test1")
        greet("Test2")
        greet("Test3")
        after = get_greeting_count()
        assert after == before + 3


# ===========================================================================
# TEST GROUP 4: get_server_time() function
# ===========================================================================

class TestServerTime:
    """Tests for the get_server_time() function."""

    def test_server_time_returns_dict(self):
        """Server time should return a dictionary."""
        result = get_server_time()
        assert isinstance(result, dict)

    def test_server_time_has_utc_field(self):
        """Response should include a UTC timestamp."""
        result = get_server_time()
        assert "utc" in result

    def test_server_time_has_timezone_field(self):
        """Response should include timezone info."""
        result = get_server_time()
        assert result["timezone"] == "UTC"

    def test_server_time_has_human_readable(self):
        """Response should include a human-readable time string."""
        result = get_server_time()
        assert "human_readable" in result
        assert "UTC" in result["human_readable"]


# ===========================================================================
# TEST GROUP 5: get_system_info() function
# ===========================================================================

class TestSystemInfo:
    """Tests for the get_system_info() function."""

    def test_system_info_returns_dict(self):
        """System info should return a dictionary."""
        result = get_system_info()
        assert isinstance(result, dict)

    def test_system_info_has_os(self):
        """Response should include the operating system."""
        result = get_system_info()
        assert "os" in result
        assert len(result["os"]) > 0

    def test_system_info_has_python_version(self):
        """Response should include the Python version."""
        result = get_system_info()
        assert "python_version" in result
        # Python version should start with a number
        assert result["python_version"][0].isdigit()

    def test_system_info_has_architecture(self):
        """Response should include the machine architecture."""
        result = get_system_info()
        assert "architecture" in result

    def test_system_info_has_hostname(self):
        """Response should include the hostname."""
        result = get_system_info()
        assert "hostname" in result


# ===========================================================================
# BONUS: PARAMETERIZED TESTS
# ===========================================================================

class TestParameterized:
    """
    Parameterized tests run the SAME test with DIFFERENT inputs.
    This is powerful for testing many cases without writing many functions.

    The @pytest.mark.parametrize decorator provides test data.
    pytest runs the test function ONCE for each set of parameters.
    """

    @pytest.mark.parametrize("name", [
        "Alice",
        "Bob",
        "Charlie",
        "A",                # single character name
        "Jean-Pierre",      # hyphenated name
        "O'Brien",          # name with apostrophe
        "Maria Garcia",     # name with space
    ])
    def test_greet_various_names(self, name):
        """Test greet() with many different valid names."""
        result = greet(name)
        assert name in result
        assert "Hello" in result

    @pytest.mark.parametrize("name", [
        "Alice",
        "Bob",
        "Charlie",
    ])
    def test_farewell_various_names(self, name):
        """Test farewell() with many different valid names."""
        result = farewell(name)
        assert name in result
        assert "Goodbye" in result

    @pytest.mark.parametrize("invalid_name", [
        "",
        "   ",
        None,
    ])
    def test_greet_rejects_invalid_names(self, invalid_name):
        """Test that greet() rejects all forms of empty/invalid names."""
        with pytest.raises(ValueError):
            greet(invalid_name)

    @pytest.mark.parametrize("invalid_name", [
        "",
        "   ",
        None,
    ])
    def test_farewell_rejects_invalid_names(self, invalid_name):
        """Test that farewell() rejects all forms of empty/invalid names."""
        with pytest.raises(ValueError):
            farewell(invalid_name)
