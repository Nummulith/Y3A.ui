# from Y3A.awsClasses import PAR, bt
# import requests

def Test2(aws, param):
    url = "http://18.192.62.22/"
    response = requests.get(url)

    if response.status_code == 200:
        html_content = response.text
        print(html_content)
    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")

def Test3(aws, param):
    print("(---")

    aws.save()

    # objs = aws.EC2_SecurityGroup.fetch("sg-031f7e69b595ae094", None, True)
    
    # objs = aws.EC2_SecurityGroup_Rule.fetch(None, None, True)
    objs = aws.EC2_SecurityGroup_Rule.objects()

    for grr in objs:
        if not grr.IsEgress and grr.IpProtocol == "tcp" and grr.FromPort == 80:
            print(f"{grr.GroupId} \\ {grr.IsEgress} {grr.IpProtocol} / {grr.FromPort} -> {grr.ToPort}")
            sg = grr['GroupId']
        else:
            aws.EC2_SecurityGroup_Rule.release(grr.get_id())

    # key_pair_name = "Pavel"

    # objs = aws.EC2_KeyPair.fetch(
    #     filter = {"KeyNames" : (["key-" + key_pair_name], PAR.PAR)},
    #     create_par = {"name": key_pair_name}
    # )
    objs = aws.EC2_KeyPair.objects()

    for obj in objs:
        print(f"{obj.KeyPairId} - {obj.KeyName}")

    # objs = aws.EC2_Instance.fetch(
    #     {"instance-state-name" : (['running'], PAR.FILTER)}
    # )
    # objs = aws.EC2_Instance.fetch({"key-name" : ([key_pair_name], PAR.FILTER)})
    objs = aws.EC2_Instance.fetch("i-0091b120c539d10e8")
    # objs = aws.EC2_Instance.objects()

    # for obj in objs:
    #     cur_key_pair_name = obj["KeyPairId"].KeyName if hasattr(obj, "KeyPairId") else "-"
    #     print(f"{obj.Tag_Name} : {cur_key_pair_name} - {obj.PublicIpAddress}")

    print("---)")

def Test4(aws, param):
    print("(---")

    objs = aws.EC2_SecurityGroup.fetch(None, None, True)
    for obj in objs:
        ec2 = obj["_parent"]
        sg  = obj["GroupId"]
        sgrs = aws.EC2_SecurityGroup_Rule.fetch(f"{obj.GroupId}|*", None, True)

        for sgr in sgrs:
            if sgr.FromPort != 80:
                continue
            
            print(f"{ec2.InstanceId} - {getattr(ec2, "PublicIpAddress", "x")} - {ec2.Tag_Name} - {sg.VpcId} - {obj.GroupName} - {sgr.FromPort}")

    print("---)")

def Test5(aws, param):
    print("(---")

    objs = aws.AWS_AvailabilityZone.fetch()
    for obj in objs:
        print(f"{obj.ZoneId} - {obj.ZoneName}")
    

    objs = aws.EC2_Subnet.fetch(None, None, True)
    for obj in objs:
        print(f"{obj} - {obj}")

    print("---)")

def Test(aws, param):
    print("(---")

    # objs = aws.CloudFormation_Stack.fetch()
    # for obj in objs:
    #     print(f"{obj}")

    aws.print()

    print("---)")



    # aws.SNS_Topic.create(Name)
