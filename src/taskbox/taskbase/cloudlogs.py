from collections import deque
from os import getenv
import time

import boto3

from taskbox.utils.tools import LOG


# https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs.html
class TaskLog:
    '''The log of a single task'''

    client = boto3.client('logs')

    def __init__(self, task_propety) -> None:
        '''task_propety: {result:xxx, exec_log: queue[stream_id ...],}'''
        tmp = task_propety.get('log_streams')
        self.stream_q = deque(tmp, maxlen=30) if tmp else deque(maxlen=30)

    def get_latest_log_event_format(self):
        if not self.stream_q:
            return None
        event = self.client.get_log_events(
            logGroupName=getenv('LOG_GROUP'),
            logStreamName=self.stream_q[-1],
        ).get('events', [])

        return self.adapter_log_events_for_display(event)

    def get_log_event_by_stream(self, stream_id):
        '''Get log events(details) by stream_id

        :params stream_id: str,
            2023/02/05/[$LATEST]ec5960da2dce42ed8cc8f85dd7c7eb27
        :return events: [{'timestamp': 1675586561742, 'message':''},]
        '''
        response = self.client.get_log_events(
            logGroupName=getenv('LOG_GROUP'),
            logStreamName=stream_id,
        )
        return response.get('events')

    def append(self, stream_id):
        if not self.stream_q:
            self.stream_q.append(stream_id)
        elif self.stream_q[-1] != stream_id:
            self.stream_q.append(stream_id)

    @staticmethod
    def adapter_log_events_for_display(log_events: list):
        def format_time(time_str):
            return time.strftime('%Y-%m-%d %H:%M:%S',
                                 time.localtime(time_str))

        res = []
        for d in log_events:
            tmp = {}
            tmp['timestamp'] = format_time(d['timestamp'])
            tmp['message'] = \
                d['message'].replace('\t', ' ').strip('\n')
            res.append(tmp)

        return res

    def __iter__(self):
        for i in self.stream_q:
            yield i

    def __getitem__(self, index):
        return self.stream_q[index]
