"""
api.py - A simple REST API built with Flask.

This represents a real-world web service that GitHub Actions
will build, test, and deploy. The API provides greeting endpoints
that exercise the greeter module.

ENDPOINTS:
  GET  /          - Welcome message with list of endpoints
  GET  /health    - Health check (used by Docker and deployment pipelines)
  GET  /greet     - Greet someone (pass ?name=Alice as query param)
  GET  /time      - Current server time in UTC
  POST /greet     - Greet someone (pass {"name": "Alice"} as JSON body)

HOW TO RUN:
  python -m app.api

EXPERIMENT:
  1. Run the server: python -m app.api
  2. Open browser:   http://127.0.0.1:5000/health
  3. Try greeting:   http://127.0.0.1:5000/greet?name=YourName
  4. Break a route and run tests -- see the failure!
"""

from flask import Flask, request, jsonify
from app.greeter import greet, farewell, get_greeting_count, get_server_time, get_system_info


# ===========================================================================
# CREATE THE FLASK APPLICATION
# ===========================================================================

app = Flask(__name__)


# ===========================================================================
# ROUTE: Health Check
# ===========================================================================

@app.route("/health", methods=["GET"])
def health():
    """
    Health check endpoint.

    In a real CI/CD pipeline, the DEPLOY stage calls /health
    after deployment to verify the app is alive and responding.
    If /health fails, the deployment is rolled back!

    Docker HEALTHCHECK also uses this endpoint to monitor the container.
    """
    return jsonify({
        "status": "healthy",
        "service": "greeter-api",
        "version": "1.0.0"
    }), 200


# ===========================================================================
# ROUTE: Welcome / Root
# ===========================================================================

@app.route("/", methods=["GET"])
def root():
    """
    Root endpoint - shows a welcome message and available endpoints.

    This is useful for developers discovering the API.
    """
    return jsonify({
        "message": "Greeter API - GitHub Actions Basics Lab",
        "endpoints": [
            "GET  /           - This welcome message",
            "GET  /health     - Health check",
            "GET  /greet?name=X - Greet someone",
            "GET  /time       - Server time (UTC)",
            "POST /greet      - Greet someone (JSON body)"
        ]
    }), 200


# ===========================================================================
# ROUTE: Greet (GET)
# ===========================================================================

@app.route("/greet", methods=["GET"])
def greet_get():
    """
    Greet someone via query parameter.

    Usage: GET /greet?name=Alice
    """
    name = request.args.get("name")
    if not name:
        return jsonify({"error": "Missing 'name' query parameter"}), 400

    try:
        message = greet(name)
        return jsonify({
            "greeting": message,
            "total_greetings": get_greeting_count()
        }), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


# ===========================================================================
# ROUTE: Greet (POST)
# ===========================================================================

@app.route("/greet", methods=["POST"])
def greet_post():
    """
    Greet someone via JSON body.

    Usage: POST /greet  {"name": "Alice"}
    Optionally include "farewell": true to get a goodbye message.
    """
    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "Request body must be valid JSON"}), 400

    name = data.get("name")
    if not name:
        return jsonify({"error": "Missing 'name' field in JSON body"}), 400

    try:
        include_farewell = data.get("farewell", False)
        response = {
            "greeting": greet(name),
            "total_greetings": get_greeting_count()
        }
        if include_farewell:
            response["farewell"] = farewell(name)

        return jsonify(response), 200

    except ValueError as e:
        return jsonify({"error": str(e)}), 400


# ===========================================================================
# ROUTE: Server Time
# ===========================================================================

@app.route("/time", methods=["GET"])
def server_time():
    """
    Return the current server time.

    WHY THIS MATTERS FOR GITHUB ACTIONS:
      Scheduled workflows (cron) run in UTC.
      This endpoint helps you verify what time the server thinks it is.
      Compare with the timestamp in your GitHub Actions logs!
    """
    time_info = get_server_time()
    system_info = get_system_info()

    return jsonify({
        "time": time_info,
        "system": system_info
    }), 200


# ===========================================================================
# ERROR HANDLERS
# ===========================================================================

@app.errorhandler(404)
def not_found(error):
    """Handle 404 Not Found errors."""
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(405)
def method_not_allowed(error):
    """Handle 405 Method Not Allowed errors."""
    return jsonify({"error": "Method not allowed"}), 405


# ===========================================================================
# RUN THE SERVER
# ===========================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("  Greeter API - GitHub Actions Basics Lab")
    print("=" * 60)
    print()
    print("  Server running at: http://127.0.0.1:5000")
    print()
    print("  Try these URLs in your browser:")
    print("    http://127.0.0.1:5000/")
    print("    http://127.0.0.1:5000/health")
    print("    http://127.0.0.1:5000/greet?name=World")
    print("    http://127.0.0.1:5000/time")
    print()
    print("  Press Ctrl+C to stop")
    print("=" * 60)

    app.run(host="0.0.0.0", port=5000, debug=False)
