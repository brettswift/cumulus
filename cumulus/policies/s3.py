import awacs
import awacs.aws
from awacs import s3
from awacs.aws import Condition, SourceIp
from troposphere import iam


def get_policy_static_website(policy_name, bucket_name_or_ref, ip_access_filter):

    # TODO: fix this.. awacs doesn't have an IpAddress class apparently?
    
    policy = iam.Policy(
        PolicyName=policy_name,
        PolicyDocument=awacs.aws.PolicyDocument(
            Version="2012-10-17",
            Id="%sId" % policy_name,
            Statement=[
                awacs.aws.Statement(
                    Effect=awacs.aws.Allow,
                    Action=[
                        awacs.s3.GetObject
                    ],
                    Resource=[
                         "arn:aws:s3:::",
                         bucket_name_or_ref,
                         "/*"
                    ],
                    Condition=awacs.aws.Condition([

                            {"IpAddress": {"aws::SourceIp": ip_access_filter}}
                    ])
                ),
            ]
        )
    )

    # "Condition"([
    #     IpAddress("aws:SourceIp", ["192.0.2.0/24", "203.0.113.0/24"]),
    # ])

    # Condition(
    # IpAddress=(SourceIp(ip_access_filter))
    # )

    return policy
