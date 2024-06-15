def is_vpc(aws, res, par):
    return type(res) == aws.EC2_VPC.Class

def CF_VPCPeering(aws, param):
    list = aws.fetch_cf_res_list(f"{param}0")
    Vpc0 = aws.get_cf_res(list, is_vpc)

    list = aws.fetch_cf_res_list(f"{param}1")
    Vpc1 = aws.get_cf_res(list, is_vpc)

    vpcp = aws.EC2_VPCPeeringConnection.create(Vpc0.get_id(), Vpc1.get_id(), f"VPC peering - {param}")

    return vpcp

def clean(aws, param, result):
    aws.EC2_VPCPeeringConnection.delete(result)
