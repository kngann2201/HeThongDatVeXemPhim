import pytest

from app.test.base_test import driver, reset_selenium_database, sel_app


@pytest.fixture(autouse=True)
def reset_database(sel_app):
    reset_selenium_database(sel_app)
    yield
    reset_selenium_database(sel_app)


@pytest.fixture(autouse=True)
def mock_cloudinary_upload(monkeypatch):
    monkeypatch.setattr(
        'cloudinary.uploader.upload',
        lambda file: {'secure_url': 'https://res.cloudinary.com/test/avatar-cute-3.jpg'}
    )
