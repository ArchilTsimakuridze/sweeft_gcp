from dataclasses import dataclass
from typing import Optional

from utilities.gcp_client_creator import CredentialManager


@dataclass
class BlobCreator:
    """Returns a bucket and a blob for a given GCP client"""

    credentials_json: str
    project_name: str
    bucket_name: str
    blob_name: Optional[str] = None
    blob_path: Optional[str] = ''

    @property
    def bucket(self):
        """Returns a bucket from a gcp client"""
        client = CredentialManager(self.credentials_json,
                                   self.project_name).get_client

        return client.get_bucket(self.bucket_name)

    @property
    def get_blob(self):
        """Returns a blob for a given bucket"""
        if self.blob_path:
            return self.bucket.blob(self.blob_path + '/' + self.blob_name)
        else:
            return self.bucket.blob(self.blob_name)
