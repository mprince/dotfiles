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


def filter_rds_db_security_groups(nat_instance_eip, region):
    rds_client = boto3.client('rds', region_name=region)
    """ :type: pyboto3.rds """
    filters = aws_filter('ip-permission.cidr', nat_instance_eip)
    db_security_groups = rds_client.describe_db_security_groups(Filters=filters)['DBSecurityGroups']
    rds_security_groups = []
    for security_group in db_security_groups:
        for ip in security_group['IPRanges']:
            if ip['CIDRIP'] == nat_instance_eip and ip['Status'] == 'authorized':
                rds_security_groups.append(security_group)
    # for security_group in rds_security_groups:
    #     try:
    #         rds_client.authorize_db_security_group_ingress(DBSecurityGroupName=security_group['DBSecurityGroupName'],
    #                                                        CIDRIP='')
    #     except ClientError as error:
    #         print error
    return rds_security_groups


def get_rds():
    result = []
    rds_client = boto3.client('rds')
    """ :type: pyboto3.rds"""
    rds_db_instances = rds_client.describe_db_instances()['DBInstances']
    for instance in rds_db_instances:
        for db_security_group in instance['DBSecurityGroups']:
            if '' == db_security_group['DBSecurityGroupName']:
                result.append(instance['DBInstanceIdentifier'])
    return result


if __name__ == '__main__':
    args = get_args()
    print(get_rds())
    # groups = filter_rds_db_security_groups(args.nat_instance_eip, args.region)
    # with open('groups.txt', 'w') as f:
    #     f.write(json.dumps(groups, indent=2, sort_keys=True))
