from blob_manager import BlobManager
from helpers.path_formatter import absolute_path

# Blob manager class parameters
BUCKET_NAME = 'original-bucket'
BLOB_NAME = 'nika.csv'
BLOB_PATH = ''
PROJECT_NAME = '3rd-month-project'
CREDENTIALS_JSON = absolute_path('config/credentials.json')

# Object template, uncomment for use
# blob_object = BlobManager(credentials_path=CREDENTIALS_JSON,
#                           blob_path=BLOB_PATH,
#                           blob_name=BLOB_NAME,
#                           bucket_name=BUCKET_NAME,
#                           project_name=PROJECT_NAME)


def main():
    # blob_object.upload('data/nika.csv')
    return True


if __name__ == '__main__':
    main()
