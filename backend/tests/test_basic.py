import pytest
# We try to import the global 'app' object directly
# If your variable in __init__.py is named 'application', change 'app' to 'application' below
from app import app as flask_app


@pytest.fixture
def client():
    # Configure the app for testing
    flask_app.config['TESTING'] = True

    # Create a test client using the existing app
    with flask_app.test_client() as client:
        yield client


def test_home_page(client):
    """
    GIVEN the Flask application
    WHEN the '/' page is requested
    THEN check that the response is valid (200 OK) or redirects (302)
    """
    response = client.get('/')

    # We accept 200 (Success) or 302 (Redirect to Login)
    assert response.status_code in [200, 302]