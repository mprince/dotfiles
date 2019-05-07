import boto3
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from botocore.exceptions import ClientError


def aws_filter(name, values):
    return [
        {'Name': name, 'Values': [values]}
    ]


def aws_tag(name, value):
    return [
        {'Key': name, 'Value': value}
    ]


def get_args():
    parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument('--nat-instance-eip', help="Elastic IP of current NAT instance")
    parser.add_argument('--dry-run', action='store_true')
    return parser.parse_args()


def copy_route_table(original_name, copy_name):
    """
    Method that allows to duplicate a route table with the same routes

    :param original_name: Name of the route table to duplicate
    :param copy_name: Name of targeted route table
    :return:
    """
    ec2_client = boto3.client('ec2')
    filter_original_route_table = aws_filter('tag:Name', original_name)
    tags_copy_route_table = aws_tag('Name', copy_name)
    route_table_original = ec2_client.describe_route_tables(Filters=filter_original_route_table)['RouteTables'][0]
    routes_to_duplicate = route_table_original['Routes']
    route_table_copy = ec2_client.create_route_table(VpcId=route_table_original['VpcId'])['RouteTable']
    route_table_id_copy = route_table_copy['RouteTableId']
    ec2_client.create_tags(Resources=[route_table_id_copy], Tags=tags_copy_route_table)
    for route in routes_to_duplicate:
        try:
            if 'DestinationPrefixListId' in route:
                ec2_client.modify_vpc_endpoint(
                    VpcEndpointId=route['GatewayId'],
                    AddRouteTableIds=[
                        route_table_id_copy
                    ]
                )
            elif 'GatewayId' in route and route['GatewayId'] != 'local':
                ec2_client.create_route(
                    RouteTableId=route_table_id_copy,
                    DestinationCidrBlock=route['DestinationCidrBlock'],
                    DryRun=False,
                    GatewayId=route['GatewayId']
                )
            elif 'VpcPeeringConnectionId' in route:
                ec2_client.create_route(
                    RouteTableId=route_table_id_copy,
                    DestinationCidrBlock=route['DestinationCidrBlock'],
                    DryRun=False,
                    VpcPeeringConnectionId=route['VpcPeeringConnectionId']
                )
            elif 'NatGatewayId' in route:
                ec2_client.create_route(
                    RouteTableId=route_table_id_copy,
                    DestinationCidrBlock=route['DestinationCidrBlock'],
                    DryRun=False,
                    NatGatewayId=route['NatGatewayId']
                )
        except ClientError as error:
            print(error)


def switch_to_nat(route_changes, dry_run):
    ec2_client = boto3.client('ec2')
    for route_table_id, interface in route_changes.iteritems():
        try:
            if interface[0:3] == 'nat':
                ec2_client.replace_route(
                    DestinationCidrBlock='0.0.0.0/0',
                    RouteTableId=route_table_id,
                    DryRun=dry_run,
                    NatGatewayId=interface,
                )
            elif interface[0:3] == 'eni':
                ec2_client.replace_route(
                    DestinationCidrBlock='0.0.0.0/0',
                    RouteTableId=route_table_id,
                    DryRun=dry_run,
                    NetworkInterfaceId=interface,
                )
        except ClientError as err:
            print(err)


if __name__ == '__main__':
    print("Nothing to see here!")
    deploy = {
        'rtb-': 'nat-'
    }
    rollback = {
        'rtb-': 'eni-'
    }
    switch_to_nat(deploy, True)
