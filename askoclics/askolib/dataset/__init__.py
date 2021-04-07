from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from future import standard_library

from askoclics.askolib.client import Client
from askoclics.askolib.exceptions import AskoclicsParametersError
standard_library.install_aliases()


class DatasetClient(Client):
    """
    Manipulate datasets managed by Askomics
    """

    def list(self):
        """
        List datasets added in Askomics

        :rtype: list
        :return: List of datasets
        """

        return self._api_call("get", "list_datasets", {})['datasets']

    def publicize(self, dataset_id):
        """
        Publicize a dataset

        :type dataset_id: str
        :param dataset_id: Dataset ID

        :rtype: dict
        :return: Dictionary with info and datasets
        """

        return self._api_call("get", "publicize_datasets", {"id": dataset_id})

    def delete(self, datasets):
        """
        Delete a list of files

        :type datasets: str
        :param datasets: Comma-separated list of datasets IDs

        :rtype: list
        :return: List of the remaining files
        """

        if isinstance(datasets, list):
            body = {'datasetsIdToDelete': datasets}
        elif isinstance(datasets, str):
            datasets = [data.strip() for data in datasets.split(",")]
            body = {'datasetsIdToDelete': datasets}
        else:
            raise AskoclicsParametersError("Datasets must either be a list or a comma-separated string")

        return self._api_call("post", "delete_files", body)
