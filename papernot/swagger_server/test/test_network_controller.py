# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.network_coverage_response import NetworkCoverageResponse  # noqa: E501
from swagger_server.test import BaseTestCase

import six
import pandas as pd
from swagger_server.models.network_coverage_response import NetworkCoverageResponse  # noqa: E501
from swagger_server import util
import geopandas as gpd
from shapely.geometry import Point
import json
from flask import Flask, jsonify, request

df = pd.read_csv("/usr/src/app/data/result.csv")
# Assuming df is your DataFrame with geographic data
gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.lon, df.lat))


class TestNetworkController(BaseTestCase):
    """NetworkController integration test stubs"""

    def test_retrieve_coverage(self):
        """Test case for retrieve_coverage

        Request for network Coverage
        """
        body = import connexion


def retrieve_coverage(body):  # noqa: E501
    """Request for network Coverage

    Retrieve Network Coverage for a list of adresses by Operators # noqa: E501

    :param body: CoverageByIds
    :type body: dict | bytes

    :rtype: NetworkCoverageResponse
    """

    # Assuming gdf is your GeoDataFrame containing points data

    # 1. Define the center point and radius of the circular area
    center_point = Point(-2, 48)  # Center point of the circle
    radius_meters = 300  # Radius of the circle in meters

    # 2. Create a circular geometry
    circle_geometry = center_point.buffer(radius_meters)
    # 3. Perform a spatial query to find points within the circular area
    points_within_circle = gdf[gdf.geometry.within(circle_geometry)]

    # Display the result (optional)
    print(len(points_within_circle))


    body = {
    "additionalProp1": {
    "additionalProp1": {
      "2G": True,
      "3G": True,
      "4G": True
    },
    "additionalProp2": {
      "2G": True,
      "3G": True,
      "4G": True
    },
    "additionalProp3": {
      "2G": True,
      "3G": True,
      "4G": True
    }
    },
    "additionalProp2": {
    "additionalProp1": {
      "2G": True,
      "3G": True,
      "4G": True
      }}}

    response = self.client.open(
            '/api/v3/network',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
