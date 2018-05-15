from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import IsAuthenticated

@api_view(['GET'])
# @permission_classes((IsAuthenticated, ))
def sign_s3(request):
  from ShoppingCart.settings import AWS_STORAGE_BUCKET_NAME
  from ShoppingCart.settings import S3_MEDIA_FOLDER

  file_name = request.GET.get('file_name')
  file_type = request.GET.get('file_type')

  import boto3
  from botocore.config import Config
  s3 = boto3.client('s3', region_name='eu-central-1', config=Config(signature_version='s3v4'))

  presigned_post = s3.generate_presigned_post(
    Bucket=AWS_STORAGE_BUCKET_NAME,
    Key=S3_MEDIA_FOLDER + "/" + file_name,
    Fields={"acl": "public-read", "Content-Type": file_type},
    Conditions=[
      {"acl": "public-read"},
      {"Content-Type": file_type}
    ],
    ExpiresIn=3600
  )

  url = 'https://%s.s3.amazonaws.com/%s/%s' % (AWS_STORAGE_BUCKET_NAME, S3_MEDIA_FOLDER, file_name)
  from django.http import JsonResponse
  response =  JsonResponse({
    'data': presigned_post,
    'url': url,
  })

  return response
