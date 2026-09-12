import json
from pathlib import Path

import pytest

try:
    import jsonschema
except ImportError:
    jsonschema = None

REPO_ROOT = Path(__file__).resolve().parents[4]
SCHEMA_PATH = REPO_ROOT / 'schemas' / 'station-skill-mask-v1.schema.json'
EXAMPLE_PATH = REPO_ROOT / 'templates' / 'station_skill_mask.example.json'


@pytest.mark.skipif(jsonschema is None, reason='jsonschema not installed')
def test_schema_validates_example():
    assert SCHEMA_PATH.exists(), f'Schema not found at {SCHEMA_PATH}'
    assert EXAMPLE_PATH.exists(), f'Example not found at {EXAMPLE_PATH}'

    schema = json.loads(SCHEMA_PATH.read_text(encoding='utf-8'))
    example = json.loads(EXAMPLE_PATH.read_text(encoding='utf-8'))

    # Will raise ValidationError if invalid
    jsonschema.validate(instance=example, schema=schema)


@pytest.mark.skipif(jsonschema is None, reason='jsonschema not installed')
def test_schema_rejects_missing_ausloeser():
    schema = json.loads(SCHEMA_PATH.read_text(encoding='utf-8'))
    example = json.loads(EXAMPLE_PATH.read_text(encoding='utf-8'))

    invalid_example = dict(example)
    del invalid_example['ausloeser']

    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(instance=invalid_example, schema=schema)


@pytest.mark.skipif(jsonschema is None, reason='jsonschema not installed')
def test_schema_rejects_invalid_skill_name():
    schema = json.loads(SCHEMA_PATH.read_text(encoding='utf-8'))
    example = json.loads(EXAMPLE_PATH.read_text(encoding='utf-8'))

    invalid_example = dict(example)
    invalid_example['skill_name'] = 'Invalid_Skill_Name!'

    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(instance=invalid_example, schema=schema)
