# -*- coding: utf-8 -*-

"""Classes for Route 53 domain."""

import uuid



class DomainManager:
    """Manage a Route 53 domains."""

    def __init__(self, session):
        """Create a DOMAIN object."""
        self.session = session
        self.client = self.session.client('route53')

# kittenweb.miludigital.com
# subdomain.kittenweb.miludigital.com
    def find_hosted_zone(self, domain_name):
        """Find hosted zone for domain."""
        paginator = self.client.get_paginator('list_hosted_zones')
        for page in paginator.paginate():
            for zone in page['HostedZones']:
                if domain_name.endswith(zone['Name'][:-1]):
                    return zone

        return None

# domain_name = 'subdomain.kettentest.miludigital.com'
# zone_name = 'miludigital.com.'
    def create_hosted_zone(self, domain_name):
        """Crate hosted zone for domain."""
        zone_name = '.'.join(domain_name.split('.')[-2:]) + '.'
        self.client.create_hosted_zone(
            Name=zone_name,
            CallerReference=str(uuid.uuid4())
        )

    def create_s3_domain_record(self, zone, domain_name, endpoint):
        """Create route 53 record set for domain."""
        return self.client.change_resource_record_sets(
            HostedZoneId=zone['Id'],
            ChangeBatch={
                'Comment': 'Created by webotron',
                'Changes': [
                    {
                        'Action': 'UPSERT',
                        'ResourceRecordSet': {
                            'Name': domain_name,
                            'Type': 'A',
                            'AliasTarget': {
                                'HostedZoneId': endpoint.zone,
                                'DNSName': endpoint.host,
                                'EvaluateTargetHealth': False
                            }

                        }
                    }
                ]
            }
        )

    def create_cf_domain_record(self, zone, domain_name, cf_domain):
        """Create a domain record in zone for domain_name."""
        return self.client.change_resource_record_sets(
            HostedZoneId=zone['Id'],
            ChangeBatch={
                'Comment': 'Created by webotron',
                'Changes': [
                    {
                        'Action': 'UPSERT',
                        'ResourceRecordSet': {
                            'Name': domain_name,
                            'Type': 'A',
                            'AliasTarget': {
                                'HostedZoneId': 'Z2FDTNDATAQYW2', #hard coded for cloudfront
                                'DNSName': cf_domain,
                                'EvaluateTargetHealth': False
                            }

                        }
                    }
                ]
            }
        )
