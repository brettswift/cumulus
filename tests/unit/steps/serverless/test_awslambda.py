# try:
#     #python 3
#     from unittest.mock import patch
# except:
#     #python 2
#     from mock import patch

import unittest

import troposphere

from cumulus.chain import chaincontext
from cumulus.steps.serverless import lambda_function


class TestAwsLambda(unittest.TestCase):

    def setUp(self):
        self.context = chaincontext.ChainContext(
            template=troposphere.Template(),
            instance_name='justtestin',
        )

    def tearDown(self):
        del self.context

    def test_should_camel_case_file_name(self):

        name = 'create_the_aws_thing'
        camels = lambda_function.underscore_to_camelcase(name)

        self.assertEqual("CreateTheAwsThing", camels)

    def test_should_normalize_folder_name_if_doesnt_end_in_slash(self):

        folder = "../lambdas"

        normalized = lambda_function.normalize_dir(folder)

        expected_folder = "../lambdas/"
        self.assertEqual(expected_folder, normalized)
