---
layout: default
title: 常见问题
---

其他问题请移步 [TaskBox/issues](https://github.com/jneeee/taskbox/issues)


#### 1 如何删除创建的所有资源？
在 [CloudFormation][1] 先删除 taskbox 再删除 toolchain。一定要是这个顺序，因为删toolchain 会把创建的 IAM Cloudformation 角色也删掉。目前已知的会删除失败的原因有：apigw绑定了自定义域名（要去删掉映射），S3存储桶没清空导致删不掉（去S3界面清空存储桶）。然后删除日志组，[官方参考][2]。如果设置过定时器，到 [Eventbridge][3] 删除

![](/static/img/deletestack.png)

#### 2 用来部署的IAM ACCESS 需要具有哪些权限？
建议的权限配置：

![](/static/img/qa_access_id_policy.png)



[1]: https://ap-southeast-1.console.aws.amazon.com/cloudformation/home?region=ap-southeast-1#/stacks?filteringStatus=active&filteringText=&viewNested=true 'CloudFormation'
[2]: https://docs.aws.amazon.com/zh_cn/lambda/latest/dg/applications-tutorial.html#applications-tutorial-cleanup '清除资源'
[3]: https://ap-southeast-1.console.aws.amazon.com/scheduler/home?region=ap-southeast-1#/schedules '定时器列表'
