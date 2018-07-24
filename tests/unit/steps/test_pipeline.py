# try:
#     #python 3
#     from unittest.mock import patch
# except:
#     #python 2
#     from mock import patch

import unittest

from cumulus.chain import step, chaincontext
from cumulus.steps import pipeline
import troposphere

from cumulus.steps.pipeline import VpcConfig
from cumulus.util.tropo import TemplateQuery
from troposphere import codepipeline, codebuild


class TestPipelineStep(unittest.TestCase):

    def setUp(self):
        self.context = chaincontext.ChainContext(
            template=troposphere.Template(),
            instance_name='justtestin',
            vpc_id=troposphere.Ref("nope")
        )
        self.environment = codebuild.Environment(
            ComputeType='BUILD_GENERAL1_SMALL',
            Image='aws/codebuild/python:2.7.12',
            Type='LINUX_CONTAINER',
            EnvironmentVariables=[
                {'Name': 'TEST_VAR', 'Value': 'demo'}
            ],
        )

    def tearDown(self):
        del self.context

    def test_pipeline_records_metadata(self):
        sut = pipeline.Pipeline(
            name='test', bucket_name='testbucket'
        )
        sut.handle(self.context)
        self.assertIsInstance(sut, step.Step)
        self.assertTrue(
            expr=(pipeline.META_LAST_STAGE_OUTPUT in self.context.metadata),
            msg="Expected Pipeline would set output artifact"
        )

    def test_pipeline_has_two_stages(self):

        sut = pipeline.Pipeline(
            name='test', bucket_name='testbucket'
        )
        sut.handle(self.context)
        t = self.context.template

        pipelines = TemplateQuery.get_resource_by_type(t, codepipeline.Pipeline)
        self.assertTrue(len(pipelines), 1)

    def test_codebuild_should_add_stage(self):

        sut = pipeline.Pipeline(
            name='test', bucket_name='testbucket'
        )
        sut.handle(self.context)
        t = self.context.template

        codebuild = pipeline.CodeBuildStage()
        codebuild.handle(self.context)

        found_pipeline = TemplateQuery.get_resource_by_type(t, codepipeline.Pipeline)[0]
        stages = found_pipeline.properties['Stages']
        self.assertTrue(len(stages) == 2, msg="Expected Code Build to add a stage to the pipeline")

    def test_code_build_should_not_add_vpc_config(self):

        codebuild = pipeline.CodeBuildStage()

        project = codebuild.create_project(
            chain_context=self.context,
            codebuild_role='dummy-role',
            environment=self.environment
        )

        self.assertNotIn('VpcConfig', project.to_dict())

    def test_code_build_should_add_vpc_config(self):

        codebuild = pipeline.CodeBuildStage(
            vpc_config=VpcConfig(
                vpc_id='dummy-vpc',
                subnets=[
                    'dummy-subnet1'
                ]
            )
        )

        project = codebuild.create_project(
            chain_context=self.context,
            codebuild_role='dummy-role',
            environment=self.environment
        )

        self.assertIn('VpcConfig', project.properties)
