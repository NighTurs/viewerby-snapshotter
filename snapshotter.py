import argparse
import os
import sys
import datetime
import filecmp
import logging
from urllib.error import URLError
from urllib.request import urlopen
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger

URL = 'https://viewer.by/img/client/{}/1/view01.jpg'


def init_clients(clients):
    for client in clients:
        next_min_flag[client] = False
        try:
            os.stat(client)
        except:
            os.mkdir(client)


def snapshot_clients(clients):
    for client in clients:
        dt = datetime.datetime.now()

        if client in prev_snapshot_time and next_min_flag[client] and prev_snapshot_time[client].minute == dt.minute:
            logger.info('Skipped snapshot, client={}, prev_snapshot_time={}, next_min_flag={}'
                        .format(client, prev_snapshot_time.get(client), next_min_flag.get(client)))
            continue

        file_path = '{}/{}.jpg'.format(client, dt.strftime('%Y%m%d%H%M%S'))

        request = urlopen(URL.format(client), timeout=30)
        with open(file_path, 'wb') as f:
            try:
                f.write(request.read())
            except URLError as e:
                print('Failed to get snapshot, client={}, prev_snapshot_time={}, reason={}'
                      .format(client, prev_snapshot_time.get(client), e.reason))

        if client in prev_snapshot and filecmp.cmp(file_path, prev_snapshot[client]):
            next_min_flag[client] = False
            os.remove(file_path)
            logger.info('Duplicate snapshot, client={}, prev_snapshot_time={}, cur_snapshot_time={}'
                        .format(client, prev_snapshot_time.get(client), dt))
            continue

        next_min_flag[client] = True
        prev_snapshot[client] = file_path
        logger.info('New snapshot, client={}, prev_snapshot_time={}, cur_snapshot_time={}'
                    .format(client, prev_snapshot_time.get(client), dt))
        prev_snapshot_time[client] = dt


def setup_logger():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    return logger


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--clients', nargs='+', default=[126, 127], required=False, help='List of client to snapshot')
    args = parser.parse_args()

    logger = setup_logger()

    prev_snapshot = {}
    prev_snapshot_time = {}
    next_min_flag = {}
    init_clients(args.clients)

    scheduler = BlockingScheduler()
    scheduler.add_job(snapshot_clients, trigger=CronTrigger(second='*/15'), args=[args.clients], max_instances=1,
                      misfire_grace_time=30)
    scheduler.start()
