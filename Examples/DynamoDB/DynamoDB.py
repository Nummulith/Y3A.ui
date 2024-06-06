id = "DB-Pavel"

def DynamoDB_Table(aws, param):
    aws.DynamoDB_Table.fetch()

    aws.DynamoDB_Table.create(id)

def clean(aws, param):
    aws.DynamoDB_Table.delete(id)
