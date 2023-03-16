from collections import OrderedDict
from os import getenv

import boto3

from taskbox.utils.tools import LOG


# https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs.html
class TaskLog(OrderedDict):
    '''The log of a single task'''

    client = boto3.client('logs')

    def __init__(self, *args, **kwargs) -> None:
        '''
        :params log_inst: Dict({
                          <req_id>:{'logStreamName': <logStreamName>.
                                    'startTime':<>,
                                    'endTime':<>}
                      }),
                      TODO 这里不确定 loads dumps 是否会改变顺序
        }
        '''
        super().__init__(*args, **kwargs)

    def get_log_event_by_reqid(self, req_id):
        '''Get log events(details) by req_id

        :params req_id: str, the aws_request_id in context
            237f0819-4b3b-4973-9585-af2e884fe1a9
        :return events: [{'timestamp': 1675586561742, 'message':''},]
        '''
        if req_id not in self:
            raise ValueError(f'Can\'t find logs by req_id: {req_id}')

        log_info = self.get(req_id)
        assert(isinstance(log_info, dict))

        LOG.debug(f'Try get log info of: {log_info}')
        response = self.client.get_log_events(
            logGroupName=getenv('LOG_GROUP'),
            logStreamName=log_info.get('logStreamName'),
            startTime=log_info.get('startTime'),
            endTime=log_info.get('endTime'),
        )
        return response.get('events')

    def append(self, item: dict):
        pass
