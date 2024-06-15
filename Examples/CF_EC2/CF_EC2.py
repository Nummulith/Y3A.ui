def is_vpc(aws, res, par):
    return type(res) == aws.EC2_VPC.Class

def is_sg(aws, res, par):
    return type(res) == aws.EC2_SecurityGroup.Class

def is_sn(aws, res, par):
    return type(res) == aws.EC2_Subnet.Class and res["Tag_Name"] == par

def CF_EC2(aws, param):
    keyid = aws.EC2_KeyPair.Class.NameToId(param["KeyPair"])
    
    list = aws.fetch_cf_res_list(param["Stack"])
    # Vpc0 = aws.get_cf_res(list, is_vpc)
    sg   = aws.get_cf_res(list, is_sg)
    snPr = aws.get_cf_res(list, is_sn, param["Subnet"])

    # print(f"EC2: sg:{sg.get_id()} ")

    ec20 = aws.EC2_Instance.create(f"EC2-{param["Stack"]}",
        aws.Const["EC2.ImageId.Linux"], aws.Const["EC2.InstanceType"],
        keyid, snPr.get_id(), [sg.get_id()], param["PrivateIp"], aws.Const["EC2.UserData.Apache"],
    )

    return ec20

def clean(aws, param, result):
    aws.EC2_Instance.delete(result)
