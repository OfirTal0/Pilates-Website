from app import api_classes
import json


def test_get_classes():
    classes = json.loads(api_classes)  # Parse the JSON data
    assert isinstance(classes, list)  # Example assertion