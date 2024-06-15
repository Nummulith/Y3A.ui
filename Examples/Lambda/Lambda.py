def Lambda(aws, param):
    with open(param["CodePath"], 'r') as file: Code = file.read()
    return aws.Lambda_Function.create(param["Name"], Code, param["Role"])
    
def update(aws, param, result):
    with open(param["CodePath"], 'r') as file: Code = file.read()
    aws.Lambda_Function.Class.update_code(param["Name"], Code)

def clean(aws, param, result):
    aws.Lambda_Function.delete(param["Name"])
