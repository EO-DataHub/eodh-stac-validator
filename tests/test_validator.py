from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_validate_success() -> None:
    payload = {
        "content": {
            "id": "example-collection",
            "type": "Collection",
            "stac_version": "1.0.0",
            "summaries": {"eo:bands": ["B4", "B3", "B2"]},
            "extent": {
                "spatial": {"bbox": [[10.0, 20.0, 10.0, 20.0]]},
                "temporal": {"interval": [["2023-01-01T00:00:00Z", None]]},
            },
            "links": [
                {
                    "rel": "self",
                    "href": "https://example.com/collections/example-collection",
                    "type": "application/json",
                    "title": "Self link to this STAC Collection",
                }
            ],
            "description": "Example collection",
            "license": "CC-BY-4.0",
        }
    }

    response = client.post("/validate-stac", json=payload)
    body = response.json()[0]
    code = response.json()[1]

    assert code == 200
    assert body.get("status") == "success"


def test_validate_failure() -> None:
    payload = {
        "content": {
            "id": "example-collection",
            "type": "Collection",
            "stac_version": "1.0.0",
            "summaries": {"eo:bands": ["B4", "B3", "B2"]},
            "extent": {
                # missing spatial field - should fail test
                "temporal": {"interval": [["2023-01-01T00:00:00Z", None]]},
            },
            "links": [
                {
                    "rel": "self",
                    "href": "https://example.com/collections/example-collection",
                    "type": "application/json",
                    "title": "Self link to this STAC Collection",
                }
            ],
            "description": "Example collection",
            "license": "CC-BY-4.0",
        }
    }

    response = client.post("/validate-stac", json=payload)

    body = response.json()[0]
    code = response.json()[1]

    assert code == 400
    assert body.get("status") == "error"
