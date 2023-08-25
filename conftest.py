"""
For pytest
initialise a test database and profile
"""
import pytest

pytest_plugins = ["aiida.manage.tests.pytest_fixtures"]  # pylint: disable=invalid-name


@pytest.fixture(scope="function", autouse=True)
def clear_database_auto(clear_database):  # pylint: disable=unused-argument
    """Automatically clear database in between tests."""


@pytest.fixture(scope="function")
def network_code(aiida_local_code_factory):
    """Get a diff code."""
    code = aiida_local_code_factory(executable="network", entry_point="zeopp.network")
    return code


@pytest.fixture(scope="function")
def basic_options():
    """Return basic calculation options."""
    options = {
        "max_wallclock_seconds": 120,
    }
    return options
