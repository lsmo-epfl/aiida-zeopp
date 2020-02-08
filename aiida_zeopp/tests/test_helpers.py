"""Testing zeo++ test helpers."""


def test_get_code():
    """Test helper for setting up a code."""
    from aiida_zeopp import tests
    code = tests.get_code(entry_point='zeopp.network')
    assert 'network' in code.get_execname()
