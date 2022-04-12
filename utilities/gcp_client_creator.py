from typing import Optional
from dataclasses import dataclass

from gcloud import storage
from oauth2client.service_account import ServiceAccountCredentials

from helpers.json_formatter import json_to_dict


@dataclass
class CredentialManager:
    """Returns a GCP client from credentials.json and project name"""

    path: str
    project_name: Optional[str] = None

    @property
    def credentials_dict(self):
        """Transforms json of credentials json into dictonary"""
        return json_to_dict(self.path)

    @property
    def get_credentials(self):
        """Returns credentials object from a credentials dict"""
        try:
            return ServiceAccountCredentials.from_json_keyfile_dict(
                keyfile_dict=self.credentials_dict)
        except ValueError as ve:
            print('Invalid credentials, please enter correct credentials')

    @property
    def get_client(self):
        """
        Returns a client object for a given credentials and a project name
        """
        return storage.Client(credentials=self.get_credentials,
                              project=self.project_name)
