<img align="right" width=300 src="https://github.com/jneeee/taskbox/raw/master/docs/static/img/taskbox.png"> 
## Task Box TaskBox

TaskBox (hereinafter referred to as TaskBox) is a personal scheduled task framework running on the Serverless platform. It focuses on stability, performance, and scalability. Based on AWS Lambda + [DynamoDB][2] + S3 + APIGW + EventBridge scheduler.

![deploytoaws](https://github.com/jneeee/taskbox/workflows/DeployToAWS/badge.svg)

📦 [Project homepage](https://jneeee.github.io/taskbox)
📦 [Demo Address](https://demo.taskbox.cn)

! [index](docs/static/img/box_index.png)
! [exc page](docs/static/img/box_exc.png)

It has the following features:

- All free, using AWS's [perpetual free credit] (https://aws.amazon.com/cn/free/) 🎉 for developers
- Simple deployment. Based on AWS SAM application templates, it can be automated, never manual.
- Web task list. Supports adding, deleting, modifying, and querying tasks, and can bind a personal domain name.
- Simple login authentication function, and use AWS Api-Gateway to make **access security restrictions** to prevent brute force attacks!
- The configuration and task cycle can be set on the webpage (different tasks support custom configuration), and the task cookie expires in 1 second to change!
- Focus on performance. No web frameworks (flask/bottle, etc.), no redundant code. Thanks to the high availability and high performance of AWS Function Compute and database, the cold start time of the webpage is less than 1s, and subsequent webpage requests are basically completed within 5ms. <small>It does not include DynamoDB query latency of less than 10ms</small>
- Provides a web version of the Shell and Python command interfaces, which can be used temporarily.
- Extremely scalable. Task plug-in (Submodule management) to create your own task in one minute according to the contribution guide. You can also look for ~~rich extensions~~ PR in the quest market

## 2 How to use
Box enables deployment to AWS Lambda through github actions. To do this, you need to configure your AWS account information in GitHub Action. As recommended by AWS, you can create a user group and add [Necessary Permissions Question 2] (https://jneeee.github.io/taskbox/qa)

1. Fork this repository and set the following three variables in the setting -> Actions secrets of your repository
```
AWS_ACCESS_KEY_ID 
AWS_SECRET_ACCESS_KEY
WEB_PASSWORD
```
The first two variables are obtained from your AWS account, generally set in [here][1], and the third is the password used to log in to the box, and now the authentication method is relatively simple, so it is recommended to set a strong password.

2. Push a commit to the master branch to trigger automatic deployment to AWS  
The accessed APIs can then be found from the AWS api-gateway console or the GitHub action task echo.

### 3 Create your own tasks

The box is highly extensible, take the task of creating a timed access URL as an example. Add the file 'src/taskbox/user_task/taskcronreq.py', inheriting the 'taskbox.taskbase.task.Task' class, as follows

```
import requests

from taskbox.taskbase.task import Task
from taskbox.utils.tools import LOG

__all__ = ['CornReq']

class CornReq(Task):
    '''Regularly visit a URL, a golden oil task, and then add custom data/param
    '''
    name_zh = 'Timed access'

def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

def step(self, config):
        '''Here'
The box will call this method according to the set period. The returned results are displayed in the 'Results' section of the web.
        '''
        res = getattr(requests, config.get('method'))(config.get('url'))
        return f'execution {config} success: {res.json}'

def get_conf_list(self):
        '''method is a request method supported by requests, data/param fields are not supported'''
        return {
            'url': 'address to access',
            'method': 'get, option, post',
        }

CornReq.register()
```
After the box parses the comments and configuration requirements of the code, the task details page will automatically appear as follows:
! [cronreq] (docs/static/img/box_cronreq.png)

You can also manage the task TODO through the git submodule

In a quick update, PRs are welcome

[1]: https://us-east-1.console.aws.amazon.com/iam/home#/security_credentials$access_key
[2]: https://docs.amazonaws.cn/amazondynamodb/latest/developerguide/Introduction.html 'Introduction to DynamoDB'
