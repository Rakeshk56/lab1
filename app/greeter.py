"""
greeter.py - A simple greeting module.

This is the CORE APPLICATION code that GitHub Actions workflows will:
  1. BUILD   (install dependencies)
  2. TEST    (run unit + integration tests against this code)
  3. DEPLOY  (ship to production)

The greeter module provides functions for generating greetings,
farewells, and server information. It's intentionally simple so
you can focus on learning GitHub Actions workflow syntax.

EXPERIMENT:
  - Try changing a greeting message and push to GitHub
  - Watch the workflow trigger automatically
  - Break a function to see tests catch it in the Actions tab
"""

import platform
from datetime import datetime, timezone


# ──────────────────────────────────────────────────────────────────────────────
# GREETING COUNTER
# ──────────────────────────────────────────────────────────────────────────────
# This module-level variable tracks how many greetings have been generated.
# In a real app, this would be stored in a database or cache.

_greeting_count = 0


def greet(name):
    """
    Generate a friendly greeting for the given name.

    Args:
        name (str): The name of the person to greet.

    Returns:
        str: A greeting message.

    Raises:
        ValueError: If name is empty or None.

    Example:
        >>> greet("Alice")
        'Hello, Alice! Welcome to the GitHub Actions Basics Lab!'

    TRY THIS:
        Change the greeting text and push to GitHub.
        The workflow will run your tests against the new message.
        If a test expects the old message, it will FAIL -- and
        that's exactly what CI/CD is designed to catch!
    """
    global _greeting_count

    if not name or not name.strip():
        raise ValueError("Name cannot be empty")

    name = name.strip()
    _greeting_count += 1
    return f"Hello, {name}! Welcome to the GitHub Actions Basics Lab!"


def farewell(name):
    """
    Generate a farewell message for the given name.

    Args:
        name (str): The name of the person to say goodbye to.

    Returns:
        str: A farewell message.

    Raises:
        ValueError: If name is empty or None.

    Example:
        >>> farewell("Bob")
        'Goodbye, Bob! Happy automating!'
    """
    if not name or not name.strip():
        raise ValueError("Name cannot be empty")

    name = name.strip()
    return f"Goodbye, {name}! Happy automating!"


def get_greeting_count():
    """
    Return the total number of greetings generated since the app started.

    Returns:
        int: The number of times greet() has been called.

    NOTE:
        This counter resets when the server restarts.
        In production, you'd use Redis or a database for persistence.
    """
    return _greeting_count


def get_server_time():
    """
    Return the current server time in UTC as an ISO 8601 string.

    Returns:
        dict: A dictionary with 'utc' time and 'timezone' info.

    WHY UTC?
        GitHub Actions runners always operate in UTC.
        Scheduled workflows (cron) also use UTC.
        Using UTC everywhere avoids timezone confusion.
    """
    now = datetime.now(timezone.utc)
    return {
        "utc": now.isoformat(),
        "timezone": "UTC",
        "human_readable": now.strftime("%Y-%m-%d %H:%M:%S UTC")
    }


def get_system_info():
    """
    Return basic system information about the machine running this code.

    Returns:
        dict: System information including OS, Python version, etc.

    WHY IS THIS USEFUL?
        In GitHub Actions, your code runs on a cloud VM (runner).
        This function lets you see what that runner looks like:
        - What OS is it? (ubuntu-latest, windows-latest, macos-latest)
        - What Python version is installed?
        - What is the machine architecture?

        Compare the output when running locally vs. in GitHub Actions!
    """
    return {
        "os": platform.system(),
        "os_version": platform.version(),
        "architecture": platform.machine(),
        "python_version": platform.python_version(),
        "hostname": platform.node()
    }
