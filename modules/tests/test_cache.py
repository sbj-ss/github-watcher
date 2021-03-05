import pytest

from ..cache import PickledDictCache


def test_pickled_dict_cache():
    FILE = '/tmp/pickled_dict.bin'
    d = PickledDictCache(FILE)
    d['a'] = 1
    assert d['a'] == 1
    with pytest.raises(KeyError):
        _ = d['b']
    assert d.get('b') is None
    assert d.get('b', 2) == 2
    d.save()

    d2 = PickledDictCache(FILE)
    assert d2['a'] == 1
    with pytest.raises(KeyError):
        _ = d2['b']
