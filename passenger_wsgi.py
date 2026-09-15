import os
import sys

# Ensure the project directory is at the top of the Python module lookup path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

# Set production environment flags if not already set
os.environ.setdefault("ENV", "production")

# Import the FastAPI ASGI application from main.py
from main import app

# cPanel Phusion Passenger expects a WSGI callable named `application`.
# We wrap the ASGI FastAPI app with a2wsgi to run seamlessly under Passenger WSGI.
try:
    from a2wsgi import ASGIMiddleware
    application = ASGIMiddleware(app)
except ImportError:
    # Fallback if a2wsgi is not installed
    from starlette.middleware.wsgi import WSGIMiddleware
    application = app
