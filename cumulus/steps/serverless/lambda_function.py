import troposphere.serverless
from troposphere import GetAtt

from cumulus.chain import chaincontext  # noqa
from cumulus.chain import step

LAMBDA_FUNCTION_ARGS_NAME = "LambdaConfig-"


class LambdaFunction(step.Step):

    def __init__(self,
                 file_name,
                 function_name=None,
                 package_dir='',
                 code_function='handler',
                 config=None
                 ):
        """
        Note: Must be used with `aws cloudformation package`

        This function makes things simple if you follow some conventions:
        1. name your file: 'my_function_name.js'
           * and pass in 'function_name=my_function_name'
           * cumulus will create a function called: 'MyFunctionName'.
        2. Export your function in a method called 'handler'

        or

        Override at will.

        Usage:
        Other parameters can be overridden as follows:

        node6 = {
            "Runtime": "nodejsj6.10",
            "MemorySize": 128,
            "Timeout": 30,
            "Role": GetAtt("StateMachineLambdaRole", "Arn"),
            "Environment": troposphere.awslambda.Environment(
                Variables={
                    'TABLE_NAME': Ref("table_name")
                }
            ),
            Events={
                'GetResource': ApiEvent(
                    'GetResource',
                    Path='/resource/{resourceId}',
                    Method='get'
                )
            }
        }

        the_chain.add(cumulus.steps.serverless.awslambda.LambdaFunction(
            file_name='create_thinga_majig',
            package_dir="lambdas",
            config=node6
        ))


        :type config: dict to use this you must first use chain.add(LambdaConfiguration)
        :type file_name: basestring if omitted,
        :type package_dir: basestring path to file. Omit extension.
        :type environment: codebuild.Environment
        """
        step.Step.__init__(self)
        self.config = config
        self.package_dir = normalize_dir(package_dir)

        self.file_name = file_name
        self.code_function = code_function
        self.function_name = function_name

    def handle(self, chain_context):
        """
        :type chain_context: chaincontext.ChainContext
        """
        t = chain_context.template

        t.add_transform('AWS::Serverless-2016-10-31')

        # TODO: review, should this be set or should we force it?
        default_config = {
            "Runtime": "nodejsj6.10",
            "MemorySize": 128,
            "Timeout": 30,
        }

        # Create the name if it's not supplied, using the filename, but CamelCase it
        function_name = self.function_name if self.function_name \
            else underscore_to_camelcase(self.file_name)

        # Use injected config, otherwise use this default.
        config = self.config if self.config \
            else default_config

        the_function = troposphere.serverless.FunctionForPackaging(
            title=function_name,
            FunctionName=function_name,
            Handler="%s%s.%s" % (self.package_dir, self.file_name, self.code_function),
            **config
        )

        t.add_resource(the_function)


def underscore_to_camelcase(value):
    def camelcase():
        # yield str.lower
        while True:
            yield str.capitalize

    c = camelcase()
    return "".join(c.next()(x) if x else '_' for x in value.split("_"))


def normalize_dir(package_dir):

    if not package_dir:
        # don't append slash if package dir is empty
        return package_dir
    elif not package_dir.endswith('/'):
        return package_dir + '/'
    else:
        return package_dir
