import sys

sys.path.append("../src")
from calculation import dates_intersect
import pytest


def test_intersection():

    map_lower = 50
    map_upper = 100
    object_lower = 70
    object_upper = 100

    assert dates_intersect(map_lower, map_upper, object_lower, object_upper) == 30
    assert isinstance(30, int)

    map_lower = 50
    map_upper = 100
    object_lower = 20
    object_upper = 100

    assert dates_intersect(map_lower, map_upper, object_lower, object_upper) == 50
    assert isinstance(50, int)

    map_lower = 50
    map_upper = 100
    object_lower = 50
    object_upper = 200

    assert dates_intersect(map_lower, map_upper, object_lower, object_upper) == 50
    assert isinstance(50, int)

    map_lower = 50
    map_upper = 100
    object_lower = 20
    object_upper = 30

    assert dates_intersect(map_lower, map_upper, object_lower, object_upper) == 0
    assert isinstance(0, int)
