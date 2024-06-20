def update(aws, param, result):
    func = aws.Lambda_Function.fetch(param["Name"])[0]
    res = func.invoke(param["Parameter"])
    return res
