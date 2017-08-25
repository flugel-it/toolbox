#!/usr/bin/env python

import boto3
import sys
import yaml

zone_id = sys.argv[1]
zone_alias = sys.argv[2]

client = boto3.client('route53')
r = client.list_resource_record_sets(HostedZoneId=zone_id)

record_template = """  %(rname)sDNSRecord:
    Type: AWS::Route53::RecordSet
    Properties:
      HostedZoneId: !Ref %(zone_alias)s
      Name: %(name)s
      Type: %(type)s
      TTL: '%(ttl)s'
      ResourceRecords:
      - %(value)s"""

for i in r['ResourceRecordSets']:
    if i["Type"] not in [ "A", "CNAME" ]:
        continue

    print record_template % {
            "zone_alias": zone_alias,
            "rname": i["Name"].split('.')[0].capitalize(),
            "name": i["Name"],
            "type": i["Type"],
            "ttl": i["TTL"],
            "value": i["ResourceRecords"][0]["Value"]
            }

