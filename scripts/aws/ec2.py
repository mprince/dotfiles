import boto3
from argparse import ArgumentDefaultsHelpFormatter, ArgumentParser


def get_args():
    parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument('name', help='Name of the instances looking for')
    parser.add_argument('--file', help='Path of file you want to save the private instances ip')
    return parser.parse_args()


def get_client():
    return boto3.resource('ec2', region_name='us-west-2')


def get_instances(name):
    ec2 = get_client()
    instances = ec2.instances.filter(Filters=[
        {'Name': 'tag:Name', 'Values': [name]},
        {'Name': 'instance-state-name', 'Values': ['running']}
    ])
    return instances


def get_private_ips():
    args = get_args()
    instances = get_instances()
    if args.file:
        with open(args.file, 'w')as instances_list_file:
            for instance in instances:
                instances_list_file.write('ec2-user@' + instance.private_ip_address + '\n')


def edit_tags(name, value):
    get_args()
    ec2 = get_client()
    """ :type: pyboto3.ec2 """
    instances = get_instances(name)
    for instance in instances:
        ec2.create_tags(DryRun=False, Resources=[instance.id], Tags=[{'Key': 'Product', 'Value': value}])


if __name__ == '__main__':
    ec2_resource = boto3.resource('ec2', region_name='us-west-2')
    instances = list(ec2_resource.instances.filter(Filters=[{'Name': 'instance-state-name', 'Values': ['running']}]))
    instances_names = []
    for instance in instances:
        for tag in instance.tags:
            if tag['Key'] == 'Name' and 'String to search for' in tag['Value']:
                instances_names.append(tag['Value'])
    clusters = set(instances_names)
    for cluster in clusters:
        print(cluster.split(' - ')[0])
