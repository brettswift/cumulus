# try:
#     #python 3
#     from unittest.mock import patch
# except:
#     #python 2
#     from mock import patch

import unittest

from cumulus.policies import s3


class TestPolicies(unittest.TestCase):

    # Not supported yet.
    # def test_bucket_policy_should_not_add_condition_without_ip_restriction(self):
    #
    #     policy = s3.get_policy_static_website(
    #         policy_name="test_policy",
    #         bucket_name_or_ref="the-bucket"
    #     )
    #
    #     self.assertTrue('PolicyDocument' in policy.to_dict())
    #     self.assertFalse('Condition' in policy.to_dict())

    def test_bucket_policy_should_add_condition_with_ip_restriction(self):

        policy = s3.get_policy_static_website(
            policy_name="test_policy",
            bucket_name_or_ref="the-bucket",
            ip_access_filter=['192.168.1.1/8', '1.2.3.4/5']
        )

        self.assertTrue('PolicyDocument' in policy.to_dict())

        doc = policy.PolicyDocument
        print(policy.PolicyDocument)
        from pprint import PrettyPrinter
        pp = PrettyPrinter()
        pp.pprint(doc.to_json())
        # return policy


        self.assertTrue('Condition' in doc)
        # self.assertTrue('IpAddress' in policy.to_dict())
