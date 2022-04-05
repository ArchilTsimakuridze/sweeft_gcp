from typing import Optional
from dataclasses import dataclass

from gcloud import storage
from oauth2client.service_account import ServiceAccountCredentials

from helpers.json_formatter import json_to_dict


@dataclass
class CredentialManager:

    path: str
    project_name: Optional[str] = None

    @property
    def credentials_dict(self):
        return json_to_dict(self.path)

    @property
    def get_credentials(self):
        return ServiceAccountCredentials.from_json_keyfile_dict(
            keyfile_dict=self.credentials_dict)

    @property
    def get_client(self):
        return storage.Client(credentials=self.get_credentials,
                              project=self.project_name)
