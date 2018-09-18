import troposphere   # noqa
from cumulus.util.tropo import TemplateQuery   # noqa
from troposphere import s3   # noqa

from cumulus.chain import step   # noqa
from cumulus.chain import chaincontext   # noqa


class StaticWebsiteConfig(step.Step):

    def __init__(self,
                 index_doc='index.html',
                 error_doc='404.html',
                 bucket_name=None):
        """

        :type error_doc: basestring or troposphere.Ref (to parameter)
        :type index_doc: basestring or troposphere.Ref (to parameter)
        :type bucket_name: basestring or troposphere.Ref (to parameter)
        """
        step.Step.__init__(self)
        self.index_doc = index_doc
        self.error_doc = error_doc
        self.bucket_name = bucket_name

    def handle(self, chain_context):
        """

        :type chain_context: chaincontext.ChainContext
        """
        if self.bucket_name:
            bucket = TemplateQuery.get_resource_by_title(chain_context.template, self.bucket_name)
        else:
            bucket = self.find_sole_template_bucket(chain_context.template)

        bucket.AccessControl = 'PublicRead'
        bucket.WebsiteConfiguration = s3.WebsiteConfiguration(
            "StaticSite",
            IndexDocument=self.index_doc,
            ErrorDocument=self.error_doc
        )

        bucket_policy = troposphere.s3.Policy(


        )

        # dns_record = tpl.add_resource(RecordSetType(
        #     "DroneServerDNSRecord",
        #     HostedZoneName=Join("", [Ref(aws_dns_zone), "."]),
        #     Comment="Redirect to ALB For Drone",
        #     Name=get_dns_for_server(),
        #     Type="A",
        #     AliasTarget=AliasTarget(
        #         HostedZoneId=GetAtt(alb_drone_server, "CanonicalHostedZoneID"),
        #         DNSName=GetAtt(alb_drone_server, "DNSName")
        #     )
        # ))

        # tpl.add_output(Output(
        #     "URLToCiServer",
        #     Value=Join('', [
        #         'http://',
        #         Ref(dns_record)
        #     ]),
        #     Description="Url to Drone Server"
        # ))

    @staticmethod
    def find_sole_template_bucket(template):

        # assume only one, or error.
        buckets = TemplateQuery.get_resource_by_type(
            template=template,
            type_to_find=troposphere.s3.Bucket,
        )
        if len(buckets) > 1:
            raise AssertionError("If there are more than one bucket in the template you must specify a name")

        if len(buckets) == 0:
            raise AssertionError("Expected to find a bucket in the template but did not")

        return buckets[0]
