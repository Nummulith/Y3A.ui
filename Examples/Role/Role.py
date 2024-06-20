def Role(aws, param):
    return aws.IAM_Role.create(param["Name"])

def clean(aws, param, result):
    aws.IAM_Role.delete(param["Name"])
