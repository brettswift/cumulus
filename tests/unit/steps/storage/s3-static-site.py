# try:
#     #python 3
#     from unittest.mock import patch
# except:
#     #python 2
#     from mock import patch

import unittest

import troposphere
from troposphere import s3

from cumulus.chain import chaincontext, chain
from cumulus.steps.storage, , s3_website_config


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

        t.add_resource(troposphere.s3.Bucket("TestBucket", BucketName="SuperBucket"))

        the_chain = chain.Chain()

        the_chain.add(s3_website_config.StaticWebsiteConfig())

        the_chain.run(chain_context=self.context)

        print(t.to_yaml())
