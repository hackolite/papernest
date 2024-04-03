# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server import util


class NetworkCoverageResponse(Model):
    """
        data manager
    """
    def __init__(self):  # noqa: E501
        """NetworkCoverageResponse - a model defined in Swagger

        """
        self.swagger_types = {
        }

        self.attribute_map = {
        }

    @classmethod
    def from_dict(cls, dikt) -> 'NetworkCoverageResponse':
        """Returns the dict as a model
        :param dikt: A dict.
        :type: dict
        :return: The NetworkCoverageResponse of this NetworkCoverageResponse.  # noqa: E501
        :rtype: NetworkCoverageResponse
        """
        return util.deserialize_model(dikt, cls)
