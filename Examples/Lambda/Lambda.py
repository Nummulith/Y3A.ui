def Lambda(aws, param):
    role = aws.IAM_Role.fetch(param["Role"])[0]

    with open(param["CodePath"], 'r') as file: Code = file.read()
    return aws.Lambda_Function.create(param["Name"], Code, role["Arn"])
    
def update(aws, param, result):
    with open(param["CodePath"], 'r') as file: Code = file.read()

    func = aws.Lambda_Function.fetch(param["Name"])[0]
    func.update_code(Code)

def clean(aws, param, result):
    aws.Lambda_Function.delete(param["Name"])
