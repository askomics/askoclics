from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import mimetypes
import os
import sys

from future import standard_library

from askoclics.client import Client
from askoclics.exceptions import *
standard_library.install_aliases()


class FileClient(Client):
    """
    Manipulate files managed by Askomics
    """

    def list(self):
        """
        List files added in Askomics

        :rtype: list
        :return: List with files
        """

        return self._api_call("get", "list_files", {})['files']


    def upload(self, url="", file_path="", verbose=False):
        """
        Upload a file from askomics

        :type url: str
        :param url: URL to the file

        :type file_path: str
        :param file_path: Path to the file to upload

        :type verbose: bool
        :param verbose: Show progression bar for local file upload

        :rtype: dict
        :return: Dict with results
        """
        if not (url or file_path) or (url and file_path):
            raise AskoclicsParametersError("Please provided either an url or a file path")

        if url:
            return self._api_call("post", "upload_url_file", {"url": url})

        if not os.path.isfile(file_path):
            raise AskoclicsParametersError("Local file not found")

        file_name = os.path.basename(file_path)
        mimetype = mimetypes.guess_type(file_path)[0]
        # Chunk size to 10 Mo
        file_size = os.stat(file_path).st_size
        chunk_size = 1024*1024*10
        first = True
        last = False
        uploaded_size = 0

        if file_size <= chunk_size:
            last = True

        with open(file_path, "rb") as f:
            if verbose:
                print("0%")

            for piece in self._read_in_chunks(f, chunk_size):
                size = sys.getsizeof(piece)
                body = {"chunk": piece.decode("utf-8"), "first": first, "last": last, "type": mimetype, "name": file_name, "size": file_size}
                res = self._api_call("post", "upload_local_file", body)
                first = False
                body['path'] = res["path"]
                uploaded_size += size
                if verbose:
                    print("{0:.0%}".format(file_size/uploaded_size * 100))

        return res


    def preview(self, files):
        """
        Get preview for a list of files

        :type files: str
        :param files: Comma-separated file IDs

        :rtype: dict
        :return: Dictionary containing the information
        """


        files = self._parse_input_values(files, "Files")
        body = {'filesId': files}

        return self._api_call("post", "preview_files", body)


    def describe(self, files):
        """
        Show file information

        :type files: str
        :param files: Comma-separated file IDs

        :rtype: list
        :return: List of files containing info
        """

        files = self._parse_input_values(files, "Files")
        body = {'filesId': files}

        res = self._api_call("post", "preview_files", body)

        files = []

        for file in res.get("previewFiles"):
            if "data" in file:
                file["data"].pop("content_preview", None)
            files.append(file)

        return files


    def integrate_csv(self, file_id, columns="", headers="", custom_uri=None, external_endpoint=None):
        """
        Send an integration task for a specified file_id

        :type file_id: str
        :param file_id: File_id

        :type columns: str
        :param columns: Comma-separated columns (default to detected columns)

        :type headers: str
        :param headers: Comma-separated headers (default to file headers)

        :type custom_uri: str
        :param custom_uri: Custom uri

        :type external_endpoint: str
        :param external_endpoint: External endpoint

        :rtype: dict
        :return: Dictionary of task information
        """

        columns = self._parse_input_values(columns, "Columns")
        headers = self._parse_input_values(columns, "Headers")

        body = {"fileId": file_id, "columns_type": columns, "header_names": headers, "customUri": custom_uri, "externalEndpoint": external_endpoint}
        return self._api_call("post", "integrate_file", body)


    def integrate_bed(self, file_id, entity="", custom_uri=None, external_endpoint=None):
        """
        Send an integration task for a specified file_id

        :type file_id: str
        :param file_id: File_id

        :type entity: str
        :param entity: Name of the entity (default to file name)

        :type custom_uri: str
        :param custom_uri: Custom uri

        :type external_endpoint: str
        :param external_endpoint: External endpoint

        :rtype: dict
        :return: Dictionary of task information
        """

        body = {"fileId": file_id, "entity_name": entity, "customUri": custom_uri, "externalEndpoint": external_endpoint}
        return self._api_call("post", "integrate_file", body)


    def integrate_gff(self, file_id, entities="", custom_uri=None, external_endpoint=None):
        """
        Send an integration task for a specified file_id

        :type file_id: str
        :param file_id: File_id

        :type entities: str
        :param entities: Comma-separated list of entities to integrate. (Default to all available entities)

        :type custom_uri: str
        :param custom_uri: Custom uri

        :type external_endpoint: str
        :param external_endpoint: External endpoint

        :rtype: dict
        :return: Dictionary of task information
        """

        entities = self._parse_input_values(entities, "Entities")
        body = {"fileId": file_id, "entities": entities, "customUri": custom_uri, "externalEndpoint": external_endpoint}
        return self._api_call("post", "integrate_file", body)


    def integrate_rdf(self, file_id, custom_uri=None, external_endpoint=None):
        """
        Send an integration task for a specified file_id

        :type file_id: str
        :param file_id: File_id

        :type custom_uri: str
        :param custom_uri: Custom uri

        :type external_endpoint: str
        :param external_endpoint: External endpoint

        :rtype: dict
        :return: Dictionary of task information
        """

        body = {"fileId": file_id, "customUri": custom_uri, "externalEndpoint": external_endpoint}
        return self._api_call("post", "integrate_file", body)


    def delete(self, files):
        """
        Delete a list of files

        :type files: str
        :param files: Comma-separated file IDs to delete

        :rtype: dict
        :return: Dictionary containing the remaining files
        """

        files = self._parse_input_values(files, "Files")
        body = {'filesIdToDelete': files}

        return self._api_call("post", "delete_files", body)


    def _read_in_chunks(self, file_object, chunk_size):
        """Lazy function (generator) to read a file piece by piece.
        Default chunk size: 10 Mo."""
        while True:
            data = file_object.read(chunk_size)
            if not data:
                break
            yield data
