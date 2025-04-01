from fastapi.testclient import TestClient
from unittest import TestCase
from main import app

class ValidatorTestCase(TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_validate(self):
        payload = {
            "content": {
            "id": "example-collection",
            "type": "Collection",
            "stac_version": "1.0.0",
            "summaries": {
                "eo:bands": ["B4", "B3", "B2"]
            },
            "extent": {
                "spatial": {
                "bbox": [[10.0, 20.0, 10.0, 20.0]]
                },
                "temporal": {
                "interval": [["2023-01-01T00:00:00Z", None]]
                }
            },
            "links": [
                    {
                "rel": "self",
                "href": "https://example.com/collections/example-collection",
                "type": "application/json",
                "title": "Self link to this STAC Collection"
                }

            ],
            "description": "Example collection",
            "license": "CC-BY-4.0"
            }
        }

        response = self.client.post("/validate-stac", json=payload)
        body = response.json()[0]
        code = response.json()[1]

        self.assertEqual(code, 200)
        self.assertEqual(body.get("status"), "success")
