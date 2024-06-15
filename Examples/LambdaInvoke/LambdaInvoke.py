    # Lambda = "demo0"
    # Role = "arn:aws:iam::047989593255:role/service-role/tomasz-api-hello-world-role-53pra235"
    # payload = {
    #     "key1": "value1",
    #     "key2": "value2"
    # }
    # "./Examples/Lambda/initial.py"

def update(aws, param):
    res = aws.Lambda_Function.Class.invoke(param["Name"], param["PayLoad"])
    return res
