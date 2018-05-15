from storages.backends.s3boto3 import S3Boto3Storage
from .settings import S3_MEDIA_FOLDER

class MediaStorage(S3Boto3Storage):
    location = S3_MEDIA_FOLDER
    file_overwrite = False