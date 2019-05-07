import boto3
import unittest


class Test(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None
        pass

    def filter_name(self, name):
        return [
            {'Name': 'tag:Name', 'Values': [name]}
        ]

    def test_route_tables_equality(self):
        ec2_client = boto3.client('ec2')
        original = sorted(ec2_client.describe_route_tables(
            Filters=self.filter_name('bigd_vpc_private_rt'))['RouteTables'][0]['Routes'])
        copy = sorted(ec2_client.describe_route_tables(
            Filters=self.filter_name('bigd_vpc_private_rt_azb'))['RouteTables'][0]['Routes'])
        for index, item in enumerate(original):
            if index != 1:
                self.assertEqual(copy[index], original[index])
