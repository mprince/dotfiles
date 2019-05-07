import boto3


def get_dynamodb_storage_cost():
    dynamodb = boto3.client('dynamodb', region_name='us-west-2')
    """ :type: pyboto3.dynamodb """
    table_names = dynamodb.list_tables()['TableNames']
    total = 0
    for table_name in table_names:
        total += dynamodb.describe_table(TableName=table_name)['Table']['TableSizeBytes']
    print (total - 25000000000) * 0.25 / 1000000000


def get_global_tables():
    dynamodb = boto3.client('dynamodb', region_name='us-west-2')
    global_tables = dynamodb.list_global_tables()
    print global_tables


if __name__ == '__main__':
    get_dynamodb_storage_cost()
