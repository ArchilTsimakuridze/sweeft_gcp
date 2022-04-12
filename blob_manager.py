from utilities.gcp_blob_creator import BlobCreator
from helpers.path_formatter import absolute_path


class BlobManager:
    """Creates a blob object from BlobCreator class and applies CRUD
    functionality to it.
    Args:
    credentials_path: Path to service account credentials file: Str
    project_name: Str
    blob_name: Str
    blob_path: Str
    bucket_name: Str

    Methods upload/update, delete and download a given blob
    or a file.
    """
    def __init__(self, credentials_path, project_name, bucket_name,
                 blob_name, blob_path):
        self.credentials_path = credentials_path
        self.project_name = project_name
        self.bucket_name = bucket_name
        self.blob_name = blob_name
        self.blob_path = blob_path
        self.credentials = absolute_path(self.credentials_path)
        self.object = BlobCreator(bucket_name=self.bucket_name,
                                  blob_name=self.blob_name,
                                  blob_path=self.blob_path,
                                  project_name=self.project_name,
                                  credentials_json=self.credentials)
        self.bucket = self.object.bucket
        self.blob = self.object.get_blob

    def upload(self, file_path):
        """Uploads to a bucket from a local file path"""
        self.blob.upload_from_filename(absolute_path(file_path))
        return f'Uploading {self.object.blob_name}'

    def delete(self):
        """Deletes a blob"""
        self.blob.delete()
        return f'{self.blob_name} Deleted'

    def download_file(self, download_to='downloads/'):
        """Downloads a blob locally, default folder - downloads"""
        self.blob.download_to_filename(
            f'{download_to}{self.blob_name}')
        return f'Downloaded {self.blob_name}'

    @property
    def get_string(self):
        """Saves bytes string of a blob to a variable"""
        return self.blob.download_as_string()

