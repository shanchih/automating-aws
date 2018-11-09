# -*- coding: utf-8 -*-

"""Classes for S3 Buckets."""
from pathlib import Path
import mimetypes

from botocore.exceptions import ClientError


class BucketManager:
    """Manage an S3 Bucket."""

    def __init__(self, session):
        """Create a BucketManager object."""
        self.session = session
        self.s3 = session.resource('s3')

    def all_buckets(self):
        """Get an iterator for all buckets."""
        return self.s3.buckets.all()

    def all_objects(self, bucket_name):
        """Get an iterator for all objects in bucket."""
        return self.s3.Bucket(bucket_name).objects.all()

    def init_bucket(self, bucket_name):
        """Create a new bucket or return the existing one."""
        s3_bucket = None

        try:

            if self.session.region_name == 'us-east-1':
                s3_bucket = self.s3.create_bucket(Bucket=bucket_name)
            else:
                s3_bucket = self.s3.create_bucket(
                    Bucket=bucket_name,
                    CreateBucketConfiguration={
                        'LocationConstraint': self.session.region_name
                    }
                )
        except ClientError as error:
            raise error

        return s3_bucket

    @staticmethod
    def set_policy(bucket):
        """Set bucket policy to be readable by everyone."""
        policy = """
        {
          "Version":"2012-10-17",
          "Statement":[{
          "Sid":"PublicReadGetObject",
          "Effect":"Allow",
          "Principal": "*",
              "Action":["s3:GetObject"],
              "Resource":["arn:aws:s3:::%s/*"
              ]
            }
          ]
        }
        """ % bucket.name
        policy = policy.strip()
        bucket.Policy().put(Policy=policy)

    @staticmethod
    def configure_website(bucket):
        """Configure Websit."""
        bucket.Website().put(WebsiteConfiguration={
            'ErrorDocument': {
                'Key': 'error.html'
            },
            'IndexDocument': {
                'Suffix': 'index.html'
            }
        })

    @staticmethod
    def upload_file(bucket, path, key):
        """Upload files to bucket."""
        content_type = mimetypes.guess_type(key)[0] or 'text/plain'

        return bucket.upload_file(
            path,
            key,
            ExtraArgs={
                'ContentType': content_type
            })

    def sync(self, pathname, bucket_name):
        """Sync contents of PATHNAME to BUCKET."""
        bucket = self.s3.Bucket(bucket_name)
        root = Path(pathname).expanduser().resolve()

        def handle_directory(target):
            for obj in target.iterdir():
                if obj.is_dir():
                    handle_directory(obj)
                if obj.is_file():
                    self.upload_file(
                        bucket, str(obj), str(obj.relative_to(root))
                    )
        handle_directory(root)
