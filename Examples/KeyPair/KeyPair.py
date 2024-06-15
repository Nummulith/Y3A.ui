def KeyPair(aws, param):
    return aws.EC2_KeyPair.create(param, f'./PublicKeys/{param}.pem')

def clean(aws, param, result):
    aws.EC2_KeyPair.delete(result, f'./PublicKeys/{param}.pem')
