from collections import deque
from os import getenv

import boto3


# https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs.html
class TaskLog:
    '''The log of a single task'''

    client = boto3.client('logs')

    def __init__(self, task_propety) -> None:
        '''task_propety: {result:xxx, exec_log: queue[stream_id ...],}'''
        tmp = task_propety.get('log_streams')
        self.stream_q = deque(tmp, maxlen=30) if tmp else deque(tmp, maxlen=30)

    def get_latest_log_event(self):
        if not self.stream_q:
            return None
        return self.client.self.client.get_log_events(
            logGroupName=getenv('LOG_GROUP'),
            logStreamName=self.stream_q[-1],
        )

    def get_log_event_by_stream(self, stream):
        response = self.client.get_log_events(
            logGroupName=getenv('LOG_GROUP'),
            logStreamName=stream,
        )
        return response

    def append(self, stream_id):
        self.stream_q.append(stream_id)
