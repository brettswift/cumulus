import troposphere
from cumulus.util.tropo import TemplateQuery
from troposphere import s3

from cumulus.chain import step
from cumulus.chain import chaincontext


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
        step.Step.handle(self, chain_context)

        if self.bucket_name:
            bucket = TemplateQuery.get_resource_by_title(chain_context.template, self.bucket_name)
        else:
            bucket = self.find_sole_template_bucket(chain_context.template)

        bucket['AccessControl'] = 'PublicRead'
        bucket['WebsiteConfiguration'] = {
            'IndexDocument': self.index_doc,
            'ErrorDocument': self.error_doc
        }



    @staticmethod
    def find_sole_template_bucket(template):

        #assume only one, or error.
        buckets = TemplateQuery.get_resource_by_type(
            template=template,
            type_to_find=troposphere.s3.Bucket,
        )

        if buckets.count(buckets) > 1:
            raise AssertionError("If there are more than one bucket in the template you must specify a name")

        if buckets.count(buckets) == 0:
            raise AssertionError("Expected to find a bucket in the template but did not")

        return buckets[0]
