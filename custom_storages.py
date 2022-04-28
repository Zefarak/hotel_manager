from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage

'''
class StaticStorage(S3BotoStorage):
    location = settings.STATICFILES_LOCATION
'''


class PublicMediaStorage(S3Boto3Storage):
    location = 'media'
    default_acl = 'public-read'
    file_overwrite = False


class MediaStorage(S3Boto3Storage):
    location = settings.PUBLIC_MEDIA_LOCATION
    # host = "s3-%s.amazonaws.com" % settings.AWS_REGION

    '''
    @property
    def connection(self):
        if self._connection is None:
            self._connection = self.connection_class(
                self.access_key, self.secret_key,
                calling_format=self.calling_format, host=self.host)
        return self._connection
    '''