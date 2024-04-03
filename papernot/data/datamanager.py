import csv
import io
import os
import warnings
from typing import Tuple

import numpy as np
import pandas as pd
import pyproj
import requests
from pandarallel import pandarallel
import tqdm 
from tqdm import tqdm
import geopandas as gpd
from shapely.geometry import Point
from typing import Tuple
import geopandas as gpd






# Suppress deprecation warnings from the console as pyproj transform is deprecated
warnings.filterwarnings("ignore", category=DeprecationWarning)

# Lambert and WGS84 projections for coordinate conversion
LAMBERT = pyproj.Proj('+proj=lcc +lat_1=49 +lat_2=44 +lat_0=46.5 +lon_0=3 +x_0=700000 +y_0=6600000 +ellps=GRS80 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs')
WGS84 = pyproj.Proj('+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs')


operators = {20801 :"Orange", 20810:"SFR", 20820:"Bouygues", 20815:"Free"}



def main() -> None:
    """
    Main function to orchestrate the data processing workflow.
    """
    original_data_frame = get_original_data_frame()
    create_networks_csv(original_data_frame)
    create_operators_csv(original_data_frame)
    gps_coordinates = get_gps_coordinates(original_data_frame)
    gps_coordinates.to_csv('dataset.csv', index=False)



def get_coverage(center: Tuple[float, float], radius: float, gdf: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    """
    Get points within a circular coverage area.

    Args:
        center: A tuple containing the longitude and latitude of the center point of the circular area.
        radius: The radius of the circular area in meters.
        gdf: A GeoDataFrame containing the points data.

    Returns:
        A GeoDataFrame containing points that fall within the circular coverage area.
    """
    # 1. Define the center point and radius of the circular area
    center_point = Point(center)  # Center point of the circle
    radius_meters = radius  # Radius of the circle in meters
    # 2. Create a circular geometry
    circle_geometry = center_point.buffer(radius_meters)
    # 3. Perform a spatial query to find points within the circular area
    points_within_circle = gdf[gdf.geometry.within(circle_geometry)]
    return points_within_circle



def lambert93_to_gps(x, y):
    long, lat = pyproj.transform(LAMBERT, WGS84, x, y)
    return long, lat



def get_original_data_frame() -> pd.DataFrame:
    """
    Retrieve the original data frame from the CSV file.
    """
    original_data_frame = pd.read_csv('2018_01_Sites_mobiles_2G_3G_4G_France_metropolitaine_L93.csv',
                                     header=0,
                                     delimiter=';')
    original_data_frame.dropna(subset=['X', 'Y'], inplace=True)
    original_data_frame.drop_duplicates(inplace=True)
    return original_data_frame


def create_networks_csv(original_data_frame: pd.DataFrame) -> None:
    """
    Create a CSV file with network names.
    """
    networks = original_data_frame.columns[-3:]
    with open("networks.csv", mode='w') as csv_file:
        file_writer = csv.writer(csv_file)
        file_writer.writerow(['network_name'])
        for value in networks:
            file_writer.writerow([value])


def create_operators_csv(original_data_frame: pd.DataFrame) -> None:
    """
    Create a CSV file with operator details.
    """
    operators = original_data_frame[['Operateur']].drop_duplicates()
    operators = append_operator_details_from_code(operators)[['Operateur', 'Nom']]
    operators = operators.rename(columns={"Operateur": "code", "Nom": "provider_name"})
    operators.to_csv('operators.csv', index=False)


def get_gps_coordinates(original_data_frame: pd.DataFrame) -> pd.DataFrame:
    """
    Retrieve GPS coordinates from the original data frame.
    """
    coordinates = original_data_frame[['X', 'Y']].drop_duplicates()
    coordinates = original_data_frame[['X', 'Y']]    
    lon_lat_list = []
    for _, row in tqdm(coordinates.iterrows(), total=len(coordinates)):
        lon, lat = lambert93_to_gps(row['X'], row['Y'])
        lon_lat_list.append((lon, lat))
    original_data_frame[['lon', 'lat']] = lon_lat_list
    return original_data_frame


def get_city_details(coordinates: pd.DataFrame) -> pd.DataFrame:
    """
    Retrieve city details from GPS coordinates.
    """
    city_details = pd.DataFrame()
    for idx, chunk in enumerate(np.array_split(coordinates, 10)):
        coordinate_csv = chunk.to_csv(columns=['lat', 'lon'], index=False)
        current_city_details = get_city_from_gps_coord(coordinate_csv).dropna()
        if city_details.empty:
            city_details = current_city_details
        else:
            city_details = city_details.append(current_city_details)
    city_details = city_details.rename(columns={"result_city": "city"})
    return city_details


def create_cities_csv(city_details: pd.DataFrame) -> None:
    """
    Create a CSV file with city details.
    """
    cities = city_details[['city']].drop_duplicates()
    cities.to_csv('cities.csv', index=False)


def create_city_provider_network(original_data_frame: pd.DataFrame, city_details_df: pd.DataFrame, gps_coordinates: pd.DataFrame) -> None:
    """
    Create a CSV file with city-provider network details.
    """
    city_details = city_details_df.round({'lon': 12, 'lat': 12})
    gps_coordinates = gps_coordinates.round({'lon': 12, 'lat': 12})
    city_details_with_xy = city_details.merge(gps_coordinates, on=['lon', 'lat'])
    city_network_provider = city_details_with_xy.merge(original_data_frame, on=['X', 'Y'])[['city', 'Operateur', '2G', '3G', '4G']]
    city_network_provider.drop_duplicates(inplace=True)
    city_network_provider.to_csv('city_provider_network.csv', index=False)


def convert_lambert93_to_gps_coord(x: float, y: float) -> Tuple[float, float]:
    """
    Convert Lambert 93 coordinates to GPS coordinates.
    """
    lon, lat = pyproj.transform(LAMBERT, WGS84, x, y)
    return lon, lat


def get_city_from_gps_coord(csv_file: str) -> pd.DataFrame:
    """
    Retrieve city details from GPS coordinates using an external API.
    """
    resp = requests.post('https://api-adresse.data.gouv.fr/reverse/csv/', files={'data': csv_file, 'result_columns': 'result_city'})
    resp.raise_for_status()
    data = resp.text
    buffer = io.StringIO(data)
    address_details = pd.read_csv(buffer, delimiter=',', header=0)
    return address_details[['lon', 'lat', 'result_city']]


def append_operator_details_from_code(code_list: pd.DataFrame) -> pd.DataFrame:
    """
    Append operator details from code list using MCC-MNC codes.
    """
    mcc_mnc_code_data_frame = pd.read_csv('mcc_mnc_codes.csv', header=0)
    return code_list.merge(mcc_mnc_code_data_frame, how='inner', left_on='Operateur', right_on='MCC-MNC')


if __name__ == "__main__":
    main()
