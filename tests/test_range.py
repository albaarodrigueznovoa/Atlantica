import pytest
import pandas as pd
from plot import create_series
from calculation import get_Y_range

def test_range():

    data1 = {5: "Tom", 8: "Sarah", 10: "Jack"}
    data2 = {3: "Sam", 20: "John", 50: "Ane"}
    series1 = create_series(data=data1, name="People", index_name="Age")
    series2 = create_series(data=data2, name="People", index_name="Age")

    df_dictionary = {'S1': series1, 'S2': series2}

    minimum, maximum = get_Y_range(df_dictionary)

    assert minimum == 3
    assert maximum == 50