import sys

sys.path.append("../src")
from calculation import propor_to_map_range
import pytest
import pandas as pd


def test_proportion():

    data = {
        "Type": ["spatheia"],
        "Lower_date": [375.0],
        "Upper_date": [700.0],
        "Frequency": [2.0],
        "Provenance": ["Africa"],
        "Freq_per_year": [0.006153846153846154],
    }

    df = pd.DataFrame(data)

    map_lower = 100
    map_upper = 200

    propor = propor_to_map_range(
        data=df,
        map_lower_date=map_lower,
        map_upper_date=map_upper,
        object_lower_date="Lower_date",
        object_upper_date="Upper_date",
        freq_per_year="Freq_per_year",
    )

    for value in propor["Proportion"]:

        assert isinstance(value, int)

        assert value == 0

    map_lower = 400
    map_upper = 500

    propor = propor_to_map_range(
        data=df,
        map_lower_date=map_lower,
        map_upper_date=map_upper,
        object_lower_date="Lower_date",
        object_upper_date="Upper_date",
        freq_per_year="Freq_per_year",
    )

    for value in propor["Proportion"]:

        assert isinstance(value, float)

        assert value == 0.6153846153846154
