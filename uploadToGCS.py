import os
from os.path import join,dirname
from dotenv import load_dotenv

from google.cloud import storage

# alternately, just load_dotenv() as it's in the same directory
#another alternate is to import find_dotenv, then add pass that function as a
#parameter for load_dotenv()
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
GCProject = os.getenv('GCLOUD_PROJECT')

bucketName = 'electric-usage-files'
#localPathToFile = '/Users/kevinrhodes/Downloads/SCE_Usage_8013433518_01-02-23_to_01-02-23.csv'
cleanedFileDirectory = '/Users/kevinrhodes/Desktop/cleanedFiles/'


def upload_blob(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    # The ID of your GCS bucket
    # bucket_name = "your-bucket-name"
    # The path to your file to upload
    # source_file_name = "local/path/to/file"
    # The ID of your GCS object
    # destination_blob_name = "storage-object-name"

    storage_client = storage.Client(project='electric-usage-files')
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)


    print(
        f"File {source_file_name} uploaded to {destination_blob_name}."
    )

for file in os.listdir(cleanedFileDirectory):
    if file.startswith("."):
        pass
    else:
        print(GCProject)
        print("Bucket:",bucketName)
        print("Local Path:",cleanedFileDirectory+file)
        print("File Name:",file)
        upload_blob(bucketName,cleanedFileDirectory+file,file)


def remove_files(cleanedFileDirectory):
    if len(os.listdir(cleanedFileDirectory)) > 0:
        for file in os.listdir(cleanedFileDirectory):
            os.remove(cleanedFileDirectory+file)
        remove_files(cleanedFileDirectory)
    else:
        os.rmdir(cleanedFileDirectory)

remove_files(cleanedFileDirectory)