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

        if file_size <= chunk_size:
            last = True

        with open(file_path, "rb") as f:

            for piece in self._read_in_chunks(f, chunk_size):
                size = sys.getsizeof(piece)
                body = {"chunk": piece.decode("utf-8"), "first": first, "last": last, "type": mimetype, "name": file_name, "size": file_size}
                res = self._api_call("post", "upload_local_file", body)
                first = False
                body['path'] = res["path"]

        return res


    def preview(self, files):
        """
        Get preview for a list of files

        :type files: str
        :param files: Comma-separated file IDs

        :rtype: dict
        :return: Dictionary containing the information
        """

        if isinstance(files, list):
            body = {'filesId': files}
        elif isinstance(files, str):
            files = [data.strip() for data in files.split(",")]
            body = {'filesId': files}
        else:
            raise AskoclicsParametersError("Files must either be a list or a comma-separated string")

        return self._api_call("post", "preview_files", body)


    def guess_columns(self, files):
        """
        Get the guessed columns for a file

        :type files: str
        :param files: Comma-separated file IDs

        :rtype: list
        :return: List of files containing info
        """

        if isinstance(files, list):
            body = {'filesId': files}
        elif isinstance(files, str):
            files = [data.strip() for data in files.split(",")]
            body = {'filesId': files}
        else:
            raise AskoclicsParametersError("Files must either be a list or a comma-separated string")

        res = self._api_call("post", "preview_files", body)


        files = []

        if res['error']:
            raise AskoclicsApiError(res['errorMessage'])

        for file in res.get("previewFiles"):
            files.append({"error": file["error"], "errorMessage": file["error_message"], "columns": file["data"].get("columns_type", [])})

        return files


    def delete(self, files):
        """
        Delete a list of files

        :type files: str
        :param files: Comma-separated file IDs to delete

        :rtype: dict
        :return: Dictionary containing the remaining files
        """

        if isinstance(files, list):
            body = {'filesIdToDelete': files}
        elif isinstance(files, str):
            files = [data.strip() for data in files.split(",")]
            body = {'filesIdToDelete': files}
        else:
            raise AskoclicsParametersError("Files must either be a list or a comma-separated string")

        return self._api_call("post", "delete_files", body)


    def _read_in_chunks(self, file_object, chunk_size):
        """Lazy function (generator) to read a file piece by piece.
        Default chunk size: 10 Mo."""
        while True:
            data = file_object.read(chunk_size)
            if not data:
                break
            yield data
