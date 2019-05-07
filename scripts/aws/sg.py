import boto3
import json
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from botocore.exceptions import ClientError


def aws_filter(name, values):
    return [
        {'Name': name, 'Values': [values]}
    ]


def get_args():
    parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument('--description', help='Description for security group rule')
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--nat-instance-eip', help='Elastic IP of current NAT instance')
    parser.add_argument('--region', help='AWS region', default='us-west-2')
    return parser.parse_args()


def filter_security_groups_with_nat_eip(nat_instance_eip, region):
    ec2_client = boto3.client('ec2', region_name=region)
    regions = ec2_client.describe_regions()['Regions']
    # Region Format
    # regions = [
    #     {
    #         'Endpoint': 'ec2.us-west-2.amazonaws.com',
    #         'RegionName': 'us-west-2'
    #     }
    # ]
    result = []
    try:
        for region in regions:
            ec2_region = boto3.client('ec2', region_name=region['RegionName'])
            filters = aws_filter('ip-permission.cidr', nat_instance_eip)
            result += ec2_region.describe_security_groups(Filters=filters)['SecurityGroups']
    except ClientError as error:
        print(error)

    return result


def add_description_to_security_rule(description, nat_instance_eip, region, groups):
    ec2_client = boto3.client('ec2', region_name=region)
    ip_permission = [
        {
            'IpProtocol': 'tcp',
            'IpRanges': [
                {
                    'CidrIp': nat_instance_eip,
                    'Description': description
                }
            ]
        }
    ]
    for group in groups:
        ec2_client.update_security_group_rule_descriptions_ingress(GroupName=group['GroupName'],
                                                                   IpPermissions=ip_permission)


def add_ingress_rule_to_security_group():
    args = get_args()
    eip_cidr = args.nat_instance_eip + '/32'
    ec2_client = boto3.client('ec2')
    # regions = ec2_client.describe_regions()['Regions']
    regions = [
        {
            'Endpoint': 'ec2.us-west-2.amazonaws.com',
            'RegionName': 'us-west-2'
        }
    ]
    try:
        for region in regions:
            ec2_region = boto3.client('ec2', region_name=region['RegionName'])
            filters = aws_filter('ip-permission.cidr', eip_cidr)
            security_groups = ec2_region.describe_security_groups(Filters=filters)['SecurityGroups']
            for security_group in security_groups:
                ip_permissions = [
                    {
                        'FromPort': 0,
                        'IpProtocol': 'tcp',
                        'IpRanges': [
                            {
                                'CidrIp': '',
                                'Description': 'NAT Gateway EIP az-a'
                            },
                            {
                                'CidrIp': '',
                                'Description': 'NAT Gateway EIP az-b'
                            },
                            {
                                'CidrIp': '',
                                'Description': 'NAT Gateway EIP az-c'
                            }
                        ],
                        'ToPort': 65535
                    },
                ]
                try:
                    ec2_client.authorize_security_group_ingress(GroupId=security_group['GroupId'],
                                                                IpPermissions=ip_permissions,
                                                                DryRun=args.dry_run)
                except ClientError as error:
                    if error.response['Error']['Code'] == "InvalidPermission.Duplicate":
                        continue
                    else:
                        print(error)
    except ClientError as error:
        print(error)


if __name__ == '__main__':
    args = get_args()
    groups = filter_security_groups_with_nat_eip(args.nat_instance_eip, args.region)
    with open('groups.txt', 'w') as f:
        f.write(json.dumps(groups, indent=2, sort_keys=True))
    # add_description_to_security_rule(args.description, args.nat_instance_eip, args.region, security_groups)
