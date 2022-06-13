import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import re

sns.set()
from bs4 import BeautifulSoup
import requests
import os
import pathlib
from pathlib import Path

from typing import List, Tuple, Dict


def preprocess(data: pd.DataFrame) -> pd.DataFrame:
    """Cleans text from punctuation, changes double spaces into single onse, converts strings to all lowercase

    Args:
        data (pd.DataFrame): A pandas dataframe

    Returns:
        pd.DataFrame: An input dataframe with cleaned text in the specified column
    """

    df = data.replace(r"[^\w\s]+", "")
    df = df.apply(lambda x: re.sub(" +", " ", str(x)))
    df = df.apply(lambda x: str(x).lower())

    return df


def create_series(data: Dict[str, int], name: str, index_name: str) -> pd.Series:
    """Creates a one-dimensional labeled array

    Args:
        date (Dict[str, int]): A dictionary with keys and values

        name (str): The name of the Series

        index_name (str): The name of the Series row

    Returns:
        pd.Series: A one-dimensional labeled array
    """

    data = pd.Series(data, name=name)
    data.index.name = index_name
    data.reset_index()

    return data


def freq_per_year(
    data: pd.DataFrame,
    lower_date: str,
    upper_date: str,
    freq: str,
    freq_per_year: str = "Freq_per_year",
) -> pd.DataFrame:
    """Calculates frequency per year per object

    Args:
        data (pd.DataFrame): A pandas dataframe

        lower_date (str): The name of the dataframe column containing start dates

        upper_date (str): The name of the dataframe column containing end dates

        freq (str): A dataframe column with frequency values per object

        freq_per_year (str): A dataframe column with resulting frequency values per year per object.
        The name of the column can be set up (by default = 'Freq_per_year')

    Returns:
        pd.DataFrame: An input dataframe with a new column containg frequency per year values
    """

    for row in range(len(data)):
        data[freq_per_year] = data[freq] / (data[upper_date] - data[lower_date])
    return data


def sum_freq_per_year(
    data: pd.DataFrame,
    sum_freq: str,
    lower_date: str,
    upper_date: str,
    freq_per_year: str = "Sum_freq_per_year",
) -> pd.DataFrame:
    """Calculates frequency per year per object

    Args:
        data (pd.DataFrame): A pandas dataframe

        sum_freq (str): A dataframe column containing summed frequency values per object type

        lower_date (str): The name of the dataframe column containing start dates

        upper_date (str): The name of the dataframe column containing end dates

        freq_per_year (str): A dataframe column with resulting sum frequency values per year per object.
        The name of the column can be set up (by default = 'Sum_freq_per_year')

    Returns:
        pd.DataFrame: An input dataframe with a new column containg sum frequency values per year
    """

    for row in range(len(data)):
        data[freq_per_year] = data[sum_freq] / (data[upper_date] - data[lower_date])
    return data


def year_freq_df(
    data: pd.DataFrame,
    lower_date: str,
    upper_date: str,
    sum_freq: str,
    name: str = "Frequency",
    index_name: str = "Year",
) -> pd.Series:
    """Creates a dataframe with years and the corresponding frequency values

    Args:
        data (pd.DataFrame): A pandas dataframe

        lower_date (str): A dataframe column containing start dates

        upper_date (str): A dataframe column containing end dates

        sum_freq (str): A dataframe column containing sum frequency values per year per object

        name (str): The name of the output Series. Can be set up (by default = 'Frequency')

        index_name (str):  The name of the row of the output Series. Can be set up (by default = 'Year')

    Returns:
        pd.Series: A one-dimensional labeled array with sum frequncy values for each year in a given date range

    """

    minimum = data[lower_date].min()
    maximum = data[upper_date].max()

    date_dict = dict.fromkeys(range(int(minimum), int(maximum)), 0)

    df = data.dropna(subset=[lower_date])
    df = df.dropna(subset=[upper_date])

    for row in range(len(df)):
        for year in range(
            df[lower_date].astype(int).iloc[row], df[upper_date].astype(int).iloc[row]
        ):
            date_dict[year] += df[sum_freq].iloc[row]

    return create_series(date_dict, name=name, index_name=index_name)


def year_object_count_df(
    data: pd.DataFrame,
    lower_date: str,
    upper_date: str,
    object_list: str,
    name: str = "Site count",
    index_name: str = "Year",
) -> pd.Series:
    """Creates a dataframe with years and the corresponding site count values

     Args:
        data (pd.DataFrame): A pandas dataframe

        lower_date (str): The name of the dataframe column containing start dates

        upper_date (str): The name of the dataframe column containing end dates

        object_list (str): the name of the dataframe column containing the list of f.ex., sites, provenances, etc

        name (str): The name of the output Series. Can be set up (by default = 'Site count')

        index_name (str): The name of the row of the output Series. Can be set up (by default = 'Year')

    Returns:
        pd.Series: A one-dimensional labeled array with years and site count values
    """

    minimum = data[lower_date].min()
    maximum = data[upper_date].max()

    date_dict = dict.fromkeys(range(int(minimum), int(maximum)), 0)

    df = data.dropna(subset=[lower_date])
    df = df.dropna(subset=[upper_date])

    for year in date_dict:

        result_list = []

        for row in range(len(df)):
            if (
                df[lower_date].astype(int).iloc[row]
                <= year
                <= df[upper_date].astype(int).iloc[row]
            ):
                result_list.append(df[object_list].iloc[row])

        length = len(result_list)

        if length == 0:
            continue

        else:

            flat_list = [item for sublist in result_list for item in sublist]

            date_dict[year] = len(set(flat_list))

    return create_series(date_dict, name=name, index_name=index_name)


