def is_vpc(aws, res, par):
    return type(res) == aws.EC2_VPC.Class

def is_rt(aws, res, par):
    return type(res) == aws.EC2_RouteTable.Class

def CF_VPCEndpoint(aws, param):
    list = aws.fetch_cf_res_list(param["Stack"])
    Vpc  = aws.get_cf_res(list, is_vpc)
    rt   = aws.get_cf_res(list, is_rt)

    return aws.EC2_VPCEndpoint.create(Vpc.get_id(), rt.get_id(), "Gateway", "arn:aws:s3:::pavel-endpoint")

def clean(aws, param):
    aws.EC2_VPCEndpoint.delete(param)
