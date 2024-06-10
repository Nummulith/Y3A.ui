def API(aws, param):
    print("((( --- API")

    with open("./Y3A/Examples/API/API.yaml", 'r') as file: yaml = file.read()
    aws.CloudFormation_Stack.create(param, yaml) # , {'Name': param}

    print("--- )))")

    update(aws)


def uploadfile(aws, param):
    bucket_name = param + ".cctstudents.com"
    file_path = './Y3A/Examples/API/index.html'
    s3_key = 'index.html'

    aws.S3_Bucket.Class.upload_file(bucket_name, s3_key, file_path)
    aws.S3_Bucket.Class.put_object_acl(bucket_name, s3_key, 'public-read')


def update(aws, param):
    print("((( --- update")

    with open("./Y3A/Examples/API/lambda.py", 'r') as file: Code = file.read()
    aws.Lambda_Function.Class.update_code(param, Code)

    uploadfile(aws, param)

    print("--- )))")


def clean(aws, param):
    print("((( --- clean")

    aws.S3_Bucket.Class.clear_bucket(f"{param}.cctstudents.com")
    aws.CloudFormation_Stack.delete(param)

    print("--- )))")
