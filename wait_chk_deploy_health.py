#!/usr/bin/env python

import boto3
import sys
import time

elb_name = sys.argv[1]
profile_name = None
try:
    profile_name = sys.argv[2]
except:
    pass


if profile_name:
    botosession = boto3.session.Session(profile_name=profile_name)
    client = botosession.client('elbv2', region_name='us-east-2')
else:
    client = boto3.client('elbv2')


def wait_for_status(target_group_arn, status, targets=None):
    """
    Assuming that we have to chk only one instance at a time.
    """
    polling_increment_secs = 5
    max_retries = 20
    status_achieved = True
    res = None

    for x in range(0, max_retries):
        # print "in loop"
        filt_dict = {"TargetGroupArn": target_group_arn}
        if targets:
            filt_dict['Targets'] = targets
        res = client.describe_target_health(
            **filt_dict
        )

        if not res['TargetHealthDescriptions']:
            return False
        # import ipdb;ipdb.set_trace();
        for tinst in res['TargetHealthDescriptions']:
            if tinst['TargetHealth']['State'] != status:
                if targets:
                    time.sleep(polling_increment_secs)
                else:
                    if not wait_for_status(target_group_arn, status, targets=[tinst['Target']]):
                        return False
                    else:
                        return True
            else:
                if targets:
                    return True
                tinst['now_healthy'] = True
                healthy_count = 0
                for tinst_temp in res['TargetHealthDescriptions']:
                    if tinst_temp.get('now_healthy'):
                        healthy_count += 1
                if healthy_count >= len(res['TargetHealthDescriptions']):
                    # print "all healthy"
                    return True

    return status_achieved


response = client.describe_target_groups(
    Names=[
        elb_name,
    ],
    PageSize=20
)

target_group_arn = response['TargetGroups'][0]['TargetGroupArn']
print(wait_for_status(target_group_arn, "healthy", targets=None))
