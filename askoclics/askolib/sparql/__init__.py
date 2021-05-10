from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import mimetypes
import os

from askoclics.askolib.client import Client
from askoclics.askolib.exceptions import AskoclicsParametersError

from future import standard_library

import requests

standard_library.install_aliases()


class SparqlClient(Client):
    """
    Send SPARQL queries to Askomics
    """

    def list(self):
        """
        List files added in AskOmics

        :rtype: list
        :return: List with files
        """

        return self._api_call("get", "list_files", {})['files']


    def get_config(self):
        pass





    def _get_config(self):
        # Return graphs, endpoints, and data uri
        data = {}
        config = self._api_call("get", "start", {})
        data["namespace_data"] = config["config"]["namespaceData"]
 
