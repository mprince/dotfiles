from argparse import ArgumentDefaultsHelpFormatter, ArgumentParser
from boto3 import client


def get_args():
    parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument('--region', default='us-east-1')
    parser.add_argument('--dry-run', action='store_true')
    return parser.parse_args()


def get_instances_with_name_and_private_ip():
    ec2_volatile_instances = ['Agent-ciq', 'Agent-ci', 'Packer Builder', 'sit_tool']
    args = get_args()
    ec2_client = client(service_name='ec2', region_name=args.region)
    # filters = [{'Name': 'route.instance-id', 'Values': [args.old_instance_id]}]
    filters = []
    instances = ec2_client.describe_instances(Filters=filters)
    with open("/Users/mprince/.ssh/config", "w") as f:
        for reservation in instances['Reservations']:
            for instance in reservation['Instances']:
                if 'Tags' in instance and 'PrivateIpAddress' in instance:
                    for tag in instance['Tags']:
                        if 'Key' in tag and tag['Key'] == 'Name' and tag['Value'] not in ec2_volatile_instances:
                            f.write("Host {0}\n    Hostname {1}\n".format(tag['Value'], instance['PrivateIpAddress']))


def get_ec2_waiters():
    ec2_client = client(service_name='ec2')
    print "ec2 waiters:"
    print ec2_client.waiter_names


if __name__ == '__main__':
    get_ec2_waiters()