def dates_intersect(
    map_lower_date: int,
    map_upper_date: int,
    object_lower_date: int,
    object_upper_date: int,
) -> int:
    """Calculates the length of intersection between two date ranges

    Args:
        map_lower_date (int): The start date of a map date range

        map_upper_date (int): The end date of a map date range

        object_lower_date (int): The start date of an object date range

        object_upper_date (int): The end date of an object date range

    Returns:
        int: The length of intersection
    """

    if (map_lower_date > map_upper_date) or (object_lower_date > object_upper_date):
        raise ValueError("Invalid input data!")

    result = min(map_upper_date, object_upper_date) - max(
        map_lower_date, object_lower_date
    )

    if result < 0:
        result = 0
    return result


def propor_to_map_range(
    data: pd.DataFrame,
    map_lower_date: int,
    map_upper_date: int,
    object_lower_date: str,
    object_upper_date: str,
    freq_per_year: str,
    proportion: str = "Proportion",
) -> pd.DataFrame:
    """Calculates the proportion of object frequency to a given date range

    Args:
        data (pd.DataFrame): A pandas dataframe

        map_lower_date (int): The start date of a map date range

        map_upper_date (int): The end date of a map date range

        object_lower_date (int): The start date of an object date range

        object_upper_date (int): The end date of an object date range

        freq_per_year (str): A dataframe column with frequency values per year per object

        proportion (str): A dataframe column with resulting object frequency values for a given date range.
        The name of the column can be set up (by default = 'Proportion')

    Returns:
        pd.DataFrame: An input dataframe with a new column containing object frequency values in
        proportion to a given map date range
    """

    data[proportion] = 0

    for row in range(len(data)):

        date_range = dates_intersect(
            map_lower_date,
            map_upper_date,
            data[object_lower_date].iloc[row],
            data[object_upper_date].iloc[row],
        )

        data[proportion].iloc[row] = data[freq_per_year].iloc[row] * date_range

    return data


def lattitude(url: str):
    """Extracts the lattitude coordinate from pleaides webpage

    Args:
        url (str): A pleaides url (str)

    Returns:
        Lattitude coordinate found on webpage
    """

    # Getting the source code of the webpage
    page = requests.get(url).text

    # Creating a parse tree
    soup = BeautifulSoup(page, "lxml")

    # Extracting the coordinates from website
    coordinates = soup.find("span", {"id": "representative-point"}).text

    # returning the coordinates (after being cleaned - see function)
    return cleanCoordinates(coordinates)[0]


def longitude(url: str):
    """Extracts the longitude coordinate from pleaides webpage

    Args:
        url (str): A pleaides url

    Returns:
        Longitude coordinate found on webpage
    """

    # Getting the source code of the webpage
    page = requests.get(url).text

    # Creating a parse tree
    soup = BeautifulSoup(page, "lxml")

    # Extracting the coordinates from website
    coordinates = soup.find("span", {"id": "representative-point"}).text

    # returning the coordinates (after being cleaned - see function)
    return cleanCoordinates(coordinates)[1]


def cleanCoordinates(txt: str) -> str:
    """Removes all characters that are not numbers, commas, or points of lattitude and longitude coordinates found on pleaides webpage

    Args:
        txt (str): Extracted coordinates from webpage

    Returns:
        str: Cleaned coordinates
    """

    # removing all characters that are not numbers, commas, or points
    txt = re.sub("[^0-9,.]", "", txt)

    # splitting up the string into a list containing lattitude and longitude
    txt = txt.split(",")

    return txt



def get_Y_range(dicts_of_df: Dict[str, pd.Series]) -> Tuple[int, int]:
    """Calculates minimum and maximum Y values.

    Args:
        dicts_of_df (Dict[str, pd.Series]): A dictionary containing series.
    Returns:
        Tuple[int, int]: Minimum and maximum value.
    """

    minimum_list = []
    maximum_list = []
    
    for key in dicts_of_df.keys():

        data = dicts_of_df.get(key)

        minimum_list.append(data.index.values.min())
        maximum_list.append(data.index.values.max())

    minimum = min(minimum_list)
    maximum = max(maximum_list)
    

    return minimum, maximum


def plot_graph(dicts_of_df: Dict[str, pd.Series], 
               ax,
               palette: List[str],
               linewidth: int = 3,
               linestyle: str = 'solid', alpha=0.9):
    """Plot line graphs with information in different dataframes.

    Args:
        dicts_of_df (Dict[str, pd.Series]): A dictionary containing series.
        ax: Axes or array of Axes.
        palette (List[str]): A list with colours names for lines.
        linewidth (int): The width of a line.
        linestyle (str): The line style f.ex., 'solid' or 'dashed'.
    """
   
    for key, colour in zip(dicts_of_df.keys(), palette):
        data = dicts_of_df.get(key)
        sns.lineplot(data=data, ax=ax,label=key, color = colour, linewidth = linewidth,  linestyle=linestyle, alpha=alpha)     