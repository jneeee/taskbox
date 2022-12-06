
### 测试的 event 和 context
```
{
  "statusCode": 200,
  "body": "\"Hello, put_item resp: None\\n
  event: {'key1': 'value1', 'key2': 'value2', 'key3': 'value3'}\\n
  context: LambdaContext([aws_request_id=f6e5d825-d87a-4078-afd7-04fcacf7cae0,log_group_name=/aws/lambda/appname-helloFromLambdaFunction-4vI8IsgslTpw,log_stream_name=2022/11/19/[$LATEST]62786a6386474290809b8b554bbbf9c3,function_name=appname-helloFromLambdaFunction-4vI8IsgslTpw,memory_limit_in_mb=128,function_version=$LATEST,invoked_function_arn=arn:aws:lambda:ap-southeast-1:044694559979:function:appname-helloFromLambdaFunction-4vI8IsgslTpw,client_context=None,identity=CognitoIdentity([cognito_identity_id=None,cognito_identity_pool_id=None])])\""
}
```

### http 访问的 event 和 context
```
"Hello, put_item resp: None\n
event: 
{
    "version": "2.0",
    "routeKey": "$default",
    "rawPath": "/db/quary",
    "rawQueryString": "",
    "headers": {
        "sec-fetch-mode": "navigate",
        "x-amzn-tls-version": "TLSv1.2",
        "sec-fetch-site": "none",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "x-forwarded-proto": "https",
        "x-forwarded-port": "443",
        "x-forwarded-for": "112.64.93.19",
        "sec-fetch-user": "?1",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "x-amzn-tls-cipher-suite": "ECDHE-RSA-AES128-GCM-SHA256",
        "sec-ch-ua": "\"Microsoft Edge\";v=\"107\", \"Chromium\";v=\"107\", \"Not=A?Brand\";v=\"24\"",
        "sec-ch-ua-mobile": "?0",
        "x-amzn-trace-id": "Root=1-6378cd2f-530900c3650f80db2a06cc5a",
        "sec-ch-ua-platform": "\"Windows\"",
        "host": "qmyyqcts32m4kj7svcbz3apkru0urztd.lambda-url.ap-southeast-1.on.aws",
        "upgrade-insecure-requests": "1",
        "cache-control": "max-age=0",
        "accept-encoding": "gzip, deflate, br",
        "sec-fetch-dest": "document",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.42"
    },
    "requestContext": {
        "accountId": "anonymous",
        "apiId": "qmyyqcts32m4kj7svcbz3apkru0urztd",
        "domainName": "qmyyqcts32m4kj7svcbz3apkru0urztd.lambda-url.ap-southeast-1.on.aws",
        "domainPrefix": "qmyyqcts32m4kj7svcbz3apkru0urztd",
        "http": {
            "method": "GET",
            "path": "/",
            "protocol": "HTTP/1.1",
            "sourceIp": "112.64.93.19",
            "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.42"
        },
        "requestId": "237f0819-4b3b-4973-9585-af2e884fe1a9",
        "routeKey": "$default",
        "stage": "$default",
        "time": "19/Nov/2022:12:33:51 +0000",
        "timeEpoch": 1668861231900
    },
    "isBase64Encoded": False,
    <!-- below from api gateway -->
    stageVariables: {'StageVar': 'Value'},
    body: "aWQ9VGFza190ZXN0",
}
context: LambdaContext([aws_request_id=237f0819-4b3b-4973-9585-af2e884fe1a9,log_group_name=/aws/lambda/appname-helloFromLambdaFunction-4vI8IsgslTpw,log_stream_name=2022/11/19/[$LATEST]4d83a69ec1e3420091ca9b4ba056e3ac,function_name=appname-helloFromLambdaFunction-4vI8IsgslTpw,memory_limit_in_mb=128,function_version=$LATEST,invoked_function_arn=arn:aws:lambda:ap-southeast-1:044694559979:function:appname-helloFromLambdaFunction-4vI8IsgslTpw,client_context=None,identity=CognitoIdentity([cognito_identity_id=None,cognito_identity_pool_id=None])])"
```
