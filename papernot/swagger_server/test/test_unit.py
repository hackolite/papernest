# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO
from swagger_server.models.network_coverage_response import NetworkCoverageResponse  # noqa: E501
from swagger_server.test import BaseTestCase


class TestNetworkController(BaseTestCase):
    """NetworkController integration test stubs"""

    def test_retrieve_coverage(self):
        """Test case for retrieve_coverage

        Request for network Coverage
        """

        data = {
            'additionalProp1': 'string',
            'additionalProp2': 'string',
            'additionalProp3': 'string'
        }

        # En-têtes de la requête
        headers = {
            'accept': 'application/json',
            'Content-Type': 'application/json'
        }
        response = self.client.open(
            '/api/v3/network',
            method='POST',
            headers=headers,
            json=data,
            content_type='application/json')
        self.assert200(response)


if __name__ == '__main__':
    import unittest
    unittest.main()

