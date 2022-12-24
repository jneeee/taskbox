import unittest
from unittest import mock

from taskbox.webx.object import Request


FAKE_EVENT = {
    'version': '2.0', 'routeKey': '$default', 'rawPath': '/cmd',
    'rawQueryString': '', 
    'cookies': ['uuid=465e50e8-f344-4009-af2b-c4eaafa7d9e8'], 
    'headers': {
        'accept': 'text/html', 'accept-encoding': 'gzip, deflate, br',
        'cache-control': 'max-age=0', 'content-length': '86',
        'content-type': 'application/x-www-form-urlencoded',
        'host': 'demo.taskbox.cn', 'origin': 'https://demo.taskbox.cn',
        'referer': 'https://demo.taskbox.cn/cmd',
        'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108","Microsoft Edge";v="108"',
        'sec-ch-ua-mobile': '?0', 'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document', 'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin', 'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.54',
        'x-amzn-trace-id': 'Root=1-63a65ac0-232f5asd387d5df61d75fa7a',
        'x-forwarded-for': '58.247.232.192', 'x-forwarded-port': '443',
        'x-forwarded-proto': 'https'},
    'requestContext': {
        'accountId': '123456789','apiId': 'csm5rlhe6d',
        'domainName': 'demo.taskbox.cn', 'domainPrefix': 'demo',
        'http': {
            'method': 'POST', 'path': '/cmd', 'protocol': 'HTTP/1.1',
            'sourceIp': '58.247.232.192', 
            'userAgent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.54'
        },
        'requestId': 'doMeCjIXSQ0EPNg=', 'routeKey': '$default',
        'stage': '$default', 'time': '24/Dec/2022:01:49:52 +0000',
        'timeEpoch': 1671846592036
    },
    'body': 'cHl0aG9uPXJlcXVlc3RzLmdldCUyOCUyMmh0dHBzJTNBJTJGJTJGd3d3LmJhaWR1LmNvbSUyRnNlYXJjaCUzRnElM0RvcmFjbGUlMjIlMjkudGV4dA==',
    'isBase64Encoded': True
}

class test_request(unittest.TestCase):

    @mock.patch('taskbox.webx.object._check_authid_is_valid')
    def test_parse_body(self, mock_auth):
        req = Request(FAKE_EVENT, {})
        self.assertEqual(
            'requests.get("https://www.baidu.com/search?q=oracle").text',
            req.body.get('python')
        )
