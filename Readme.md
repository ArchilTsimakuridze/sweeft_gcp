## About The Project

This project detects updated files in GCP Bucket, if a listener is triggered with a file update, the file is transferred to an updated bucket and contents of the file uploaded to Postgres database where historical data is also stored.

The project makes use of:
* GCP Cloud Storage
* GCP Cloud Functions
* GCP Cloud Composer 2
* GCP SQL - Postgres

Upper-limit to csv file size is 650 MB

## Getting Started

It is essential to understand, that due to the nature of the project, this specific setup of cloud composer and cloud functions work only on a specific GCP service account key. This application will not work on any service account key provided.

### Prerequisites

Run `requirements.txt` to install all dependencies.

Request `credentials.json` and Project Name to get started.


## Usage

Inside main.py, create a blob object using provided credentials and a project name. Alongside credentials and a project name you need to provide the following:
* blob_path - preferably an empty string
* blob_name - preferably a string with GCP Bucket file name conventions
* bucket_name - a name of a bucket: string, which will act as a listener

Files can be uploaded both DIRECTLY on GCP and through `main.py`, listener will catch updates in both cases.

Because PSQL table / column names are generated dynamically, it is advised to follow PSQL naming rules for csv file / columns. However, it is not mandatory and incorrect names will be formatted to meet PSQL naming criteria - alphanumeric / underscore.

Files larger than 650 MB will run into uploading issues. Chunk size is limited to 650MB due to limitation of cloud functions to process very large files. However, if needed, chunk size can be modified from `gcp_blob_creator.py` but make sure to also update `upload-to-postgres.py` cloud function to 8GB.


