import connexion
import six
import pandas as pd
from swagger_server.models.network_coverage_response import NetworkCoverageResponse  # noqa: E501
from swagger_server import util
import geopandas as gpd
from shapely.geometry import Point
import json
from flask import Flask, jsonify, request
import requests
import ast
import geopandas as gpd
from geopy.distance import distance
from math import radians, sin, cos, sqrt, atan2 



# Assuming df is your DataFrame with geographic data
# Load your dataset into a GeoDataFrame
gdf = gpd.read_file("/usr/src/app/data/result.csv")
# Assuming your dataset contains columns 'latitude' and 'longitude'
# Convert latitude and longitude columns to Point geometries
gdf['geometry'] = gpd.points_from_xy(gdf['lon'], gdf['lat'])



operator = {"Orange" : 20801, "SFR" : 20810, "Bouygues" : 20820, "Free": 20815 }
mobile_service = {"2G": 30, "3G": 5, "4G": 10}

def check(df):
    result = {}
    for ope, id_op in operator.items():
        for service, distance in mobile_service.items():
            if not df[(df['Operateur'] == str(id_op)) & (df[service] == "1") & (df["distance_to_reference_point"] < float(distance))].empty:
                result.update({ope:{service : True}})
            else:
                result.update({ope:{service : False}})
    return result

# Define the haversine distance function
def haversine_distance(lon1, lat1, lon2, lat2):
    """
    Calculate the great-circle distance between two points
    on the earth specified in decimal degrees
    """
    # Convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    radius_of_earth_km = 6371  # Radius of the Earth in kilometers
    distance_km = radius_of_earth_km * c

    return distance_km

def calculate_distance_h(longitude, latitude, lon, lat):
    return haversine_distance(longitude, latitude, lon, lat)


# Define a function to calculate the distance from each point to the reference point
def calculate_distance(point):
    return point.distance(reference_point)


def retrieve_coverage(body):  # noqa: E501
    """Request for network Coverage

    Retrieve Network Coverage for a list of adresses by Operators # noqa: E501

    :param body: CoverageByIds
    :type body: dict | bytes

    :rtype: NetworkCoverageResponse
    """

    # Charger les données JSON en tant qu'objet Python
    json_string = body.decode('utf-8')
    # Parse the JSON string into a dictionary using json.loads()
    geo_json = json.loads(json_string)
    geo_json = ast.literal_eval(geo_json)

    coverage_response = {}

    for key, address in geo_json.items():
        print(f"ID: {key}, Address: {address}")
        resp = requests.get('https://api-adresse.data.gouv.fr/search/', params={'q': address})
        resp.raise_for_status()
        resp = resp.json()
        coordinates = resp["features"][0]["geometry"]["coordinates"]
        # Assuming gdf is your GeoDataFrame containing points data
        # 1. Define the center point and radius of the circular area
        center_point = Point(coordinates[0], coordinates[1])  # Center point of the circle
        # Define the buffer distance in kilometers
        buffer_distance_km = 30  # Buffer distance in kilometers
        # Convert the buffer distance from kilometers to degrees
        buffer_distance_degrees = buffer_distance_km / 111 
        filtered_entries = gdf[gdf['geometry'].buffer(buffer_distance_degrees).contains(center_point)]
        # Add a new column 'distance_to_reference_point' to the GeoDataFrame
        filtered_entries['distance_to_reference_point'] = filtered_entries.apply(lambda row: calculate_distance_h(coordinates[0], coordinates[1], float(row['lon']), float(row['lat'])), axis=1)
        print(filtered_entries.info())
        coverage_response[key] = check(filtered_entries) 

    return coverage_response
