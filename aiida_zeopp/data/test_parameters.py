import pytest


def test_cmdline_cssr():
    from aiida_zeopp.data.parameters import NetworkParameters

    d = {"cssr": True}
    assert NetworkParameters(d).cmdline_params() == ["-cssr", "out.cssr"]
    d = {"cssr": False}
    assert NetworkParameters(d).cmdline_params() == []
    d = {}
    assert NetworkParameters(d).cmdline_params() == []


def test_output_parsers():
    from aiida_zeopp.data.parameters import NetworkParameters
    from aiida_zeopp.parsers.plain import PoreVolumeParser, SurfaceAreaParser

    d = {"cssr": True, "sa": [1.82, 1.82, 10000], "volpo": [1.82, 1.82, 100000]}
    p = NetworkParameters(d)

    assert p.output_parsers == [None, SurfaceAreaParser, PoreVolumeParser]


def test_validation():
    """Test that validation raises an exception for wrong input."""
    from voluptuous import MultipleInvalid

    from aiida_zeopp.data.parameters import NetworkParameters

    d = {
        "cssr2": True,
    }

    with pytest.raises(MultipleInvalid):
        NetworkParameters(d)
