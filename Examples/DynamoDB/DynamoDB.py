def DynamoDB_Table(aws, param):
    aws.DynamoDB_Table.fetch()

    aws.DynamoDB_Table.create(f"DB-{param}")

def clean(aws, param):
    aws.DynamoDB_Table.delete(f"DB-{param}")
