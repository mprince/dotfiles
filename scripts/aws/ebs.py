import boto3
import json


def get_client():
    return boto3.client('ec2')


def aws_filter(name, values):
    return [
        {'Name': name, 'Values': [values]}
    ]


def get_available_volumes():
    ec2_client = get_client()
    filters = aws_filter('status', 'available')
    return ec2_client.describe_volumes(Filters=filters)['Volumes']


def delete_volumes():
    with open("volumes.txt") as f:
        available_volumes_with_no_tags = f.read()
    volumes = json.loads(available_volumes_with_no_tags)
    ec2_client = get_client()
    for volume in volumes:
        volume_id = volume['Id']
        print("Deleting " + volume_id)
        ec2_client.delete_volume(VolumeId=volume_id, DryRun=True)


def aggregate_volumes():
    with open("stopped_instances_volumes.txt") as f:
        file_content = f.read()
    stopped_instances_volumes = json.loads(file_content)
    ec2_client = get_client()
    """ :type: pyboto3.ec2 """

    total = 0
    for volumes in stopped_instances_volumes:
        for volume in volumes['Volume']:
            real_volume = ec2_client.describe_volumes(VolumeIds=[volume['Ebs']['VolumeId']])
            total += real_volume['Volumes'][0]['Size']
    print total


if __name__ == '__main__':
    aggregate_volumes()
