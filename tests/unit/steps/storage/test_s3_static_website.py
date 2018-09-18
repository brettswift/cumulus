# try:
#     #python 3
#     from unittest.mock import patch
# except:
#     #python 2
#     from mock import patch

import unittest

import troposphere
from troposphere import s3  # noqa

from cumulus.chain import chaincontext, chain  # noqa
from cumulus.steps.storage import s3_website_config   # noqa


class TestS3WebsiteConfig(unittest.TestCase):

    def setUp(self):
        self.context = chaincontext.ChainContext(
            template=troposphere.Template(),
            instance_name='justtestin',
        )

    def tearDown(self):
        del self.context

    def test_website_config_is_added_if_no_bucket_supplied(self):

        t = self.context.template

        t.add_resource(troposphere.s3.Bucket("TestBucket", BucketName="superbucket"))

        the_chain = chain.Chain()

        the_chain.add(s3_website_config.StaticWebsiteConfig())

        the_chain.run(chain_context=self.context)
        #
        # print(t.to_yaml())
        # self.assertTrue(False)

    def test_should_find_s3_bucket_in_template(self):
        t = self.context.template
        t.add_resource(troposphere.s3.Bucket("TestBucket", BucketName="superbucket"))
        print(t.to_yaml())

        result = s3_website_config.StaticWebsiteConfig.find_sole_template_bucket(t)

        self.assertTrue(result.__class__, troposphere.s3.Bucket)
