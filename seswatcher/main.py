#!/usr/bin/env python
import click
import boto3
import math
import time
from datetime import datetime, timezone


def send_statistics_aggregate(stats, time_window = 3600, max_bounces_rate = 0.04, max_complaints_rate = 0.0007):
    now = datetime.now(timezone.utc)
    total = {
        'DeliveryAttempts': 0,
        'Bounces': 0,
        'Complaints': 0,
        'Rejects': 0
    }

    for data_point in stats['SendDataPoints']:
        ts = data_point['Timestamp']
        diff = (now - data_point['Timestamp']).total_seconds()
        if diff < time_window:
            for key, value in data_point.items():
                if key != 'Timestamp':
                    total[key] = total[key] + value
    
    total['BouncesRate'] = total['Bounces'] / total['DeliveryAttempts'] if total['DeliveryAttempts'] else 0
    total['ComplaintsRate'] = total['Complaints'] / total['DeliveryAttempts'] if total['DeliveryAttempts'] else 0
    total['RejectsRate'] = total['Rejects'] / total['DeliveryAttempts'] if total['DeliveryAttempts'] else 0
    total['BounceNumToSend'] = calc_num_to_send(total['DeliveryAttempts'], total['Bounces'], max_bounces_rate)
    total['ComplaintNumToSend'] = calc_num_to_send(total['DeliveryAttempts'], total['Complaints'], max_complaints_rate)
    total['NumToSend'] = max(total['BounceNumToSend'], total['ComplaintNumToSend'])

    return total

def calc_num_to_send(delivery, error_num, rate):
    return max(0, math.ceil(error_num / rate - delivery))

@click.command()
@click.argument('access_key', required=1)
@click.argument('secret_key', required=1)
@click.argument('from_email', required=1)
@click.argument('to_email', required=1)
@click.option('--region', default='us-east-1', help='AWS SES Region (default is us-east-1)')
@click.option('--interval', default=3600, help='Timer interval')
def watch(access_key, secret_key, from_email, to_email, region, interval):
    client = boto3.client(
        'ses',
        region_name=region,
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key
    )
    
    stats_data = client.get_send_statistics()
    quota_data = client.get_send_quota()
    data = send_statistics_aggregate(stats_data, interval)
    remaining = num_to_send = data['NumToSend']
    # Half speed to avoid real emails would be rejected by rate limit
    send_rate = (int) (quota_data['MaxSendRate'] / 2)
    print(data)
    
    while remaining > 0:
        remaining = remaining - send_rate
        time1 = time.time()

        for i in range(0, send_rate):
            client.send_email(
                Source=from_email,
                Destination={
                    'ToAddresses': [to_email],
                },
                Message={
                    'Subject': {
                        'Data': 'Lorem Ipsum is simply dummy text',
                    },
                    'Body': {
                        'Text': {
                            'Data': 'Lorem Ipsum is simply dummy text of the printing and typesetting industry.'
                        },
                        'Html': {
                            'Data': '<p>Lorem Ipsum is simply dummy text of the printing and typesetting industry.</p>'
                        }
                    }
                }
            )
        print('Sent '+str(send_rate)+' emails.')
        time2 = time.time()
        wait_time = max(0, 1.2 - (time2 - time1))
        print('Wait '+str(wait_time)+' seconds.')
        time.sleep(wait_time)


if __name__ == '__main__':
    watch()
