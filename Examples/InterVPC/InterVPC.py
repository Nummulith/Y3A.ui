import importlib

def example(aws, module_name, function_name = None, param = None):
    """ 'Example' run """

    if function_name == None:
        function_name = module_name

    try:
        module = importlib.import_module(f"Examples." + module_name + "." + module_name)
        importlib.reload(module)

        func = getattr(module, function_name)
        func(aws, param)
                
    except Exception as e:
        print(f"Example: An exception occurred: {type(e).__name__} - {e}")

def fetch_cf_res_list(aws, stack):
    do_auto_save_after = aws.do_auto_save
    aws.do_auto_save = False

    result = []
    for res in aws.CloudFormation_StackResource.fetch(f"{stack}|*"):
        if res.ResourceType == None:
            continue
        try: # to do ..
            result.append(aws[res.ResourceType].fetch(res.PhysicalResourceId)[0])
        except Exception as e:
            print(f"Cannot get object: {res.ResourceType} - {res.PhysicalResourceId} - {e}")

    aws.save()
    aws.do_auto_save = do_auto_save_after

    return result

def release_cf_res_list(aws, stack):
    return aws.CloudFormation_StackResource.release(f"{stack}|*")

def is_vpc(aws, res, par):
    return type(res) == aws.EC2_VPC.Class

def is_sg(aws, res, par):
    return type(res) == aws.EC2_SecurityGroup.Class

def is_sn(aws, res, par):
    return type(res) == aws.EC2_Subnet.Class and res["Tag_Name"] == par

def get_cf_res(aws, listname, criteria, par = None) -> str:
    list = listname
    if type(list) is str:
        list = fetch_cf_res_list(aws, list)

    for res in list:
        if criteria(aws, res, par):
            return res
    return None


def InterVPC(aws, param):
    print("( creating ---")


    keyid = aws.EC2_KeyPair.create(param, f'./PublicKeys/{param}.pem')
    print(f"Key = {key}")


    stack = f"{param}0"
    example(aws, "CloudFormation", None, (stack, "TwoTier", {"CidrPrefix": "10.0"}))
    list = fetch_cf_res_list(aws, stack)
    Vpc0 = get_cf_res(aws, list, is_vpc)
    sg   = get_cf_res(aws, list, is_sg)
    snPr = get_cf_res(aws, list, is_sn, "Private SN")

    ec20 = aws.EC2_Instance.create(stack,
        aws.Const["EC2.ImageId.Linux"], aws.Const["EC2.InstanceType"],
        keyid, snPr.get_id(), [sg.get_id()], "10.0.1.8", aws.Const["EC2.UserData.Apache"],
    )


    stack = f"{param}1"
    example(aws, "CloudFormation", None, (stack, "TwoTier", {"CidrPrefix": "11.0"}))
    list = fetch_cf_res_list(aws, stack)
    Vpc1 = get_cf_res(aws, list, is_vpc)
    sg   = get_cf_res(aws, list, is_sg)
    snPr = get_cf_res(aws, list, is_sn, "Private SN")

    ec20 = aws.EC2_Instance.create(stack,
        aws.Const["EC2.ImageId.Linux"], aws.Const["EC2.InstanceType"],
        keyid, snPr.get_id(), [sg.get_id()], "10.0.1.9", aws.Const["EC2.UserData.Apache"],
    )


    aws.EC2_VPCPeeringConnection.create(Vpc0.get_id(), Vpc1.get_id(), param)


    print("---)")


def update(aws, param):
    print("( upading ---")

    keyid = aws.EC2_KeyPair.Class.NameToId(param)
    print(f"Key = {keyid}")
    # aws.EC2_KeyPair.fetch(keyid)


    stack = f"{param}0"
    # example(aws, "CloudFormation", "update", (stack, "TwoTier", {"CidrPrefix": "10.0"}))
    # aws.CloudFormation_Stack.fetch(stack)
    # list = fetch_cf_res_list(aws, stack)
    # Vpc0 = get_cf_res(aws, list, is_vpc)
    # sg   = get_cf_res(aws, list, is_sg)
    
    # snPr = get_cf_res(aws, list, is_sn, "Private SN")

    # ec20 = aws.EC2_Instance.create(f"{stack} - Private SN",
    #     aws.Const["EC2.ImageId.Linux"], aws.Const["EC2.InstanceType"],
    #     keyid, snPr.get_id(), [sg.get_id()], "10.0.1.9", aws.Const["EC2.UserData.Apache"],
    # )

    # print(f"{stack}: vpc: {Vpc0.get_id()}, sg: {sg.get_id()}, sn: {snPr.get_id()}, ec2: {ec20}")

    # snPu = get_cf_res(aws, list, is_sn, "Public SN")
    # ec20 = aws.EC2_Instance.create(f"{stack} - Public SN",
    #     aws.Const["EC2.ImageId.Linux"], aws.Const["EC2.InstanceType"],
    #     keyid, snPu.get_id(), [sg.get_id()], "10.0.3.7", aws.Const["EC2.UserData.Apache"],
    # )

    # print(f"{stack}: vpc: {Vpc0.get_id()}, sg: {sg.get_id()}, sn: {snPu.get_id()}, ec2: {ec20}")


    stack = f"{param}1"
    # example(aws, "CloudFormation", "update", (stack, "TwoTier", {"CidrPrefix": "11.0"}))
    # aws.CloudFormation_Stack.fetch(stack)
    list = fetch_cf_res_list(aws, stack)
    Vpc1 = get_cf_res(aws, list, is_vpc)
    sg   = get_cf_res(aws, list, is_sg)

    # snPr = get_cf_res(aws, list, is_sn, "Private SN")
    # ec20 = aws.EC2_Instance.create(stack,
    #     aws.Const["EC2.ImageId.Linux"], aws.Const["EC2.InstanceType"],
    #     keyid, snPr.get_id(), [sg.get_id()], "11.0.1.8", aws.Const["EC2.UserData.Apache"],
    # )

    # print(f"{stack}: vpc: {Vpc1.get_id()}, sg: {sg.get_id()}, sn: {snPr.get_id()}, ec2: {ec20}")

    snPu = get_cf_res(aws, list, is_sn, "Public SN")
    ec20 = aws.EC2_Instance.create(f"{stack} - Public SN",
        aws.Const["EC2.ImageId.Linux"], aws.Const["EC2.InstanceType"],
        keyid, snPu.get_id(), [sg.get_id()], "11.0.3.7", aws.Const["EC2.UserData.Apache"],
    )

    print(f"{stack}: vpc: {Vpc1.get_id()}, sg: {sg.get_id()}, sn: {snPu.get_id()}, ec2: {ec20}")

    print("---)")


def clean(aws, param):
    print("( cleaning ---")

    Vpc0 = get_cf_res(aws, f"{param}0", is_vpc)
    Vpc1 = get_cf_res(aws, f"{param}1", is_vpc)

    peer_id = None
    for res in aws.EC2_VPCPeeringConnection.fetch():
        if res.AccepterVpc == Vpc0.get_id() and res.RequesterVpc == Vpc1.get_id():
            peer_id = res.VpcPeeringConnectionId
    aws.EC2_VPCPeeringConnection.delete(peer_id)

    stack = f"{param}0"
    # release_cf_res_list(aws, stack)
    example(aws, "CloudFormation", "clean", stack)

    stack = f"{param}1"
    # release_cf_res_list(aws, stack)
    example(aws, "CloudFormation", "clean", stack)

    keyid = aws.EC2_KeyPair.Class.NameToId(param)
    aws.EC2_KeyPair.delete(keyid)

    aws.release("ALL")

    print("---)")
