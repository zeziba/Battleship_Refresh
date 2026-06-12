# test/conftest.py
import pytest
import src

@pytest.fixture(autouse=True)
def reset_global_config():
    src.config.reset_defaults()

    yield # Test runs here

    src.config.reset_defaults()