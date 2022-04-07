from utilities.gcp_blob_creator import BlobCreator
from helpers.path_formatter import absolute_path


BUCKET_NAME = 'maridashvili-bucket'
BLOB_NAME = 'archil.csv'
BLOB_PATH = ''
PROJECT_NAME = 'crud-project'
CREDENTIALS_JSON = absolute_path('temporary_config/credentials.json')


class BlobManager:

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
        self.blobs = self.bucket.list_blobs(prefix=self.blob_path,
                                            versions=True)

    def upload(self, file_path):
        self.blob.upload_from_filename(absolute_path(file_path))
        return f'Uploading {self.object.blob_name}'

    def delete(self):
        self.blob.delete()
        return f'{self.blob_name} Deleted'

    def download_file(self, download_to='downloads/'):
        self.blob.download_to_filename(
            f'{download_to}{self.blob_name}')
        return f'Downloaded {self.blob_name}'

    @property
    def get_string(self):
        return self.blob.download_as_string()

    def update(self, file_path):
        self.delete()
        self.upload(file_path)
        return f'Updated {self.blob_name}'

    def some_func(self):
        hash_list = []
        for blob in self.blobs:
            hash_list.append(blob.md5_hash)


b = BlobManager(credentials_path=CREDENTIALS_JSON, blob_path=BLOB_PATH,
                blob_name=BLOB_NAME, bucket_name=BUCKET_NAME,
                project_name=PROJECT_NAME)

b.upload('temporary_data/archil.csv')

b.some_func()