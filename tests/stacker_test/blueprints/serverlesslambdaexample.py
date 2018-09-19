import troposphere
import troposphere.codebuild
from stacker.blueprints.base import Blueprint

from cumulus.chain import chain
from cumulus.chain.chaincontext import ChainContext
from cumulus.steps.serverless import lambda_function


class ServerlessLambdaExample():
    """
    This will only output yaml, with a transform in the template.
    Because we need the transform, this won't work with stacker,
    because this template requires an `aws package` and stacker
    doesn't do that.
    """

    def create_template(self):
        """

        :rtype: troposphere.Template
        """
        t = troposphere.Template()
        the_chain = chain.Chain()
        chain_context = ChainContext(
            template=t,
            instance_name="testLambda",
        )

        node6 = {
            "Runtime": "nodejsj6.10",
            "MemorySize": 128,
            "Timeout": 300,
            "Role": troposphere.GetAtt("StateMachineLambdaRole", "Arn"),
        }

        the_chain.add(lambda_function.LambdaFunction(
            file_name='create_thinga_majig',
            package_dir="lambdas",
            config=node6
        ))

        the_chain.run(chain_context)

        return t


# See output with:
# python ./blueprints/test_deploy_lambda/lambda.py

if __name__ == "__main__":
    sut = ServerlessLambdaExample()
    template = sut.create_template()

    print(template.to_json())
    print(template.to_yaml())
