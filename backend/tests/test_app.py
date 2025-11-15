import json
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

from app.main import app

client = TestClient(app)


def test_root_redirect():
    resp = client.get("/")
    assert resp.status_code in (200, 307, 308)


def test_get_categories():
    resp = client.get("/categories")
    assert resp.status_code == 200
    data = resp.json()
    assert "categories" in data


@patch("app.main.text_extractor")
@patch("app.main.listing_generator")
def test_generate_listing_json(mock_generator, mock_extractor):
    mock_extractor.extract_features.return_value = {
        "keywords": ["test"],
        "entities": [],
        "pattern_features": {}
    }
    mock_generator.generate.return_value = {
        "title": "Test Product",
        "bullets": ["Feature 1"],
        "description": "Test description",
        "search_terms": ["test"],
        "attributes": {}
    }

    resp = client.post(
        "/generate",
        json={"text_content": "Test product post", "detected_category": "water_bottle"}
    )
    assert resp.status_code == 200
    body = resp.json()
    assert body.get("success") is True
