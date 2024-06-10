def params(param):
    ty = type(param)
    if ty is dict or ty is tuple:
        return param
    else: # if ty is str:
        params = param.split(",")
        if   len(params) == 0:
            return "test", "VPC", None
        elif len(params) == 1:
            return param, "VPC", None
        elif len(params) == 2:
            return params[0], params[1], None
        else:
            return params # ?

def CloudFormation(aws, param):
    stack, yaml, stack_param = params(param)

    with open(f"./Examples/CloudFormation/{yaml}.yaml", 'r') as file: yaml = file.read()

    aws.CloudFormation_Stack.create(stack, yaml, stack_param)

def update(aws, param):
    stack, yaml, stack_param = params(param)

    with open(f"./Examples/CloudFormation/{yaml}.yaml", 'r') as file: yaml = file.read()

    aws.CloudFormation_Stack.Class.update(stack, yaml, stack_param)

def clean(aws, param):
    stack, yaml, stack_param = params(param)

    aws.CloudFormation_Stack.delete(stack)
