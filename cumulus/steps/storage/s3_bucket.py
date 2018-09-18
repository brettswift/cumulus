import troposphere
from troposphere import s3  # noqa

from cumulus.chain import step   # noqa
from cumulus.chain import chaincontext   # noqa


class S3Bucket(step.Step):

    def __init__(self, bucket_name):
        """

        :type bucket_name: String or troposphere.Ref (to parameter)
        """
        step.Step.__init__(self)
        self.bucket_name = bucket_name

    def handle(self, chain_context):
        """

        :type chain_context: chaincontext.ChainContext
        """
        step.Step.handle(self, chain_context)

        bucket = troposphere.s3.Bucket(
            "SiteBucket",
            BucketName=self.bucket_name
        )

        chain_context.template.add_resource(bucket)
