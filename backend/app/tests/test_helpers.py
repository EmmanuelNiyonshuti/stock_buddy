"""
define utility functions for various tests.
"""
from datetime import datetime

def assert_common_model_fields(instance):
    assert instance.id is not None
    assert isinstance(instance.id, str)
    assert instance.created_at is not None
    assert isinstance(instance.created_at, datetime)
    assert instance.updated_at is not None
    assert isinstance(instance.updated_at, datetime)